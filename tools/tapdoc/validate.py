"""Kiểm tra dữ liệu: chặn file bài và danh mục lỗi trước khi vào app.

Các hàm `check_*` đều trả danh sách `Issue` (rỗng là đạt) và không bao giờ ghi file.
`validate_all` đọc mọi bài đã dựng trong `UNITY_RES/lessons` cùng hai danh mục rồi chạy hết các kiểm tra.
Vị trí (`where`) theo đường dẫn JSON của file bài, ví dụ `part2[3]` hay `part1[7].spell`.
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from .curriculum import Learned, is_learned_text, learned_until, load_curriculum
from .ids import CONSONANT_NAMES
from .manifest import STATUS_NONE, STATUS_PENDING, ManifestError, load_rows
from .paths import LESSON_INDEX, MANIFESTS, UNITY_ASSETS, UNITY_RES
from .viet import is_nfc, nfc, split_syllable, syllables

GLOBAL = "-"  # `lesson` của lỗi không thuộc một bài nào

ROUNDS_MIN, ROUNDS_MAX = 6, 10

# Ký hiệu đầu mục được phép: không có, ● (em đọc), ⌂ (luyện tập), ●▨ (em đọc + em viết).
VALID_MARKERS = ("", "●", "⌂", "●▨")

NO_LESSONS = "chưa có bài nào được dựng — chạy build trước"
REVIEWED = "da_duyet"  # `review.status` của bài đã được chủ dự án duyệt
EMPTY_SPELL = "đánh vần rỗng (chưa có quy tắc) — xem can_duyet"

_ROUND_KINDS = ("listen_choose", "look_tone", "compose", "listen_picture", "match_case")
# Lượt không có đề bằng âm thanh: bé nhìn rồi chọn, không có gì để nghe nhầm theo giọng miền Nam.
_SILENT_KINDS = ("look_tone", "match_case")
_AUDIO_KEYS = ("audio", "then_audio")
_PICTURE_NN = re.compile(r"^img_b(\d+)_")
_IMAGES_DIR = ("content", "resources", "images")  # so khớp không phân biệt hoa/thường


@dataclass(frozen=True)
class Issue:
    lesson: str  # mã bài; `-` nếu là lỗi chung
    where: str
    message: str


def _lid(lesson: dict) -> str:
    return str(lesson.get("lesson_id") or GLOBAL)


def _items(value):
    """Các phần tử là đối tượng JSON của một danh sách (kèm vị trí); giá trị khác thì coi như rỗng."""
    if isinstance(value, list):
        for index, item in enumerate(value):
            if isinstance(item, dict):
                yield index, item


# ---- giọng miền Nam ----

_SOUTHERN_ONSET = {"gi": "d", "v": "d", "x": "s", "tr": "ch"}


def _southern_token(token: str) -> str:
    letter = nfc(token).lower()
    if letter in CONSONANT_NAMES:  # phụ âm đứng riêng (phương án "s", "gi" ở bài nghe chọn chữ)
        return _SOUTHERN_ONSET.get(letter, letter)
    try:
        syl = split_syllable(token)
    except ValueError:
        return letter  # không tách được (ký tự lạ): giữ nguyên
    onset = _SOUTHERN_ONSET.get(syl.onset, syl.onset)
    rime = syl.rime
    if rime.endswith("ng"):
        rime = rime[:-2] + "n"
    elif rime.endswith("c"):
        rime = rime[:-1] + "t"
    tone = "hoi" if syl.tone == "nga" else syl.tone
    return f"{onset}|{rime}|{tone or ''}"


def southern_key(text: str) -> str:
    """Khóa nghe-giống theo giọng miền Nam: hai chữ cùng khóa thì bé miền Nam khó phân biệt khi nghe.

    Mỗi tiếng: ngã -> hỏi; âm đầu gi, v -> d; x -> s; tr -> ch; âm cuối ng -> n, c -> t.
    Phụ âm đứng riêng gộp như âm đầu ("x" như "s", "gi" và "v" như "d").
    """
    return " ".join(_southern_token(token) for token in syllables(text))


# ---- NFC ----

def _walk_strings(node, path: str):
    """(vị trí, là khóa?, chuỗi) của mọi chuỗi trong dữ liệu JSON, kể cả khóa."""
    if isinstance(node, str):
        yield path, False, node
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from _walk_strings(item, f"{path}[{index}]")
    elif isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else str(key)
            if isinstance(key, str):
                yield child, True, key
            yield from _walk_strings(value, child)


def check_nfc(lesson: dict) -> list[Issue]:
    lid = _lid(lesson)
    issues = []
    for where, is_key, text in _walk_strings(lesson, ""):
        if is_key:
            # chỉ báo khóa sai; giá trị bên dưới vẫn được duyệt riêng
            if not is_nfc(text):
                issues.append(Issue(lid, where, f"khóa không chuẩn hóa NFC: {ascii(text)}"))
        elif not is_nfc(text):
            issues.append(Issue(lid, where, f"chuỗi không chuẩn hóa NFC: {ascii(text)}"))
    return issues


# ---- mã âm thanh, mã tranh ----

def _part1_refs(node, path: str, audio: list, image: list) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}"
            if key in _AUDIO_KEYS and isinstance(value, str):
                audio.append((child, value))
            elif key == "image" and isinstance(value, str):
                if value:
                    image.append((child, value))
            else:
                _part1_refs(value, child, audio, image)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            _part1_refs(item, f"{path}[{index}]", audio, image)


def _part2_refs(lesson: dict, audio: list, image: list) -> None:
    for i, rd in _items(lesson.get("part2")):
        where = f"part2[{i}]"
        for key in ("instruction_audio", "prompt_audio"):
            if rd.get(key):
                audio.append((f"{where}.{key}", rd[key]))
        if rd.get("image"):
            image.append((f"{where}.image", rd["image"]))
        for j, option in _items(rd.get("options")):
            if option.get("audio"):
                audio.append((f"{where}.options[{j}].audio", option["audio"]))
            if option.get("image"):
                image.append((f"{where}.options[{j}].image", option["image"]))


def check_refs(lesson: dict, audio_ids, image_ids) -> list[Issue]:
    """Mọi mã âm thanh và mã tranh bài dùng phải có trong danh mục tương ứng."""
    lid = _lid(lesson)
    audio: list[tuple[str, str]] = []
    image: list[tuple[str, str]] = []
    _part1_refs(lesson.get("part1"), "part1", audio, image)
    _part2_refs(lesson, audio, image)
    issues = []
    for where, audio_id in audio:
        if not audio_id:
            issues.append(Issue(lid, where, "mã âm thanh rỗng"))
        elif audio_id not in audio_ids:
            issues.append(Issue(lid, where, f"mã âm thanh {audio_id!r} không có trong danh mục"))
    for where, image_id in image:
        if image_id not in image_ids:
            issues.append(Issue(lid, where, f"mã tranh {image_id!r} không có trong danh mục"))
    return issues


def check_files(rows: list[dict], res_dir) -> list[Issue]:
    """Mỗi dòng danh mục phải có file thật tại `res_dir / file`."""
    res_dir = Path(res_dir)
    issues = []
    for row in rows:
        row_id = str(row.get("id", "?"))
        file = row.get("file")
        if not isinstance(file, str) or not file:
            issues.append(Issue(GLOBAL, row_id, "dòng danh mục không có trường file"))
        elif not (res_dir / file).is_file():
            issues.append(Issue(GLOBAL, row_id, f"không có file {file}"))
    return issues


# ---- Phần 1 ----

def _empty_spell(lid: str, where: str, spell: dict) -> list[Issue]:
    return [] if spell.get("parts") else [Issue(lid, where, EMPTY_SPELL)]


def check_part1(lesson: dict) -> list[Issue]:
    """Đánh vần không được rỗng; ký hiệu đầu mục phải nằm trong `VALID_MARKERS`."""
    lid = _lid(lesson)
    issues = []
    steps = lesson.get("part1")
    if not isinstance(steps, list):
        return [Issue(lid, "part1", "part1 phải là một danh sách")]
    for i, step in enumerate(steps):
        where = f"part1[{i}]"
        if not isinstance(step, dict):
            issues.append(Issue(lid, where, "bước không phải đối tượng JSON"))
            continue
        if "marker" in step and step["marker"] not in VALID_MARKERS:
            issues.append(Issue(lid, f"{where}.marker", f"ký hiệu {step['marker']!r} không hợp lệ "
                                f"(chỉ được {', '.join(repr(m) for m in VALID_MARKERS)})"))
        if isinstance(step.get("spell"), dict):
            issues += _empty_spell(lid, f"{where}.spell", step["spell"])
        for j, item in _items(step.get("items")):
            for k, spell in _items(item.get("spells")):
                issues += _empty_spell(lid, f"{where}.items[{j}].spells[{k}]", spell)
    return issues


# ---- Phần 2 ----

def _text_issue(lid: str, where: str, text, learned: Learned, label: str) -> Issue | None:
    if not isinstance(text, str) or not text.strip():
        return Issue(lid, where, f"{label} rỗng")
    if not is_learned_text(text, learned):
        return Issue(lid, where, f"{label} {text!r} chưa học tới bài này")
    return None


def _picture_issues(lid: str, where: str, image, lesson_no: int) -> list[Issue]:
    match = _PICTURE_NN.match(image) if isinstance(image, str) else None
    if match and int(match.group(1)) > lesson_no:
        return [Issue(lid, where, f"tranh {image!r} của bài {int(match.group(1))}, chưa học tới "
                                  f"(đang ở bài {lesson_no})")]
    return []


def _check_round(lid: str, i: int, rd, learned: Learned, lesson_no: int) -> list[Issue]:
    where = f"part2[{i}]"
    if not isinstance(rd, dict):
        return [Issue(lid, where, "lượt không phải đối tượng JSON")]
    kind = rd.get("kind")
    if kind not in _ROUND_KINDS:
        return [Issue(lid, where, f"kind lạ {kind!r}")]
    options = rd.get("options")
    if not isinstance(options, list) or not all(isinstance(o, dict) for o in options):
        return [Issue(lid, f"{where}.options", "options phải là danh sách các phương án")]

    issues = []
    answer = rd.get("answer")
    if isinstance(answer, bool) or not isinstance(answer, int) or not 0 <= answer < len(options):
        issues.append(Issue(lid, f"{where}.answer",
                            f"đáp án {answer!r} không phải vị trí hợp lệ trong {len(options)} phương án"))

    if kind == "match_case":
        issue = _text_issue(lid, f"{where}.prompt_text", rd.get("prompt_text"), learned, "chữ mẫu")
        if issue:
            issues.append(issue)

    if kind == "look_tone":
        issue = _text_issue(lid, f"{where}.prompt_text", rd.get("prompt_text"), learned, "chữ mẫu")
        if issue:
            issues.append(issue)
        for j, option in enumerate(options):
            if option.get("tone") not in learned.tones:
                issues.append(Issue(lid, f"{where}.options[{j}].tone",
                                    f"dấu {option.get('tone')!r} chưa học tới bài này"))
    elif kind != "listen_picture":  # listen_choose, compose, match_case
        for j, option in enumerate(options):
            issue = _text_issue(lid, f"{where}.options[{j}].text", option.get("text"), learned, "phương án")
            if issue:
                issues.append(issue)

    issues += _picture_issues(lid, f"{where}.image", rd.get("image"), lesson_no)
    for j, option in enumerate(options):
        issues += _picture_issues(lid, f"{where}.options[{j}].image", option.get("image"), lesson_no)

    if kind not in _SILENT_KINDS:
        seen: dict[str, str] = {}  # khóa nghe-giống -> chữ của phương án đầu tiên có khóa đó
        for j, option in enumerate(options):
            text = option.get("text")
            if not isinstance(text, str) or not text.strip():
                continue
            key = southern_key(text)
            if key in seen:
                issues.append(Issue(lid, f"{where}.options[{j}].text",
                                    f"hai phương án {seen[key]!r} và {text!r} nghe giống nhau theo giọng miền Nam"))
            else:
                seen[key] = text
    return issues


def check_part2(lesson: dict, learned: Learned) -> list[Issue]:
    """Bài tập Phần 2: chữ đã học, không nghe nhầm theo giọng miền Nam, đủ 6–10 lượt."""
    lid = _lid(lesson)
    rounds = lesson.get("part2")
    if not isinstance(rounds, list):
        return [Issue(lid, "part2", "part2 phải là một danh sách")]
    issues = []
    if not ROUNDS_MIN <= len(rounds) <= ROUNDS_MAX:
        issues.append(Issue(lid, "part2", f"số lượt Phần 2 phải từ {ROUNDS_MIN}–{ROUNDS_MAX}, "
                                          f"hiện có {len(rounds)}"))
    lesson_no = lesson["lesson_no"]
    for i, rd in enumerate(rounds):
        issues += _check_round(lid, i, rd, learned, lesson_no)
    return issues


# ---- ảnh scan ----

def _scan_reasons(name: str, in_images_dir: bool) -> list[str]:
    lower = name.lower()
    reasons = []
    if lower.endswith((".jpg", ".jpeg")):
        reasons.append("file .jpg/.jpeg (ảnh scan không được nằm trong project Unity)")
    if "trang_" in lower or "thuongmaitruongxua" in lower:
        reasons.append("tên giống ảnh scan sách")
    if in_images_dir and not lower.endswith(".meta") and not name.startswith("img_"):
        reasons.append("tranh trong Content/Resources/images phải có tên bắt đầu bằng img_")
    return reasons


def check_no_scans(unity_assets_dir) -> list[Issue]:
    root = Path(unity_assets_dir)
    issues = []
    for dirpath, _, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        in_images_dir = tuple(part.lower() for part in rel_dir.parts) == _IMAGES_DIR
        for name in filenames:
            reasons = _scan_reasons(name, in_images_dir)
            if reasons:
                issues.append(Issue(GLOBAL, (rel_dir / name).as_posix(), "; ".join(reasons)))
    return sorted(issues, key=lambda issue: issue.where)


# ---- toàn bộ ----

def _load_lesson(path: Path):
    """(bài, lỗi): đọc một file bài; không đọc được hoặc không phải đối tượng thì trả lỗi."""
    try:
        with open(path, encoding="utf-8") as f:
            lesson = json.load(f)
    except (OSError, ValueError) as e:
        return None, Issue(path.stem, "(file)", f"không đọc được {path.name}: {e}")
    if not isinstance(lesson, dict):
        return None, Issue(path.stem, "(file)", f"{path.name} phải là một đối tượng JSON")
    return lesson, None


def _learned_for(lesson: dict, curricula: dict) -> tuple[Learned | None, Issue | None]:
    """Những gì bé đã học tới bài này, theo giáo trình của sách trong `LESSON_INDEX`."""
    lid = _lid(lesson)
    book, lesson_no = lesson.get("book"), lesson.get("lesson_no")
    if not isinstance(book, str) or not book:
        return None, Issue(lid, "book", "thiếu trường 'book'")
    if isinstance(lesson_no, bool) or not isinstance(lesson_no, int):
        return None, Issue(lid, "lesson_no", "thiếu trường 'lesson_no' (số nguyên)")
    if book not in curricula:
        try:
            curricula[book] = load_curriculum(LESSON_INDEX, book)
        except (OSError, KeyError, ValueError) as e:
            return None, Issue(lid, "(giáo trình)", f"không đọc được giáo trình {Path(LESSON_INDEX).name}: {e!r}")
    cur = curricula[book]
    if not cur:
        return None, Issue(lid, "book", f"sách {book!r} không có trong giáo trình {Path(LESSON_INDEX).name}")
    try:
        return learned_until(cur, lesson_no), None
    except ValueError as e:
        return None, Issue(lid, "(giáo trình)", str(e))


def check_release_lesson(lesson: dict) -> list[Issue]:
    """Bài hiện trong app phải được chủ dự án duyệt (`review.status` = `da_duyet`)."""
    if lesson.get("in_app", True) is False:
        return []
    review = lesson.get("review")
    status = review.get("status") if isinstance(review, dict) else None
    if status == REVIEWED:
        return []
    return [Issue(_lid(lesson), "review.status", f"bài chưa duyệt (review.status = {status!r})")]


def check_release_rows(rows: list[dict], label: str) -> list[Issue]:
    """Âm thanh/tranh phải đã có file và đã nghe/xem; `khong_dat` vẫn được dùng tạm."""
    return [Issue(GLOBAL, str(row.get("id", "?")), f"{label} chưa duyệt (status = {row.get('status')})")
            for row in rows if row.get("status") in (STATUS_NONE, STATUS_PENDING)]


_RELEASE_WARN_LIST = 5  # quá số này thì chỉ in một dòng tóm tắt


def release_warnings(rows) -> list[str]:
    """Nguồn edge-tts cần xem lại quyền sử dụng khi phát hành, nhưng không chặn kiểm tra."""
    ids = [str(row.get("id", "?")) for row in rows if str(row.get("source", "")).startswith("tts_edge_")]
    if not ids:
        return []
    note = "dùng dịch vụ Edge không chính thức; cần xem lại quyền sử dụng trước khi phát hành công khai"
    if len(ids) <= _RELEASE_WARN_LIST:
        return [f"{audio_id}: nguồn edge-tts {note}" for audio_id in ids]
    return [f"{len(ids)} file âm thanh nguồn edge-tts (ví dụ {', '.join(ids[:3])}) {note}"]


def validate_all(allow_missing: bool = False, release: bool = False) -> list[Issue]:
    """Kiểm tra mọi bài đã dựng trong `UNITY_RES/lessons`, hai danh mục và project Unity.

    Thứ tự lỗi: từng bài một, rồi file của danh mục, rồi ảnh scan. `allow_missing` bỏ qua việc
    kiểm tra file âm thanh/tranh còn thiếu (lúc chưa nhập đủ file vẫn kiểm tra được phần còn lại).
    `release` thêm điều kiện phát hành: bài trong app đã duyệt, âm thanh/tranh không còn chờ duyệt.
    """
    lessons_dir = Path(UNITY_RES) / "lessons"
    paths = sorted(p for p in lessons_dir.glob("*.json") if p.is_file() and p.name != "index.json") \
        if lessons_dir.is_dir() else []
    if not paths:
        return [Issue(GLOBAL, "lessons", NO_LESSONS)]

    manifest_issues: list[Issue] = []
    manifests: dict[str, list[dict]] = {}
    for name in ("audio_manifest.json", "image_manifest.json"):
        try:
            manifests[name] = load_rows(Path(MANIFESTS) / name)
        except ManifestError as e:
            manifests[name] = []
            manifest_issues.append(Issue(GLOBAL, name, str(e)))
    audio_rows, image_rows = manifests["audio_manifest.json"], manifests["image_manifest.json"]
    audio_ids = {row["id"] for row in audio_rows}
    image_ids = {row["id"] for row in image_rows}

    issues: list[Issue] = []
    curricula: dict[str, dict] = {}
    for path in paths:
        lesson, problem = _load_lesson(path)
        if problem:
            issues.append(problem)
            continue
        issues += check_nfc(lesson)
        issues += check_part1(lesson)
        issues += check_refs(lesson, audio_ids, image_ids)
        learned, problem = _learned_for(lesson, curricula)
        if problem:
            issues.append(problem)
        else:
            issues += check_part2(lesson, learned)
        if release:
            issues += check_release_lesson(lesson)

    issues += manifest_issues
    if release:
        issues += check_release_rows(audio_rows, "âm thanh")
        issues += check_release_rows(image_rows, "tranh")
    if not allow_missing:
        issues += check_files(audio_rows, UNITY_RES)
        issues += check_files(image_rows, UNITY_RES)
    issues += check_no_scans(UNITY_ASSETS)
    return issues
