using System.Collections;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Mọi thẻ bài lớp 2 (nhãn và tên bài thật trong index.json) vừa thẻ ở danh sách bài, không tràn chữ.</summary>
    public class Grade2CardTitleTests : AppTestBase
    {
        [UnityTest, Timeout(600000)]
        public IEnumerator EveryGrade2Card_TitleFits()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.OpenBook("tv2_t1_2001");
            yield return null;
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            var ids = AppRoot.Instance.Lessons.Index.lessons.Where(e => e.book == "tv2_t1_2001").Select(e => e.lesson_id).ToList();
            Assert.That(ids.Count, Is.EqualTo(133));
            var overflowing = ids.Where(id =>
            {
                var text = list.ButtonFor(id).GetComponentInChildren<TMP_Text>();
                text.ForceMeshUpdate();
                return text.isTextOverflowing;
            }).ToList();
            Assert.That(overflowing, Is.Empty, string.Join(", ", overflowing));
        }
    }
}
