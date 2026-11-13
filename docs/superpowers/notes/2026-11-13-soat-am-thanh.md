# Soát âm thanh 8.099 mã (13/11/2026)

Root soát theo lời chủ dự án: "review lại các file audio, kiểm tra kỹ", "phân tích kỹ các audio để đọc/phát âm cho chính xác và đúng ngữ điệu".

## Root kiểm tra được gì, không được gì

- Root không nghe được bằng tai. Máy cũng không có nhận dạng giọng nói tiếng Việt, chỉ có tiếng Anh.
- Vì vậy root **không xác nhận được giọng đọc đúng âm** (ví dụ tr/ch, ươn/ương, s/x).
- Root đo được bằng máy:
  1. **Kỹ thuật** (8.099 file): file có mở được không, im lặng, vỡ tiếng, khoảng lặng, đuôi cụt, độ dài so với số tiếng, độ to, trùng file.
  2. **Chữ đọc so với chữ hiện** (8.099 mã): so chữ máy đã đọc (tts.doc) với chữ hiển thị.
  3. **Thanh điệu tiếng lẻ** (3.109 mã một tiếng): so đường cao độ với mẫu từ các tiếng chủ dự án đã duyệt đạt. Tự chấm lại chính các mẫu: 209/217 đúng.
  4. **Thanh điệu từng tiếng trong từ, câu** (3.347 mã có mốc từng tiếng, 18.002 tiếng). Phép đo này kém chắc hơn vì tiếng nối nhau làm đường cao độ lẫn vào nhau, nên chỉ giữ các lệch rõ.
  5. **Ngữ điệu:** nghỉ ở dấu phẩy, dấu chấm, giữa cụm; tốc độ; độ to.

## Kết quả chung

- 8.099/8.099 file có mặt và giải mã được. Không file im lặng, không vỡ tiếng, không khoảng lặng đầu hay cuối quá dài.
- Độ to đều: chỉ 3 tiếng lẻ nhỏ hơn trung vị khoảng 6 dB (à, ạc, ạ).
- Ngắt nghỉ đều:
  - sau dấu phẩy nghỉ 0,21–0,28 giây;
  - hết câu nghỉ khoảng 1 giây;
  - không có chỗ ngắt sai giữa cụm từ.
- Thanh hỏi, ngã ở tiếng lẻ đúng 336/336; thanh sắc ở tiếng lẻ đúng 630/632. Các lần sửa hỏi, ngã trước đây đã có tác dụng.
- Thanh huyền và thanh nặng: đường cao độ của giọng này cho hai thanh gần giống nhau (đều đi xuống), máy không tách được. **Không kết luận được, cần chủ dự án nghe.**

## 1. Lỗi chắc chắn (sửa được ngay)

| Mã | Chữ | Lỗi | Đề xuất |
|---|---|---|---|
| `hd_b04_tranh_01` (đã đạt) | Các bạn đang múa vui. Con hãy múa theo các bạn nhé. | File chỉ đọc "Các bạn đang múa" (tts.doc cũ); chữ đã thêm câu sau nhưng chưa tạo lại | Tạo lại theo chữ hiện tại |
| `hd_b10_tranh_01` (đã đạt) | Đây là hai **hòn** bi. | Giọng đọc "hai **viên** bi" | Tạo lại theo chữ (hoặc sửa chữ thành "viên") |
| `tieng_ej` | ẹ | Đuôi cụt: file dừng khi tiếng còn to 93%, không có lặng cuối (cắt kiểu giữ tiếng đầu) | Cắt lùi ra sau chỗ tắt tiếng, hoặc thêm 40–60 ms giảm dần |
| `tieng_eej` | ệ | Đuôi cụt: file dừng khi tiếng còn to 81%, không có lặng cuối (cắt kiểu giữ tiếng đầu) | Cắt lùi ra sau chỗ tắt tiếng, hoặc thêm 40–60 ms giảm dần |
| `tieng_ooj` | ộ | Đuôi cụt: file dừng khi tiếng còn to 87%, không có lặng cuối (cắt kiểu giữ tiếng đầu) | Cắt lùi ra sau chỗ tắt tiếng, hoặc thêm 40–60 ms giảm dần |
| `tieng_nuj` (đã đạt) | nụ | Đuôi cụt: file dừng khi tiếng còn to 80%, không có lặng cuối (cắt kiểu giữ tiếng đầu) | Cắt lùi ra sau chỗ tắt tiếng, hoặc thêm 40–60 ms giảm dần |
| `cau_b264_05` | Ví dụ: Sài/Gòn/là/thành/phố/… | 13 tiếng dài 8,7 giây: rất có thể đọc cả dấu "/" hoặc ngắt quá dài | Đọc theo chữ không có "/" (giữ "/" chỉ để hiển thị), hoặc ghép từng tiếng với nghỉ ngắn |

