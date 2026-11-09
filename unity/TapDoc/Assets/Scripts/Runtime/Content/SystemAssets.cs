using System.Linq;

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
        // Phần Tập đọc (tập 2). Điền chữ dùng lại hd_keo_vao_cho_trong.
        public const string hd_tim_tieng = "hd_tim_tieng";
        public const string hd_tra_loi_mieng = "hd_tra_loi_mieng";
        public const string hd_hoc_thuoc = "hd_hoc_thuoc";
        public const string hd_doan_do = "hd_doan_do";

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
            hd_tim_tieng,
            hd_tra_loi_mieng,
            hd_hoc_thuoc,
            hd_doan_do,
        };
    }

    public static class SystemImages
    {
        public const string Star = "img_chung_sao";
        public const string EmDoc = "img_chung_em_doc";
        public const string LuyenTap = "img_chung_luyen_tap";

        /// <summary>Kí hiệu "Câu hỏi" của sách tập 2 (ô vuông có dấu ?).</summary>
        public const string CauHoi = "img_chung_cau_hoi";
        /// <summary>Kí hiệu [:] giải nghĩa từ của sách lớp 2.</summary>
        public const string GiaiNghia = "img_chung_giai_nghia";

        /// <summary>Bông hoa bé ngoan (hiện là hình mặc định, sau thay bằng tranh chính thức cùng mã).</summary>
        public const string Flower = "img_chung_hoa_be_ngoan";

        /// <summary>Bạn gà con đồng hành.</summary>
        public const string Mascot = "img_chung_ga_con";

        public static readonly string[] All = new[] { Star, EmDoc, LuyenTap, CauHoi, GiaiNghia, Flower, Mascot }
            .Concat(SystemIcons.All).ToArray();

        public static string ForMarker(string marker)
        {
            if (string.IsNullOrEmpty(marker)) return null;
            if (marker.Contains('\u25cf')) return EmDoc;      // ●
            if (marker.Contains('\u2302')) return LuyenTap;   // ⌂
            if (marker.Contains('?')) return CauHoi;          // [?] Câu hỏi (tập 2)
            if (marker.Contains(':')) return GiaiNghia;       // [:] giải nghĩa từ (lớp 2)
            return null;
        }
    }

    /// <summary>Biểu tượng trên nút của bé (nút tròn, không có chữ) và hình nhỏ của hiệu ứng.</summary>
    public static class SystemIcons
    {
        public const string Home = "img_ui_nha";
        public const string Speaker = "img_ui_loa";
        public const string Forward = "img_ui_tiep";
        public const string Backward = "img_ui_lui";
        public const string Book = "img_ui_so";
        public const string Review = "img_ui_on_lai";
        public const string Check = "img_ui_xong";
        public const string Lock = "img_ui_khoa";
        public const string PagePrev = "img_ui_lat_truoc";
        public const string PageNext = "img_ui_lat_sau";
        public const string PaperStar = "img_ui_sao_giay";
        public const string Petal = "img_ui_canh_hoa";

        /// <summary>Nút bánh răng mở menu Cài đặt.</summary>
        public const string Settings = "img_ui_cai_dat";

        public static readonly string[] All =
        {
            Home, Speaker, Forward, Backward, Book, Review, Check, Lock, PagePrev, PageNext, PaperStar, Petal, Settings,
        };
    }

    /// <summary>
    /// Tiếng động khi tương tác, tách hẳn khỏi âm thanh phát âm (<see cref="SystemAudio"/>): mã luôn bắt đầu bằng
    /// <c>sfx_</c>, file nằm ở <c>Resources/sfx/</c>.
    /// </summary>
    public static class SystemSfx
    {
        public const string Prefix = "sfx_";
        public const string Tap = "sfx_cham";
        public const string Correct = "sfx_dung";
        public const string Merge = "sfx_nhap";
        public const string FlowerFly = "sfx_hoa_bay";
        public const string Stamp = "sfx_dong_dau";
        public const string PageFlip = "sfx_lat_trang";

        public static readonly string[] All = { Tap, Correct, Merge, FlowerFly, Stamp, PageFlip };

        /// <summary>Mã có phải tiếng động không (bắt đầu bằng <see cref="Prefix"/>).</summary>
        public static bool IsSfx(string id) => id != null && id.StartsWith(Prefix, System.StringComparison.Ordinal);
    }
}
