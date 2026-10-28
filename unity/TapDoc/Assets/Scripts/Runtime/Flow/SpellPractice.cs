using System.Collections.Generic;

namespace TapDoc
{
    public enum TapResult
    {
        Accepted,
        Ignored,
        WrongOrder
    }

    public class SpellPractice
    {
        private readonly Spell _spell;
        private readonly List<Part> _parts;

        public SpellPractice(Spell spell)
        {
            _spell = spell ?? new Spell();
            _parts = _spell.parts ?? new List<Part>();
            Expected = _parts.Count > 0 ? 0 : -1;
        }

        public int Expected { get; private set; }
        public bool IsDone => Expected == -1;

        public List<int> Start()
        {
            var autoJoins = new List<int>();
            var cursor = 0;
            while (cursor < _parts.Count && _parts[cursor]?.kind == "join")
            {
                autoJoins.Add(cursor);
                cursor++;
            }

            Expected = cursor < _parts.Count ? cursor : -1;
            return autoJoins;
        }

        public TapResult Act(int partIndex, out List<int> autoParts)
        {
            autoParts = new List<int>();
            if (IsDone || partIndex < 0 || partIndex >= _parts.Count)
            {
                return TapResult.Ignored;
            }

            if (partIndex < Expected)
            {
                return TapResult.Ignored;
            }

            if (partIndex > Expected)
            {
                return TapResult.WrongOrder;
            }

            var cursor = Expected + 1;
            while (cursor < _parts.Count && _parts[cursor]?.kind == "join")
            {
                autoParts.Add(cursor);
                cursor++;
            }

            Expected = cursor < _parts.Count ? cursor : -1;
            return TapResult.Accepted;
        }

        public bool RequiresDrag(int partIndex) =>
            _spell.drag_tone
            && partIndex >= 0
            && partIndex < _parts.Count
            && _parts[partIndex]?.kind == "tone";
    }
}
