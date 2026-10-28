namespace TapDoc
{
    public static class SystemAudio
    {
        public const string hd_nghe_chon_chu = "hd_nghe_chon_chu";
        public const string hd_nghe_chon_tranh = "hd_nghe_chon_tranh";
        public const string hd_nhin_keo_dau = "hd_nhin_keo_dau";
        public const string hd_keo_vao_cho_trong = "hd_keo_vao_cho_trong";
        public const string hd_danh_van_theo = "hd_danh_van_theo";
        public const string hd_keo_dau_vao_chu = "hd_keo_dau_vao_chu";
        public const string hd_thu_lai = "hd_thu_lai";
        public const string khen_01 = "khen_01";
        public const string khen_02 = "khen_02";
        public const string khen_hoan_thanh = "khen_hoan_thanh";

        public static readonly string[] All =
        {
            hd_nghe_chon_chu,
            hd_nghe_chon_tranh,
            hd_nhin_keo_dau,
            hd_keo_vao_cho_trong,
            hd_danh_van_theo,
            hd_keo_dau_vao_chu,
            hd_thu_lai,
            khen_01,
            khen_02,
            khen_hoan_thanh,
        };
    }

    public static class SystemImages
    {
        public const string Star = "img_chung_sao";
        public const string EmDoc = "img_chung_em_doc";
        public const string LuyenTap = "img_chung_luyen_tap";

        public static readonly string[] All =
        {
            Star,
            EmDoc,
            LuyenTap,
        };

        public static string ForMarker(string marker)
        {
            if (string.IsNullOrEmpty(marker)) return null;
            if (marker.Contains('\u25cf')) return EmDoc;      // ●
            if (marker.Contains('\u2302')) return LuyenTap;   // ⌂
            return null;
        }
    }
}
