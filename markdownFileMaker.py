import zoteroDataFetcher as zotero
from variables import zotero_sql_path, output_path
import secrets, string
from pathlib import Path
import re
from termList import TAGS

# LOAD DAT
db = zotero.getAllData(zotero_sql_path)

# OUTPU
output_dir = Path(output_path)
output_dir.mkdir(exist_ok=True)

# HELPER
def gen_id():
    return ''.join(
        secrets.choice(string.ascii_lowercase + string.digits)
        for _ in range(11)
    )


def clean_path(p):
    if isinstance(p, str):
        return p.replace("storage:", "")
    return ""


def safe_filename(name: str) -> str:
    name = str(name or "untitled")
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    name = name.rstrip('. ')
    return name[:150]

# TAG NORMALIZATIO
def norm(s: str) -> str:
    return re.sub(r'[\s\-_|:.,;()]+', '', s or "").lower()

# TAG MATCHING ENGINE (ROBUST FOR HTML + PDF + NOISY TEXT
def find_matches(text: str):
    if not text:
        return []

    matches = []
    n = len(text)

    # iterate over all known concepts/variants
    for concept, variants in TAGS.items():
        for v in variants:
            if not v:
                continue

            nv = norm(v)
            if not nv:
                continue

            lv = len(v)

            # scan text with tolerance window
            for i in range(n):
                window = norm(text[i:i + lv + 12])  # tolerance for separators

                if nv in window:
                    matches.append((i, i + lv, concept))

    # sort + remove overlaps
    matches.sort(key=lambda x: (x[0], -(x[1] - x[0])))

    filtered = []
    last = 0

    for s, e, c in matches:
        if s < last:
            continue
        filtered.append((s, e, c))
        last = e

    return filtered


def wrap_terms(text: str):
    if not text:
        return text

    matches = find_matches(text)
    if not matches:
        return text

    out = []
    last = 0

    for start, end, concept in matches:
        out.append(text[last:end])
        out.append(f" [[{concept}]]")
        last = end

    out.append(text[last:])
    return ''.join(out)

# GROUP BY ATTACHMENT (FIXED + STABLE
def write_md_files():

    attachments = {}

    # build attachment index (1 file = 1 node)
    for r in db:
        if not r or len(r) < 10:
            continue

        att_id = r[5]
        if att_id is None:
            continue

        if att_id not in attachments:
            attachments[att_id] = {
                "rows": [],
                "path": r[6],
                "item_key": r[9],
                "parent_id": r[7]
            }

        attachments[att_id]["rows"].append(r)

    storage_path = zotero_sql_path.replace("zotero.sqlite", "storage")

    for att_id, data in attachments.items():

        rows = data["rows"]

        parts = []

        attachment_path = clean_path(data["path"])
        item_key = data["item_key"] if data["item_key"] else f"missing_{att_id}"

        # TITLE (works for HTML, PDF, snapshots)
        raw_title = None
        for r in rows:
            if r[17] == 1 and r[18]:
                raw_title = r[18]
                break

        if not raw_title:
            raw_title = f"attachment_{att_id}"

        filename = safe_filename(raw_title)
        tagged_title = wrap_terms(raw_title)

        parts.append(
f"""---
annotation-target: {storage_path}\\{item_key}\\{attachment_path}
---

# {tagged_title}

"""
)

        # ANNOTATIONS
        seen = set()

        for r in rows:

            if not r or r[0] is None:
                continue

            ann_key = (r[0], r[1], r[2])

            if ann_key in seen:
                continue
            seen.add(ann_key)

            comment = wrap_terms(r[1] or "")
            highlight = wrap_terms(r[2] or "")

            annotation_id = gen_id()

            parts.append(
f"""
>%%
>```annotation-json
>"text":"{comment}"
>```
>%%
>*%%PREFIX%% %%HIGHLIGHT%% =={highlight}== %%POSTFIX%%*
>%%COMMENT%%
>{comment}
>
^{annotation_id}

"""
)

        file_path = output_dir / f"{filename}.md"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("".join(parts))


# RUN
write_md_files()