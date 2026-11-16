# Âm thanh đợt 2: tiếng nghe sai theo nhận dạng giọng nói (16/11/2026)

Root chạy nhận dạng giọng nói (faster-whisper large-v3) hai vòng độc lập trên 4.914 mã nhiều tiếng.
Chỉ giữ tiếng thỏa cả ba điều kiện:
- cả hai vòng đều nghe ra cùng một chữ sai;
- không phải kiểu giọng Nam gộp âm (n/ng, c/t, s/x, tr/ch, v/d/gi) hay số;
- chính chữ đó ở các mã khác máy nghe đúng ≥ 60%, tức là máy không mù chữ đó.
Đây là danh sách nghi lỗi thật, phần lớn là lệch thanh (quạ → quả, chợ → chờ, vá → và) hoặc lệch vần.

## Cách sửa (mỗi mã)

1. Tạo lại theo QUY-TRINH §6:
   - đọc nguyên câu;
   - nếu chưa được thì đọc chậm hoặc ngắt nhẹ;
   - nếu vẫn chưa được thì ghép mượt tiếng khó.
2. Báo root danh sách mã đã tạo lại. Root nhận dạng lại từng file. Đạt khi máy không còn nghe ra chữ sai đó.
3. Mã thử 3 cách vẫn chưa đạt thì giữ bản tốt nhất, ghi chú để chủ dự án nghe.

## Lớp 1 ([L1] nội dung): 46 mã