## 2. Cần chủ dự án quyết

**a) Tiếng, vần cụt không dấu (316 mã: rât, căp, êt, up…).** Đây là tiếng trung gian trong chuỗi đánh vần ("rờ – ât – rât – sắc – rất").
- 271 mã nghe ngang.
- 45 mã đọc lên giọng như có dấu sắc, nên trẻ sẽ nghe "rât" thành "rất".
- Đề nghị chủ dự án chọn một cách đọc cho cả nhóm, rồi tạo lại 45 mã lệch cho đồng đều:
  `tieng_bawt` (băt), `tieng_caat` (cât), `tieng_cawp` (căp), `tieng_cawt` (căt), `tieng_cheet` (chêt), `tieng_dawt` (dăt), `tieng_deet` (dêt), `tieng_gaac` (gâc), `tieng_gach` (gach), `tieng_gawp` (găp), `tieng_gawt` (găt), `tieng_heet` (hêt), `tieng_hep` (hep), `tieng_hip` (hip), `tieng_hoc` (hoc), `tieng_hop` (hop), `tieng_hot` (hot), `tieng_keet` (kêt), `tieng_khawp` (khăp), `tieng_khuaat` (khuât), `tieng_meet` (mêt), `tieng_nhawt` (nhăt), `tieng_raap` (râp), `tieng_raat` (rât), `tieng_rawp` (răp), `tieng_reet` (rêt), `tieng_ret` (ret), `tieng_rit` (rit), `tieng_sawp` (săp), `tieng_sawt` (săt), `tieng_taac` (tâc), `tieng_taat` (tât), `tieng_teet` (têt), `tieng_thaap` (thâp), `tieng_thaat` (thât), `tieng_thoawt` (thoăt), `tieng_thoc` (thoc), `tieng_vaap` (vâp), `tieng_vaat` (vât), `tieng_vet` (vet), `tieng_vit` (vit), `tieng_vut` (vut), `van_eep` (êp), `van_eet` (êt), `van_up` (up).

**b) Dấu "..." trong câu giao bài** (Bài viết: "Tây Nguyên... đua nở").
- Giọng đọc liền, không ngắt, nên nghe thành một câu ("Tây Nguyên đua nở").
- Đề nghị viết riêng chữ để đọc: "Bài viết: đoạn từ Tây Nguyên đến đua nở", chữ hiển thị giữ nguyên.
- Các mã: `cau_b164_02`, `cau_b171_04`, `cau_b176_02`, `cau_b184_02`, `cau_b192_04`, `cau_b199_02`, `cau_b207_02`, `cau_b207_04`, `cau_b223_06`, `cau_b231_02`, `cau_b238_02`, `cau_b254_02`, `cau_b262_04`, `cau_b270_02`, `cau_b278_06`, `cau_b286_02`, `cau_b301_02`.
- Các câu dùng "..." để kéo dài giọng (`cau_b205_10`, `cau_b206_19`, `cau_b229_08`, `cau_b290_07`, `cau_b292_35`, `tu_o_o`) cũng không có nghỉ. Có thể thêm dấu phẩy ở chữ đọc để có nhịp ngắt.

## 3. Cần nghe kỹ (máy nghi, chưa chắc)

**a) Tiếng nặng cụt nghe phẳng (thiếu nặng):** `tieng_kichj` (kịch), `tieng_phachj` (phạch), `tieng_sachj` (sạch), `tieng_thachj` (thạch).

**b) Tiếng vần cụt ngắn bất thường** (phần tiếng to chỉ khoảng 0,1 giây, có thể bị cắt mất): `tieng_achj` (ạch), `tieng_awcs` (ắc), `tieng_awps` (ắp), `tieng_awts` (ắt), `tieng_chichs` (chích), `tieng_ichj` (ịch), `tieng_ichs` (ích), `tieng_its` (ít), `tieng_phachs` (phách), `tieng_sachs` (sách), `tieng_sawcs` (sắc), `tieng_sawps` (sắp), `tieng_sawts` (sắt), `tieng_soocs` (sốc), `tieng_suwcs` (sức), `tieng_taaps` (tấp), `tieng_thichs` (thích), `tieng_tits` (tít), `tieng_xachs` (xách), `tieng_xuwcs` (xức).

