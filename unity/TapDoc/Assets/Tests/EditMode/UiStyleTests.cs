using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;

namespace TapDoc.Tests
{
    /// <summary>Kiểu giao diện mới (bản thiết kế giao diện mục 4): bảng màu, khung viền mực, nút biểu tượng.</summary>
    public class UiStyleTests
    {
        private GameObject _canvas;

        [SetUp]
        public void SetUp()
        {
            _canvas = new GameObject("TestCanvas", typeof(RectTransform), typeof(Canvas));
        }

        [TearDown]
        public void TearDown()
        {
            Object.DestroyImmediate(_canvas);
        }

        private static void AssertColor(Color expected, Color actual, string what) =>
            Assert.That(Vector4.Distance(expected, actual), Is.LessThan(1e-3f), $"{what}: {actual} khác {expected}");

        [Test]
        public void Palette_MatchesDesignHex()
        {
            AssertColor(Palette.Hex("#2B2621"), Palette.Ink, "Ink");
            AssertColor(Palette.Hex("#F6EEDB"), Palette.Paper, "Paper");
            AssertColor(Palette.Hex("#FBF6E9"), Palette.PaperLight, "PaperLight");
            AssertColor(Palette.Hex("#2F8C9B"), Palette.Teal, "Teal");
            AssertColor(Palette.Hex("#EF9D4F"), Palette.Orange, "Orange");
            AssertColor(new Color(43f / 255f, 38f / 255f, 33f / 255f, 1f), Palette.Ink, "Hex");
        }

        [Test]
        public void IconButton_IsRoundWithIconAndNoText()
        {
            var catalog = new AssetCatalog(_ => null, _ => null, _ => null);
            LogAssert.ignoreFailingMessages = true; // thiếu tranh trong catalog giả: không phải điều đang kiểm
            var button = UiKit.CreateIconButton(_canvas.transform, catalog, SystemIcons.Home, UiText.Back, null);
            LogAssert.ignoreFailingMessages = false;

            Assert.AreEqual("Button_" + UiText.Back, button.name);
            Assert.IsEmpty(button.GetComponentsInChildren<TMP_Text>(true), "Nút của bé không có chữ");
            var icon = button.GetComponent<IconButton>();
            Assert.IsNotNull(icon);
            Assert.AreEqual(SystemIcons.Home, icon.IconId);
            Assert.AreEqual(UiText.Back, icon.Label);
            Assert.AreEqual(new Vector2(UiKit.MinTouch, UiKit.MinTouch), ((RectTransform)button.transform).sizeDelta);
            Assert.IsNotNull(button.transform.Find("Icon")?.GetComponent<Image>(), "Thiếu hình biểu tượng");
            AssertColor(Palette.Ink, button.GetComponent<Image>().color, "viền nút");
        }

        [Test]
        public void IconButton_CustomFill()
        {
            var catalog = new AssetCatalog(_ => null, _ => null, _ => null);
            LogAssert.ignoreFailingMessages = true;
            var button = UiKit.CreateIconButton(_canvas.transform, catalog, SystemIcons.Forward, UiText.Next, null, Palette.Orange);
            LogAssert.ignoreFailingMessages = false;
            AssertColor(Palette.Orange, button.transform.Find("Fill").GetComponent<Image>().color, "nền nút Tiếp");
        }

        [Test]
        public void Tile_FillColors_FollowPalette()
        {
            var tile = UiKit.CreateTile(_canvas.transform, "đu");
            var fill = tile.transform.Find("Fill").GetComponent<Image>();
            AssertColor(Palette.Ink, tile.GetComponent<Image>().color, "viền thẻ");
            AssertColor(Palette.PaperLight, fill.color, "thẻ thường");
            tile.SetHighlighted(true);
            AssertColor(Palette.OrangeLight, fill.color, "thẻ đang đọc tới");
            tile.SetHint(true);
            AssertColor(Palette.HintYellow, fill.color, "thẻ gợi ý");
        }

        [Test]
        public void AdultButton_TealWithWhiteText()
        {
            var button = UiKit.CreateButton(_canvas.transform, UiText.Parent, null);
            Assert.AreEqual("Button_" + UiText.Parent, button.name);
            AssertColor(Palette.Ink, button.GetComponent<Image>().color, "viền nút");
            AssertColor(Palette.Teal, button.transform.Find("Fill").GetComponent<Image>().color, "nền nút");
            var text = button.GetComponentInChildren<TMP_Text>();
            Assert.AreEqual(UiText.Parent, text.text);
            AssertColor(Color.white, text.color, "chữ nút");
        }

