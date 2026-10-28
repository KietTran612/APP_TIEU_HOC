// node --test .agents/skills/rule-keeper/test/rk.test.mjs
// Mỗi test dựng một project git tạm, chép kit vào, chạy install và gọi hook đúng như Codex /
// Antigravity gọi (JSON trên stdin), rồi đọc lại sổ và output.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const KIT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const KIT_REL = '.agents/skills/rule-keeper';

function sh(cwd, cmd, args) {
  const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', windowsHide: true });
  if (r.status !== 0) throw new Error(`${cmd} ${args.join(' ')}: ${r.stderr}`);
  return r.stdout;
}

function makeProject() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'rk-'));
  sh(dir, 'git', ['init', '-q']);
  fs.writeFileSync(path.join(dir, 'AGENTS.md'), '# Rules\n\n- Rule A: always write tests.\n');
  fs.writeFileSync(path.join(dir, 'CLAUDE.md'), '# Claude\n\n## Section\n\nUse Decimal for money.\n');
  fs.writeFileSync(path.join(dir, 'app.txt'), 'v1\n');
  fs.cpSync(KIT, path.join(dir, KIT_REL), { recursive: true, filter: (src) => !src.includes(`${path.sep}test`) && !src.endsWith('.state') });
  sh(dir, 'git', ['add', '.']);
  sh(dir, 'git', ['-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-qm', 'init']);
  const inst = spawnSync(process.execPath, [path.join(dir, KIT_REL, 'install.mjs')], { cwd: dir, encoding: 'utf8' });
  assert.equal(inst.status, 0, inst.stdout + inst.stderr);
  return dir;
}

function hook(dir, tool, event, input, cwd) {
  const r = spawnSync(process.execPath, [path.join(dir, KIT_REL, 'bin', 'rk.mjs'), 'hook', tool, event], {
    cwd: cwd || (tool === 'agy' ? path.join(dir, '.agents') : dir),
    input: JSON.stringify(input),
    encoding: 'utf8',
  });
  assert.equal(r.status, 0, r.stderr);
  return JSON.parse(r.stdout);
}

function rk(dir, ...args) {
  return spawnSync(process.execPath, [path.join(dir, KIT_REL, 'bin', 'rk.mjs'), ...args], { cwd: dir, encoding: 'utf8' });
}

const ctxOf = (o) => o.hookSpecificOutput?.additionalContext || o.injectSteps?.[0]?.ephemeralMessage || '';
const ledgerOf = (dir, key) => path.join(dir, '.agent-ledger', `${key}.md`);
const readErrors = (dir) => {
  const f = path.join(dir, '.agent-ledger', '.state', 'hook-errors.log');
  return fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : '';
};

