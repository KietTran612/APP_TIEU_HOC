# Tiếp tục: tranh SGK Tiếng Việt 2 tập một (`tv2_t1_2001`)

Ghi ngày 10/11/2026, trước khi chủ dự án chuyển sang máy mới. Viết cho session "[L2] Vẽ tranh SGK Tiếng Việt 2 tập 1", hoặc session nào nhận việc vẽ lại tranh lớp 2.

## Tình trạng

Đã vẽ đủ tranh cả 4 đợt: **57 tranh bài và kí hiệu `img_chung_giai_nghia`**. Tất cả đã nhập, đang ở `cho_duyet`, nguồn `chatgpt_tam`. Session nội dung chạy validate: không còn lỗi tranh nào.

| Đợt | Mục | Số tranh | Commit | Cuộc trò chuyện ChatGPT (Kiet_1) |
|---|---|---|---|---|
| L2-1 | 172–195 | 9 + kí hiệu giải nghĩa | 447cf3e | `6af15747-0ab0-83ec-b497-37ba4d6ecc22` |
| L2-2 | 196–234 | 18 | d239be1 | `6af16cc1-1f40-83ec-882f-fec132d7753a` |
| L2-3 | 235–273 | 18 | d7bbff2 | `6af1710a-c704-83ec-b05c-e791cb560cbd` (chung với L2-4) |
| L2-4 | 274–304 | 12 | 957e711 | như trên |

