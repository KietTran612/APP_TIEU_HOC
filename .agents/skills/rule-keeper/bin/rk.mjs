#!/usr/bin/env node
// rule-keeper — giữ yêu cầu của người dùng và quy tắc của project trước mặt agent
// (Codex, Antigravity), và không cho báo "xong" khi công việc chưa được đối chiếu với chúng.
// Chỉ cần Node >= 18. Có git thì thêm diff quy tắc và phát hiện file đã đổi.
//
//   node rk.mjs start  --agent <codex|agy|tên>   tạo sổ yêu cầu cho một phiên không có hook
//   node rk.mjs where  --agent <codex|agy|tên>   sổ của phiên gần nhất của agent đó
//   node rk.mjs index                            liệt kê file quy tắc và mục lục của chúng
//   node rk.mjs check  --ledger <sổ>             quy tắc nào đã đổi từ lần xem trước (kèm diff)
//   node rk.mjs gate   --ledger <sổ>             done-gate: từ chối nếu sổ thiếu bằng chứng
//   node rk.mjs hook   <codex|agy> <sự kiện>     gọi từ hooks.json, đọc JSON trên stdin

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const KIT_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const GENERATED_MARK = '<!-- rule-keeper:generated';
export const ALWAYS_ON_RULE = '.agents/rules/rule-keeper.md';

const DEFAULTS = {
  ledgerDir: '.agent-ledger',
  ruleFiles: ['**/AGENTS.md', '**/AGENTS.override.md', '**/CLAUDE.md', '**/GEMINI.md', '.agents/rules/*.md', '.agent/rules/*.md'],
  exclude: [ALWAYS_ON_RULE],
  stopGate: true,
  maxConsecutiveStopBlocks: 2,
  anchorEvery: 15,
  maxDiffLines: 120,
  maxContextChars: 24000,
  maxMessageChars: 4000,
};

// ---------------------------------------------------------------------------------------------
// Nền tảng

export function loadConfig() {
  try {
    const user = JSON.parse(fs.readFileSync(path.join(KIT_DIR, 'config.json'), 'utf8'));
    return { ...DEFAULTS, ...Object.fromEntries(Object.entries(user).filter(([k]) => !k.startsWith('_'))) };
  } catch {
    return { ...DEFAULTS };
  }
}

function git(cwd, args) {
  const r = spawnSync('git', args, { cwd, encoding: 'utf8', windowsHide: true, maxBuffer: 64 << 20 });
  return r.status === 0 ? r.stdout : null;
}

// Kit ở chỗ chuẩn <project>/.agents/skills/rule-keeper thì gốc project là thư mục chứa .agents —
// không cần git. Trước đây gốc được hỏi git, nên project không dùng git lấy luôn thư mục kit làm
// gốc: install ghi file trỏ vào trong kit (báo thành công) và gate đi tìm sổ sai chỗ.
const CANONICAL_ROOT = (() => {
  const skills = path.dirname(KIT_DIR);
  const agents = path.dirname(skills);
  return path.basename(skills) === 'skills' && path.basename(agents) === '.agents' ? path.dirname(agents) : null;
})();

export function projectRoot(dir) {
  if (CANONICAL_ROOT) return CANONICAL_ROOT;
  const out = git(dir, ['rev-parse', '--show-toplevel']);
  return path.resolve(out ? out.trim() : dir);
}

const rel = (root, p) => path.relative(root, p).split(path.sep).join('/');
const sha = (s) => crypto.createHash('sha1').update(s).digest('hex');
const readText = (p) => fs.readFileSync(p, 'utf8');
const pad = (n) => String(n).padStart(2, '0');
const stamp = (d = new Date()) =>
  `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
const fileSig = (abs) => {
  const s = fs.statSync(abs);
  return `${s.size}:${Math.round(s.mtimeMs)}`;
};

function clamp(text, max) {
  if (text.length <= max) return text;
  return `${text.slice(0, max)}\n… [rule-keeper: cắt bớt ${text.length - max} ký tự — đọc thẳng file sổ/quy tắc để xem phần còn lại]`;
}

export function context(root, agent, sessionKey) {
  const cfg = loadConfig();
  const ledgerDirAbs = path.join(root, cfg.ledgerDir);
  const key = `${agent}-${sessionKey}`;
  return {
    root,
    cfg,
    agent,
    key,
    ledgerDirAbs,
    ledgerAbs: path.join(ledgerDirAbs, `${key}.md`),
    ledgerRel: `${cfg.ledgerDir}/${key}.md`,
    stateDir: path.join(ledgerDirAbs, '.state', key),
    kitRel: rel(root, KIT_DIR) || '.',
  };
}

const shortId = (id) => String(id || 'nosession').replace(/[^A-Za-z0-9]/g, '').slice(0, 8) || 'nosession';

function contextFromLedger(ledgerPath) {
  const ledgerAbs = path.resolve(ledgerPath);
  const root = projectRoot(path.dirname(ledgerAbs));
  const key = path.basename(ledgerAbs, '.md');
  const dash = key.indexOf('-');
  const ctx = context(root, dash > 0 ? key.slice(0, dash) : key, dash > 0 ? key.slice(dash + 1) : 'manual');
  return { ...ctx, ledgerAbs, ledgerRel: rel(root, ledgerAbs) };
}

function loadState(ctx) {
  try {
    return JSON.parse(readText(path.join(ctx.stateDir, 'state.json')));
  } catch {
    return {};
  }
}

function saveState(ctx, st) {
  fs.mkdirSync(ctx.stateDir, { recursive: true });
  fs.writeFileSync(path.join(ctx.stateDir, 'state.json'), JSON.stringify(st, null, 1));
}

function ensureLedgerDir(ctx) {
  fs.mkdirSync(ctx.ledgerDirAbs, { recursive: true });
  const ignore = path.join(ctx.ledgerDirAbs, '.gitignore');
  // Sổ là trí nhớ cục bộ của từng phiên, không phải mã nguồn: thư mục tự loại mình khỏi git
  // mà không phải sửa .gitignore của project.
  if (!fs.existsSync(ignore)) fs.writeFileSync(ignore, '*\n');
}

// rules/*.md viết đường dẫn mặc định của kit thành chữ, để agent đọc thẳng file gốc vẫn thấy lệnh
// chạy được; kit nằm chỗ khác thì đổi lúc chèn.
const DEFAULT_KIT_REL = '.agents/skills/rule-keeper';
const fill = (text, ctx) => (ctx.kitRel === DEFAULT_KIT_REL ? text : text.split(DEFAULT_KIT_REL).join(ctx.kitRel));

function kitRules(ctx) {
  const read = (name) => {
    try {
      return fill(readText(path.join(KIT_DIR, 'rules', name)), ctx).trim();
    } catch {
      return '';
    }
  };
  return [read('core.md'), read('user.md')].filter(Boolean).join('\n\n');
}

// ---------------------------------------------------------------------------------------------
// Sổ yêu cầu

function ledgerTemplate(ctx) {
  return `# Sổ yêu cầu — ${ctx.agent} — ${ctx.key}

