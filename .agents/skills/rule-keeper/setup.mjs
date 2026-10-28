#!/usr/bin/env node
// Setup trọn gói cho MỘT công cụ: kiểm tra máy, cài file trỏ, chạy thử hook đúng như công cụ sẽ
// gọi, xem công cụ đã có trên máy chưa, rồi chỉ (và mở sẵn) bước cuối mà người dùng phải tự làm.
// Người dùng không gọi file này trực tiếp mà bấm đúp setup-codex.cmd / setup-antigravity.cmd.
//
//   node .agents/skills/rule-keeper/setup.mjs codex        [--no-open]
//   node .agents/skills/rule-keeper/setup.mjs antigravity  [--no-open]
//
// --no-open (hoặc chạy không có bàn phím) thì không hỏi, không mở cửa sổ nào.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { createInterface } from 'node:readline/promises';
import { fileURLToPath } from 'node:url';
import { loadConfig, projectRoot } from './bin/rk.mjs';

const KIT_DIR = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const tool = String(argv[0] || '').toLowerCase().replace(/^agy$/, 'antigravity');
const interactive = !argv.includes('--no-open') && process.stdin.isTTY && process.stdout.isTTY;
const NAME = { codex: 'Codex', antigravity: 'Antigravity' }[tool];
const TEST_ID = 'rksetup0';

if (!NAME) {
  console.error('Cách dùng: node setup.mjs codex|antigravity [--no-open]');
  process.exit(2);
}

let failed = 0;
const ok = (m) => console.log(`  ✓ ${m}`);
const warn = (m) => console.log(`  ⚠ ${m}`);
const bad = (m) => {
  failed++;
  console.log(`  ✗ ${m}`);
};
const step = (n, m) => console.log(`\n[${n}/5] ${m}`);
const run = (cmd, args, opts = {}) => spawnSync(cmd, args, { encoding: 'utf8', windowsHide: true, ...opts });

console.log(`rule-keeper — setup cho ${NAME}`);

// 1. Máy -----------------------------------------------------------------------------------------
step(1, 'Kiểm tra máy');
const nodeMajor = Number(process.versions.node.split('.')[0]);
if (nodeMajor >= 18) ok(`Node.js ${process.versions.node}`);
else {
  bad(`Node.js ${process.versions.node} quá cũ — cần bản 18 trở lên (cài bản LTS ở nodejs.org).`);
  finish();
}
const root = projectRoot(KIT_DIR);
const hasGit = run('git', ['--version']).status === 0;
const inRepo = hasGit && run('git', ['rev-parse', '--show-toplevel'], { cwd: root }).status === 0;
ok(`Project: ${root}`);
if (!hasGit) warn('Máy chưa có git: kit vẫn chạy, nhưng không biết file nào đã đổi và không tính được diff quy tắc.');
else if (!inRepo) warn('Project không dùng git: kit vẫn chạy, nhưng hook không biết file nào đã đổi — gate chỉ được đòi khi agent nói "xong".');

// 2. Cài -----------------------------------------------------------------------------------------
step(2, `Cài file trỏ cho ${NAME}`);
const inst = run(process.execPath, [path.join(KIT_DIR, 'install.mjs'), '--only', tool]);
const instOut = `${inst.stdout || ''}${inst.stderr || ''}`;
if (inst.status === 0) {
  for (const l of instOut.split(/\r?\n/).filter((l) => /^\s+[+✓⚠]/.test(l))) console.log(`  ${l.trim()}`);
} else {
  // In nguyên văn: khi từ chối ghi đè, phần cần gộp tay nằm trong output này.
  console.log(instOut.replace(/^/gm, '  '));
  bad('Cài chưa xong — đọc dòng ✗ ở trên (thường là file hook có sẵn của người khác: tự gộp nội dung được in ra).');
  finish();
}

// 3. Chạy thử hook ------------------------------------------------------------------------------
step(3, 'Chạy thử hook đúng như công cụ sẽ gọi');
const cfg = loadConfig();
const ledgerDir = path.join(root, cfg.ledgerDir);
const errLog = path.join(ledgerDir, '.state', 'hook-errors.log');
const errSize = () => (fs.existsSync(errLog) ? fs.statSync(errLog).size : 0);
const errBefore = errSize();
const prefix = tool === 'codex' ? 'codex' : 'agy';
const cleanup = [path.join(ledgerDir, `${prefix}-${TEST_ID}.md`), path.join(ledgerDir, '.state', `${prefix}-${TEST_ID}`)];

