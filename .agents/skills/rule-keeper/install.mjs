#!/usr/bin/env node
// Cài rule-keeper vào project chứa thư mục kit này. Chỉ TẠO các file trỏ ở đúng chỗ Codex và
// Antigravity tự tìm; không sửa một file nào đã có mà không phải do rule-keeper tạo ra.
//
//   node .agents/skills/rule-keeper/install.mjs              cài hoặc cập nhật cho cả hai công cụ
//   node .agents/skills/rule-keeper/install.mjs --only codex         chỉ phần của Codex
//   node .agents/skills/rule-keeper/install.mjs --only antigravity   chỉ phần của Antigravity
//   node .agents/skills/rule-keeper/install.mjs --check      xem đã cài gì, còn thiếu gì
//   node .agents/skills/rule-keeper/install.mjs --uninstall  gỡ (chỉ xoá file do rule-keeper tạo)
//
// --check và --uninstall cũng nhận --only.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ALWAYS_ON_RULE, GENERATED_MARK, buildAlwaysOnRule, context, loadConfig, projectRoot } from './bin/rk.mjs';

const KIT_DIR = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const args = new Set(argv);
const onlyArg = argv.find((a) => a.startsWith('--only=')) ?? (argv.includes('--only') ? `--only=${argv[argv.indexOf('--only') + 1] ?? ''}` : null);
const only = onlyArg ? onlyArg.slice('--only='.length).toLowerCase().replace(/^agy$/, 'antigravity') : null;
if (only && only !== 'codex' && only !== 'antigravity') {
  console.error(`--only nhận "codex" hoặc "antigravity", không nhận "${only}".`);
  process.exit(2);
}
const root = projectRoot(KIT_DIR);
const kitRel = path.relative(root, KIT_DIR).split(path.sep).join('/');
const ctx = context(root, 'install', 'x');
const cfg = loadConfig();
const CODEX_DESC = 'rule-keeper';

if (!kitRel || kitRel.startsWith('..')) {
  console.error(
    `Không xác định được gốc project từ chỗ đặt kit (${KIT_DIR}).\nHãy đặt kit ở <thư mục gốc project>/.agents/skills/rule-keeper rồi chạy lại.`,
  );
  process.exit(2);
}

// Lệnh hook của Codex chạy với thư mục làm việc của phiên, có thể là một thư mục con, nên tự dò
// ngược lên tìm kit — không cần git. Kit không còn ở đó thì in {} (cho qua) thay vì làm hỏng phiên.
// Chỉ dùng dấu nháy đơn bên trong để cùng một chuỗi chạy được cả trong cmd.exe lẫn sh.
const codexLaunch = (event) =>
  `node -e "const f=require('fs'),p=require('path'),u=require('url'),k='${kitRel}/bin/rk.mjs';let d=process.cwd();while(!f.existsSync(p.join(d,k))){const up=p.dirname(d);if(up===d)break;d=up}import(u.pathToFileURL(p.join(d,k)).href).then(m=>m.main(['hook','codex','${event}'])).catch(e=>process.stdout.write('{}'))"`;

const codexHooks = () => ({
  description: `${CODEX_DESC} — giữ yêu cầu của người dùng và quy tắc project trước mặt agent, chặn báo xong khi chưa qua done-gate. Sinh bởi ${kitRel}/install.mjs; đừng sửa tay.`,
  hooks: {
    SessionStart: [
      {
        matcher: 'startup|resume|clear|compact',
        hooks: [{ type: 'command', command: codexLaunch('session-start'), timeout: 30, statusMessage: 'rule-keeper: nạp quy tắc và sổ yêu cầu', additionalContextLimit: 0 }],
      },
    ],
    UserPromptSubmit: [
      { hooks: [{ type: 'command', command: codexLaunch('prompt'), timeout: 30, statusMessage: 'rule-keeper: ghi tin nhắn vào sổ', additionalContextLimit: 0 }] },
    ],
    Stop: [{ hooks: [{ type: 'command', command: codexLaunch('stop'), timeout: 60, statusMessage: 'rule-keeper: kiểm tra done-gate' }] }],
  },
});

// Antigravity chạy lệnh hook với thư mục làm việc là thư mục chứa hooks.json (.agents/).
const agyHooks = () => {
  const script = path.relative(path.join(root, '.agents'), path.join(KIT_DIR, 'bin', 'rk.mjs')).split(path.sep).join('/');
  return {
    'rule-keeper': {
      PreInvocation: [{ type: 'command', command: `node ${script} hook agy pre`, timeout: 30 }],
      Stop: [{ type: 'command', command: `node ${script} hook agy stop`, timeout: 60 }],
    },
  };
};