function fillGate(dir, key, gateLines, reqLines = ['- R1 (M1) "sửa app" → app.txt có v2']) {
  const f = ledgerOf(dir, key);
  let text = fs.readFileSync(f, 'utf8');
  text = text.replace(/## Yêu cầu\n/, `## Yêu cầu\n${reqLines.join('\n')}\n`);
  text = text.replace(/## Done-gate\n/, `## Done-gate\n${gateLines.join('\n')}\n`);
  fs.writeFileSync(f, text);
}

const GOOD_GATE = [
  '- R1 ✅ đổi app.txt thành v2 — bằng chứng: `cat app.txt` in ra "v2"',
  '- Quy tắc: đã đối chiếu AGENTS.md Rule A — không áp dụng cho file txt',
  '- Diff: đã đọc hunk duy nhất của app.txt — ngoài phạm vi: không',
  '- Kiểm tra: `cat app.txt` → v2',
];

test('install tạo đủ file trỏ, chạy lại không đổi gì, --check báo đủ', () => {
  const dir = makeProject();
  for (const f of ['.agents/rules/rule-keeper.md', '.agents/hooks.json', '.codex/hooks.json', '.agent-ledger/.gitignore']) {
    assert.ok(fs.existsSync(path.join(dir, f)), f);
  }
  const rule = fs.readFileSync(path.join(dir, '.agents/rules/rule-keeper.md'), 'utf8');
  assert.match(rule, /^---\ntrigger: always_on\n---/);
  assert.match(rule, /Không commit khi chưa được yêu cầu rõ/);
  assert.doesNotMatch(rule, /\{\{KIT\}\}/);
  const again = spawnSync(process.execPath, [path.join(dir, KIT_REL, 'install.mjs')], { encoding: 'utf8' });
  assert.match(again.stdout, /đã khớp/);
  assert.doesNotMatch(again.stdout, /tạo mới|cập nhật\)/);
  assert.equal(spawnSync(process.execPath, [path.join(dir, KIT_REL, 'install.mjs'), '--check'], { encoding: 'utf8' }).status, 0);
});

test('install không ghi đè hooks.json có sẵn của người khác', () => {
  const dir = makeProject();
  spawnSync(process.execPath, [path.join(dir, KIT_REL, 'install.mjs'), '--uninstall'], { encoding: 'utf8' });
  assert.ok(!fs.existsSync(path.join(dir, '.codex/hooks.json')));
  const foreign = '{ "hooks": { "Stop": [] } }\n';
  fs.writeFileSync(path.join(dir, '.codex/hooks.json'), foreign);
  const r = spawnSync(process.execPath, [path.join(dir, KIT_REL, 'install.mjs')], { encoding: 'utf8' });
  assert.equal(r.status, 1);
  assert.match(r.stdout, /KHÔNG ghi đè/);
  assert.equal(fs.readFileSync(path.join(dir, '.codex/hooks.json'), 'utf8'), foreign);
});

test('codex: session-start nạp luật + sổ, prompt ghi nguyên văn, quy tắc đổi thì báo diff', () => {
  const dir = makeProject();
  const sid = 'aaaa1111-2222';
  const start = ctxOf(hook(dir, 'codex', 'session-start', { session_id: sid, cwd: dir, source: 'startup' }));
  assert.match(start, /Sổ yêu cầu của phiên này: \.agent-ledger\/codex-aaaa1111\.md/);
  assert.match(start, /AGENTS\.md — \d+ dòng/);
  assert.match(start, /CLAUDE\.md — \d+ dòng/);
  assert.match(start, /Thứ tự ưu tiên/);
  assert.ok(fs.existsSync(ledgerOf(dir, 'codex-aaaa1111')));

  const p1 = ctxOf(hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'Đổi app.txt thành v2.\nĐừng commit.' }));
  assert.match(p1, /ghi nguyên văn vào sổ là M1/);
  const ledger = fs.readFileSync(ledgerOf(dir, 'codex-aaaa1111'), 'utf8');
  assert.match(ledger, /### M1 · .*\n> Đổi app\.txt thành v2\.\n> Đừng commit\./);

  fs.appendFileSync(path.join(dir, 'AGENTS.md'), '- Rule B: never touch app.txt on Fridays.\n');
  const p2 = ctxOf(hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'tiếp tục' }));
  assert.match(p2, /M2/);
  assert.match(p2, /QUY TẮC ĐÃ ĐỔI/);
  assert.match(p2, /\+- Rule B: never touch app\.txt on Fridays\./);
  const p3 = ctxOf(hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'ok' }));
  assert.doesNotMatch(p3, /QUY TẮC ĐÃ ĐỔI/, 'một thay đổi chỉ báo một lần');

  const resumed = ctxOf(hook(dir, 'codex', 'session-start', { session_id: sid, cwd: dir, source: 'compact' }));
  assert.match(resumed, /vừa được NÉN/);
  assert.match(resumed, /M1: Đổi app\.txt thành v2\./);
  assert.equal(readErrors(dir), '');
});