> File này là TRÍ NHỚ của agent cho phiên làm việc này, không phải ngữ cảnh chat. Agent ghi mọi yêu
> cầu của người dùng vào mục "Yêu cầu" và đọc lại trước mỗi bước. Người dùng có thể sửa trực tiếp
> file này — lượt sau agent sẽ thấy bản mới.
> Bắt đầu: ${stamp()} · Project: ${ctx.root}

## Yêu cầu
<!-- Một dòng cho mỗi yêu cầu / ràng buộc / sửa sai / đổi ý của người dùng. Mẫu:
- R1 (M1) "trích nguyên văn lời người dùng" → việc cụ thể phải đạt
- R2 (M3) "..." → ... [thay bởi R4]          ← người dùng đổi ý: đánh dấu, KHÔNG xoá dòng cũ
- R3 (M3) "..." → ... [huỷ: người dùng bỏ ở M5]
Dấu đóng phải đúng dạng [thay bởi R#] hoặc [huỷ: lý do], đặt NGOÀI ngoặc kép. "[huỷ]" trần không tính.
-->

## Tin nhắn của người dùng
<!-- Hook ghi nguyên văn từng tin nhắn vào đây (M1, M2, ...). Mỗi M# phải được một dòng R# dẫn
tới bằng "(M#)", hoặc có dòng "- M# — không có yêu cầu mới" trong Done-gate. -->

## Done-gate
<!-- Điền trước khi báo xong, rồi chạy lệnh gate (xem skill rule-keeper). Mẫu:
- R1 ✅ đã làm gì — bằng chứng: <lệnh đã chạy + kết quả quan sát được | file:dòng>
- R2 ⚠️ mới xong một phần: còn thiếu gì, vì sao
- M4 — không có yêu cầu mới
- Quy tắc: đã đối chiếu <file / quy tắc nào> — vi phạm: không
- Diff: đã đọc từng hunk của <các file> — ngoài phạm vi: không
- Kiểm tra: <lệnh kiểm tra đã chạy> → <kết quả đọc được>
-->
`;
}

const ITEM = /^\s*[-*]\s*(\[[ xX]\]\s*)?\**([RM]\d+)\**(?![\w])[:.)]?(.*)$/;
// Dấu đóng chỉ tính khi nằm NGOÀI phần trích lời người dùng và mang theo lý do: "[thay bởi R4]" hoặc
// "[huỷ: …]". Trước đây "[huỷ" trần ở bất cứ đâu cũng đóng, nên R1 (M1) "thêm nút [huỷ] vào form"
// bị gate bỏ qua như đã huỷ.
const CLOSED = /\[\s*(?:(?:thay bởi|thay bằng|đã thay bằng|superseded by|replaced by)\s+R\d+|(?:huỷ|hủy|bỏ|cancell?ed|dropped)\s*:\s*[^\]\s][^\]]*)\]/i;
const BARE_CLOSE = /\[\s*(thay bởi|thay bằng|đã thay|huỷ|hủy|bỏ|superseded|replaced|cancell?ed|dropped)[\s:\]]/i;
const outsideQuotes = (s) => s.replace(/"[^"]*"|“[^”]*”|`[^`]*`/g, '');
const DONE_MARK = /✅|✔/;
const NOTDONE_MARK = /❌|⚠️|⚠|✖/;
const EVIDENCE = /(bằng chứng|evidence)\s*:\s*(.*)$/i;
const REQUIRED_LINES = [
  ['Quy tắc', /^\s*[-*]?\s*\**(quy tắc|rules)\**\s*:\s*\S.{4,}/i],
  ['Diff', /^\s*[-*]?\s*\**diff\**\s*:\s*\S.{4,}/i],
  ['Kiểm tra', /^\s*[-*]?\s*\**(kiểm tra|checks?|verify|verification)\**\s*:\s*\S.{4,}/i],
];

function sectionOf(heading) {
  const h = heading.toLowerCase();
  if (/lịch sử|history/.test(h)) return 'hist';
  if (/done[- ]?gate/.test(h)) return 'gate';
  if (/tin nhắn|message/.test(h)) return 'msg';
  if (/yêu cầu|requirement/.test(h)) return 'req';
  return null;
}

export function parseLedger(text) {
  const clean = text.replace(/<!--[\s\S]*?-->/g, '');
  const sec = { req: [], msg: [], gate: [], hist: [] };
  let cur = null;
  for (const line of clean.split(/\r?\n/)) {
    const h = /^##\s+(.*)$/.exec(line);
    if (h) {
      cur = sectionOf(h[1]);
      continue;
    }
    if (cur) sec[cur].push(line);
  }
  const reqs = [];
  for (const line of sec.req) {
    const m = ITEM.exec(line);
    if (!m || m[2][0] !== 'R') continue;
    const tail = outsideQuotes(m[3]);
    reqs.push({
      id: m[2],
      line: line.trim(),
      closed: CLOSED.test(tail),
      malformedClose: !CLOSED.test(tail) && BARE_CLOSE.test(tail),
      refs: [...m[3].matchAll(/\bM(\d+)\b/g)].map((x) => `M${x[1]}`),
    });
  }
  const msgs = [];
  const msgBodies = {};
  let curMsg = null;
  for (const line of sec.msg) {
    const m = /^###\s+(M\d+)\b/.exec(line);
    if (m) {
      curMsg = m[1];
      msgs.push(curMsg);
      msgBodies[curMsg] = [];
    } else if (curMsg) msgBodies[curMsg].push(line.replace(/^>\s?/, ''));
  }
  return { reqs, msgs, msgBodies, gate: sec.gate.map((l) => l.trim()).filter(Boolean) };
}

export function validateGate(parsed) {
  const problems = [];
  const open = parsed.reqs.filter((r) => !r.closed);
  if (!parsed.reqs.length) {
    problems.push('Mục "Yêu cầu" chưa có dòng R# nào — ít nhất yêu cầu trong tin nhắn đầu tiên phải thành R1.');
  }
  const gateById = new Map();
  for (const line of parsed.gate) {
    const m = ITEM.exec(line);
    if (m) gateById.set(m[2], `${gateById.get(m[2]) || ''} ${m[1] || ''}${m[3]}`);
  }
  const done = [];
  const notDone = [];
  for (const r of open) {
    const g = gateById.get(r.id);
    if (!g) {
      problems.push(
        r.malformedClose
          ? `${r.id} chưa có dòng trong Done-gate. Nếu người dùng đã bỏ yêu cầu này, đánh dấu đúng dạng "[huỷ: <lý do, M#>]" hoặc "[thay bởi R#]" — dấu trần như "[huỷ]" không được tính.`
          : `${r.id} chưa có dòng trong Done-gate.`,
      );
      continue;
    }
    if (NOTDONE_MARK.test(g) || /\[ \]/.test(g)) {
      if (g.replace(NOTDONE_MARK, '').replace(/\[ \]/, '').trim().length < 8) {
        problems.push(`${r.id} đánh dấu chưa xong nhưng không nói còn thiếu gì.`);
      }
      notDone.push(r);
    } else if (DONE_MARK.test(g) || /\[[xX]\]/.test(g)) {
      const ev = EVIDENCE.exec(g);
      if (!ev || ev[2].trim().length < 8) {
        problems.push(`${r.id} đánh dấu ✅ nhưng thiếu "bằng chứng: ..." cụ thể (lệnh đã chạy + kết quả, hoặc file:dòng).`);
      } else done.push(r);
    } else {
      problems.push(`${r.id} trong Done-gate thiếu dấu trạng thái (✅ xong / ⚠️ một phần / ❌ chưa).`);
    }
  }
  const referenced = new Set(parsed.reqs.flatMap((r) => r.refs));
  for (const m of parsed.msgs) {
    if (!referenced.has(m) && !gateById.has(m)) {
      problems.push(`${m} chưa được dòng R# nào dẫn tới "(${m})" và chưa có dòng "- ${m} — không có yêu cầu mới" trong Done-gate.`);
    }
  }
  for (const [label, re] of REQUIRED_LINES) {
    if (!parsed.gate.some((l) => re.test(l))) problems.push(`Done-gate thiếu dòng "- ${label}: ...".`);
  }
  return { problems, done, notDone, open };
}

// Done-gate là của LƯỢT hiện tại. Một tin nhắn mới mở lượt mới, nên phần gate cũ được dời xuống
// "Lịch sử done-gate" để agent điền lại từ đầu — Codex đã từng nối thêm bộ dòng R# mới dưới bộ cũ,
// và sổ thành hai bản chồng nhau mà validator phải đoán.
function archiveGate(text, newId) {
  const lines = text.split(/\r?\n/);
  const isHeading = (l, kind) => /^##\s+/.test(l) && sectionOf(l.replace(/^##\s+/, '')) === kind;
  const start = lines.findIndex((l) => isHeading(l, 'gate'));
  if (start < 0) return text;
  let end = lines.findIndex((l, i) => i > start && /^##\s+/.test(l));
  if (end < 0) end = lines.length;
  const body = lines.slice(start + 1, end).join('\n');
  const content = body.replace(/<!--[\s\S]*?-->/g, '').trim();
  if (!content) return text;
  const comment = /<!--[\s\S]*?-->/.exec(body)?.[0];
  const fresh = [lines[start], ...(comment ? comment.split('\n') : []), ''];
  const kept = [...lines.slice(0, start), ...fresh, ...lines.slice(end)].join('\n').replace(/\s*$/, '');
  const hist = lines.some((l) => isHeading(l, 'hist')) ? '' : '\n\n## Lịch sử done-gate\n<!-- Hook dời Done-gate của các lượt trước xuống đây. Chỉ để tra cứu; gate không đọc mục này. -->';
  return `${kept}${hist}\n\n### Trước ${newId}\n${content}\n`;
}

function appendMessage(ctx, raw) {
  let body = String(raw || '').replace(/\r\n/g, '\n').trim();
  if (!body) return null;
  const max = ctx.cfg.maxMessageChars;
  if (body.length > max) body = `${body.slice(0, max)}\n[… cắt bớt ${body.length - max} ký tự]`;
  let text = fs.existsSync(ctx.ledgerAbs) ? readText(ctx.ledgerAbs) : ledgerTemplate(ctx);
  const nums = [...text.matchAll(/^###\s+M(\d+)\b/gm)].map((m) => Number(m[1]));
  const id = `M${(nums.length ? Math.max(...nums) : 0) + 1}`;
  text = archiveGate(text, id);
  const entry = `### ${id} · ${stamp()}\n${body.split('\n').map((l) => `> ${l}`).join('\n')}\n`;
  const lines = text.split(/\r?\n/);
  const start = lines.findIndex((l) => /^##\s+/.test(l) && sectionOf(l.replace(/^##\s+/, '')) === 'msg');
  if (start < 0) {
    text = `${text.replace(/\s*$/, '')}\n\n## Tin nhắn của người dùng\n${entry}`;
  } else {
    let end = lines.findIndex((l, i) => i > start && /^##\s+/.test(l));
    if (end < 0) end = lines.length;
    while (end > start + 1 && lines[end - 1].trim() === '') end--;
    lines.splice(end, 0, '', ...entry.trimEnd().split('\n'));
    text = lines.join('\n');
  }
  fs.writeFileSync(ctx.ledgerAbs, text);
  return id;
}

// ---------------------------------------------------------------------------------------------
// File quy tắc

function listRuleFiles(ctx, st) {
  const now = Date.now();
  if (st && st.ruleList && now - st.ruleList.at < 60_000) return st.ruleList.files.filter((f) => fs.existsSync(path.join(ctx.root, f)));
  const { root, cfg } = ctx;
  let files = [];
  const out = git(root, ['ls-files', '-co', '--exclude-standard', '-z', '--', ...cfg.ruleFiles.map((p) => `:(glob)${p}`)]);
  if (out != null) files = out.split('\0').filter(Boolean);
  else {
    for (const p of cfg.ruleFiles) {
      const m = /^(?:\*\*\/)?([^*/]+)$/.exec(p);
      if (m) files.push(m[1]);
      const d = /^(.+)\/\*\.md$/.exec(p);
      if (d) {
        try {
          for (const f of fs.readdirSync(path.join(root, d[1]))) if (f.endsWith('.md')) files.push(`${d[1]}/${f}`);
        } catch {}
      }
    }
  }
  for (const f of ['rules/core.md', 'rules/user.md', 'SKILL.md']) files.push(`${ctx.kitRel}/${f}`);
  const ex = new Set(cfg.exclude);
  files = [...new Set(files)]
    .filter((f) => !ex.has(f) && !f.startsWith(`${cfg.ledgerDir}/`) && fs.existsSync(path.join(root, f)))
    .sort((a, b) => a.split('/').length - b.split('/').length || a.localeCompare(b));
  if (st) st.ruleList = { at: now, files };
  return files;
}

const snapPath = (ctx, file) => path.join(ctx.stateDir, 'snap', encodeURIComponent(file));

function unifiedDiff(ctx, file, oldAbs, newAbs) {
  const r = spawnSync('git', ['diff', '--no-index', '--no-color', '-U2', '--', oldAbs, newAbs], {
    encoding: 'utf8',
    windowsHide: true,
    maxBuffer: 64 << 20,
  });
  if (r.status !== 1 || !r.stdout) return null;
  const lines = r.stdout.split(/\r?\n/);
  const first = lines.findIndex((l) => l.startsWith('@@'));
  const body = first < 0 ? [] : lines.slice(first);
  const max = ctx.cfg.maxDiffLines;
  const shown = body.slice(0, max);
  if (body.length > max) {
    const hunks = body.slice(max).filter((l) => l.startsWith('@@')).map((l) => l.replace(/@@ -\d+(,\d+)? \+(\d+)(,(\d+))? @@.*/, 'dòng $2'));
    shown.push(`… còn ${body.length - max} dòng diff nữa — đọc lại ${file} quanh: ${hunks.slice(0, 20).join(', ') || 'phần sau'}`);
  }
  return [`--- ${file} (bản bạn đã đọc)`, `+++ ${file} (bản hiện tại)`, ...shown].join('\n');
}

// So file quy tắc với bản chụp lần trước. update=false chỉ xem, không ghi nhận là "đã đọc".
function checkRules(ctx, st, { update = true } = {}) {
  const known = st.rules || {};
  const files = listRuleFiles(ctx, st);
  const changes = [];
  const next = {};
  for (const f of files) {
    const abs = path.join(ctx.root, f);
    let sig;
    try {
      sig = fileSig(abs);
    } catch {
      continue;
    }
    const prev = known[f];
    if (prev && prev.sig === sig) {
      next[f] = prev;
      continue;
    }
    const content = readText(abs);
    const hash = sha(content);
    next[f] = { sig, hash };
    if (!prev) {
      if (st.rulesInitialized) changes.push({ file: f, kind: 'added', lines: content.split('\n').length });
    } else if (prev.hash !== hash) {
      changes.push({ file: f, kind: 'modified', diff: unifiedDiff(ctx, f, snapPath(ctx, f), abs) });
    }
    if (update && (!prev || prev.hash !== hash)) {
      fs.mkdirSync(path.dirname(snapPath(ctx, f)), { recursive: true });
      fs.writeFileSync(snapPath(ctx, f), content);
    }
  }
  for (const f of Object.keys(known)) if (!next[f]) changes.push({ file: f, kind: 'removed' });
  if (update) {
    st.rules = next;
    st.rulesInitialized = true;
  }
  return { files, changes };
}

function changesBlock(changes) {
  if (!changes.length) return '';
  const parts = [
    '[rule-keeper] ⚠ QUY TẮC ĐÃ ĐỔI kể từ lần bạn đọc trước. Việc phải làm NGAY: đọc thay đổi dưới đây → áp dụng cho phần việc còn lại → rà lại phần đã làm theo luật mới → nếu luật mới mâu thuẫn một yêu cầu R# trong sổ, hỏi người dùng thay vì tự chọn.',
  ];
  for (const c of changes) {
    if (c.kind === 'added') parts.push(`• File quy tắc MỚI: ${c.file} (${c.lines} dòng) — đọc HẾT file này.`);
    else if (c.kind === 'removed') parts.push(`• File quy tắc đã bị XOÁ: ${c.file} — các luật trong đó không còn áp dụng.`);
    else parts.push(c.diff ? `• ${c.file} đã sửa:\n${c.diff}` : `• ${c.file} đã sửa (không tính được diff) — đọc lại toàn bộ file này.`);
  }
  return parts.join('\n');
}

function headings(text) {
  const out = [];
  let fence = false;
  text.split(/\r?\n/).forEach((line, i) => {
    if (/^\s*(```|~~~)/.test(line)) fence = !fence;
    else if (!fence) {
      const m = /^(#{1,2})\s+(.+?)\s*#*\s*$/.exec(line);
      if (m) out.push(`L${i + 1} ${m[2].replace(/\*\*/g, '').slice(0, 60)}`);
    }
  });
  return out;
}

function indexBlock(ctx, files) {
  const lines = [
    'File quy tắc của project — đọc HẾT trước lần sửa đầu tiên. File dài: đọc theo đoạn ≤ 250 dòng tới dòng cuối; output bị cắt KHÔNG phải là cả file. Hai file mâu thuẫn → theo cái chặt hơn và nói ra một dòng.',
  ];
  // Luật của chính kit đã được chèn (Codex) hoặc nằm trong luật luôn bật (Antigravity): vẫn theo
  // dõi để báo khi đổi, nhưng không bắt agent đọc lại lần nữa.
  const project = files.filter((f) => !f.startsWith(`${ctx.kitRel}/`));
  if (!project.length) lines.push('- (project này không có file quy tắc nào ngoài luật của rule-keeper)');
  for (const f of project) {
    let text;
    try {
      text = readText(path.join(ctx.root, f));
    } catch {
      continue;
    }
    const hs = headings(text);
    let toc = hs.slice(0, 40).join(' · ');
    if (toc.length > 700) toc = `${toc.slice(0, 700)} …`;
    lines.push(`- ${f} — ${text.split('\n').length} dòng, ${Math.ceil(Buffer.byteLength(text) / 1024)} KB${toc ? `\n    mục: ${toc}` : ''}`);
  }
  return lines.join('\n');
}

// Bản luôn-bật cho Antigravity là bản sao của rules/*.md; giữ nó khớp mỗi khi hook chạy, để sửa
// rules/core.md là đủ, không phải nhớ chạy lại install.
export function buildAlwaysOnRule(ctx) {
  return `---\ntrigger: always_on\n---\n${GENERATED_MARK} từ ${ctx.kitRel}/rules/*.md — đừng sửa file này, sửa file gốc; hook tự đồng bộ. -->\n\n${kitRules(ctx)}\n`;
}

function syncAlwaysOnRule(ctx) {
  const target = path.join(ctx.root, ALWAYS_ON_RULE);
  try {
    const cur = readText(target);
    if (!cur.includes(GENERATED_MARK)) return;
    const want = buildAlwaysOnRule(ctx);
    if (cur !== want) fs.writeFileSync(target, want);
  } catch {}
}

// ---------------------------------------------------------------------------------------------
// Cây làm việc (để biết đã có gì đổi kể từ lần gate trước)

// Project có thể là thư mục con của một repo git lớn hơn: "-- ." giữ trạng thái trong cây của
// project, còn đường dẫn porcelain luôn tính từ gốc repo (đo 14/10/2026), nên stat theo gốc repo.
function worktree(ctx) {
  const top = (git(ctx.root, ['rev-parse', '--show-toplevel']) || '').trim();
  if (!top) return null;
  const out = git(ctx.root, ['status', '--porcelain=v1', '-z', '--untracked-files=all', '--', '.']);
  if (out == null) return null;
  const head = (git(ctx.root, ['rev-parse', '--verify', '-q', 'HEAD']) || '').trim();
  const ledgerPrefix = `${rel(top, path.join(ctx.root, ctx.cfg.ledgerDir))}/`;
  const toks = out.split('\0');
  const entries = {};
  for (let i = 0; i < toks.length; i++) {
    const t = toks[i];
    if (t.length < 4) continue;
    const xy = t.slice(0, 2);
    const p = t.slice(3);
    if (xy[0] === 'R' || xy[0] === 'C') i++;
    if (p.startsWith(ledgerPrefix)) continue;
    let sig = 'gone';
    try {
      sig = fileSig(path.join(top, p));
    } catch {}
    entries[p] = `${xy}:${sig}`;
  }
  const fp = sha(`${head}\n${Object.keys(entries).sort().map((k) => `${k}=${entries[k]}`).join('\n')}`);
  return { fp, head, entries };
}

function changedFiles(ctx, ref, wt) {
  if (!ref || !wt) return [];
  const out = new Set();
  for (const [p, sig] of Object.entries(wt.entries)) if (ref.entries?.[p] !== sig) out.add(p);
  for (const p of Object.keys(ref.entries || {})) if (!(p in wt.entries)) out.add(p);
  if (ref.head && wt.head && ref.head !== wt.head) {
    const names = git(ctx.root, ['diff', '--name-only', ref.head, wt.head, '--', '.']);
    for (const p of (names || '').split(/\r?\n/).filter(Boolean)) out.add(p);
  }
  return [...out].filter((p) => !p.startsWith(`${ctx.cfg.ledgerDir}/`)).sort();
}

// ---------------------------------------------------------------------------------------------
// Nội dung chèn vào ngữ cảnh của agent

const cmd = (ctx, sub) => `node ${ctx.kitRel}/bin/rk.mjs ${sub} --ledger ${ctx.ledgerRel}`;

function openRequirements(ctx) {
  try {
    return parseLedger(readText(ctx.ledgerAbs)).reqs.filter((r) => !r.closed);
  } catch {
    return [];
  }
}

function anchorBlock(ctx, { newMsg, unresolved } = {}) {
  const open = openRequirements(ctx);
  const lines = [`[rule-keeper] Sổ yêu cầu của phiên: ${ctx.ledgerRel}`];
  if (unresolved) {
    lines.push(
      `⚠ Lượt trước kết thúc khi CHƯA qua done-gate (${unresolved.why}). Việc đó chưa được coi là xong: nếu chưa nói rõ với người dùng thì nói, và chạy gate trước khi báo xong bất cứ điều gì.`,
    );
  }
  if (newMsg) {
    lines.push(
      `Tin nhắn mới của người dùng đã được ghi nguyên văn vào sổ là ${newMsg}. TRƯỚC KHI LÀM GÌ KHÁC: nếu nó nêu yêu cầu, ràng buộc, sửa sai, "đừng…/luôn…/chỉ…" hoặc đổi ý → thêm hoặc cập nhật dòng R# trong mục "Yêu cầu" (ghi "(${newMsg})"); yêu cầu cũ bị thay thì đánh dấu [thay bởi R#], không xoá.`,
    );
  } else {
    lines.push('Nhắc định kỳ: đọc lại mục "Yêu cầu" của sổ trước bước tiếp theo — đừng dựa vào trí nhớ.');
  }
  if (open.length) {
    lines.push(`Yêu cầu còn hiệu lực (${open.length}):`);
    for (const r of open.slice(0, 30)) lines.push(`  ${r.line.length > 240 ? `${r.line.slice(0, 240)}…` : r.line}`);
    if (open.length > 30) lines.push(`  … và ${open.length - 30} yêu cầu nữa — đọc sổ.`);
  } else {
    lines.push('Sổ chưa có dòng R# nào — ghi yêu cầu từ các tin nhắn của người dùng vào mục "Yêu cầu" trước khi làm.');
  }
  lines.push(`Không báo "xong / đã sửa / hoàn thành / pass" khi chưa làm done-gate (skill rule-keeper) và \`${cmd(ctx, 'gate')}\` chưa in GATE OK.`);
  return lines.join('\n');
}

function introBlock(ctx, files, { withRules }) {
  const parts = [
    `[rule-keeper] Phiên mới (${ctx.agent}). Sổ yêu cầu của phiên này: ${ctx.ledgerRel} — đây là trí nhớ của bạn; đọc lại trước mỗi bước.`,
    `Lệnh (chạy ở thư mục gốc project):\n  ${cmd(ctx, 'check')}   xem quy tắc nào đã đổi\n  ${cmd(ctx, 'gate')}    done-gate trước khi báo xong`,
  ];
  if (withRules) parts.push(kitRules(ctx));
  parts.push(indexBlock(ctx, files));
  return parts.join('\n\n');
}

function recoveryBlock(ctx, source) {
  let recent = '';
  try {
    const p = parseLedger(readText(ctx.ledgerAbs));
    recent = p.msgs
      .slice(-3)
      .map((m) => {
        const b = p.msgBodies[m].join('\n').trim();
        return `${m}: ${b.length > 600 ? `${b.slice(0, 600)}…` : b}`;
      })
      .join('\n');
  } catch {}
  return [
    `[rule-keeper] Ngữ cảnh vừa được ${source === 'compact' ? 'NÉN' : 'khôi phục'} — chi tiết về yêu cầu bạn "nhớ" có thể đã mất. Sổ mới là nguồn đúng: đọc lại TOÀN BỘ ${ctx.ledgerRel} và các file quy tắc trước khi làm tiếp.`,
    anchorBlock(ctx),
    recent ? `Tin nhắn gần nhất của người dùng:\n${recent}` : '',
  ]
    .filter(Boolean)
    .join('\n\n');
}

// ---------------------------------------------------------------------------------------------
// Phiên

function ensureSession(ctx, st) {
  ensureLedgerDir(ctx);
  let created = false;
  if (!st.createdAt) {
    st.createdAt = new Date().toISOString();
    st.agent = ctx.agent;
    st.ledger = ctx.ledgerRel;
    const wt = worktree(ctx);
    st.baseline = wt ? { fp: wt.fp, head: wt.head, entries: wt.entries } : null;
    created = true;
  }
  if (!fs.existsSync(ctx.ledgerAbs)) fs.writeFileSync(ctx.ledgerAbs, ledgerTemplate(ctx));
  return created;
}

// Một câu hỏi ở cuối chỉ miễn gate khi câu trả lời không kể việc đã làm: model hay chốt bằng "Bạn
// có muốn mình làm thêm…?", nên nếu câu hỏi nào cũng được miễn thì gate bị lách ở mọi lượt.
const DONE_CLAIM =
  /(\bxong\b|hoàn thành|hoàn tất|sẵn sàng|đã (sửa|fix|khắc phục|chạy được|cập nhật|thêm|tạo|đổi|thay|xoá|xóa|chỉnh|viết|cài|triển khai|refactor|làm)|\bdone\b|\bcompleted?\b|\bfinished\b|\bfixed\b|\bresolved\b|\b(updated|added|created|implemented|changed|refactored|wrote)\b|tests? (all )?pass|all tests|\bpass(es|ed)?\b)/i;
const ASKING = /(\?\s*$|bạn (có )?muốn|có muốn|xác nhận giúp|bạn chọn|nên làm theo cách nào|should i\b|do you want|would you like|which (one|option))/i;

function lastParagraph(text) {
  const t = String(text || '').trim().split(/\n\s*\n/);
  return t[t.length - 1] || '';
}

// Quyết định ở cuối một lượt: cho dừng, hay bắt agent làm done-gate trước.
function stopDecision(ctx, st, { lastMessage = '' } = {}) {
  if (!ctx.cfg.stopGate) return {};
  const wt = worktree(ctx);
  let ledgerText = '';
  try {
    ledgerText = readText(ctx.ledgerAbs);
  } catch {}
  const parsed = parseLedger(ledgerText);
  const ledgerHash = sha(ledgerText);
  const gate = st.lastGate;
  const { changes } = checkRules(ctx, st, { update: false });
  const files = changedFiles(ctx, gate || st.baseline, wt);
  const claims = DONE_CLAIM.test(lastMessage);
  const asking = !claims && ASKING.test(lastParagraph(lastMessage));
  const gateFresh = gate && wt && gate.fp === wt.fp && gate.ledgerHash === ledgerHash;
  const why = [];
  if (changes.length) why.push('file quy tắc đã đổi trong lúc bạn làm');
  if (files.length && !asking && !gateFresh) why.push(`có ${files.length} file đổi kể từ lần done-gate trước (hoặc từ đầu phiên)`);
  if (claims && !gateFresh && parsed.msgs.length > (gate?.msgCount ?? 0)) why.push('câu trả lời cuối nói là đã xong nhưng chưa có GATE OK cho lượt này');
  if (!why.length) {
    st.stop = { blocks: 0 };
    return {};
  }
  const sigNow = sha(`${wt?.fp || ''}|${ledgerHash}`);
  const prev = st.stop || { blocks: 0 };
  // Đã báo người dùng về đúng trạng thái này rồi: cho dừng. Không có dòng này thì sau lần cảnh báo,
  // bộ đếm về 0 và lần Stop kế lại chặn từ đầu.
  if (prev.warnedSig === sigNow) return {};
  if (prev.blocks >= ctx.cfg.maxConsecutiveStopBlocks || prev.sig === sigNow) {
    // Đã nhắc mà agent không làm gì thêm: không chặn lặp vô hạn, chỉ báo người dùng.
    st.stop = { blocks: 0, warnedSig: sigNow };
    st.unresolvedGate = { at: new Date().toISOString(), why: why.join('; ') };
    return {
      why: why.join('; '),
      warn: `rule-keeper: agent kết thúc lượt mà CHƯA qua done-gate (${why.join('; ')}). Đừng coi việc này là xong cho tới khi agent chạy gate và in GATE OK. Sổ: ${ctx.ledgerRel}`,
    };
  }
  st.stop = { blocks: prev.blocks + 1, sig: sigNow };
  if (changes.length) checkRules(ctx, st, { update: true });
  const shown = files.slice(0, 15).join(', ') + (files.length > 15 ? ` (+${files.length - 15})` : '');
  const reason = [
    `[rule-keeper] Chưa được kết thúc lượt: ${why.join('; ')}.`,
    files.length ? `File đã đổi (có thể gồm file của người/agent khác — khi đó ghi rõ là không phải của bạn): ${shown}` : '',
    changesBlock(changes),
    'Làm ngay, theo thứ tự:',
    `1. Đọc lại sổ ${ctx.ledgerRel} và mục "Done-gate" trong ${ctx.kitRel}/SKILL.md.`,
    '2. Điền mục "## Done-gate" của sổ: mỗi R# còn hiệu lực một dòng ✅ + "bằng chứng: …" hoặc ⚠️/❌ + còn thiếu gì; mỗi M# không sinh R# một dòng "- M# — không có yêu cầu mới"; thêm các dòng "- Quy tắc: …", "- Diff: …", "- Kiểm tra: …".',
    `3. Chạy: ${cmd(ctx, 'gate')} — sửa cho tới khi nó in GATE OK.`,
    '4. Sau đó mới trả lời người dùng, và nói rõ R# nào chưa xong hoặc chưa kiểm chứng.',
    'Nếu việc CHƯA xong và bạn chỉ đang báo tiến độ: vẫn chạy gate, đánh ⚠️ cho phần chưa xong — gate kiểm tra sự trung thực, không đòi mọi thứ phải xong. Đừng sửa sổ cho "qua" gate khi công việc thật sự không như vậy.',
  ]
    .filter(Boolean)
    .join('\n');
  return { block: true, reason: clamp(reason, ctx.cfg.maxContextChars) };
}

// Antigravity không gửi tin nhắn của người dùng cho hook, nhưng ghi transcript JSONL; đọc tiếp
// từ chỗ lần trước dừng để không phải đọc lại cả file mỗi lần gọi model.
function readTranscript(ctx, st, transcriptPath) {
  const out = [];
  if (!transcriptPath) return out;
  let fd;
  try {
    const size = fs.statSync(transcriptPath).size;
    let offset = st.transcript?.path === transcriptPath ? st.transcript.offset : 0;
    if (offset > size) offset = 0;
    if (size === offset) return out;
    fd = fs.openSync(transcriptPath, 'r');
    const buf = Buffer.alloc(size - offset);
    fs.readSync(fd, buf, 0, buf.length, offset);
    const chunk = buf.toString('utf8');
    const lastNl = chunk.lastIndexOf('\n');
    if (lastNl < 0) return out;
    st.transcript = { path: transcriptPath, offset: offset + Buffer.byteLength(chunk.slice(0, lastNl + 1)) };
    for (const line of chunk.slice(0, lastNl).split('\n')) {
      let o;
      try {
        o = JSON.parse(line);
      } catch {
        continue;
      }
      const content = typeof o.content === 'string' ? o.content : '';
      if (o.type === 'USER_INPUT') {
        const m = /<USER_REQUEST>\s*([\s\S]*?)\s*<\/USER_REQUEST>/.exec(content);
        const text = (m ? m[1] : content.replace(/<([A-Z_]+)>[\s\S]*?<\/\1>/g, '')).trim();
        if (text && !isOwnContinuation(text)) out.push(text);
      } else if (o.type === 'PLANNER_RESPONSE' && content.trim()) {
        st.lastModelMessage = content.slice(-4000);
      }
    }
  } catch {
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
  }
  return out;
}

// ---------------------------------------------------------------------------------------------
// Hook

async function readStdin() {
  if (process.stdin.isTTY) return {};
  let s = '';
  for await (const c of process.stdin) s += c;
  try {
    return JSON.parse(s || '{}');
  } catch {
    return {};
  }
}

const isOwnContinuation = (prompt) => String(prompt || '').trimStart().startsWith('[rule-keeper]');

async function hook(tool, event) {
  const input = await readStdin();
  let ctx;
  try {
    if (tool === 'codex') {
      ctx = context(projectRoot(input.cwd || process.cwd()), 'codex', shortId(input.session_id));
      const st = loadState(ctx);
      if (event === 'session-start') {
        const created = ensureSession(ctx, st);
        const { files, changes } = checkRules(ctx, st);
        syncAlwaysOnRule(ctx);
        const parts = [introBlock(ctx, files, { withRules: true })];
        if (!created && input.source && input.source !== 'startup') parts.push(recoveryBlock(ctx, input.source));
        if (changes.length) parts.push(changesBlock(changes));
        saveState(ctx, st);
        return out({ hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: clamp(parts.join('\n\n'), ctx.cfg.maxContextChars) } });
      }
      if (event === 'prompt') {
        const created = ensureSession(ctx, st);
        const id = isOwnContinuation(input.prompt) ? null : appendMessage(ctx, input.prompt);
        const { files, changes } = checkRules(ctx, st);
        syncAlwaysOnRule(ctx);
        const parts = [];
        if (created) parts.push(introBlock(ctx, files, { withRules: true }));
        parts.push(anchorBlock(ctx, { newMsg: id, unresolved: st.unresolvedGate }));
        if (changes.length) parts.push(changesBlock(changes));
        saveState(ctx, st);
        return out({ hookSpecificOutput: { hookEventName: 'UserPromptSubmit', additionalContext: clamp(parts.join('\n\n'), ctx.cfg.maxContextChars) } });
      }
      if (event === 'stop') {
        if (!st.createdAt) return out({});
        const d = stopDecision(ctx, st, { lastMessage: input.last_assistant_message });
        saveState(ctx, st);
        if (d.block) return out({ decision: 'block', reason: d.reason });
        return out(d.warn ? { systemMessage: d.warn } : {});
      }
    }
    if (tool === 'agy') {
      const root = projectRoot(input.workspacePaths?.[0] || path.resolve(process.cwd(), '..'));
      ctx = context(root, 'agy', shortId(input.conversationId));
      const st = loadState(ctx);
      if (event === 'pre') {
        const created = ensureSession(ctx, st);
        const msgs = readTranscript(ctx, st, input.transcriptPath);
        const ids = msgs.map((m) => appendMessage(ctx, m)).filter(Boolean);
        const { files, changes } = checkRules(ctx, st);
        syncAlwaysOnRule(ctx);
        st.invocations = (st.invocations || 0) + 1;
        const parts = [];
        if (created) parts.push(introBlock(ctx, files, { withRules: !fs.existsSync(path.join(root, ALWAYS_ON_RULE)) }));
        if (ids.length) parts.push(anchorBlock(ctx, { newMsg: ids.join(', '), unresolved: st.unresolvedGate }));
        else if (!created && st.invocations % ctx.cfg.anchorEvery === 0) parts.push(anchorBlock(ctx));
        if (changes.length) parts.push(changesBlock(changes));
        saveState(ctx, st);
        return out(parts.length ? { injectSteps: [{ ephemeralMessage: clamp(parts.join('\n\n'), ctx.cfg.maxContextChars) }] } : {});
      }
      if (event === 'stop') {
        if (!st.createdAt) return out({});
        if (/error|cancel|interrupt|max/i.test(String(input.terminationReason || ''))) return out({});
        for (const m of readTranscript(ctx, st, input.transcriptPath)) appendMessage(ctx, m);
        const d = stopDecision(ctx, st, { lastMessage: st.lastModelMessage });
        saveState(ctx, st);
        if (d.block) return out({ decision: 'continue', reason: d.reason });
        // Stop của Antigravity không có kênh nhắn thẳng cho người dùng như systemMessage của Codex,
        // nên trả {} là lượt kết thúc im lặng. Ép một bước cuối mà việc duy nhất là nói ra.
        if (d.warn) {
          return out({
            decision: 'continue',
            reason: `[rule-keeper] Không chặn nữa. Việc DUY NHẤT còn lại của lượt này: viết cho người dùng, ngay câu đầu, rằng việc CHƯA qua done-gate (${d.why}) nên chưa được coi là xong, và họ có thể bảo bạn chạy gate (sổ: ${ctx.ledgerRel}). Không sửa file, không chạy lệnh nào khác, rồi dừng.`,
          });
        }
        return out({});
      }
    }
    return out({});
  } catch (err) {
    // Hook không bao giờ được làm hỏng phiên của agent: lỗi thì ghi lại và cho qua.
    try {
      const dir = ctx ? path.join(ctx.ledgerDirAbs, '.state') : path.join(KIT_DIR, '.state');
      fs.mkdirSync(dir, { recursive: true });
      fs.appendFileSync(path.join(dir, 'hook-errors.log'), `${new Date().toISOString()} ${tool} ${event}: ${err?.stack || err}\n`);
    } catch {}
    return out({});
  }
}

function out(obj) {
  process.stdout.write(JSON.stringify(obj));
}

// ---------------------------------------------------------------------------------------------
// Lệnh cho agent chạy tay

function parseArgs(argv) {
  const a = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const k = argv[i].slice(2);
      a[k] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    } else a._.push(argv[i]);
  }
  return a;
}

function requireLedger(args) {
  if (!args.ledger || args.ledger === true) {
    console.error('Thiếu --ledger <đường dẫn sổ>. Hook đã báo đường dẫn; không có hook thì chạy: rk.mjs start --agent <tên>');
    process.exitCode = 2;
    return null;
  }
  if (!fs.existsSync(args.ledger)) {
    console.error(`Không thấy sổ ${args.ledger}.`);
    process.exitCode = 2;
    return null;
  }
  return contextFromLedger(args.ledger);
}

function cmdStart(args) {
  const agent = String(args.agent && args.agent !== true ? args.agent : 'agent').replace(/[^A-Za-z0-9_]/g, '') || 'agent';
  const d = new Date();
  const id = `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
  const ctx = context(projectRoot(process.cwd()), agent, id);
  const st = loadState(ctx);
  ensureSession(ctx, st);
  const { files } = checkRules(ctx, st);
  saveState(ctx, st);
  console.log(introBlock(ctx, files, { withRules: true }));
}

function cmdWhere(args) {
  const agent = String(args.agent && args.agent !== true ? args.agent : '');
  const ctx = context(projectRoot(process.cwd()), agent || 'x', 'x');
  const base = path.join(ctx.ledgerDirAbs, '.state');
  let best = null;
  try {
    for (const k of fs.readdirSync(base)) {
      if (agent && !k.startsWith(`${agent}-`)) continue;
      const f = path.join(base, k, 'state.json');
      if (!fs.existsSync(f)) continue;
      const t = fs.statSync(f).mtimeMs;
      if (!best || t > best.t) best = { t, k };
    }
  } catch {}
  if (!best) {
    console.log('Chưa có sổ nào. Tạo bằng: node rk.mjs start --agent <tên>');
    process.exitCode = 1;
  } else console.log(`${ctx.cfg.ledgerDir}/${best.k}.md`);
}

function cmdIndex() {
  const ctx = context(projectRoot(process.cwd()), 'index', 'x');
  console.log(indexBlock(ctx, listRuleFiles(ctx, null)));
}

function cmdCheck(args) {
  const ctx = requireLedger(args);
  if (!ctx) return;
  const st = loadState(ctx);
  ensureSession(ctx, st);
  const { changes } = checkRules(ctx, st);
  saveState(ctx, st);
  console.log(changes.length ? changesBlock(changes) : 'Không có file quy tắc nào đổi kể từ lần xem trước.');
}

function cmdGate(args) {
  const ctx = requireLedger(args);
  if (!ctx) return;
  const st = loadState(ctx);
  ensureSession(ctx, st);
  const text = readText(ctx.ledgerAbs);
  const parsed = parseLedger(text);
  const v = validateGate(parsed);
  const { changes } = checkRules(ctx, st);
  if (changes.length) {
    v.problems.unshift('Quy tắc đã đổi kể từ lần bạn xem trước — đọc thay đổi bên dưới, đối chiếu lại công việc, cập nhật Done-gate rồi chạy lại gate.');
  }
  if (v.problems.length) {
    saveState(ctx, st);
    // Mã ASCII đứng đầu vì Codex chạy lệnh qua PowerShell 5.1 và nhận tiếng Việt về thành mojibake.
    console.log(`GATE FAILED — chưa đạt, ${v.problems.length} vấn đề:`);
    for (const p of v.problems) console.log(`  - ${p}`);
    if (changes.length) console.log(`\n${changesBlock(changes)}`);
    console.log(`\nSửa sổ ${ctx.ledgerRel} (và công việc nếu cần) rồi chạy lại. Đừng báo người dùng là đã xong.`);
    process.exitCode = 1;
    return;
  }
  const wt = worktree(ctx);
  st.lastGate = { at: new Date().toISOString(), fp: wt?.fp, head: wt?.head, entries: wt?.entries, ledgerHash: sha(text), msgCount: parsed.msgs.length };
  st.stop = { blocks: 0 };
  delete st.unresolvedGate;
  saveState(ctx, st);
  console.log(`GATE OK — ${v.done.length} xong, ${v.notDone.length} chưa xong/một phần.`);
  if (v.done.length) console.log(`  ✅ ${v.done.map((r) => r.id).join(', ')}`);
  if (v.notDone.length) {
    console.log('  Câu trả lời cuối PHẢI nói rõ những mục này chưa xong, kèm lý do:');
    for (const r of v.notDone) console.log(`  ⚠️ ${r.line}`);
  }
  console.log('Giờ mới trả lời người dùng: việc đã làm + bằng chứng ngắn, việc chưa xong, điều chưa kiểm chứng.');
}

export async function main(argv) {
  const args = parseArgs(argv);
  const [sub, a1, a2] = args._;
  if (sub === 'hook') return hook(a1, a2);
  if (sub === 'start') return cmdStart(args);
  if (sub === 'where') return cmdWhere(args);
  if (sub === 'index') return cmdIndex();
  if (sub === 'check') return cmdCheck(args);
  if (sub === 'gate') return cmdGate(args);
  console.log(readText(fileURLToPath(import.meta.url)).split('\n').slice(1, 12).join('\n').replace(/^\/\/ ?/gm, ''));
  process.exitCode = sub ? 2 : 0;
}

const invoked = process.argv[1] ? path.resolve(process.argv[1]) : '';
const self = fileURLToPath(import.meta.url);
if (invoked && (process.platform === 'win32' ? invoked.toLowerCase() === self.toLowerCase() : invoked === self)) {
  await main(process.argv.slice(2));
}
