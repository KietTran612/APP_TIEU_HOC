using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Màn bước học và lượt luyện tập chỉ hỏi tranh, âm thanh đã có trong bộ của bài (cộng bộ chung). Không đi hết 80
    /// bài: chọn từ dữ liệu một nhóm nhỏ sao cho mỗi loại bước và mỗi loại lượt có ít nhất một màn.
    /// </summary>
    public class PreparedCoverageTests : ViewTestBase
    {
        /// <summary>Một màn cần dựng: bước (Phần 1) hoặc lượt (Phần 2) thứ <c>index</c> của bài.</summary>
        private readonly struct Pick
        {
            public readonly string LessonId;
            public readonly bool IsRound;
            public readonly int Index;
            public readonly string Type;

            public Pick(string lessonId, bool isRound, int index, string type)
            {
                LessonId = lessonId;
                IsRound = isRound;
                Index = index;
                Type = type;
            }

            public override string ToString() => $"{LessonId} {(IsRound ? "lượt" : "bước")} {Index} ({Type})";
        }

        /// <summary>
        /// Mỗi loại bước và loại lượt lấy màn đầu tiên trong sách; riêng bước giới thiệu chữ (<c>unit</c>) lấy bước có
        /// nhiều cách đọc (<c>readings</c>) nếu có, vì các âm thanh đó chỉ phát khi chạm.
        /// </summary>
        private static List<Pick> Picks(out HashSet<string> allTypes)
        {
            var picks = new Dictionary<string, Pick>();
            allTypes = new HashSet<string>();
            foreach (var entry in TestLessons.Real.Index.lessons)
            {
                var lesson = TestLessons.Real.Get(entry.lesson_id);
                for (var i = 0; i < lesson.part1.Count; i++)
                {
                    var step = lesson.part1[i];
                    if (step == null) continue;
                    var type = "bước:" + step.type;
                    allTypes.Add(type);
                    var better = step.type == "unit" && step.readings.Count > 0 && picks.TryGetValue(type, out var old) &&
                                 TestLessons.Real.Get(old.LessonId).part1[old.Index].readings.Count == 0;
                    if (!picks.ContainsKey(type) || better) picks[type] = new Pick(entry.lesson_id, false, i, type);
                }
                for (var i = 0; i < lesson.part2.Count; i++)
                {
                    var round = lesson.part2[i];
                    if (round == null) continue;
                    var type = "lượt:" + round.kind;
                    allTypes.Add(type);
                    if (!picks.ContainsKey(type)) picks[type] = new Pick(entry.lesson_id, true, i, type);
                }
            }
            return picks.Values.ToList();
        }

        [UnityTest]
        public IEnumerator EveryStepTypeAndRoundKind_AsksOnlyPrepared()
        {
            var picks = Picks(out var allTypes);
            CollectionAssert.AreEquivalent(allTypes, picks.Select(p => p.Type).Distinct(), "Chưa phủ đủ loại màn");

            var unprepared = new List<string>();
            foreach (var group in picks.GroupBy(p => p.LessonId))
            {
                var lesson = TestLessons.Real.Get(group.Key);
                var catalog = TestCatalog.FromLoaders(
                    id => AudioClip.Create(id, 441, 1, 44100, false),
                    _ => FakeContentSource.NewSprite(),
                    id => AudioClip.Create(id, 441, 1, 44100, false));
                yield return AwaitableTestUtil.Wait(catalog.PrepareCommonAsync());
                yield return AwaitableTestUtil.Wait(catalog.PrepareAsync(LessonAssets.ContentIds(lesson)), _ => { });
                Ctx.Assets = catalog;
                Ctx.Speech.Init(catalog);
                Ctx.Lesson = lesson;

                foreach (var pick in group)
                {
                    object view = pick.IsRound
                        ? CreateTrackedRound(lesson.part2[pick.Index])
                        : CreateTrackedStep(lesson.part1[pick.Index]);
                    yield return PlayEverything(view);
                    foreach (var id in catalog.UnpreparedAsks.Where(id => !unprepared.Any(u => u.StartsWith(id + " "))))
                    {
                        unprepared.Add($"{id} ({pick})");
                    }
                    Ctx.Speech.Stop();
                    Object.Destroy(RootOf(view));
                    yield return null;
                }
            }
            Assert.IsEmpty(unprepared, "Màn hỏi mã chưa chuẩn bị:\n  " + string.Join("\n  ", unprepared));
        }

        /// <summary>Chờ màn phát xong phần mở đầu, rồi chạm mọi nút và mọi thẻ chữ (mỗi lần chờ giọng đọc xong).</summary>
        private IEnumerator PlayEverything(object view)
        {
            yield return WaitSpeechIdle();
            var root = RootOf(view);
            if (root == null) yield break;
            foreach (var button in root.GetComponentsInChildren<Button>(false).ToList())
            {
                if (button == null || !button.isActiveAndEnabled || !button.interactable) continue;
                button.onClick.Invoke();
                yield return WaitSpeechIdle();
            }
            foreach (var tile in root.GetComponentsInChildren<Tile>(false).ToList())
            {
                if (tile == null || !tile.isActiveAndEnabled) continue;
                tile.SimulateTap();
                yield return WaitSpeechIdle();
            }
        }

        private IEnumerator WaitSpeechIdle()
        {
            yield return null;
            for (var i = 0; i < 300 && Ctx.Speech.IsBusy; i++) yield return null;
        }
    }
}