test('codex: stop chặn khi có việc mà chưa qua gate, không chặn lặp, gate OK thì cho dừng', () => {
  const dir = makeProject();
  const sid = 'bbbb2222';
  hook(dir, 'codex', 'session-start', { session_id: sid, cwd: dir, source: 'startup' });
  hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'sửa app thành v2' });

  assert.deepEqual(hook(dir, 'codex', 'stop', { session_id: sid, cwd: dir, last_assistant_message: 'Mình đọc code rồi.' }), {});

  fs.writeFileSync(path.join(dir, 'app.txt'), 'v2\n');
  const asking = hook(dir, 'codex', 'stop', { session_id: sid, cwd: dir, last_assistant_message: 'Có hai cách đổi định dạng.\n\nBạn muốn giữ định dạng cũ không?' });
  assert.deepEqual(asking, {}, 'chỉ hỏi người dùng, không kể việc đã làm → không chặn');
  const offer = hook(dir, 'codex', 'stop', { session_id: sid, cwd: dir, last_assistant_message: 'Mình đã cập nhật app.txt.\n\nBạn có muốn mình làm thêm gì không?' });
  assert.equal(offer.decision, 'block', 'kể việc đã làm rồi chốt bằng câu hỏi xã giao vẫn phải qua gate');
  fs.writeFileSync(path.join(dir, 'app.txt'), 'v2 \n');
  fs.writeFileSync(path.join(dir, 'app.txt'), 'v2\n');

  const b1 = hook(dir, 'codex', 'stop', { session_id: sid, cwd: dir, last_assistant_message: 'Đã xong.' });
  assert.equal(b1.decision, 'block');
  assert.match(b1.reason, /app\.txt/);
  assert.match(b1.reason, /rk\.mjs gate --ledger \.agent-ledger\/codex-bbbb2222\.md/);

  const b2 = hook(dir, 'codex', 'stop', { session_id: sid, cwd: dir, stop_hook_active: true, last_assistant_message: 'Đã xong.' });
  assert.equal(b2.decision, undefined, 'agent không làm gì thêm thì không chặn lặp');
  assert.match(b2.systemMessage, /CHƯA qua done-gate/);
  assert.deepEqual(
    hook(dir, 'codex', 'stop', { session_id: sid, cwd: dir, last_assistant_message: 'Đã xong.' }),
    {},
    'đã cảnh báo đúng trạng thái này rồi thì không chặn lại từ đầu',
  );
  const next = ctxOf(hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'còn gì nữa không' }));
  assert.match(next, /Lượt trước kết thúc khi CHƯA qua done-gate/, 'tin nhắn kế nhắc agent');

  const bad = rk(dir, 'gate', '--ledger', '.agent-ledger/codex-bbbb2222.md');
  assert.equal(bad.status, 1);
  assert.match(bad.stdout, /chưa có dòng R# nào/);

  fillGate(dir, 'codex-bbbb2222', [...GOOD_GATE, '- M2 — không có yêu cầu mới']);
  const ok = rk(dir, 'gate', '--ledger', '.agent-ledger/codex-bbbb2222.md');
  assert.equal(ok.status, 0, ok.stdout);
  assert.doesNotMatch(
    ctxOf(hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'ok' })),
    /Lượt trước kết thúc khi CHƯA/,
    'GATE OK thì thôi nhắc',
  );
  fillGate(dir, 'codex-bbbb2222', [...GOOD_GATE, '- M2 — không có yêu cầu mới', '- M3 — không có yêu cầu mới'], []);
  assert.equal(rk(dir, 'gate', '--ledger', '.agent-ledger/codex-bbbb2222.md').status, 0);
  assert.match(ok.stdout, /GATE OK — 1 xong/);
  assert.deepEqual(hook(dir, 'codex', 'stop', { session_id: sid, cwd: dir, last_assistant_message: 'Đã xong.' }), {});

  fs.writeFileSync(path.join(dir, 'app.txt'), 'v3\n');
  assert.equal(hook(dir, 'codex', 'stop', { session_id: sid, cwd: dir, last_assistant_message: 'Sửa thêm rồi.' }).decision, 'block', 'sửa sau gate thì phải gate lại');
  assert.equal(readErrors(dir), '');
});