        [Test]
        public void AdultButton_NextHasNoSpecialColor()
        {
            var next = UiKit.CreateButton(_canvas.transform, UiText.Next, null);
            AssertColor(Palette.Teal, next.transform.Find("Fill").GetComponent<Image>().color, "nút chữ Tiếp");
        }

        [Test]
        public void CardButton_PaperWithInkTextAndShadow()
        {
            var card = UiKit.CreateCardButton(_canvas.transform, "Bông", null);
            AssertColor(Palette.PaperLight, card.transform.Find("Fill").GetComponent<Image>().color, "nền thẻ");
            AssertColor(Palette.Ink, card.GetComponentInChildren<TMP_Text>().color, "chữ thẻ");
            // Bóng là con đầu tiên (nằm dưới cùng), để thẻ vẫn là một ô duy nhất trong layout group.
            Assert.AreEqual("Shadow", card.transform.GetChild(0).name, "Bóng gạch chéo nằm dưới cùng trong thẻ");
            Assert.AreEqual(1, _canvas.transform.childCount, "Thẻ không thêm anh em nào");
            Assert.IsTrue(card.GetComponent<Image>().raycastTarget, "Thẻ vẫn nhận chạm");
        }

        [Test]
        public void HatchShadow_BehindTarget_OffsetAndNotClickable()
        {
            var target = UiKit.CreateTile(_canvas.transform, "a");
            var rt = (RectTransform)target.transform;
            rt.anchoredPosition = new Vector2(100f, 50f);
            var shadow = UiKit.AddHatchShadow(rt);
            Assert.AreEqual(target.transform.GetSiblingIndex() - 1, shadow.transform.GetSiblingIndex());
            var srt = (RectTransform)shadow.transform;
            Assert.AreEqual(rt.anchoredPosition + UiKit.ShadowOffset, srt.anchoredPosition);
            Assert.AreEqual(rt.sizeDelta, srt.sizeDelta);
            Assert.IsFalse(shadow.GetComponentsInChildren<Graphic>(true).Any(g => g.raycastTarget), "Bóng không nhận chạm");
        }

        [Test]
        public void Catalog_MissingSfx_WarnsOnce()
        {
            var asked = new System.Collections.Generic.List<string>();
            var catalog = new AssetCatalog(_ => null, _ => null, id => { asked.Add(id); return null; });
            LogAssert.Expect(LogType.Warning, "[TapDoc] Thiếu tiếng động: khong_co");
            Assert.IsNull(catalog.Sfx("khong_co"));
            Assert.IsNull(catalog.Sfx("khong_co"));
            LogAssert.NoUnexpectedReceived();
            Assert.AreEqual(2, asked.Count);
        }

        [Test]
        public void SystemIcons_AllInSystemImages()
        {
            Assert.AreEqual(12, SystemIcons.All.Length);
            CollectionAssert.IsSubsetOf(SystemIcons.All, SystemImages.All);
            CollectionAssert.Contains(SystemImages.All, SystemImages.Flower);
            CollectionAssert.Contains(SystemImages.All, SystemImages.Mascot);
            Assert.AreEqual("img_chung_hoa_be_ngoan", SystemImages.Flower);
            Assert.AreEqual("img_chung_ga_con", SystemImages.Mascot);
        }

        [Test]
        public void SystemSfx_AllPrefixed()
        {
            CollectionAssert.AreEquivalent(
                new[] { "sfx_cham", "sfx_dung", "sfx_nhap", "sfx_hoa_bay", "sfx_dong_dau", "sfx_lat_trang" },
                SystemSfx.All);
            Assert.IsFalse(SystemAudio.All.Any(id => id.StartsWith("sfx_")), "Âm thanh phát âm không có mã sfx_");
        }

        [Test]
        public void UiText_NewStringsListed()
        {
            foreach (var s in new[]
                     {
                         UiText.Book, UiText.BookTitleFormat, UiText.BookPageFormat, UiText.StampText,
                         UiText.MascotCorrect, UiText.MascotLessonDone, UiText.SfxOn, UiText.SfxOff
                     })
            {
                CollectionAssert.Contains(UiText.All, s);
            }
        }
    }
}
