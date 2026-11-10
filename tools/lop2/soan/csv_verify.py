import csv, io, json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
p=R/"docs/source-inventory/LESSON_INDEX.csv"; raw=p.read_text(encoding="utf-8-sig")
src={}
for f in (R/"content/src").glob("tv2_t1_b*.json"):
    s=json.loads(f.read_text(encoding="utf-8")); src[s["lesson_no"]]=s
out=[]; n=0
for line in raw.split("\n"):
    if line.startswith("tv2_t1_2001,") and "metadata_verified,lesson_no " in line:
        r=next(csv.reader([line])); no=int(r[-1].split()[1])
        if no in src:
            s=src[no]; pg=[x for x in s["source"]["pages"] if x < 122] or s["source"]["pages"]
            r[6],r[7],r[8],r[10]=str(pg[0]),str(pg[-1]),s["source"]["scan_file"],"page_verified"
            b=io.StringIO(); csv.writer(b,lineterminator="").writerow(r); line=b.getvalue(); n+=1
    out.append(line)
p.write_text("\ufeff"+"\n".join(out),encoding="utf-8"); print("csv rows verified:", n)