test('gate: đòi bằng chứng cho ✅, chấp nhận ⚠️ có lý do, bỏ qua yêu cầu đã bị thay, đòi tính mọi tin nhắn', () => {
  const dir = makeProject();
  const sid = 'cccc3333';
  hook(dir, 'codex', 'session-start', { session_id: sid, cwd: dir, source: 'startup' });
  hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'làm A và B' });
  hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'thôi bỏ B, làm C' });
  const key = 'codex-cccc3333';
  fillGate(
    dir,
    key,
    ['- R1 ✅ làm A', '- R3 ⚠️ C mới xong một nửa: còn thiếu phần xuất file', '- Quy tắc: AGENTS.md Rule A', '- Diff: không sửa file', '- Kiểm tra: chưa chạy — không có lệnh test'],
    ['- R1 (M1) "làm A" → A', '- R2 (M1) "làm B" → B [huỷ: người dùng bỏ ở M2]', '- R3 (M2) "làm C" → C'],
  );
  const r1 = rk(dir, 'gate', '--ledger', `.agent-ledger/${key}.md`);
  assert.equal(r1.status, 1);
  assert.match(r1.stdout, /R1 đánh dấu ✅ nhưng thiếu "bằng chứng/);
  assert.doesNotMatch(r1.stdout, /R2/);

  const f = ledgerOf(dir, key);
  fs.writeFileSync(f, fs.readFileSync(f, 'utf8').replace('- R1 ✅ làm A', '- R1 ✅ làm A — bằng chứng: a.txt dòng 1 là "A"'));
  const r2 = rk(dir, 'gate', '--ledger', `.agent-ledger/${key}.md`);
  assert.equal(r2.status, 0, r2.stdout);
  assert.match(r2.stdout, /PHẢI nói rõ/);
  assert.match(r2.stdout, /R3/);

  hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'ok' });
  const r3 = rk(dir, 'gate', '--ledger', `.agent-ledger/${key}.md`);
  assert.equal(r3.status, 1);
  assert.match(r3.stdout, /M3 chưa được dòng R# nào dẫn tới/);
});

test('gate từ chối khi quy tắc đổi sau lần xem cuối, rồi cho qua ở lần sau', () => {
  const dir = makeProject();
  const sid = 'dddd4444';
  hook(dir, 'codex', 'session-start', { session_id: sid, cwd: dir, source: 'startup' });
  hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'sửa app' });
  fillGate(dir, 'codex-dddd4444', GOOD_GATE);
  fs.appendFileSync(path.join(dir, 'CLAUDE.md'), '\nNever ship on Monday.\n');
  const r1 = rk(dir, 'gate', '--ledger', '.agent-ledger/codex-dddd4444.md');
  assert.equal(r1.status, 1);
  assert.match(r1.stdout, /\+Never ship on Monday\./);
  assert.equal(rk(dir, 'gate', '--ledger', '.agent-ledger/codex-dddd4444.md').status, 0);
});

test('codex: chuỗi lệnh trong .codex/hooks.json chạy được qua shell, kể cả từ thư mục con', () => {
  const dir = makeProject();
  fs.mkdirSync(path.join(dir, 'sub'));
  const conf = JSON.parse(fs.readFileSync(path.join(dir, '.codex/hooks.json'), 'utf8'));
  const command = conf.hooks.SessionStart[0].hooks[0].command;
  const r = spawnSync(command, {
    shell: true,
    cwd: path.join(dir, 'sub'),
    input: JSON.stringify({ session_id: 'eeee5555', cwd: path.join(dir, 'sub'), source: 'startup' }),
    encoding: 'utf8',
  });
  assert.equal(r.status, 0, r.stderr);
  assert.match(ctxOf(JSON.parse(r.stdout)), /codex-eeee5555/);
  assert.ok(fs.existsSync(ledgerOf(dir, 'codex-eeee5555')), 'sổ nằm ở gốc project, không ở thư mục con');
});