| Mã | Chữ | Tiếng nghi (đúng → máy nghe) | Máy nghe (vòng 2) |
|---|---|---|---|
| `cau_b125_05` | Hải âu ơi, cánh chim vờn sóng biển | âu → ô | Hải, ô ơi, cánh chim vờn sóng biển. |
| `cau_b126_05` | Vẫy chào những bước chân nhanh tới trường. | vẫy → vậy | Vậy chào những bước chân nhanh tới trường. |
| `cau_b133_06` | Trong khu rừng vắng, Hươu, Nai yên lặng ngắm nhìn; | ngắm → nắm | Trong khu rừng vắng, thư, Nai yên lặng nắm nhìn. |
| `cau_b133_07` | Chim, Sóc cũng chuyền cành xuống trông cho rõ. | trông → trong | Chim, sóc cũng truyền cành xuống trong cho rõ. |
| `cau_b136_06` | Quạ bèn nghĩ ra một cách. | quạ → quả | Quả bền nghĩ ra một cách. |
| `cau_b136_09` | Quạ tha hồ uống. | quạ → quả | Quả tha hồ uống |
| `cau_b138_14` | Chim, Sóc cũng chuyền cành xuống trông cho rõ. | trông → trong | Chim, sóc cũng truyền cành xuống trong cho rõ. |
| `cau_b142_06` | Đánh vần và đọc những tiếng: cho, chợ, chạy, trơn. | chợ → chờ | Đánh vần và đọc những tiếng cho, chờ, chạy, trơn. |
| `cau_b144_01` | Tập chép: Cái võng | cái → trái | Tập chết, trái vỏng |
| `cau_b147_07` | Anh em hòa thuận, hai thân vui vầy. | thuận → thượng | Anh em hòa thượng, hai thân vui vầy. |
| `cau_b149_08` | Bé khẽ reo lên: "Ôi! Bông hồng đẹp quá!". | reo → treo | Bé khẽ treo lên, y ôi! Bông hồng đẹp quá! |
| `cau_b150_15` | Con gì bé tí, chăm chỉ suốt ngày, bay khắp vườn cây, tìm hoa gây mật? | gì → dì | Con dì bé tí, chăm chỉ suốt ngày, bay khắp vườn cây, tìm hoa gây mật. |
| `cau_b153_02` | Trưa mùa hè, nắng vàng như mật ong trải nhẹ trên khắp các cánh đồng cỏ. | vàng → và | Trưa mùa hè, nắng và như mật ong trải nhẹ trên khắp các cánh đồng cỏ. |
| `cau_b163_11` | Hòn gì bằng đất nặn ra, xếp vào lò lửa nung ba bốn ngày, khi ra da đỏ hây hây, t | gì → dì | Hòn dì bằng đất nặng ra, xếp vào lò lửa, nung ba bốn ngày, khi ra da đỏ, hay hay |
| `cau_b168_03` | Giặc đem ra bãi bắn, | giặc → dạch | Dạch đêm ra bãi, bắn. |
| `cau_b25_01` | bà kể để dì ghi | dì → gì | Bà kể để gì ghi? |
| `cau_b27_01` | Ghép thêm dấu thanh để tạo tiếng mới ở nhà. | ghép → kép | Kép thêm dấu thanh để tạo tiếng mới ở nhà. |
| `cau_b28_01` | mẹ bế bé ngủ | bế → bé | Mẹ bé bé ngủ |
| `cau_b29_01` | bé kể bà nghe, nghỉ hè bố và bé đi ra bờ bể. | hè → hề | Bé kể bà nghe, nghĩ hề bố và bé đi ra bờ bể. |
| `cau_b45_01` | Mẹ bế bé đi nhà trẻ. | bế → bé | Mẹ bé bé đi nhà trẻ |
| `cau_b51_01` | Thôn xóm đã lên đèn. | thôn → thung | Thung xóm đã lên đèn. |
| `cau_b56_03` | Bè bạn xum vầy, | bè → bề | Bề bạn xung vầy. |
| `cau_b69_02` | Thôn xóm vui cấy cày gặt hái. | thôn → thung | Thung xóm vui cấy cày gạch hái. |
| `cau_b77_01` | Búp sen nhỏ | sen → xe | Búp xe nhỏ |
| `cau_b90_02` | Lá xanh bông trắng lại chen nhị vàng | chen → trên | Lá xanh bông trắng lại trên nhị vàng. |
| `cau_b95_01` | Cái cò đi đón cơn mưa | cò → cỏ | Cái cỏ đi đón cơn mưa |
| `hd_b109_tranh_01` | Đèn và trăng, bên nào tỏ hơn? | tỏ → tỏa | Đèn và trăng, bên nào tỏa hơn? |
| `hd_b136_tranh_01` | Con quạ gắp sỏi bỏ vào lọ nước. | quạ → quả | Con quả gắp sỏi bỏ vào lọ nước. |
| `hd_b141_tranh_01` | Hoạch bưng cốc nước mời bác đưa thư. | hoạch → hoặc | Hoặc bưng cốc nước mời bác đưa thư. |
| `hd_b146_tranh_01` | Bé nặn quả thị, quả na và con chuột. | thị → thì | Bé nặng quả, thì quả, na và con chuột. |
| `hd_b152_tranh_01` | Các bạn hái sim, thả diều trên đồi. | thả → thải | Các bạn hái xiêm, thải dìu trên đồi. |
| `hd_b57_tranh_01` | Chim mẹ mớm mồi cho chim non. | mồi → mùi | Chim mẹ mớ mùi cho chim non. |
| `hd_b76_tranh_01` | Đây là đôi dép cao su. | dép → vết | Đây là đôi vết trao su. |
| `hoi_b128_02` | Tìm và đọc lên những tiếng trong bài có vần ay, ai. | ai → i | Tìm và đọc lên những tiếng trong bài có vần A, I. |
| `hoi_b141_02` | Thấy bác đưa thư mệt, Hoạch đã làm gì? | hoạch → hoặc | Thấy bác đưa thư mệt hoặc đã làm gì? |
| `hoi_b160_03` | Ông Ké làm việc gì ở suối? Ông Ké đó là ai? | ké → kế; ké → kế | Ông kế làm việc gì ở suối? Ông kế đó là ai? |
| `hoi_b167_02` | Tìm những tiếng trong bài có vần oang, uyên, iên. | uyên → viên | Tìm những tiếng trong bài có vần ngoan, viên, yên. |
| `tu_chen_chucs` | chen chúc | chen → trên | Trên chút. |
| `tu_chiaf_vooi` | chìa vôi | vôi → vui | Thì vui. |
| `tu_chieecs_cawpj` | chiếc cặp | chiếc → chí | Chí cặp |
| `tu_con_nghes` | con nghé | nghé → nghe | Con nghe! |
| `tu_hais_mawng` | hái măng | hái → hải | Hải Măng |
| `tu_maatj_ngotj` | mật ngọt | mật → mực | Mực Ngọc |
| `tu_ngay_ngawns` | ngay ngắn | ngay → ngày | Ngày ngắn |
| `tu_reo_quanh` | reo quanh | reo → rêu | Rêu quanh. |
| `tu_vawnj_ddenf` | vặn đèn | đèn → đền | Vạn đền |

## Lớp 2 ([L2] nội dung): 49 mã