function callHook(command, cwd, input) {
  const r = spawnSync(command, { shell: true, cwd, input: JSON.stringify(input), encoding: 'utf8', windowsHide: true, timeout: 60_000 });
  try {
    return { json: JSON.parse(r.stdout || ''), raw: r };
  } catch {
    return { json: null, raw: r };
  }
}

try {
  if (tool === 'codex') {
    const conf = JSON.parse(fs.readFileSync(path.join(root, '.codex', 'hooks.json'), 'utf8')).hooks;
    const base = { session_id: TEST_ID, cwd: root, model: 'setup-test' };
    const s = callHook(conf.SessionStart[0].hooks[0].command, root, { ...base, hook_event_name: 'SessionStart', source: 'startup' });
    const sctx = s.json?.hookSpecificOutput?.additionalContext || '';
    if (/Sổ yêu cầu của phiên này/.test(sctx)) ok('SessionStart: nạp luật + sổ yêu cầu');
    else bad(`SessionStart không trả nội dung mong đợi. ${(s.raw.stderr || s.raw.stdout || '').slice(0, 300)}`);
    const p = callHook(conf.UserPromptSubmit[0].hooks[0].command, root, { ...base, hook_event_name: 'UserPromptSubmit', prompt: 'tin nhắn thử của setup' });
    const ledger = fs.existsSync(cleanup[0]) ? fs.readFileSync(cleanup[0], 'utf8') : '';
    if (/là M1/.test(p.json?.hookSpecificOutput?.additionalContext || '') && /> tin nhắn thử của setup/.test(ledger)) ok('UserPromptSubmit: chép nguyên văn tin nhắn vào sổ');
    else bad(`UserPromptSubmit không ghi được tin nhắn vào sổ. ${(p.raw.stderr || '').slice(0, 300)}`);
    const st = callHook(conf.Stop[0].hooks[0].command, root, { ...base, hook_event_name: 'Stop', stop_hook_active: false, last_assistant_message: 'ok' });
    if (st.json && typeof st.json === 'object') ok('Stop: trả JSON hợp lệ');
    else bad(`Stop không trả JSON hợp lệ. ${(st.raw.stderr || st.raw.stdout || '').slice(0, 300)}`);
  } else {
    const conf = JSON.parse(fs.readFileSync(path.join(root, '.agents', 'hooks.json'), 'utf8'))['rule-keeper'];
    const brain = fs.mkdtempSync(path.join(os.tmpdir(), 'rk-setup-'));
    const transcript = path.join(brain, 'transcript_full.jsonl');
    fs.writeFileSync(transcript, `${JSON.stringify({ step_index: 0, type: 'USER_INPUT', content: '<USER_REQUEST>\ntin nhắn thử của setup\n</USER_REQUEST>' })}\n`);
    cleanup.push(brain);
    const base = { conversationId: TEST_ID, workspacePaths: [root.split(path.sep).join('/')], transcriptPath: transcript, modelName: 'setup-test' };
    const agentsDir = path.join(root, '.agents');
    const pre = callHook(conf.PreInvocation[0].command, agentsDir, { ...base, invocationNum: 0, initialNumSteps: 1 });
    const msg = pre.json?.injectSteps?.[0]?.ephemeralMessage || '';
    if (/Phiên mới \(agy\)/.test(msg) && /là M1/.test(msg)) ok('PreInvocation: nạp sổ + đọc được tin nhắn từ transcript');
    else bad(`PreInvocation không trả nội dung mong đợi. ${(pre.raw.stderr || pre.raw.stdout || '').slice(0, 300)}`);
    const st = callHook(conf.Stop[0].command, agentsDir, { ...base, executionNum: 0, terminationReason: 'NO_TOOL_CALL', fullyIdle: true });
    if (st.json && typeof st.json === 'object') ok('Stop: trả JSON hợp lệ');
    else bad(`Stop không trả JSON hợp lệ. ${(st.raw.stderr || st.raw.stdout || '').slice(0, 300)}`);
    const rule = fs.readFileSync(path.join(root, '.agents', 'rules', 'rule-keeper.md'), 'utf8');
    if (/^---\ntrigger: always_on\n---/.test(rule)) ok('Luật luôn bật: .agents/rules/rule-keeper.md');
    else bad('.agents/rules/rule-keeper.md thiếu "trigger: always_on" — Antigravity sẽ bỏ qua nó.');
  }
  if (errSize() > errBefore) bad(`Hook ghi lỗi vào ${path.relative(root, errLog)} — mở file đó xem dòng cuối.`);
} catch (e) {
  bad(`Không chạy thử được hook: ${e.message}`);
} finally {
  // Chỉ xoá đúng phiên thử do chính setup vừa tạo.
  for (const p of cleanup) fs.rmSync(p, { recursive: true, force: true });
}