test('antigravity: đọc tin nhắn từ transcript, chỉ chèn khi có gì mới, báo quy tắc đổi, stop yêu cầu gate', () => {
  const dir = makeProject();
  const tr = path.join(dir, 'transcript_full.jsonl');
  const line = (o) => fs.appendFileSync(tr, `${JSON.stringify(o)}\n`);
  line({ step_index: 0, type: 'USER_INPUT', content: '<USER_REQUEST>\nĐổi app.txt thành v2\n</USER_REQUEST>\n<ADDITIONAL_METADATA>\ngiờ\n</ADDITIONAL_METADATA>' });
  const base = { conversationId: 'ffff6666-x', workspacePaths: [dir.split(path.sep).join('/')], transcriptPath: tr };

  const first = ctxOf(hook(dir, 'agy', 'pre', { ...base, invocationNum: 0 }));
  assert.match(first, /Phiên mới \(agy\)/);
  assert.match(first, /ghi nguyên văn vào sổ là M1/);
  const ledger = fs.readFileSync(ledgerOf(dir, 'agy-ffff6666'), 'utf8');
  assert.match(ledger, /> Đổi app\.txt thành v2/);
  assert.doesNotMatch(ledger, /ADDITIONAL_METADATA|giờ/);

  line({ step_index: 1, type: 'PLANNER_RESPONSE', content: 'Đang sửa.' });
  assert.deepEqual(hook(dir, 'agy', 'pre', { ...base, invocationNum: 1 }), {}, 'không có gì mới thì không chèn');

  fs.appendFileSync(path.join(dir, 'CLAUDE.md'), '\n- New rule: log everything.\n');
  assert.match(ctxOf(hook(dir, 'agy', 'pre', { ...base, invocationNum: 2 })), /\+- New rule: log everything\./);

  line({ step_index: 2, type: 'USER_INPUT', content: '<USER_REQUEST>\nNhớ: không dùng tab\n</USER_REQUEST>' });
  assert.match(ctxOf(hook(dir, 'agy', 'pre', { ...base, invocationNum: 0 })), /là M2/);

  fs.writeFileSync(path.join(dir, 'app.txt'), 'v2\n');
  line({ step_index: 3, type: 'PLANNER_RESPONSE', content: 'Xong rồi.' });
  const stop = hook(dir, 'agy', 'stop', { ...base, terminationReason: 'NO_TOOL_CALL', executionNum: 0 });
  assert.equal(stop.decision, 'continue');
  assert.match(stop.reason, /agy-ffff6666\.md/);
  assert.equal(readErrors(dir), '');
});

test('sửa rules/user.md của kit thì bản luôn-bật của Antigravity tự cập nhật ở lần hook kế', () => {
  const dir = makeProject();
  fs.appendFileSync(path.join(dir, KIT_REL, 'rules', 'user.md'), '\n6. **Luật mới thử nghiệm.**\n');
  hook(dir, 'codex', 'session-start', { session_id: 'gggg7777', cwd: dir, source: 'startup' });
  assert.match(fs.readFileSync(path.join(dir, '.agents/rules/rule-keeper.md'), 'utf8'), /Luật mới thử nghiệm/);
});

test('hook không bao giờ làm hỏng phiên: input rác vẫn trả JSON hợp lệ', () => {
  const dir = makeProject();
  const r = spawnSync(process.execPath, [path.join(dir, KIT_REL, 'bin', 'rk.mjs'), 'hook', 'codex', 'stop'], { cwd: dir, input: 'not json', encoding: 'utf8' });
  assert.equal(r.status, 0);
  assert.deepEqual(JSON.parse(r.stdout), {});
});

