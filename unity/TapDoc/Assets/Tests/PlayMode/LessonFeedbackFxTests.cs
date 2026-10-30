using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Hiệu ứng phản hồi trong bước học và lượt luyện tập (bản thiết kế giao diện mục 6, 7.2): đúng thì "ting", sao giấy,
    /// gà con khen; sai thì thẻ lắc, gà con nghiêng đầu, không đỏ, không tiếng; chạm làm giọng đọc phát ngay thì không có
    /// tiếng "tách"; tiếng "bụp" khi nhập thẻ nằm trong khoảng nghỉ.
    /// </summary>
    public class LessonFeedbackFxTests : ViewTestBase
    {
        private const string Lesson = "tv1_t1_b13";
        private const int SpellStep = 3;
        private const int SentenceStep = 9;
        private const int ChooseRound = 0;
        private const int ComposeRound = 6;

        private GameObject _fxRoot;
        private SfxPlayer _sfx;
        private Mascot _mascot;

        public override void SetUp()
        {
            base.SetUp();
            _fxRoot = new GameObject("FxRoot");
            _sfx = _fxRoot.AddComponent<SfxPlayer>();
            _sfx.Init(Ctx.Assets, Ctx.Speech);
            _mascot = Mascot.Create(Canvas.transform, Ctx.Assets);
            Ctx.Fx = new LessonFx((RectTransform)Canvas.transform, Ctx.Assets, _sfx, _mascot);
        }

        public override void TearDown()
        {
            if (_fxRoot != null) Object.Destroy(_fxRoot);
            if (_mascot != null) Object.Destroy(_mascot.gameObject);
            base.TearDown();
        }

        private static Color FillOf(Tile tile) => tile.transform.Find("Fill").GetComponent<Image>().color;

        private static Tile[] Tiles(object view) => RootOf(view).GetComponentsInChildren<Tile>(true);

        [UnityTest]
        public IEnumerator Round_Correct_PlaysDingAndCheers()
        {
            var view = BindRound(Lesson, ChooseRound);
            yield return ((ITestCompletable)view).CompleteForTest();
            CollectionAssert.Contains(_sfx.History, SystemSfx.Correct);
            Assert.AreEqual(MascotMood.Cheer, _mascot.LastMood);
        }

        [UnityTest]
        public IEnumerator Round_Wrong_NoSfx_Ponders_NoRed()
        {
            var view = (RoundViewBase)BindRound(Lesson, ChooseRound);
            yield return null;
            view.ActWrongForTest();
            yield return new WaitForSeconds(.2f);
            CollectionAssert.IsEmpty(_sfx.History, "Chọn sai không có tiếng động riêng");
            Assert.AreEqual(MascotMood.Ponder, _mascot.LastMood);
            foreach (var tile in Tiles(view))
            {
                Assert.That(Vector4.Distance(FillOf(tile), Palette.PaperLight), Is.LessThan(1e-3f), "Không tô đỏ thẻ sai");
            }
        }

        [UnityTest]
        public IEnumerator Round_SecondWrong_HintPulses()
        {
            var view = (RoundViewBase)BindRound(Lesson, ChooseRound);
            yield return null;
            view.ActWrongForTest();
            yield return new WaitForSeconds(.2f);
            view.ActWrongForTest();
            yield return new WaitForSeconds(.2f);
            var hinted = Tiles(view).Single(t => t.IsHinted);
            Assert.IsTrue(Pulse.IsRunning(hinted.transform), "Thẻ gợi ý nhún nhẹ");
            hinted.SetHint(false);
            Assert.IsFalse(Pulse.IsRunning(hinted.transform));
            Assert.AreEqual(Vector3.one, hinted.transform.localScale);
        }

        [UnityTest]
        public IEnumerator Spell_Demo_NoTapSound_MergeOncePerJoin()
        {
            var view = Bind(Lesson, SpellStep);
            yield return WaitPracticeReady(view);
            CollectionAssert.DoesNotContain(_sfx.History, SystemSfx.Tap, "Đang đánh vần mẫu thì không có tiếng tách");
            var joins = LessonRepository.Load(Lesson).part1[SpellStep].spell.parts.Count(p => p.kind == "join");
            Assert.Greater(joins, 0);
            Assert.AreEqual(joins, _sfx.History.Count(id => id == SystemSfx.Merge), "Mỗi lần nhập thẻ một tiếng bụp");
        }

        [UnityTest]
        public IEnumerator Spell_Tiles_NoTapSound_FinishCheers()
        {
            var view = Bind(Lesson, SpellStep);
            yield return WaitPracticeReady(view);
            foreach (var tile in Tiles(view)) Assert.IsNull(tile.GetComponent<TapFeedback>().Sound, "Chạm thẻ là nghe đánh vần ngay");
            yield return ((ITestCompletable)view).CompleteForTest();
            CollectionAssert.Contains(_sfx.History, SystemSfx.Correct);
            Assert.AreEqual(MascotMood.Cheer, _mascot.LastMood);
        }

        [UnityTest]
        public IEnumerator Sentence_DoneButton_HasTapSound_ListenDoesNot()
        {
            var view = Bind(Lesson, SentenceStep);
            yield return null;
            var done = ButtonWithText(view, UiText.DoneReading);
            var listen = ButtonWithText(view, UiText.ListenSentence);
            Assert.AreEqual(SystemIcons.Check, done.GetComponent<IconButton>().IconId);
            Assert.AreEqual(SystemIcons.Speaker, listen.GetComponent<IconButton>().IconId);
            Assert.AreEqual(SystemSfx.Tap, done.GetComponent<TapFeedback>().Sound);
            Assert.IsNull(listen.GetComponent<TapFeedback>().Sound);
        }

        [UnityTest]
        public IEnumerator PageButtons_AreIconButtons()
        {
            var lesson = LessonRepository.Load("tv1_t1_b41");
            var index = lesson.part1.FindIndex(s => s.type == "letter_pairs");
            var view = Bind("tv1_t1_b41", index);
            yield return null;
            var next = ButtonWithText(view, UiText.PageNext);
            Assert.AreEqual(SystemIcons.PageNext, next.GetComponent<IconButton>().IconId);
            Assert.AreEqual(SystemSfx.Tap, next.GetComponent<TapFeedback>().Sound);
        }

        [UnityTest]
        public IEnumerator Highlight_GrowsTile()
        {
            var tile = UiKit.CreateTile(Ctx.Stage, "đ");
            tile.SetHighlighted(true);
            Assert.That(tile.transform.localScale.x, Is.EqualTo(1.1f).Within(1e-3f), "Thẻ đang đọc tới phồng lên");
            tile.SetHighlighted(false);
            Assert.That(tile.transform.localScale.x, Is.EqualTo(1f).Within(1e-3f));
            yield return null;
        }

        [UnityTest]
        public IEnumerator AdvanceWhileSparks_NoErrors()
        {
            Motion.Scale = 1f;
            var view = BindRound(Lesson, ChooseRound);
            yield return null;
            Ctx.Fx.Correct((RectTransform)Tiles(view)[0].transform);
            Assert.Greater(Ctx.Fx.ActiveSparks, 0, "Sao giấy đang bung");
            Object.Destroy(RootOf(view));
            Object.Destroy(_mascot.gameObject);
            yield return new WaitForSecondsRealtime(1f);
            Assert.AreEqual(0, Ctx.Fx.ActiveSparks);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Drag_MissedDrop_ReturnsToStart()
        {
            var view = BindRound(Lesson, ComposeRound);
            yield return null;
            var drag = RootOf(view).GetComponentsInChildren<DragTile>().First();
            var rt = (RectTransform)drag.transform;
            var start = rt.anchoredPosition;
            Motion.Scale = 1f;
            var data = new PointerEventData(EventSystem.current) { position = new Vector2(5f, 5f), delta = new Vector2(300f, 200f) };
            drag.OnBeginDrag(data);
            Assert.That(rt.localScale.x, Is.GreaterThan(1f).Or.EqualTo(1f));
            CollectionAssert.Contains(_sfx.History, SystemSfx.Tap, "Nhấc thẻ lên có tiếng tách");
            drag.OnDrag(data);
            drag.OnEndDrag(data);
            yield return new WaitForSecondsRealtime(.4f);
            Assert.That(Vector2.Distance(rt.anchoredPosition, start), Is.LessThan(.5f), "Thả trượt thì thẻ bay về chỗ cũ");
            Assert.That(rt.localScale.x, Is.EqualTo(1f).Within(1e-3f));
        }
    }
}