const targets = [
  {
    file: ALWAYS_ON_RULE,
    tool: 'antigravity',
    who: 'Antigravity — luật luôn bật',
    want: () => buildAlwaysOnRule(ctx),
    ours: (text) => text.includes(GENERATED_MARK),
  },
  {
    file: '.agents/hooks.json',
    tool: 'antigravity',
    who: 'Antigravity — hook',
    want: () => `${JSON.stringify(agyHooks(), null, 2)}\n`,
    ours: (text) => {
      try {
        const keys = Object.keys(JSON.parse(text));
        return keys.length > 0 && keys.every((k) => k === 'rule-keeper');
      } catch {
        return false;
      }
    },
  },
  {
    file: '.codex/hooks.json',
    tool: 'codex',
    who: 'Codex — hook',
    want: () => `${JSON.stringify(codexHooks(), null, 2)}\n`,
    ours: (text) => {
      try {
        return String(JSON.parse(text).description || '').startsWith(CODEX_DESC);
      } catch {
        return false;
      }
    },
  },
  {
    file: `${cfg.ledgerDir}/.gitignore`,
    tool: 'both',
    who: 'Sổ yêu cầu — tự loại khỏi git',
    want: () => '*\n',
    ours: (text) => text.trim() === '*',
  },
].filter((t) => !only || t.tool === only || t.tool === 'both');

function status(t) {
  const abs = path.join(root, t.file);
  if (!fs.existsSync(abs)) return 'missing';
  const text = fs.readFileSync(abs, 'utf8');
  if (!t.ours(text)) return 'foreign';
  return text === t.want() ? 'current' : 'outdated';
}

const LABEL = { missing: 'chưa có', current: 'đã cài, khớp', outdated: 'đã cài, cũ', foreign: 'FILE CÓ SẴN, KHÔNG PHẢI CỦA rule-keeper' };
const forCodex = !only || only === 'codex';
const forAgy = !only || only === 'antigravity';

if (args.has('--check')) {
  console.log(`Project: ${root}\nKit:     ${kitRel}\n`);
  let bad = 0;
  for (const t of targets) {
    const s = status(t);
    if (s !== 'current') bad++;
    console.log(`  ${s === 'current' ? '✓' : '✗'} ${t.file.padEnd(32)} ${LABEL[s]}   (${t.who})`);
  }
  if (forAgy) console.log(`\n  Luật luôn bật: ${Buffer.byteLength(buildAlwaysOnRule(ctx))} byte (Antigravity cắt file luật ở 24.000 byte).`);
  console.log(bad ? '\nChạy lại không có --check để cài/cập nhật.' : `\nĐủ cả.${forCodex ? ' Nhớ duyệt hook trong Codex (/hooks) nếu chưa làm.' : ''}`);
  process.exit(bad ? 1 : 0);
}

if (args.has('--uninstall')) {
  for (const t of targets) {
    // Thư mục sổ dùng chung cho cả hai công cụ: gỡ một công cụ thì giữ, và luôn giữ để sổ cũ
    // không lộ ra git status.
    if (t.tool === 'both') continue;
    const s = status(t);
    if (s === 'current' || s === 'outdated') {
      fs.rmSync(path.join(root, t.file));
      console.log(`  - đã xoá ${t.file}`);
    } else if (s === 'foreign') console.log(`  · giữ nguyên ${t.file} (không phải của rule-keeper)`);
  }
  console.log(`\nSổ yêu cầu trong ${cfg.ledgerDir}/ được giữ lại (đó là dữ liệu). Không cần thì tự xoá thư mục đó.`);
  process.exit(0);
}

let refused = 0;
for (const t of targets) {
  const s = status(t);
  const abs = path.join(root, t.file);
  if (s === 'foreign') {
    refused++;
    console.log(`  ✗ ${t.file}: đã có sẵn và không phải của rule-keeper — KHÔNG ghi đè. Tự gộp nội dung sau vào file đó:\n${t.want().replace(/^/gm, '      ')}`);
    continue;
  }
  if (s === 'current') {
    console.log(`  ✓ ${t.file} (đã khớp)`);
    continue;
  }
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, t.want());
  console.log(`  + ${t.file} (${s === 'missing' ? 'tạo mới' : 'cập nhật'}) — ${t.who}`);
}

if (forAgy) {
  const ruleBytes = Buffer.byteLength(buildAlwaysOnRule(ctx));
  if (ruleBytes > 24000) console.log(`\n  ⚠ Luật luôn bật dài ${ruleBytes} byte > 24.000 — Antigravity sẽ cắt. Rút gọn rules/core.md hoặc rules/user.md.`);
}

const next = ['', 'Việc còn lại (một lần):'];
if (forCodex) {
  next.push(
    '  • Codex: hook của project chỉ chạy khi được tin cậy. Mở Codex trong project này, gõ /hooks và',
    '    tin cậy 3 hook "rule-keeper". Mỗi lần .codex/hooks.json đổi (chạy lại install sau khi đổi chỗ',
    '    kit) phải tin cậy lại.',
  );
}
if (forAgy) next.push('  • Antigravity: không cần làm gì; kiểm tra bằng /hooks nếu muốn.');
next.push(`  • Kiểm tra: node ${kitRel}/install.mjs --check${only ? ` --only ${only}` : ''}`);
console.log(next.join('\n'));
process.exit(refused ? 1 : 0);
