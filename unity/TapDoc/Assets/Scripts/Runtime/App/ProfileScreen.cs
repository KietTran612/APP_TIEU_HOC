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

        /// <summary>Gà con chào bé ở phần chọn bé (nâng cấp UI mục 4.4).</summary>
        internal Mascot Mascot { get; private set; }

        /// <summary>Tiếng chào đã phát lần vào màn gần nhất; <c>null</c> khi chưa có file tiếng (chỉ hiện chữ).</summary>
        internal string GreetingAudio { get; private set; }

        /// <summary>Thẻ bé theo thứ tự hiện (bé học gần nhất trước).</summary>
        internal IReadOnlyList<Button> ProfileCards => _profileOrder;

        /// <summary>Lớp cảnh nền (tranh không bắt buộc); <c>null</c> khi chưa có tranh.</summary>
        internal Image Scene { get; private set; }

        private readonly List<Button> _profileOrder = new();
        private RectTransform _cardsArea;
        private GridLayoutGroup _grid;

        /// <summary>Cột trái cho gà con và bong bóng chào.</summary>
        private const float GreetColumn = 420f;
        private const float MascotSize = 300f;
        private const float CardGap = 40f;
        private static readonly Vector2 MaxCard = new(420f, 500f);

        /// <summary>Bánh răng mở menu Cài đặt (ở cả phần chọn lẫn phần tạo bé).</summary>
        internal Button SettingsButton { get; private set; }

        /// <summary>Nút "Về" ở phần tạo hồ sơ (chỉ hiện khi đã có hồ sơ để quay về chọn).</summary>
        internal Button CancelButton { get; private set; }

        public void Build(AppRoot app)
        {
            _app = app;
            _pickPanel = Panel("PickPanel");
            BuildPick();
            _createPanel = Panel("CreatePanel");
            BuildCreate();

            SettingsButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Settings, UiText.Settings,
                () => app.ShowSettings(app.ShowProfiles), Palette.PaperLight);
            Place((RectTransform)SettingsButton.transform, Vector2.one, new Vector2(UiKit.MinTouch, UiKit.MinTouch),
                new Vector2(-20f, -20f));
            SettingsButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

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
        /// Tranh đại diện, hoặc <c>null</c> khi chưa có file. Hỏi <see cref="AssetCatalog.HasImage"/> trước, để hình
        /// đại diện chưa nhập chỉ hiện ô màu mà không báo lỗi thiếu tranh.
        /// </summary>
        internal static Sprite AvatarSprite(AssetCatalog assets, string avatarId)
        {
            if (assets == null || !assets.HasImage(avatarId)) return null;
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

            // Cảnh sân trường nét mực rất nhạt phía sau (không chạm được); chưa có tranh thì chỉ có nét đất.
            var sceneSprite = _app.Assets.Image(SystemImages.WelcomeScene);
            if (sceneSprite != null)
            {
                var sceneGo = new GameObject("WelcomeScene", typeof(RectTransform), typeof(Image));
                sceneGo.transform.SetParent(_pickPanel.transform, false);
                var srt = (RectTransform)sceneGo.transform;
                srt.anchorMin = Vector2.zero;
                srt.anchorMax = Vector2.one;
                srt.offsetMin = srt.offsetMax = Vector2.zero;
                Scene = sceneGo.GetComponent<Image>();
                Scene.sprite = sceneSprite;
                Scene.preserveAspect = true;
                Scene.color = new Color(1f, 1f, 1f, .3f);
                Scene.raycastTarget = false;
                sceneGo.transform.SetAsFirstSibling();
            }
            var ground = new GameObject("Ground", typeof(RectTransform), typeof(Image));
            ground.transform.SetParent(_pickPanel.transform, false);
            var grt = (RectTransform)ground.transform;
            grt.anchorMin = new Vector2(0f, 0f);
            grt.anchorMax = new Vector2(1f, 0f);
            grt.offsetMin = new Vector2(0f, 110f);
            grt.offsetMax = new Vector2(0f, 113f);
            var gimg = ground.GetComponent<Image>();
            gimg.sprite = UiKit.WhiteSprite;
            gimg.color = new Color(Palette.Ink.r, Palette.Ink.g, Palette.Ink.b, .22f);
            gimg.raycastTarget = false;

            // Gà con to ở cột trái, chào bé bằng tiếng (nâng cấp UI mục 4.4).
            Mascot = Mascot.Create(_pickPanel.transform, _app.Assets, MascotSize);
            var mrt = (RectTransform)Mascot.transform;
            mrt.anchorMin = mrt.anchorMax = new Vector2(0f, .5f);
            mrt.pivot = new Vector2(.5f, .5f);
            mrt.anchoredPosition = new Vector2(GreetColumn / 2f + 20f, -110f);
            Mascot.SetBubbleLayout(Mascot.BubbleSide.AboveLeft, GreetColumn - 40f);

            var gridGo = new GameObject("ProfileCards", typeof(RectTransform), typeof(GridLayoutGroup));
            gridGo.transform.SetParent(_pickPanel.transform, false);
            _cardsArea = (RectTransform)gridGo.transform;
            _cardsArea.anchorMin = Vector2.zero;
            _cardsArea.anchorMax = Vector2.one;
            _cardsArea.offsetMin = new Vector2(GreetColumn + 40f, 140f);
            _cardsArea.offsetMax = new Vector2(-40f, -200f);
            var grid = gridGo.GetComponent<GridLayoutGroup>();
            _grid = grid;
            grid.cellSize = new Vector2(300f, 320f);
            grid.spacing = new Vector2(CardGap, CardGap);
            grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            grid.constraintCount = 4;
            grid.childAlignment = TextAnchor.MiddleCenter;

            // Bé học gần nhất đứng đầu, có quầng cam.
            var ordered = _app.Progress.ProfilesByRecent;
            foreach (var profile in ordered)
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
                _profileOrder.Add(card);
                if (profile == ordered[0] && profile.last_played > 0) MarkRecent(card);
            }

            NewChildButton = UiKit.CreateCardButton(gridGo.transform, UiText.AddChild, OpenCreate);
            NewChildButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            NewChildButton.gameObject.SetActive(_app.Progress.Profiles.Count < MaxProfiles);

            FrameWatcher.On(gameObject).Changed += _ => ApplyPickLayout();
        }

        /// <summary>Bé học gần nhất: viền cam, nhún chậm.</summary>
        private static void MarkRecent(Button card)
        {
            var border = card.transform.Find("Border")?.GetComponent<Image>() ?? card.GetComponent<Image>();
            border.color = Palette.Orange;
            Pulse.StartOn(card.transform, .03f, 1.8f);
        }

        /// <summary>Thẻ bé lớn nhất vừa vùng thẻ (tối đa 420×500, hai hàng), ít bé thì thẻ to.</summary>
        internal void ApplyPickLayout()
        {
            if (_cardsArea == null) return;
            Canvas.ForceUpdateCanvases();
            var area = _cardsArea.rect.size;
            if (area.x < 1f || area.y < 1f) return;
            var count = _profileOrder.Count + (NewChildButton != null && NewChildButton.gameObject.activeSelf ? 1 : 0);
            var aspect = MaxCard.y / MaxCard.x;
            var best = Vector2.zero;
            var bestCols = 1;
            for (var rows = 1; rows <= 2; rows++)
            {
                var cols = Mathf.Max(1, Mathf.CeilToInt(count / (float)rows));
                var w = Mathf.Min(MaxCard.x, (area.x - (cols - 1) * CardGap) / cols);
                var h = w * aspect;
                if (rows * h + (rows - 1) * CardGap > area.y)
                {
                    h = (area.y - (rows - 1) * CardGap) / rows;
                    w = h / aspect;
                }
                if (w > best.x)
                {
                    best = new Vector2(w, h);
                    bestCols = cols;
                }
            }
            _grid.cellSize = best;
            _grid.constraintCount = bestCols;
        }

        /// <summary>Gà con chào (bong bóng và tiếng hd_chao_be nếu đã có file).</summary>
        private void Greet()
        {
            if (Mascot == null) return;
            Mascot.Cheer(UiText.Greeting, keepBubble: true);
            GreetingAudio = _app.Assets.Audio(SystemAudio.hd_chao_be) != null ? SystemAudio.hd_chao_be : null;
            if (GreetingAudio != null) _ = _app.Speech.PlayAsync(GreetingAudio);
        }

        /// <summary>Vào Tủ sách sau khi chọn bé; gà con rủ "Mình cùng học nhé!" nếu đã có tiếng.</summary>
        private void GoLearn(string profileId)
        {
            _app.Progress.MarkPlayed(profileId);
            _app.SaveProgress();
            _app.StartSession();
            _app.ShowShelf();
            if (_app.Assets.Audio(SystemAudio.hd_cung_hoc) != null) _ = _app.Speech.PlayAsync(SystemAudio.hd_cung_hoc);
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

            _nameInput = CreateNameInput(_createPanel.transform, RefreshDone);
            Place((RectTransform)_nameInput.transform, new Vector2(0.5f, 1f), new Vector2(900f, UiKit.MinTouch), new Vector2(0f, -190f));

            const float size = 170f, gap = 30f;
            for (var i = 0; i < Avatars.Length; i++)
            {
                var id = Avatars[i];
                var x = -((Avatars.Length - 1) * (size + gap)) / 2f + i * (size + gap);
                var frame = CreateAvatarChoice(_createPanel.transform, _app.Assets, id, () => PickAvatar(id));
                Place((RectTransform)frame.transform, new Vector2(0.5f, 1f), new Vector2(size, size), new Vector2(x, -410f));
                _avatarFrames[id] = frame;
            }

            DoneButton = UiKit.CreateButton(_createPanel.transform, UiText.Done, OnDone);
            Place((RectTransform)DoneButton.transform, new Vector2(0.5f, 0f), new Vector2(320f, UiKit.MinTouch), new Vector2(0f, 80f));
        }

        /// <summary>
        /// Ô chọn một hình đại diện: khung nền (đổi màu khi được chọn, trả về để tô) có nút bấm, hình ở trong. Dùng chung
        /// cho màn tạo bé và phần sửa hồ sơ của Cài đặt.
        /// </summary>
        internal static Image CreateAvatarChoice(Transform parent, AssetCatalog assets, string id, Action onPick)
        {
            var go = new GameObject($"Avatar_{id}", typeof(RectTransform), typeof(Image), typeof(Button));
            go.transform.SetParent(parent, false);
            var frame = go.GetComponent<Image>();
            frame.sprite = UiKit.WhiteSprite;
            frame.color = FrameColor;
            var button = go.GetComponent<Button>();
            button.targetGraphic = frame;
            button.onClick.AddListener(() => onPick?.Invoke());

            var picGo = new GameObject("AvatarBox", typeof(RectTransform));
            picGo.transform.SetParent(go.transform, false);
            var prt = (RectTransform)picGo.transform;
            prt.anchorMin = Vector2.zero;
            prt.anchorMax = Vector2.one;
            prt.offsetMin = new Vector2(14f, 14f);
            prt.offsetMax = new Vector2(-14f, -14f);
            AddAvatar(picGo.transform, assets, id, null);
            return frame;
        }

        /// <summary>Tô khung hình đại diện: đang chọn thì viền cam và phóng nhẹ.</summary>
        internal static void PaintAvatarChoice(Image frame, bool picked)
        {
            frame.color = picked ? PickedColor : FrameColor;
            _ = Motion.ScaleTo(frame.transform, picked ? PickedScale : 1f, .15f);
        }

        /// <summary>Ô nhập tên gọi của bé (một dòng, tối đa <see cref="ProgressStore.MaxNameLength"/> ký tự).</summary>
        internal static TMP_InputField CreateNameInput(Transform parent, Action onChanged)
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

            input.onValueChanged.AddListener(_ => onChanged?.Invoke());
            return input;
        }

        private void ShowPick()
        {
            _createPanel.SetActive(false);
            _pickPanel.SetActive(true);
            ApplyPickLayout();
            Greet();
        }

        private bool CanCreate =>
            _avatar != null && ProgressStore.CleanName(_nameInput != null ? _nameInput.text : null).Length > 0;

        private void RefreshDone()
        {
            if (DoneButton != null) DoneButton.interactable = CanCreate;
        }

        private void RefreshAvatarFrames()
        {
            foreach (var pair in _avatarFrames) PaintAvatarChoice(pair.Value, pair.Key == _avatar);
        }

        private void Choose(string profileId)
        {
            _app.Progress.Select(profileId);
            GoLearn(profileId);
        }

        private void OnDone()
        {
            if (!CanCreate) return;
            var profile = _app.Progress.CreateProfile(_nameInput.text, _avatar);
            GoLearn(profile.id);
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
