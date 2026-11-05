using System;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Menu Cài đặt (bản thiết kế màn mở đầu, cảnh báo, cài đặt mục 5.3), mở bằng nút bánh răng ở danh sách bài và màn
    /// chọn bé. Ai cũng dùng được: tiếng động, xem lại lưu ý, thông tin ứng dụng. Chạy được cả khi chưa chọn bé nào.
    /// </summary>
    public class SettingsScreen : MonoBehaviour
    {
        private const float Margin = 20f;
        private const float RowGap = 20f;
        private const float InfoHeight = 260f;

        private AppRoot _app;
        private Action _back;

        public Button BackButton { get; private set; }
        public Button SfxToggle { get; private set; }
        public Button ReviewNoticeButton { get; private set; }
        public TMP_Text InfoLabel { get; private set; }

        /// <summary>Mở nhóm có khoá phụ huynh (quản lý hồ sơ, xoá dữ liệu).</summary>
        public Button ManageButton { get; private set; }

        /// <summary>Khoá phụ huynh của nhóm quản lý (đang mở); <c>null</c> khi chưa mở nhóm.</summary>
        internal ParentGatePanel GatePanel { get; private set; }

        internal Button DeleteAllButton { get; private set; }
        internal TMP_InputField EditNameInput { get; private set; }
        internal Button EditSaveButton { get; private set; }

        private const float RowHeight = 180f;
        private const float RowButtonWidth = 240f;

        private GameObject _manage;
        private RectTransform _manageContent;
        private GameObject _edit;
        private string _editAvatar;
        private readonly Dictionary<string, Button> _renameButtons = new();
        private readonly Dictionary<string, Button> _avatarButtons = new();
        private readonly Dictionary<string, Button> _deleteButtons = new();
        private readonly Dictionary<string, Image> _editAvatarFrames = new();

        internal Button RenameButtonFor(string profileId) => Lookup(_renameButtons, profileId);
        internal Button AvatarButtonFor(string profileId) => Lookup(_avatarButtons, profileId);
        internal Button DeleteButtonFor(string profileId) => Lookup(_deleteButtons, profileId);

        internal Button EditAvatarChoice(string avatarId) =>
            avatarId != null && _editAvatarFrames.TryGetValue(avatarId, out var f) ? f.GetComponent<Button>() : null;

        private static Button Lookup(Dictionary<string, Button> map, string id) =>
            id != null && map.TryGetValue(id, out var b) && b != null ? b : null;

        /// <summary>Hàng các mục, cuộn được, rộng bằng khung chuẩn 1440 ở giữa.</summary>
        internal RectTransform Content { get; private set; }

        public void Build(AppRoot app, Action back)
        {
            _app = app;
            _back = back;

            BackButton = UiKit.CreateButton(transform, UiText.Back, () => _back?.Invoke());
            var backRt = (RectTransform)BackButton.transform;
            backRt.anchorMin = backRt.anchorMax = backRt.pivot = new Vector2(0f, 1f);
            backRt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
            backRt.anchoredPosition = new Vector2(Margin, -Margin);

            var header = UiKit.CreateLabel(transform, UiText.Settings, 64f);
            var hrt = header.rectTransform;
            hrt.anchorMin = hrt.anchorMax = hrt.pivot = new Vector2(.5f, 1f);
            hrt.sizeDelta = new Vector2(800f, UiKit.MinTouch);
            hrt.anchoredPosition = new Vector2(0f, -Margin);

            Content = BuildScroll(transform);

            SfxToggle = Row(SfxLabel(), ToggleSfx);
            ReviewNoticeButton = Row(UiText.ReviewNotice, () => _app.ShowNotice(firstRun: false));

            ManageButton = Row(UiText.ManageProfiles, OpenManage);

            InfoLabel = UiKit.CreateLabel(Content, InfoText(), 40f);
            InfoLabel.alignment = TextAlignmentOptions.TopLeft;
            InfoLabel.gameObject.AddComponent<LayoutElement>().preferredHeight = InfoHeight;
        }

        private static string InfoText() =>
            $"<b>{UiText.AppInfo}</b>\n{UiText.AppTitle} · {string.Format(UiText.VersionFormat, Application.version)}\n{UiText.Credits}";

        /// <summary>Một hàng là một nút người lớn có chữ, cao bằng vùng chạm tối thiểu.</summary>
        internal Button Row(string label, Action onClick) => Row(Content, label, onClick);

        private static Button Row(Transform parent, string label, Action onClick)
        {
            var button = UiKit.CreateButton(parent, label, onClick);
            var le = button.GetComponent<LayoutElement>() ?? button.gameObject.AddComponent<LayoutElement>();
            le.preferredHeight = UiKit.MinTouch;
            le.minHeight = UiKit.MinTouch;
            return button;
        }

        private static RectTransform BuildScroll(Transform parent)
        {
            var scrollGo = new GameObject("Rows", typeof(RectTransform), typeof(ScrollRect));
            scrollGo.transform.SetParent(parent, false);
            var srt = (RectTransform)scrollGo.transform;
            srt.anchorMin = new Vector2(.5f, 0f);
            srt.anchorMax = new Vector2(.5f, 1f);
            srt.pivot = new Vector2(.5f, .5f);
            srt.offsetMin = new Vector2(-UiKit.SafeWidth / 2f + 2f * Margin, 2f * Margin);
            srt.offsetMax = new Vector2(UiKit.SafeWidth / 2f - 2f * Margin, -(2f * Margin + UiKit.MinTouch));

            var viewport = new GameObject("Viewport", typeof(RectTransform), typeof(Image), typeof(RectMask2D));
            viewport.transform.SetParent(scrollGo.transform, false);
            var vrt = (RectTransform)viewport.transform;
            vrt.anchorMin = Vector2.zero;
            vrt.anchorMax = Vector2.one;
            vrt.offsetMin = Vector2.zero;
            vrt.offsetMax = Vector2.zero;
            viewport.GetComponent<Image>().color = Color.clear; // nhận thao tác kéo cuộn

            var contentGo = new GameObject("Content", typeof(RectTransform), typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
            contentGo.transform.SetParent(viewport.transform, false);
            var crt = (RectTransform)contentGo.transform;
            crt.anchorMin = new Vector2(0f, 1f);
            crt.anchorMax = Vector2.one;
            crt.pivot = new Vector2(.5f, 1f);
            crt.sizeDelta = Vector2.zero;
            var vlg = contentGo.GetComponent<VerticalLayoutGroup>();
            vlg.spacing = RowGap;
            vlg.childControlWidth = vlg.childControlHeight = true;
            vlg.childForceExpandWidth = true;
            vlg.childForceExpandHeight = false;
            contentGo.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            var scroll = scrollGo.GetComponent<ScrollRect>();
            scroll.viewport = vrt;
            scroll.content = crt;
            scroll.horizontal = false;
            scroll.vertical = true;
            scroll.movementType = ScrollRect.MovementType.Clamped;
            return crt;
        }

        /// <summary>Lớp phủ nền giấy (chặn chạm phía sau) có nút Về đóng lớp phủ.</summary>
        private GameObject Overlay(string name, Action onBack)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var paper = go.GetComponent<Image>();
            paper.sprite = UiKit.WhiteSprite;
            paper.color = Palette.Paper;
            paper.raycastTarget = true;

            var back = UiKit.CreateButton(go.transform, UiText.Back, onBack);
            var brt = (RectTransform)back.transform;
            brt.anchorMin = brt.anchorMax = brt.pivot = new Vector2(0f, 1f);
            brt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
            brt.anchoredPosition = new Vector2(Margin, -Margin);
            return go;
        }

        /// <summary>Nhóm có khoá: phải giải phép tính trước, xong mới hiện danh sách bé và nút xoá toàn bộ.</summary>
        private void OpenManage()
        {
            CloseManage();
            _manage = Overlay("Manage", CloseManage);
            var header = UiKit.CreateLabel(_manage.transform, UiText.ManageProfiles, 64f);
            var hrt = header.rectTransform;
            hrt.anchorMin = hrt.anchorMax = hrt.pivot = new Vector2(.5f, 1f);
            hrt.sizeDelta = new Vector2(800f, UiKit.MinTouch);
            hrt.anchoredPosition = new Vector2(0f, -Margin);
            GatePanel = ParentGatePanel.Create(_manage.transform, new System.Random(), BuildManageList);
        }

        private void CloseManage()
        {
            CloseEdit();
            if (_manage != null) Destroy(_manage);
            _manage = null;
            _manageContent = null;
            GatePanel = null;
            DeleteAllButton = null;
            _renameButtons.Clear();
            _avatarButtons.Clear();
            _deleteButtons.Clear();
        }

        /// <summary>Dựng (lại) danh sách bé: mỗi bé một hàng có Đổi tên, Đổi hình, Xoá hồ sơ; cuối là Xoá toàn bộ.</summary>
        private void BuildManageList()
        {
            if (_manage == null) return;
            if (_manageContent != null) Destroy(_manageContent.parent.parent.gameObject);
            _renameButtons.Clear();
            _avatarButtons.Clear();
            _deleteButtons.Clear();
            _manageContent = BuildScroll(_manage.transform);
            foreach (var profile in _app.Progress.Profiles) ProfileRow(profile);
            DeleteAllButton = Row(_manageContent, UiText.DeleteAll, ConfirmDeleteAll);
            DeleteAllButton.transform.Find("Fill").GetComponent<Image>().color = Palette.StampRed;
        }

        private void ProfileRow(Profile profile)
        {
            var row = new GameObject($"Child_{profile.id}", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
            row.transform.SetParent(_manageContent, false);
            var le = row.GetComponent<LayoutElement>();
            le.minHeight = le.preferredHeight = RowHeight;
            var bg = row.GetComponent<Image>();
            bg.sprite = UiKit.WhiteSprite;
            bg.color = Palette.PaperLight;

            var avatarBox = new GameObject("AvatarBox", typeof(RectTransform));
            avatarBox.transform.SetParent(row.transform, false);
            var art = (RectTransform)avatarBox.transform;
            art.anchorMin = art.anchorMax = art.pivot = new Vector2(0f, .5f);
            art.sizeDelta = new Vector2(130f, 130f);
            art.anchoredPosition = new Vector2(Margin, 0f);
            ProfileScreen.AddAvatar(avatarBox.transform, _app.Assets, profile.avatar, profile.name);

            var name = UiKit.CreateLabel(row.transform, profile.name, 48f);
            name.alignment = TextAlignmentOptions.Left;
            name.overflowMode = TextOverflowModes.Ellipsis;
            var nrt = name.rectTransform;
            nrt.anchorMin = new Vector2(0f, 0f);
            nrt.anchorMax = new Vector2(1f, 1f);
            nrt.offsetMin = new Vector2(2f * Margin + 130f, 0f);
            nrt.offsetMax = new Vector2(-(3f * RowButtonWidth + 4f * Margin), 0f);

            var id = profile.id;
            _renameButtons[id] = RowButton(row.transform, UiText.Rename, 2, () => OpenEdit(id));
            _avatarButtons[id] = RowButton(row.transform, UiText.ChangeAvatar, 1, () => OpenEdit(id));
            var delete = RowButton(row.transform, UiText.DeleteProfile, 0, () => ConfirmDelete(id));
            delete.transform.Find("Fill").GetComponent<Image>().color = Palette.StampRed;
            _deleteButtons[id] = delete;
        }

        /// <summary>Nút ở mép phải hàng; <paramref name="fromRight"/> = 0 là nút sát mép.</summary>
        private static Button RowButton(Transform row, string label, int fromRight, Action onClick)
        {
            var button = UiKit.CreateButton(row, label, onClick);
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(1f, .5f);
            rt.sizeDelta = new Vector2(RowButtonWidth, UiKit.MinTouch);
            rt.anchoredPosition = new Vector2(-(Margin + fromRight * (RowButtonWidth + Margin)), 0f);
            return button;
        }

        private void ConfirmDelete(string profileId)
        {
            var profile = _app.Progress.Profiles.FirstOrDefault(p => p.id == profileId);
            if (profile == null) return;
            ConfirmDialog.Show(_app.Canvas.transform, string.Format(UiText.DeleteProfileConfirmFormat, profile.name),
                UiText.Delete, () =>
                {
                    if (this == null) return;
                    _app.Progress.DeleteProfile(profileId);
                    _app.SaveProgress();
                    BuildManageList();
                });
        }

        private void ConfirmDeleteAll()
        {
            ConfirmDialog.Show(_app.Canvas.transform, UiText.DeleteAllConfirm1, UiText.Delete, () =>
                ConfirmDialog.Show(_app.Canvas.transform, UiText.DeleteAllConfirm2, UiText.Delete, _app.ResetAllData,
                    confirmOnLeft: true));
        }

        /// <summary>Sửa hồ sơ: ô tên gọi, 6 hình đại diện, nút Lưu (như phần tạo bé).</summary>
        private void OpenEdit(string profileId)
        {
            var profile = _app.Progress.Profiles.FirstOrDefault(p => p.id == profileId);
            if (profile == null) return;
            CloseEdit();
            _edit = Overlay("Edit", CloseEdit);
            _editAvatar = profile.avatar;

            EditNameInput = ProfileScreen.CreateNameInput(_edit.transform, null);
            EditNameInput.text = profile.name;
            var irt = (RectTransform)EditNameInput.transform;
            irt.anchorMin = irt.anchorMax = irt.pivot = new Vector2(.5f, 1f);
            irt.sizeDelta = new Vector2(900f, UiKit.MinTouch);
            irt.anchoredPosition = new Vector2(0f, -190f);

            const float size = 170f, gap = 30f;
            var avatars = ProfileScreen.Avatars;
            for (var i = 0; i < avatars.Length; i++)
            {
                var avatarId = avatars[i];
                var frame = ProfileScreen.CreateAvatarChoice(_edit.transform, _app.Assets, avatarId, () => PickEditAvatar(avatarId));
                var rt = (RectTransform)frame.transform;
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(.5f, 1f);
                rt.sizeDelta = new Vector2(size, size);
                rt.anchoredPosition = new Vector2(-((avatars.Length - 1) * (size + gap)) / 2f + i * (size + gap), -410f);
                _editAvatarFrames[avatarId] = frame;
            }
            PickEditAvatar(_editAvatar);

            EditSaveButton = UiKit.CreateButton(_edit.transform, UiText.Save, () => SaveEdit(profileId));
            var srt = (RectTransform)EditSaveButton.transform;
            srt.anchorMin = srt.anchorMax = srt.pivot = new Vector2(.5f, 0f);
            srt.sizeDelta = new Vector2(320f, UiKit.MinTouch);
            srt.anchoredPosition = new Vector2(0f, 80f);
        }

        private void PickEditAvatar(string avatarId)
        {
            _editAvatar = avatarId;
            foreach (var pair in _editAvatarFrames) ProfileScreen.PaintAvatarChoice(pair.Value, pair.Key == avatarId);
        }

        private void SaveEdit(string profileId)
        {
            _app.Progress.RenameProfile(profileId, EditNameInput.text);
            _app.Progress.SetAvatar(profileId, _editAvatar);
            _app.SaveProgress();
            CloseEdit();
            BuildManageList();
        }

        private void CloseEdit()
        {
            if (_edit != null) Destroy(_edit);
            _edit = null;
            EditNameInput = null;
            EditSaveButton = null;
            _editAvatarFrames.Clear();
        }

        private string SfxLabel() => _app.Progress.SfxEnabled ? UiText.SfxOn : UiText.SfxOff;

        private void ToggleSfx()
        {
            _app.Progress.SfxEnabled = !_app.Progress.SfxEnabled;
            if (_app.Sfx != null) _app.Sfx.Enabled = _app.Progress.SfxEnabled;
            _app.SaveProgress();
            SfxToggle.GetComponentInChildren<TMP_Text>().text = SfxLabel();
        }
    }
}
