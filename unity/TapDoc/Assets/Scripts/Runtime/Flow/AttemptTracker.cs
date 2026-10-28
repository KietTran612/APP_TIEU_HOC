namespace TapDoc
{
    public enum Feedback
    {
        Correct,
        TryAgain,
        ShowHint
    }

    public class AttemptTracker
    {
        public int Mistakes { get; private set; }

        public Feedback Submit(bool correct)
        {
            if (correct)
            {
                return Feedback.Correct;
            }

            Mistakes++;
            return Mistakes == 1 ? Feedback.TryAgain : Feedback.ShowHint;
        }
    }
}