// 4. Công cụ -------------------------------------------------------------------------------------
step(4, `Kiểm tra ${NAME} trên máy`);
const cli = tool === 'codex' ? 'codex' : 'agy';
// Một chuỗi lệnh, không mảng tham số: Node 24 cảnh báo DEP0190 khi shell:true đi kèm mảng tham số.
const ver = spawnSync(`${cli} --version`, { shell: true, encoding: 'utf8', windowsHide: true, timeout: 30_000 });
const cliFound = ver.status === 0;
if (cliFound) ok(`${cli} ${(ver.stdout || '').trim().split(/\r?\n/).pop()}`);
else if (tool === 'codex') warn('Chưa thấy lệnh "codex" — cài Codex rồi làm bước 5. (App Codex không kèm lệnh này thì làm bước 5 trong app.)');
else warn('Chưa thấy lệnh "agy" (Antigravity CLI) — không sao nếu bạn dùng app/IDE Antigravity.');

// 5. Bước cuối -----------------------------------------------------------------------------------
step(5, 'Việc bạn tự làm');
if (tool === 'codex') {
  console.log(`  Codex chỉ chạy hook của project sau khi bạn duyệt (bước an toàn của Codex, kit không làm thay):
    a. Mở Codex ở thư mục gốc project. Nếu Codex hỏi "Do you trust the contents of this
       directory?" → chọn tin cậy.
    b. Codex báo "3 hooks need review before they can run." → gõ /hooks, bấm phím "trust all"
       (xem dòng hướng dẫn phím ở cuối màn hình) để tin cậy 3 hook rule-keeper → /exit.
    c. Kiểm tra: gửi một tin nhắn bất kỳ; trong ${cfg.ledgerDir}/ phải có file codex-xxxxxxxx.md.`);
} else {
  console.log(`  Thường không cần làm gì thêm:
    a. Mở thư mục project trong Antigravity (app, IDE hoặc lệnh agy). Nếu nó hỏi có tin cậy
       workspace không → chọn tin cậy.
    b. Kiểm tra: gửi một tin nhắn bất kỳ; trong ${cfg.ledgerDir}/ phải có file agy-xxxxxxxx.md.
       Không có → gõ /hooks trong Antigravity, bật hook "rule-keeper".`);
}

if (failed) finish();
if (!interactive || !cliFound) {
  console.log(`\n  Lệnh mở ${NAME} ở đúng thư mục:  cd "${root}"  rồi  ${cli}`);
  finish();
}
const rl = createInterface({ input: process.stdin, output: process.stdout });
const ans = (await rl.question(`\n  Mở ${NAME} ngay bây giờ trong một cửa sổ mới, ở thư mục project? (Y/n) `)).trim().toLowerCase();
rl.close();
if (ans === '' || ans.startsWith('y') || ans.startsWith('c')) {
  if (process.platform === 'win32') {
    spawn('cmd.exe', ['/c', `start "${NAME} - rule-keeper" /D "${root}" cmd /k ${cli}`], {
      windowsVerbatimArguments: true,
      detached: true,
      stdio: 'ignore',
    }).unref();
    ok(`Đã mở ${NAME} trong cửa sổ mới.${tool === 'codex' ? ' Làm tiếp bước b ở trên trong cửa sổ đó.' : ''}`);
  } else {
    console.log(`  Mở terminal mới rồi chạy:  cd "${root}" && ${cli}`);
  }
}
finish();

function finish() {
  console.log(failed ? `\nSetup ${NAME}: CÓ ${failed} lỗi — xem các dòng ✗ ở trên.` : `\nSetup ${NAME}: xong phần tự động.`);
  process.exit(failed ? 1 : 0);
}