- Ảnh không vào git. Session nội dung sẽ đóng gói media một lần, khi âm thanh lớp 2 tạo xong.
- Session tranh động lớp 2 đã nhận đủ 57 mã. Kí hiệu không làm tranh động.
- Thư mục tải `C:\Users\trant\Downloads\tranh_tv2_t1\` đang trống: file đã nhập đều đã vào Thùng rác.

## Tranh chủ dự án cần để ý khi duyệt

Không tranh nào sai mô tả rõ ràng. Ba chi tiết nhỏ chưa vẽ lại, chờ chủ dự án quyết:

- `img_b190_bes_hocj_baif`: cô bé mặc **áo hoa**, không phải áo bông (áo chần bông mùa đông).
- `img_b268_vungf_mor`: ChatGPT trả về 2 bản. Đã chọn bản thấy rõ thuyền chở đầy cá; bản kia có thuyền buồm và tàu than nhưng không thấy cá.
- `img_b274_vieetj_bawcs`: hai cô gái miền núi **không đội nón** (mô tả có "đội nón").

Chủ dự án yêu cầu vẽ lại tranh nào thì làm theo `QUY-TRINH-LAM-VIEC.md` §4, phần "Vẽ lại theo duyệt".

## Cách vẽ (tóm tắt, chi tiết ở `QUY-TRINH-LAM-VIEC.md` §4, §10, §12)

- Trình duyệt: chỉ Claude in Chrome trên Edge của máy này; kiểm tra `onThisComputer` và brand "Microsoft Edge" trước. Trên máy mới, id thiết bị sẽ khác, nên phải kiểm tra lại. Không nhập mật khẩu, không đổi tài khoản.
- Chủ dự án đã cho phép tải ảnh tranh lớp 2 về Downloads ở mọi đợt (09/11).
- Mỗi đợt khoảng 30 tranh thì mở một cuộc trò chuyện mới trong Kiet_1. 30 tranh liên tiếp (L2-3 + L2-4) không bị hết lượt; mỗi tranh mất khoảng 45–70 giây.
- Lời nhắc tranh bài: lấy mô tả từ phiếu `content/requests/images_tv2_t1_bNNN.md` (dòng `Vẽ:`), ghép với câu phong cách như §4.
- Kí hiệu `img_chung_*` dùng lời nhắc riêng, không dùng câu phong cách (vì câu đó ghi "không có khung viền"). Lời nhắc đã dùng cho `img_chung_giai_nghia`:
  > Tạo một hình mới (ảnh PNG): kí hiệu đơn giản, không phải tranh cảnh.
  >
  > Một ô vuông bo góc ở giữa, viền mực đen dày đều tay như in trong sách giáo khoa cũ; bên trong ô là một dấu hai chấm (:) màu đen, hai chấm tròn to, đậm, xếp dọc ở chính giữa ô. Chỉ dùng màu đen trên nền trơn màu giấy ngà; không có chữ, không tô màu khác, không bóng đổ; ô chiếm khoảng 60% khung hình; tỉ lệ vuông 1:1.
  > (Mã tranh: img_chung_giai_nghia. Không viết mã này lên tranh.)
- Tờ kiểm tra: `tools/sheet.ps1`.
- Commit: chỉ các dòng của mình trong `image_manifest.json`, theo §10. `json.dumps(rows, ensure_ascii=False, indent=2) + "\n"` cho ra đúng định dạng HEAD. Các session khác commit liên tục, nên dựng blob, stage và commit liền một lượt.

### Đoạn JS dán vào trang ChatGPT

Một lần điều hướng trang đầy đủ sẽ xoá các hàm này, nên phải dán lại sau mỗi lần mở cuộc trò chuyện mới.

```js
const STYLE = "<câu phong cách trong content/style/image_style.txt>";
window.BUILD = (pairs) => pairs.map(([id, d], i) => [id, (i === 0 ? "Tạo một tranh (ảnh PNG)." : "Tạo một tranh mới (ảnh PNG), cùng phong cách với tranh trước.") + "\n\n" + STYLE + "\nVẽ: " + d + "\n(Mã tranh: " + id + ". Không viết mã này lên tranh.)"]);
// window.__P = BUILD([["img_...", "mô tả"], ...]);  rồi RUN();  theo dõi window.__prog
window.__prog = { done: [], current: null, error: null };
window.RUN = async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const busy = () => !!(document.querySelector('button[data-testid="stop-button"]') || document.querySelector('button[aria-label="Ngừng"]'));
  const findSend = () => document.querySelector('button[data-testid="send-button"]') || document.querySelector('button[aria-label="Gửi"]');
  const limited = () => /giới hạn|hạn mức/i.test((document.querySelector('main') || document.body).innerText.slice(-3000));
  for (const [id, text] of window.__P) {
    if (window.__prog.done.includes(id)) continue;
    try {
      let n = 0; while (busy() && n < 300) { await sleep(2000); n++; }
      await sleep(4000);
      if (limited()) throw new Error('hết lượt');
      window.__prog.current = id;
      for (let t = 0; t < 3; t++) {
        const el = document.querySelector('.ProseMirror'); el.focus();
        if (el.innerText.includes('Mã tranh: ' + id)) break;
        if (el.innerText.trim()) { document.execCommand('selectAll'); document.execCommand('delete'); el.focus(); }
        const dt = new DataTransfer(); dt.setData('text/plain', text);
        el.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
        await sleep(1500);
      }
      if (!document.querySelector('.ProseMirror').innerText.includes('Mã tranh: ' + id)) throw new Error('dán không được');
      let btn; n = 0; while (!(btn = findSend()) && n < 150) { await sleep(2000); n++; }
      if (!btn) throw new Error('không thấy nút Gửi');
      btn.click();
      n = 0; while (!busy() && n < 20) { await sleep(1000); n++; }
      n = 0; while (busy() && n < 300) { await sleep(2000); n++; }
      window.__prog.done.push(id);
    } catch (e) { window.__prog.error = id + ': ' + e; break; }
  }
  window.__prog.current = 'ALL DONE';
};
// Ghép mã -> file ảnh. Token chỉ giữ trong biến trang, không in ra.
window.MAPIMG = async (cid) => {
  const s = await (await fetch('/api/auth/session')).json(); window.__tok = s.accessToken;
  const c = await (await fetch('/backend-api/conversation/' + cid, { headers: { Authorization: 'Bearer ' + window.__tok } })).json();
  const chain = []; let n = c.current_node; while (n) { chain.unshift(c.mapping[n]); n = c.mapping[n].parent; }
  const res = {}; let pending = null;
  for (const node of chain) {
    const m = node.message; if (!m) continue;
    const parts = m.content?.parts || [];
    if (m.author?.role === 'user') { const mm = parts.filter(p => typeof p === 'string').join(' ').match(/Mã tranh: (img_[a-z0-9_]+)/); if (mm) pending = mm[1]; continue; }
    for (const p of parts) if (p && typeof p === 'object' && p.content_type === 'image_asset_pointer' && pending) {
      const fid = p.asset_pointer.replace(/^(file-service|sediment):\/\//, '');
      res[pending] = res[pending] || []; if (!res[pending].includes(fid)) res[pending].push(fid);
    }
  }
  window.__map = res; window.__cid = cid; return res;
};
// Tải <mã>.png về Downloads. Gọi KHÔNG await (quá 45 giây sẽ bị báo hết giờ), rồi đọc window.__dlres.
window.DL = async (ids) => {
  const sleep = ms => new Promise(r => setTimeout(r, ms)); const out = {};
  for (const id of ids) {
    try {
      const arr = window.__map[id]; const fid = arr[arr.length - 1];
      const meta = await (await fetch(`/backend-api/files/download/${fid}?conversation_id=${window.__cid}&inline=false`, { headers: { Authorization: 'Bearer ' + window.__tok } })).json();
      let blob = await (await fetch(meta.download_url)).blob();
      if (blob.type !== 'image/png') { const b = await createImageBitmap(blob); const c = document.createElement('canvas'); c.width = b.width; c.height = b.height; c.getContext('2d').drawImage(b, 0, 0); blob = await new Promise(r => c.toBlob(r, 'image/png')); }
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = id + '.png'; document.body.appendChild(a); a.click(); a.remove();
      out[id] = blob.size; await sleep(900);
    } catch (e) { out[id] = 'ERR ' + e; }
  }
  window.__dlres = out; return out;
};
```

Một mã có nhiều file (`__map[id].length > 1`) thì tải từng bản ra xem rồi chọn. `DL` mặc định lấy bản cuối.
