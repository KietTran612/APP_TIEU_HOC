using System;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Màn chọn bé, gồm hai phần.
    /// Phần chọn: mỗi hồ sơ là một thẻ (hình đại diện và tên), cùng thẻ "+ Bé mới".
    /// Phần tạo hồ sơ: ô nhập tên ở nhà (tối đa 20 ký tự), 6 hình đại diện và nút "Xong". Nút "Xong" chỉ bấm được
    /// khi tên không rỗng (sau khi bỏ khoảng trắng) và bé đã chọn hình.
    /// </summary>
    public class ProfileScreen : MonoBehaviour
    {
        internal static readonly string[] Avatars =
        {
            "img_chung_avatar_01",
            "img_chung_avatar_02",
            "img_chung_avatar_03",
            "img_chung_avatar_04",
            "img_chung_avatar_05",
            "img_chung_avatar_06",
        };

        /// <summary>Số hồ sơ tối đa: 7 thẻ bé cùng thẻ "+ Bé mới" vừa 2 hàng 4 thẻ.</summary>
        internal const int MaxProfiles = 7;

        // Màu ô thay cho hình đại diện chưa có file, theo thứ tự Avatars.
        private static readonly Color[] AvatarColors =
        {
            new(0.98f, 0.67f, 0.60f, 1f),
            new(0.99f, 0.84f, 0.45f, 1f),
            new(0.62f, 0.85f, 0.58f, 1f),
            new(0.55f, 0.78f, 0.95f, 1f),
            new(0.80f, 0.68f, 0.93f, 1f),
            new(0.98f, 0.70f, 0.85f, 1f),
        };

        /// <summary>Cỡ của hình đại diện đang chọn ở phần tạo bé.</summary>
        internal const float PickedScale = 1.08f;

        private static readonly Color FrameColor = Palette.PaperLight;
        private static readonly Color PickedColor = Palette.Orange;

        private AppRoot _app;
        private GameObject _pickPanel;
        private GameObject _createPanel;
        private TMP_InputField _nameInput;
        private string _avatar;
        private readonly Dictionary<string, Button> _profileButtons = new();
        private readonly Dictionary<string, Image> _avatarFrames = new();

        internal Button DoneButton { get; private set; }
        internal Button NewChildButton { get; private set; }

        /// <summary>Nút "Về" ở phần tạo hồ sơ (chỉ hiện khi đã có hồ sơ để quay về chọn).</summary>
        internal Button CancelButton { get; private set; }

        public void Build(AppRoot app)
        {
            _app = app;
            _pickPanel = Panel("PickPanel");
            BuildPick();
            _createPanel = Panel("CreatePanel");
            BuildCreate();

            if (_app.Progress.Profiles.Count == 0) OpenCreate();
            else ShowPick();
        }

        /// <summary>Thẻ của hồ sơ <paramref name="profileId"/> ở phần chọn; <c>null</c> nếu không có.</summary>
        internal Button ButtonForProfile(string profileId) =>
            profileId != null && _profileButtons.TryGetValue(profileId, out var b) ? b : null;

        /// <summary>Mở phần tạo hồ sơ với ô tên trống và chưa chọn hình.</summary>
        internal void OpenCreate()
        {
            _pickPanel.SetActive(false);
            _createPanel.SetActive(true);
            CancelButton.gameObject.SetActive(_app.Progress.Profiles.Count > 0);
            _nameInput.text = string.Empty;
            _avatar = null;
            RefreshAvatarFrames();
            RefreshDone();
        }

        internal void SetName(string name)
        {
            _nameInput.text = name ?? string.Empty;
            RefreshDone();
        }

        /// <summary>Khung của hình đại diện <paramref name="avatarId"/> ở phần tạo bé (cho test).</summary>
        internal Image AvatarFrame(string avatarId) =>
            avatarId != null && _avatarFrames.TryGetValue(avatarId, out var frame) ? frame : null;

        internal void PickAvatar(string avatarId)
        {
            if (Array.IndexOf(Avatars, avatarId) < 0) return;
            _avatar = avatarId;
            RefreshAvatarFrames();
            RefreshDone();
        }

        /// <summary>Móc cho test: tạo hồ sơ như bé làm (mở phần tạo, gõ tên, chọn hình, bấm "Xong").</summary>
        internal void SimulateCreate(string name, string avatarId)
        {
            OpenCreate();
            SetName(name);
            PickAvatar(avatarId);
            DoneButton.onClick.Invoke();
        }

        /// <summary>
        /// Tranh đại diện, hoặc <c>null</c> khi chưa có file. Kiểm tra trong Resources trước khi hỏi catalog, để hình
        /// đại diện chưa nhập chỉ hiện ô màu mà không báo lỗi thiếu tranh.
        /// </summary>
        internal static Sprite AvatarSprite(AssetCatalog assets, string avatarId)
        {
            if (assets == null || string.IsNullOrEmpty(avatarId)) return null;
            if (Resources.Load<Sprite>($"images/{avatarId}") == null) return null;
            return assets.Image(avatarId);
        }

        /// <summary>Hình đại diện cỡ đầy <paramref name="parent"/>: tranh nếu có, không thì ô màu kèm chữ đầu của tên.</summary>
        internal static void AddAvatar(Transform parent, AssetCatalog assets, string avatarId, string name)
        {
            var go = new GameObject("Avatar", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var img = go.GetComponent<Image>();
            img.raycastTarget = false;
            img.preserveAspect = true;

            var sprite = AvatarSprite(assets, avatarId);
            if (sprite != null)
            {
                img.sprite = sprite;
                img.color = Color.white;
                return;
            }

            img.sprite = UiKit.WhiteSprite;
            img.preserveAspect = false;
            var index = Array.IndexOf(Avatars, avatarId);
            img.color = index >= 0 ? AvatarColors[index] : new Color(0.85f, 0.85f, 0.85f, 1f);
            var initial = FirstLetter(name);
            if (initial.Length > 0)
            {
                var label = UiKit.CreateLabel(go.transform, initial, 96f);
                var lrt = label.rectTransform;
                lrt.anchorMin = Vector2.zero;
                lrt.anchorMax = Vector2.one;
                lrt.offsetMin = Vector2.zero;
                lrt.offsetMax = Vector2.zero;
            }
        }

        private static string FirstLetter(string name)
        {
            var s = (name ?? string.Empty).Trim();
            if (s.Length == 0) return string.Empty;
            return System.Globalization.StringInfo.GetNextTextElement(s, 0).ToUpperInvariant();
        }

        private GameObject Panel(string name)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            return go;
        }

        private void BuildPick()
        {
            var header = UiKit.CreateLabel(_pickPanel.transform, UiText.AppTitle, 64f);
            Place(header.rectTransform, new Vector2(0.5f, 1f), new Vector2(900f, 140f), new Vector2(0f, -40f));

            var gridGo = new GameObject("ProfileCards", typeof(RectTransform), typeof(GridLayoutGroup));
            gridGo.transform.SetParent(_pickPanel.transform, false);
            Place((RectTransform)gridGo.transform, new Vector2(0.5f, 0.5f), new Vector2(1320f, 680f), new Vector2(0f, -60f));
            var grid = gridGo.GetComponent<GridLayoutGroup>();
            grid.cellSize = new Vector2(300f, 320f);
            grid.spacing = new Vector2(40f, 40f);
            grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            grid.constraintCount = 4;
            grid.childAlignment = TextAnchor.MiddleCenter;

            foreach (var profile in _app.Progress.Profiles)
            {
                var id = profile.id;
                var card = UiKit.CreateCardButton(gridGo.transform, profile.name, () => Choose(id));
                card.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
                card.name = $"Profile_{id}";
                var label = card.GetComponentInChildren<TMP_Text>();
                var lrt = label.rectTransform;
                lrt.anchorMin = new Vector2(0f, 0f);
                lrt.anchorMax = new Vector2(1f, 0.36f);
                lrt.offsetMin = new Vector2(12f, 6f);
                lrt.offsetMax = new Vector2(-12f, 0f);
                label.fontSizeMax = 40f;
                label.overflowMode = TextOverflowModes.Ellipsis; // tên 20 ký tự rất rộng vẫn không tràn khỏi thẻ

                var picGo = new GameObject("AvatarBox", typeof(RectTransform));
                picGo.transform.SetParent(card.transform, false);
                var prt = (RectTransform)picGo.transform;
                prt.anchorMin = new Vector2(0.14f, 0.38f);
                prt.anchorMax = new Vector2(0.86f, 0.95f);
                prt.offsetMin = Vector2.zero;
                prt.offsetMax = Vector2.zero;
                AddAvatar(picGo.transform, _app.Assets, profile.avatar, profile.name);

                _profileButtons[id] = card;
            }

            NewChildButton = UiKit.CreateCardButton(gridGo.transform, UiText.AddChild, OpenCreate);
            NewChildButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            NewChildButton.gameObject.SetActive(_app.Progress.Profiles.Count < MaxProfiles);
        }

        private void BuildCreate()
        {
            CancelButton = UiKit.CreateButton(_createPanel.transform, UiText.Back, ShowPick);
            var backRt = (RectTransform)CancelButton.transform;
            backRt.anchorMin = new Vector2(0f, 1f);
            backRt.anchorMax = new Vector2(0f, 1f);
            backRt.pivot = new Vector2(0f, 1f);
            backRt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
            backRt.anchoredPosition = new Vector2(20f, -20f);

            var header = UiKit.CreateLabel(_createPanel.transform, UiText.NamePrompt, 60f);
            Place(header.rectTransform, new Vector2(0.5f, 1f), new Vector2(900f, 140f), new Vector2(0f, -30f));

            _nameInput = CreateNameInput(_createPanel.transform);
            Place((RectTransform)_nameInput.transform, new Vector2(0.5f, 1f), new Vector2(900f, UiKit.MinTouch), new Vector2(0f, -190f));

            const float size = 170f, gap = 30f;
            for (var i = 0; i < Avatars.Length; i++)
            {
                var id = Avatars[i];
                var go = new GameObject($"Avatar_{id}", typeof(RectTransform), typeof(Image), typeof(Button));
                go.transform.SetParent(_createPanel.transform, false);
                var x = -((Avatars.Length - 1) * (size + gap)) / 2f + i * (size + gap);
                Place((RectTransform)go.transform, new Vector2(0.5f, 1f), new Vector2(size, size), new Vector2(x, -410f));
                var frame = go.GetComponent<Image>();
                frame.sprite = UiKit.WhiteSprite;
                frame.color = FrameColor;
                var button = go.GetComponent<Button>();
                button.targetGraphic = frame;
                button.onClick.AddListener(() => PickAvatar(id));

                var picGo = new GameObject("AvatarBox", typeof(RectTransform));
                picGo.transform.SetParent(go.transform, false);
                var prt = (RectTransform)picGo.transform;
                prt.anchorMin = Vector2.zero;
                prt.anchorMax = Vector2.one;
                prt.offsetMin = new Vector2(14f, 14f);
                prt.offsetMax = new Vector2(-14f, -14f);
                AddAvatar(picGo.transform, _app.Assets, id, null);

                _avatarFrames[id] = frame;
            }

            DoneButton = UiKit.CreateButton(_createPanel.transform, UiText.Done, OnDone);
            Place((RectTransform)DoneButton.transform, new Vector2(0.5f, 0f), new Vector2(320f, UiKit.MinTouch), new Vector2(0f, 80f));
        }

        private TMP_InputField CreateNameInput(Transform parent)
        {
            var go = TMP_DefaultControls.CreateInputField(new TMP_DefaultControls.Resources());
            go.name = "NameInput";
            go.transform.SetParent(parent, false);
            var input = go.GetComponent<TMP_InputField>();
            input.lineType = TMP_InputField.LineType.SingleLine;
            input.contentType = TMP_InputField.ContentType.Standard;
            input.characterLimit = ProgressStore.MaxNameLength;
            input.richText = false;

            foreach (var text in new[] { input.textComponent, input.placeholder as TMP_Text })
            {
                if (text == null) continue;
                text.font = FontProvider.Main;
                text.fontSize = 60f;
                text.enableAutoSizing = false;
                text.alignment = TextAlignmentOptions.Center;
                text.fontStyle = FontStyles.Normal;
            }
            input.textComponent.color = Palette.Ink;
            if (input.placeholder is TMP_Text placeholder)
            {
                placeholder.text = UiText.NamePrompt;
                placeholder.color = Palette.LockedInk;
            }

            input.onValueChanged.AddListener(_ => RefreshDone());
            return input;
        }

        private void ShowPick()
        {
            _createPanel.SetActive(false);
            _pickPanel.SetActive(true);
        }

        private bool CanCreate =>
            _avatar != null && ProgressStore.CleanName(_nameInput != null ? _nameInput.text : null).Length > 0;

        private void RefreshDone()
        {
            if (DoneButton != null) DoneButton.interactable = CanCreate;
        }

        private void RefreshAvatarFrames()
        {
            foreach (var pair in _avatarFrames)
            {
                var picked = pair.Key == _avatar;
                pair.Value.color = picked ? PickedColor : FrameColor;
                _ = Motion.ScaleTo(pair.Value.transform, picked ? PickedScale : 1f, .15f);
            }
        }

        private void Choose(string profileId)
        {
            _app.Progress.Select(profileId);
            _app.SaveProgress();
            _app.ShowLessonList();
        }

        private void OnDone()
        {
            if (!CanCreate) return;
            _app.Progress.CreateProfile(_nameInput.text, _avatar);
            _app.SaveProgress();
            _app.ShowLessonList();
        }

        /// <summary>Đặt <paramref name="rt"/> theo điểm neo <paramref name="anchor"/> (cũng là tâm xoay).</summary>
        private static void Place(RectTransform rt, Vector2 anchor, Vector2 size, Vector2 position)
        {
            rt.anchorMin = anchor;
            rt.anchorMax = anchor;
            rt.pivot = anchor;
            rt.sizeDelta = size;
            rt.anchoredPosition = position;
        }
    }
}