test('tin nhắn mới dời Done-gate cũ xuống lịch sử; gate chỉ đọc mục hiện tại', () => {
  const dir = makeProject();
  const sid = 'hhhh8888';
  const key = 'codex-hhhh8888';
  hook(dir, 'codex', 'session-start', { session_id: sid, cwd: dir, source: 'startup' });
  hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'sửa app' });
  fillGate(dir, key, GOOD_GATE);
  assert.equal(rk(dir, 'gate', '--ledger', `.agent-ledger/${key}.md`).status, 0);

  hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'giờ sửa thêm B' });
  const text = fs.readFileSync(ledgerOf(dir, key), 'utf8');
  assert.match(text, /## Lịch sử done-gate[\s\S]*### Trước M2[\s\S]*R1 ✅ đổi app\.txt/);
  const current = text.split('## Done-gate')[1].split('## Lịch sử')[0];
  assert.doesNotMatch(current.replace(/<!--[^]*?-->/g, ""), /R1 ✅/, 'mục Done-gate hiện tại phải trống để điền lại');
  const r1 = rk(dir, 'gate', '--ledger', `.agent-ledger/${key}.md`);
  assert.equal(r1.status, 1);
  assert.match(r1.stdout, /^GATE FAILED/m);
  assert.match(r1.stdout, /R1 chưa có dòng trong Done-gate/);

  fillGate(dir, key, [...GOOD_GATE, '- M2 — không có yêu cầu mới'], []);
  const r2 = rk(dir, 'gate', '--ledger', `.agent-ledger/${key}.md`);
  assert.equal(r2.status, 0, r2.stdout);
  assert.match(r2.stdout, /GATE OK — 1 xong/);

  hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'ok' });
  const again = fs.readFileSync(ledgerOf(dir, key), 'utf8');
  assert.equal((again.match(/## Lịch sử done-gate/g) || []).length, 1, 'chỉ một mục lịch sử');
  assert.match(again, /### Trước M2[\s\S]*### Trước M3/);
});

test('dấu đóng: "[huỷ]" trong lời trích không đóng yêu cầu; chỉ [huỷ: lý do] / [thay bởi R#] ngoài ngoặc kép mới đóng', () => {
  const dir = makeProject();
  const sid = 'iiii9999';
  const key = 'codex-iiii9999';
  hook(dir, 'codex', 'session-start', { session_id: sid, cwd: dir, source: 'startup' });
  hook(dir, 'codex', 'prompt', { session_id: sid, cwd: dir, prompt: 'thêm nút [huỷ] vào form; bỏ ý B' });
  fillGate(
    dir,
    key,
    ['- Quy tắc: AGENTS.md Rule A', '- Diff: không sửa file', '- Kiểm tra: chưa chạy — chưa có code'],
    [
      '- R1 (M1) "thêm nút [huỷ] vào form" → form có nút huỷ',
      '- R2 (M1) “đừng [bỏ] trống tiêu đề” → tiêu đề bắt buộc',
      '- R3 (M1) "ý B" → B [huỷ: người dùng bỏ ở M1]',
      '- R4 (M1) "ý C" → C [huỷ]',
      '- R5 (M1) "ý D" → D [thay bởi R6]',
      '- R6 (M1) "ý D mới" → D2',
    ],
  );
  const r = rk(dir, 'gate', '--ledger', `.agent-ledger/${key}.md`);
  assert.equal(r.status, 1);
  assert.match(r.stdout, /R1 chưa có dòng trong Done-gate/, '"[huỷ]" trong lời trích không được đóng R1');
  assert.match(r.stdout, /R2 chưa có dòng trong Done-gate/, 'ngoặc kép cong cũng là lời trích');
  assert.doesNotMatch(r.stdout, /R3 /, '[huỷ: lý do] đóng R3');
  assert.match(r.stdout, /R4 chưa có dòng[^\n]*\[huỷ: <lý do, M#>\]/, '[huỷ] trần không đóng, và gate chỉ cách viết đúng');
  assert.doesNotMatch(r.stdout, /R5 /, '[thay bởi R6] đóng R5');
  assert.match(r.stdout, /R6 chưa có dòng/);
  assert.doesNotMatch(r.stdout, /R1 chưa có dòng[^\n]*lý do/, 'R1 không bị gợi ý sai về dấu đóng');
});

test('antigravity: hết lượt chặn thì ép một bước báo người dùng, không chặn lặp, tin nhắn kế nhắc lại tới khi gate qua', () => {
  const dir = makeProject();
  const tr = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'rk-brain-')), 'transcript_full.jsonl'); // như Antigravity: ngoài repo
  const line = (o) => fs.appendFileSync(tr, `${JSON.stringify(o)}\n`);
  const base = { conversationId: 'jjjj0000-x', workspacePaths: [dir], transcriptPath: tr };
  const stop = () => hook(dir, 'agy', 'stop', { ...base, terminationReason: 'NO_TOOL_CALL', executionNum: 0 });
  line({ type: 'USER_INPUT', content: '<USER_REQUEST>\nĐổi app.txt thành v2\n</USER_REQUEST>' });
  hook(dir, 'agy', 'pre', { ...base, invocationNum: 0 });
  fs.writeFileSync(path.join(dir, 'app.txt'), 'v2\n');
  line({ type: 'PLANNER_RESPONSE', content: 'Xong rồi.' });

  const s1 = stop();
  assert.equal(s1.decision, 'continue');
  assert.match(s1.reason, /Chưa được kết thúc lượt/);

  const s2 = stop();
  assert.equal(s2.decision, 'continue', 'agent không làm gì thêm: không được kết thúc im lặng');
  assert.match(s2.reason, /Việc DUY NHẤT còn lại[^]*CHƯA qua done-gate/);

  line({ type: 'USER_INPUT', content: `<USER_REQUEST>\n${s2.reason}\n</USER_REQUEST>` });
  line({ type: 'PLANNER_RESPONSE', content: 'Lưu ý: việc này CHƯA qua done-gate nên chưa được coi là xong.' });
  assert.deepEqual(stop(), {}, 'đã báo người dùng đúng trạng thái này rồi thì cho dừng');
  assert.doesNotMatch(fs.readFileSync(ledgerOf(dir, 'agy-jjjj0000'), 'utf8'), /Việc DUY NHẤT/, 'lời nhắc của chính hook không thành tin nhắn người dùng');

  line({ type: 'USER_INPUT', content: '<USER_REQUEST>\nok, tiếp đi\n</USER_REQUEST>' });
  const pre = ctxOf(hook(dir, 'agy', 'pre', { ...base, invocationNum: 0 }));
  assert.match(pre, /là M2/);
  assert.match(pre, /Lượt trước kết thúc khi CHƯA qua done-gate/);

  fillGate(dir, 'agy-jjjj0000', [...GOOD_GATE, '- M2 — không có yêu cầu mới']);
  assert.equal(rk(dir, 'gate', '--ledger', '.agent-ledger/agy-jjjj0000.md').status, 0);
  line({ type: 'USER_INPUT', content: '<USER_REQUEST>\ncảm ơn\n</USER_REQUEST>' });
  assert.doesNotMatch(ctxOf(hook(dir, 'agy', 'pre', { ...base, invocationNum: 0 })), /Lượt trước kết thúc khi CHƯA/);
  assert.equal(readErrors(dir), '');
});

function makeKitOnly({ git }) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), git ? 'rk-git-' : 'rk-nogit-'));
  fs.writeFileSync(path.join(dir, 'AGENTS.md'), '# Rules\n\n- Rule A.\n');
  fs.writeFileSync(path.join(dir, 'app.txt'), 'v1\n');
  fs.cpSync(KIT, path.join(dir, KIT_REL), { recursive: true, filter: (src) => !src.includes(`${path.sep}test`) && !src.endsWith('.state') });
  if (git) {
    sh(dir, 'git', ['init', '-q']);
    sh(dir, 'git', ['add', '.']);
    sh(dir, 'git', ['-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-qm', 'init']);
  }
  return dir;
}