**c) Tiếng trong từ, câu lệch thanh rõ (108 tiếng ở 103 mã).**
- Hay gặp nhất là tiếng nặng có vần cụt đọc lên giọng như sắc. Ví dụ "Việt" nghe như "Viết", "mặt" như "mắt", "một" như "mốt", "việc" như "viếc", "học" như "hóc".
- Kế đến là tiếng hỏi đọc lên thẳng như sắc. Ví dụ "Chỉ", "cảnh", "quả", "cỏ".
- Trên các mã chủ dự án đã duyệt, máy cũng gắn cờ 2 tiếng mà tai nghe vẫn ổn ("nhé" cuối câu, "mẫu"). Vậy danh sách này có lẫn báo nhầm, chỉ dùng để nghe ưu tiên.

| Mã | Chữ | Tiếng nghi |
|---|---|---|
| `cau_b115_01` | Trần Quốc Toản ra trận | Toản: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b123_01` | Tổ quốc Việt Nam | Việt: nang nghe như đi lên (sắc) |
| `cau_b128_09` | Chỉ nói điều hay thôi. | Chỉ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b131_12` | Chỉ nói điều hay thôi. | Chỉ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b150_14` | Con gì ăn cỏ, đầu có hai sừng, lỗ mũi buộc thừng, cày bừa rất khỏe? | cỏ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b152_13` | Diều ai vừa thả. | thả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b156_03` | Đang đi, hai người bỗng gặp một con gấu. | gặp: nang nghe như đi lên (sắc) |
| `cau_b156_08` | Người ở trên cây tụt xuống, hỏi: | hỏi: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b166_11` | Có máy cày, bác ấy đỡ vất vả. | vả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b167_01` | Buổi sáng trên đất bãi | bãi: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b169_08` | - Ông Gấu ơi! Ông để cho tôi gieo ít cải. | cải: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b170_08` | Tất cả! Chào ở lại | cả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b172_04` | biết ăn ở sạch sẽ, biết giữ kỉ luật, lễ phép, | kỉ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b172_08` | Tuổi các cháu còn nhỏ thì các cháu làm những công việc nhỏ. | việc: nang nghe như đi lên (sắc) |
| `cau_b172_09` | Nhiều công việc nhỏ cộng lại thành công việc to. | việc: nang nghe như đi lên (sắc) |
| `cau_b188_05` | Chẳng thành hàng đôi. | Chẳng: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b188_12` | Chẳng như kiến nọ | Chẳng: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b190_11` | Nó bay tràn qua vườn cải. | cải: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b191_16` | em vẫn là học sinh cũ của cô, | là: huyen nghe như đi lên (sắc) |
| `cau_b196_04` | sách vở sạch sẽ, luôn luôn được thầy yêu bạn mến. | sẽ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b197_07` | Giấy trắng sờ mát rượi | mát: sắc nghe như đi xuống (huyền/nặng) |
| `cau_b203_07` | Cậu học thật chăm, khó khăn không nản. | học: nang nghe như đi lên (sắc) |
| `cau_b206_07` | Vừa xuống xe, Nam chạy ngay đến chỗ chị Bích, chị Diệp. | chị: nang nghe như đi lên (sắc) |
| `cau_b206_12` | - Thế còn chị Diệp vượt được mấy bậc? | được: nang nghe như đi lên (sắc) |
| `cau_b206_26` | - Vì chị Diệp tháng trước xếp thứ nhì, tháng này lên thứ nhất, | chị: nang nghe như đi lên (sắc) |
| `cau_b206_28` | Còn chị Bích thì toàn xếp thứ nhất thôi. | chị: nang nghe như đi lên (sắc) |
| `cau_b216_07` | Những lúc rỗi rãi, em thường đỡ đần bố mẹ. | rãi: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b216_08` | Anh chị em trong một nhà phải thương yêu và đùm bọc nhau. | chị: nang nghe như đi lên (sắc) |
| `cau_b224_10` | Thường ngày, Tâm vẫn giúp đỡ bà, xâu kim cho bà may vá. | vá: sắc nghe như đi xuống (huyền/nặng) |
| `cau_b225_03` | Hỏi: Trong câu, nói đến ai? | Hỏi: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b226_07` | Có quà bánh ngon, chị Lan đều để phần cho Sơn. | chị: nang nghe như đi lên (sắc) |
| `cau_b228_12` | Tay bồng bế, sớm khuya vất vả | vả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b232_06` | Lan gọi các anh, các chị của bố và mẹ đều bằng bác. | chị: nang nghe như đi lên (sắc) |
| `cau_b232_10` | Có hôm chị em tôi hái không xuể. | chị: nang nghe như đi lên (sắc) |
| `cau_b235_20` | Cuối cùng, Minh cũng mặc xong quần áo và tìm thấy dép. | mặc: nang nghe như đi lên (sắc) |
| `cau_b237_06` | Tuy bé nhưng Chổi Rơm rất được việc. | việc: nang nghe như đi lên (sắc) |
| `cau_b237_08` | Chỉ quét nhà thôi, còn sân, vườn đã có loại chổi khác cứng hơn. | Chỉ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b238_02` | Bài viết: "Minh nhìn lên... đâu cả" và "Cuối cùng... vẫn chậm". | vẫn: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b252_13` | Sáng bừng cả mặt sông. | mặt: nang nghe như đi lên (sắc) |
| `cau_b256_03` | Chúng em yêu quý Tổ quốc Việt Nam. | Việt: nang nghe như đi lên (sắc) |
| `cau_b256_04` | Con rùa nhô đầu lên khỏi mặt nước. | mặt: nang nghe như đi lên (sắc) |
| `cau_b259_05` | Kéo mặt trời lên cao. | mặt: nang nghe như đi lên (sắc) |
| `cau_b261_14` | Tên em không thiếu, chẳng thừa | chẳng: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b261_21` | Tên em không thiếu, chẳng thừa Chín vàng ngon ngọt rất vừa lòng anh. L | chẳng: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b264_06` | Cảng Sài Gòn có nhiều bến. | Cảng: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b266_12` | ta liên tưởng đến hình ảnh một đàn bướm vàng rập rờn bay lượn. | một: nang nghe như đi lên (sắc) |
| `cau_b267_02` | Cảnh mùa xuân: | Cảnh: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b267_05` | Cảnh mùa hè: | Cảnh: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b267_08` | Cảnh mùa thu: | Cảnh: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b274_12` | Việt Bắc: chỉ một số tỉnh miền núi phía bắc nước ta, trước kia được xâ | Việt: nang nghe như đi lên (sắc) |
| `cau_b276_03` | Mùa xuân, cả nhà Gấu kéo nhau đi bẻ măng và uống mật ong. | mật: nang nghe như đi lên (sắc) |
| `cau_b276_10` | Sang xuân ấm áp, cả nhà Gấu đi bẻ măng, tìm uống mật ong | mật: nang nghe như đi lên (sắc) |
| `cau_b277_27` | Chúng làm ra mật ngọt lịm mà mọi người ưa thích. | người: huyen nghe như đi lên (sắc) |
| `cau_b285_11` | Chúng dang cánh sà xuống mặt nước, rồi vội vã bay vọt lên, | mặt: nang nghe như đi lên (sắc) |
| `cau_b285_15` | Buổi chiều, nắng vừa nhạt, sương đã buông nhanh xuống mặt biển. | mặt: nang nghe như đi lên (sắc) |
| `cau_b287_05` | Ở ngoài hải đảo, các anh bộ đội phải canh phòng ngày đêm. | phải: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b290_05` | Mùa xoài nào, mẹ em cũng chọn những quả chín mọng, | những: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b290_09` | Mùi thơm dịu dàng, vị ngọt đậm đà, màu sắc đẹp, quả lại to. | dịu: nang nghe như đi lên (sắc) |
| `cau_b292_06` | đều cử một cây lên trời để nhận tên. | một: nang nghe như đi lên (sắc) |
| `cau_b298_07` | Tản Viên, núi đẹp như tranh giữa trời. | Tản: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b298_08` | Ba Vì: tên một ngọn núi cao thuộc tỉnh Hà Tây ở về phía tây Thủ đô Hà  | Vì: huyen nghe như đi lên (sắc) |
| `cau_b299_06` | Hàng cột như bước | cột: nang nghe như đi lên (sắc) |
| `cau_b299_22` | Hàng cột như bước | cột: nang nghe như đi lên (sắc) |
| `cau_b303_02` | Nhân dân Việt Nam rất anh hùng. | Việt: nang nghe như đi lên (sắc) |
| `cau_b32_01` | bé thủ thỉ kể bà nghe, nhà bé có đủ thứ. | thỉ: hỏi/ngã nghe như sắc (lên thẳng, không võng); bà: huyen nghe như đi lên (sắc) |
| `cau_b62_02` | Bay đi đâu cả tối ngày sếu ơi? | cả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b63_01` | Đầu nhà cây lựu sai trĩu quả. | quả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b65_02` | Quân đi như thác chảy. | chảy: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b66_04` | – Nếu là thỏ | thỏ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `cau_b82_04` | Nối đôi bờ cỏ. | cỏ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `hd_b126_tranh_01` | Đây là ngôi trường của các bạn nhỏ. | nhỏ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `hd_b146_tranh_01` | Bé nặn quả thị, quả na và con chuột. | quả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `hd_b221_tranh_01` | Hoa đưa võng ru em Nụ ngủ. | ngủ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `hd_b251_tranh_01` | Nhà máy gạch đang làm việc. | việc: nang nghe như đi lên (sắc) |
| `hd_b289_tranh_01` | Con nhìn kĩ tranh biển buổi sáng nhé. | nhé: sắc nghe như đi xuống (huyền/nặng) |
| `hd_b97_tranh_01` | Đây là bản đồ nước Việt Nam. | Việt: nang nghe như đi lên (sắc) |
| `hd_keo_vao_cho_trong` | Con kéo chữ vào chỗ trống nhé. | nhé: sắc nghe như đi xuống (huyền/nặng) |
| `hd_nhin_keo_dau` | Con nhìn chữ mẫu rồi kéo dấu vào cho đúng nhé. | mẫu: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `hd_tra_loi_mieng` | Con trả lời cùng bố mẹ nhé. | trả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `hoi_b146_03` | Bé nặn những thứ gì? Bé tặng quả thị, quả na cho ai? Bé tặng "thằng ch | quả: hỏi/ngã nghe như sắc (lên thẳng, không võng); quả: hỏi/ngã nghe như sắc (lên thẳng, không võng); chuột: nang nghe như đi lên (sắc) |
| `hoi_b158_03` | Khổ thơ thứ hai có những từ nào tả tiếng máy kêu? | tả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `hoi_b165_04` | Chú thợ mỏ làm việc ở đâu? Câu nào cho em biết dù làm việc vất vả nhưn | việc: nang nghe như đi lên (sắc); việc: nang nghe như đi lên (sắc) |
| `hoi_b176_01` | Câu bắt đầu bằng một chữ cái viết hoa và kết thúc bằng một dấu chấm. E | chấm: sắc nghe như đi xuống (huyền/nặng) |
| `hoi_b254_01` | Đố em: Trong các chữ lượn, đổi, cánh, trả, chữ nào có thể ghép với chữ | trả: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `hoi_b288_01` | Em hãy học thuộc bảng chữ cái trên theo đúng thứ tự. | học: nang nghe như đi lên (sắc); bảng: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_baix_cor` | bãi cỏ | cỏ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_canhr_vaatj` | cảnh vật | cảnh: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_canhr_vaatj_im_lawngj` | cảnh vật im lặng | cảnh: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_cawts_cor` | cắt cỏ | cỏ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_chowr_gachj` | chở gạch | gạch: nang nghe như đi lên (sắc) |
| `tu_chumf_vair` | chùm vải | vải: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_chuwx_vieetj` | chữ Việt | Việt: nang nghe như đi lên (sắc) |
| `tu_gawps_soir` | gắp sỏi | sỏi: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_gawtj_luas` | gặt lúa | lúa: sắc nghe như đi xuống (huyền/nặng) |
| `tu_honf_soir` | hòn sỏi | sỏi: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_howpj_tacs_xax` | hợp tác xã | xã: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_luwowcj_chair` | lược chải | chải: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_nhuoomj_vair` | nhuộm vải | vải: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_roonj_rax` | rộn rã | rã: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_tanr_vieen` | Tản Viên | Tản: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_thowj_mor` | thợ mỏ | mỏ: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_toar_mats` | tỏa mát | tỏa: hỏi/ngã nghe như sắc (lên thẳng, không võng) |
| `tu_xe_vaanj_tair` | xe vận tải | tải: hỏi/ngã nghe như sắc (lên thẳng, không võng) |

## 4. Ghi chú

- `tieng_ddox` (đõ) đọc thành "đỏ", `tieng_ngax` (ngã) đọc thành "ngả": cố ý (giọng này đọc ngã như hỏi), chủ dự án đã duyệt.
- 4 nhóm file trùng nhau chỉ khác dấu chấm cuối câu: bình thường.
- Đã chạy `python -m tapdoc pitch` trên toàn bộ: 3.716 tiếng hỏi/ngã, "đạt" 953, "không đạt" 2.108, chưa đo 655 (thiếu mốc từng tiếng). Con số "không đạt" này **không dùng được** cho tiếng trong từ, câu: công cụ so với mẫu lấy từ tiếng đọc riêng lẻ, mà trong câu tiếng hỏi/ngã ngắn và bị tiếng bên cạnh kéo, nên phần lớn bị chấm sai. Mục 3c dùng mẫu dựng từ chính các tiếng trong câu, đáng tin hơn. Ở tiếng lẻ (dùng đúng mẫu), hỏi/ngã đạt 336/336 như mục Kết quả chung.