| Mã | Chữ | Tiếng nghi (đúng → máy nghe) | Máy nghe (vòng 2) |
|---|---|---|---|
| `cau_b174_06` | Chao ôi! Sắp đến ngày khai trường, | ôi → ơi | Chào ơi! Sắp đến ngày khai trường. |
| `cau_b188_11` | Sóng bước hai hàng. | sóng → sống | Sống bước 2 hàng |
| `cau_b190_21` | Chim chích bông: loại chim nhỏ, còn gọi là chim sâu, thường ở các vườn cây, vườn | chích → chíp | Chim chíp bông, loại chim nhỏ, còn gọi là chim sâu, thường ở các vườn cây, vườn  |
| `cau_b191_05` | Một bạn vào thưa với cô. | thưa → thư | Một bạn vào thư với cô |
| `cau_b193_05` | Nhưng trường em chỉ có một cô hiệu trưởng trông nom chung mọi việc trong trường. | trông → trong | Nhưng trường em chỉ có một cô hiệu trưởng trong năm chung mọi việc trong trường. |
| `cau_b196_11` | vẫn thấy một dúm lông màu vàng nhạt, | vàng → và | Vẫn thấy một dúng lông màu và nhạt. |
| `cau_b203_16` | "Hoan hô em Bắc! | hoan → hoàng | Hoàng hô em bắt. |
| `cau_b203_19` | Tối dạ: chậm hiểu, chậm nhớ. | dạ → già | Tối già, chậm hiểu, chậm nhớ |
| `cau_b204_05` | Không cày không có thóc, không học không biết chữ. | cày → trầy | Không trầy không có thóc, không học không biết chữ. |
| `cau_b213_07` | Những làn sóng, lúc thì cong vồng, lúc thì loăn xoăn, | cong → công | Những làn sóng, lúc thì công vòng, lúc thì loan soan. |
| `cau_b213_17` | hương gỗ như còn theo Tuấn vào trong cả giấc mơ. | tuấn → túng | Hương gỗ như còn theo túng vào trong cả giấc mơ. |
| `cau_b216_05` | Mẹ còn gọi là má. | còn → con | Mẹ con gọi là má. |
| `cau_b217_04` | Mẹ Thắng vá áo. – đã thành câu. | vá → và | Mẹ thắng và áo đã thành câu. |
| `cau_b235_16` | - Tôi đây! Dưới gầm tủ ấy! - Chiếc dép bên phải trả lời. | tủ → tụ | Tôi đây. Dưới gầm tụ ấy. Chiếc dép bên phải trả lời. |
| `cau_b236_08` | Mẹ ngẩng đầu trông | trông → trong | Mẹ ngẩn đầu trong. |
| `cau_b239_01` | Từ ngữ: Ôn tập | ôn → ôm | Từ ngữ ôm tập |
| `cau_b243_04` | Yêu con sông mặt sóng xao, | sóng → sống | Yêu con sông mặt sống sao? |
| `cau_b244_09` | Có buổi, người ta thấy có con rùa lớn, | buổi → bụi | Có bụi, người ta thấy có con rùa lớn. |
| `cau_b244_10` | đầu to như trái bưởi, nhô lên khỏi mặt nước. | nhô → nhua | đầu to như trái bưởi, nhua lên khỏi mặt nước. |
| `cau_b245_03` | Tàu lá dầu liệng xuống như cánh diều, phủ vàng mặt đất. | mặt → mạch | Tàu lá dầu liện xuống như cánh diều, phủ vàng mạch đất. |
| `cau_b245_09` | Đang giữa trưa nắng, gặp rừng dầu non, | gặp → cặp | đang giữa trưa nắng, cặp rừng dầu non. |
| `cau_b250_14` | - Giỏi quá ông nhỉ! | nhỉ → nghĩ | Giỏi quá ông nghĩ. |
| `cau_b256_05` | Dòng sông rì rào hát ca. | rì → trì | Dòng sông Trì Rào HK |
| `cau_b258_07` | như hòa nhịp với tiếng hát trên các thửa ruộng. | thửa → thử | Như hòa nhịp với tiếng hát trên các thử ruộng. |
| `cau_b258_10` | như một đoàn quân đang nhịp nhàng tiến bước. | đang → đa | như một đoàn quân đa nhịp nhàng tiến bước. |
| `cau_b261_21` | Tên em không thiếu, chẳng thừa Chín vàng ngon ngọt rất vừa lòng anh. Là quả gì? | vàng → và | Tên em không thiếu, chẳng cửa chín và ngon ngọt rất vừa lòng anh. Là quả gì? |
| `cau_b263_07` | Trên con đường làng, đoàn xe cải tiến chất đầy những bó lúa vàng đang nối đuôi n | đuôi → đua | Trên con đường làng, đoàn xe cải tiến chất đầy những bó lúa vàng đang nối đua nh |
| `cau_b266_04` | Những nụ mai không phô hồng mà ngời xanh màu ngọc bích. | ngời → người | Những nụ mai không phô hồng mà người xanh màu ngọc bích. |
| `cau_b272_08` | đáy, nước, in và trời là những từ một tiếng. | đáy → đấy | Đấy, nước, in và trời là những từ một tiếng. |
| `cau_b274_12` | Việt Bắc: chỉ một số tỉnh miền núi phía bắc nước ta, trước kia được xây dựng thà | kia → khi | Việt Bắc, chỉ một số tỉnh miền núi phía bắc nước ta, trước khi được xây dựng thà |
| `cau_b276_05` | Gấu bố, gấu mẹ, gấu con cùng béo rung rinh, | rung → trung; rinh → trinh | Gấu bố, gấu mẹ, gấu con cùng béo trung trinh. |
| `cau_b276_11` | và đến mùa thu lại nhặt quả hạt dẻ. | nhặt → nhạt | Và đến mùa thu lại nhạt quả hạt dẻ. |
| `cau_b277_08` | Một hạt thóc vàng, chín giọt mồ hôi. | thóc → khóc | Một hạt khóc vàng, chín giọt mồ hôi. |
| `cau_b282_04` | Mặt biển sáng trong như tấm thảm khổng lồ bằng ngọc thạch. | trong → trông | Mặt biển sáng trông như tấm thảm khổng lồ bằng ngọc thạch. |
| `cau_b285_07` | Tiếng sóng vỗ long bong bên mạn thuyền. | long → lông | Tiếng sóng vỗ lông bông bên mạng thuyền |
| `cau_b290_04` | Trông từng chùm quả to, đu đưa theo gió đầu hè, em càng nhớ ông. | trông → trong | Trong từng trùng quả to, đu đưa theo gió đầu hè, em càng nhớ ông. |
| `cau_b290_10` | Ăn quả xoài cát chín trẩy từ cây của ông em trồng, | cát → cắt | Ăn quả xoài cắt chín rẫy từ cây của ông em trồng. |
| `cau_b291_12` | Trời trong đầy tiếng rì rào | rì → trì | Trời trong đầy tiếng trì rào. |
| `cau_b291_13` | Đàn cò đánh nhịp bay vào bay ra... | cò → cỏ | Đàn cỏ đánh nhịp bay vào bay ra. |
| `cau_b294_01` | Từ ngữ: Ruộng vườn, cây cối | ruộng → rụng | Từ ngữ, rụng vườn, cây cối |
| `hd_b275_tranh_01` | Núi đồi Sa Pa với ruộng bậc thang. | đồi → đồ | Núi Đồ Sa Pa với ruộng bậc thang |
| `hd_b282_tranh_01` | Biển buổi sáng thật đẹp. | buổi → mũi | Biển mũi sáng thật đẹp. |
| `hd_b289_tranh_01` | Con nhìn kĩ tranh biển buổi sáng nhé. | buổi → mũi | Con nhìn kỹ tranh biển mũi sáng nhé! |
| `hoi_b205_02` | 2. Tìm những từ tả dáng điệu khỏe khoắn của chú gà trống. | tả → tải | 2. Tìm những từ tải gián điệu khỏe khoắn của chú gà trống. |
| `hoi_b235_01` | 1. Đồ dùng của Minh để như thế nào? Để như vậy có đúng chỗ không? Nên để như thế | minh → mình | Một đồ dùng của mình để như thế nào? Để như vậy có đúng chỗ không? Nên để như th |
| `hoi_b244_01` | 1. Tác giả so sánh Hồ Gươm với vật gì? | gươm → gương | Một tác giả so sánh hồ gương với vật gì? |
| `hoi_b265_04` | 4. Hình ảnh nào cho ta biết cánh đồng được mùa? | mùa → mua | Bốn hình ảnh nào cho ta biết cánh đồng được mua? |
| `hoi_b283_02` | 2. Tác giả dùng những từ nào để tả chim chiền chiện bay rất cao? | tác → các; giả → giải | 2. Các giải dùng những từ nào để tả chim triền triện bay rất cao? |
| `hoi_b289_01` | 1. Mặt biển buổi sáng ra sao? | buổi → mũi | Một mặt biển mũi sáng ra sao? |

