using System;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Khoá phụ huynh dạng phép tính (<see cref="ParentGate"/>) với 3 nút đáp án, phủ kín vùng cha. Dùng chung cho màn
    /// Phụ huynh và nhóm có khoá của menu Cài đặt. Đúng thì gọi <c>onUnlocked</c> một lần; sai thì đổi phép tính.
    /// </summary>
    public class ParentGatePanel : MonoBehaviour
    {
        private const float ChoiceWidth = 280f;
        private const float ChoiceGap = 60f;

        private readonly List<Button> _choiceButtons = new();
        private TMP_Text _questionLabel;
        private Action _onUnlocked;

        public ParentGate Gate { get; private set; }
        public IReadOnlyList<Button> ChoiceButtons => _choiceButtons;
        public bool IsUnlocked { get; private set; }

        public static ParentGatePanel Create(Transform parent, System.Random rng, Action onUnlocked)
        {
            var go = new GameObject("GatePanel", typeof(RectTransform), typeof(ParentGatePanel));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var panel = go.GetComponent<ParentGatePanel>();
            panel.Gate = new ParentGate(rng ?? new System.Random());
            panel._onUnlocked = onUnlocked;
            panel.Build();
            return panel;
        }

        /// <summary>Móc cho test: bấm nút đáp án đúng.</summary>
        public void SimulateUnlock()
        {
            var k = Gate.Choices.ToList().IndexOf(Gate.Expected);
            _choiceButtons[k].onClick.Invoke();
        }

        private void Build()
        {
            var prompt = UiKit.CreateLabel(transform, UiText.ParentGatePrompt, 48f);
            Place(prompt.rectTransform, new Vector2(.5f, 1f), new Vector2(1000f, 110f), new Vector2(0f, -220f));

            _questionLabel = UiKit.CreateLabel(transform, Gate.Question, 110f);
            Place(_questionLabel.rectTransform, new Vector2(.5f, .5f), new Vector2(1000f, 180f), new Vector2(0f, 60f));

            for (var k = 0; k < Gate.Choices.Count; k++)
            {
                var index = k;
                var button = UiKit.CreateButton(transform, string.Empty, () => OnChoice(index));
                button.name = $"Choice_{k}";
                var x = -((Gate.Choices.Count - 1) * (ChoiceWidth + ChoiceGap)) / 2f + k * (ChoiceWidth + ChoiceGap);
                Place((RectTransform)button.transform, new Vector2(.5f, .5f), new Vector2(ChoiceWidth, UiKit.MinTouch),
                    new Vector2(x, -200f));
                button.GetComponentInChildren<TMP_Text>().fontSizeMax = 64f;
                _choiceButtons.Add(button);
            }
            Refresh();
        }

        private void Refresh()
        {
            _questionLabel.text = Gate.Question;
            for (var k = 0; k < _choiceButtons.Count; k++)
            {
                _choiceButtons[k].GetComponentInChildren<TMP_Text>().text = Gate.Choices[k].ToString();
            }
        }

        private void OnChoice(int index)
        {
            if (IsUnlocked || index < 0 || index >= Gate.Choices.Count) return;
            if (Gate.Answer(Gate.Choices[index]))
            {
                IsUnlocked = true;
                gameObject.SetActive(false);
                _onUnlocked?.Invoke();
            }
            else
            {
                Refresh();
            }
        }

        private static void Place(RectTransform rt, Vector2 anchor, Vector2 size, Vector2 position)
        {
            rt.anchorMin = rt.anchorMax = rt.pivot = anchor;
            rt.sizeDelta = size;
            rt.anchoredPosition = position;
        }
    }
}