const node = (dir, script, ...args) =>
  spawnSync(process.execPath, [path.join(dir, KIT_REL, script), ...args], { cwd: dir, encoding: 'utf8', input: '' });

test('project không dùng git: install cài ở gốc project (không vào trong kit), --only tách phần từng công cụ, gate chạy đúng', () => {
  const dir = makeKitOnly({ git: false });
  assert.equal(node(dir, 'install.mjs', '--only', 'codex').status, 0);
  assert.ok(fs.existsSync(path.join(dir, '.codex/hooks.json')), '.codex/hooks.json ở gốc project');
  assert.ok(!fs.existsSync(path.join(dir, '.agents/hooks.json')), '--only codex không cài phần Antigravity');
  assert.ok(!fs.existsSync(path.join(dir, KIT_REL, '.codex')), 'không có gì bị cài vào trong thư mục kit');
  assert.equal(node(dir, 'install.mjs', '--check', '--only', 'codex').status, 0);
  assert.equal(node(dir, 'install.mjs', '--check').status, 1, 'phần Antigravity vẫn chưa cài');
  assert.equal(node(dir, 'install.mjs', '--only=antigravity').status, 0);
  assert.ok(fs.existsSync(path.join(dir, '.agents/hooks.json')));
  assert.ok(fs.existsSync(path.join(dir, '.agents/rules/rule-keeper.md')));
  assert.equal(node(dir, 'install.mjs', '--check').status, 0);

  fs.mkdirSync(path.join(dir, 'sub'));
  const command = JSON.parse(fs.readFileSync(path.join(dir, '.codex/hooks.json'), 'utf8')).hooks.SessionStart[0].hooks[0].command;
  const r = spawnSync(command, { shell: true, cwd: path.join(dir, 'sub'), input: JSON.stringify({ session_id: 'kkkk1111', cwd: path.join(dir, 'sub'), source: 'startup' }), encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  assert.match(ctxOf(JSON.parse(r.stdout)), /codex-kkkk1111/);
  assert.ok(fs.existsSync(ledgerOf(dir, 'codex-kkkk1111')), 'không có git, mở từ thư mục con: sổ vẫn ở gốc project');

  hook(dir, 'codex', 'prompt', { session_id: 'kkkk1111', cwd: dir, prompt: 'sửa app' });
  fillGate(dir, 'codex-kkkk1111', GOOD_GATE);
  const g = rk(dir, 'gate', '--ledger', '.agent-ledger/codex-kkkk1111.md');
  assert.equal(g.status, 0, g.stdout);
  assert.deepEqual(hook(dir, 'codex', 'stop', { session_id: 'kkkk1111', cwd: dir, last_assistant_message: 'Đã xong.' }), {}, 'gate ghi dấu đúng phiên');
  assert.equal(readErrors(dir), '');
});

test('setup.mjs: cài, chạy thử hook đúng như công cụ gọi, dọn phiên thử — cho Codex và Antigravity', () => {
  const dir = makeKitOnly({ git: true });
  const c = node(dir, 'setup.mjs', 'codex', '--no-open');
  assert.equal(c.status, 0, c.stdout + c.stderr);
  for (const s of ['✓ SessionStart', '✓ UserPromptSubmit', '✓ Stop', 'Setup Codex: xong phần tự động']) assert.ok(c.stdout.includes(s), s);
  assert.doesNotMatch(c.stderr, /DEP0190|Warning/);
  assert.ok(!fs.existsSync(path.join(dir, '.agents/hooks.json')), 'setup Codex không cài phần Antigravity');

  const a = node(dir, 'setup.mjs', 'antigravity', '--no-open');
  assert.equal(a.status, 0, a.stdout + a.stderr);
  for (const s of ['✓ PreInvocation', '✓ Stop', '✓ Luật luôn bật', 'Setup Antigravity: xong phần tự động']) assert.ok(a.stdout.includes(s), s);

  const left = fs.readdirSync(path.join(dir, '.agent-ledger')).concat(fs.readdirSync(path.join(dir, '.agent-ledger', '.state')));
  assert.ok(!left.some((f) => f.includes('rksetup0')), `phiên thử phải được dọn: ${left.join(', ')}`);
  assert.equal(readErrors(dir), '');
  assert.equal(sh(dir, 'git', ['status', '--porcelain', '--', '.agent-ledger']).trim(), '', 'sổ không lộ ra git');
});

test('setup.mjs trên project không dùng git: vẫn xong, và nói rõ giới hạn', () => {
  const dir = makeKitOnly({ git: false });
  const c = node(dir, 'setup.mjs', 'codex', '--no-open');
  assert.equal(c.status, 0, c.stdout + c.stderr);
  assert.match(c.stdout, /Project không dùng git/);
  assert.match(c.stdout, /✓ UserPromptSubmit/);
});

test('setup-*.cmd chạy được qua cmd.exe (bấm đúp)', { skip: process.platform !== 'win32' }, () => {
  const dir = makeKitOnly({ git: true });
  for (const [file, name] of [['setup-codex.cmd', 'Codex'], ['setup-antigravity.cmd', 'Antigravity']]) {
    const r = spawnSync('cmd.exe', ['/c', path.join(dir, KIT_REL, file), '--no-open'], { cwd: os.tmpdir(), input: '\r\n', encoding: 'utf8', windowsHide: true });
    assert.equal(r.status, 0, `${file}: ${r.stdout}${r.stderr}`);
    assert.ok(r.stdout.includes(`Setup ${name}: xong phần tự động`), `${file}: ${r.stdout.slice(-400)}`);
  }
});
