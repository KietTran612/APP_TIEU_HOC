using System.Collections.Generic;

namespace TapDoc
{
    public class TapProgress
    {
        private readonly int _count;
        private readonly HashSet<int> _tapped = new();

        public TapProgress(int count)
        {
            _count = count < 0 ? 0 : count;
        }

        public bool AllTapped => _tapped.Count >= _count;

        public void Tap(int i)
        {
            if (i >= 0 && i < _count)
            {
                _tapped.Add(i);
            }
        }
    }
}
