namespace TapDoc
{
    /// <summary>Đăng ký mọi màn theo <c>type</c>/<c>kind</c>. Gọi nhiều lần vẫn an toàn.</summary>
    public static class StepViewRegistry
    {
        public static void RegisterAll()
        {
            StepViewFactory.Register("unit", () => new UnitView());
            StepViewFactory.Register("keyword", () => new KeywordView());
            StepViewFactory.Register("picture", () => new KeywordView());
            StepViewFactory.Register("analyze", () => new AnalyzeView());
            StepViewFactory.Register("tone_intro", () => new ToneIntroView());
            StepViewFactory.Register("spell", () => new SpellView());
            StepViewFactory.Register("tone_attach", () => new SpellView());
            StepViewFactory.Register("words", () => new ItemsView());
            StepViewFactory.Register("reading", () => new ItemsView());
            StepViewFactory.Register("sentence", () => new SentenceView());
            StepViewFactory.Register("letter_grid", () => new LetterGridView());
            StepViewFactory.Register("letter_pairs", () => new LetterPairsView());
            StepViewFactory.Register("rime_table", () => new RimeTableView());
            StepViewFactory.Register("rime_grid", () => new RimeGridView());
            StepViewFactory.Register("rule", () => new RuleView());
            StepViewFactory.Register("tone_table", () => new ToneTableView());
            StepViewFactory.Register("combine_table", () => new CombineTableView());
            // Phần Tập đọc (tập 2).
            StepViewFactory.Register("title", () => new TitleView());
            StepViewFactory.Register("question", () => new QuestionView());
            StepViewFactory.Register("passage", () => new PassageView());
            StepViewFactory.Register("find_words", () => new FindWordsView());
            StepViewFactory.Register("memorize", () => new MemorizeView());
            StepViewFactory.Register("fill_blank", () => new FillBlankView());
            StepViewFactory.Register("riddle_answer", () => new RiddleAnswerView());

            StepViewFactory.RegisterRound("listen_choose", () => new ListenChooseView());
            StepViewFactory.RegisterRound("match_case", () => new MatchCaseView());
            StepViewFactory.RegisterRound("look_tone", () => new LookToneView());
            StepViewFactory.RegisterRound("compose", () => new ComposeView());
            StepViewFactory.RegisterRound("listen_picture", () => new ListenPictureView());
        }
    }
}
