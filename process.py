from baml_client.sync_client import b
from baml_client.types import TVShowInfo
import os.path
import subprocess
import shlex
import json
import time
import sys

base_dir = sys.argv[1]
if not base_dir.endswith("/"):
    base_dir += "/"

json_path = sys.argv[2]

old_data = json.loads(open(json_path, "r").read())
old_shows_data = {}
for bucket in old_data:
    for show in bucket:
        if len(show) == 3:
            old_shows_data[show[0]] = show[2]
print(old_shows_data)

def find_shows(directory):
    all_files_cmd = f"find {shlex.quote(directory)} -type f"
    all_files_result = (
        subprocess.run(
            all_files_cmd, shell=True, check=True, text=True, capture_output=True
        )
        .stdout.strip()
        .split("\n")
    )
    mapping = {}
    for f in all_files_result:
        base, ext = os.path.splitext(f)
        if base not in mapping:
            mapping[base] = []
        mapping[base].append(base + ext)

    video_cmd = f"find {shlex.quote(directory)} -type f | parallel -q sh -c \"(mediainfo '{{}}' --Output=JSON | grep '\"Video\"' > /dev/null) && echo '{{}}'\" | sort -n"
    video_result = (
        subprocess.run(
            video_cmd, shell=True, check=True, text=True, capture_output=True
        )
        .stdout.strip()
        .split("\n")
    )
    for v in video_result:
        base, ext = os.path.splitext(v)
        yield [
            v,
            list(
                map(
                    lambda ff: os.path.splitext(ff)[1],
                    filter(lambda f: f != v, mapping[base]),
                )
            ),
        ]


shows = list(find_shows(base_dir))
buckets = []
current_show = ""
for show in shows:
    show_name = os.path.dirname(show[0]).replace(base_dir, "")
    print(show_name, show)
    if current_show != show_name:
        buckets.append([])
        current_show = show_name
    buckets[-1].append(show)

print(json.dumps(buckets, indent=2))
# exit()
for bucket in buckets:
    for show in bucket:
        if show[0] in old_shows_data:
            show.append(old_shows_data[show[0]])

    show_files = list(
        map(
            lambda f: {
                "filename": os.path.basename(f[0]),
                "folder": os.path.dirname(f[0].replace(base_dir, "")),
            },
            filter(lambda f: len(f) < 3, bucket),
        )
    )

    if len(show_files) == 0:
        continue

    print(show_files)
    dup_count = 0
    while True:
        try:
            info = b.ExtractShowInfo(show_files)
            if len(set(map(lambda show_ei: show_ei.idx, info))) != len(show_files):
                print("len(info) != len(show_files)")
                continue
            dup_check = set()
            has_dup = False
            for show_ei in info:
                s = f"{show_ei.series_name}/{show_ei.season_number}/{show_ei.episode_number}/{show_ei.special_name}"
                if s in dup_check:
                    print(f"dup: {s}")
                    has_dup = True
                dup_check.add(s)
            if has_dup:
                dup_count += 1
                if dup_count < 3:
                    continue
                print(f"dup bail")
            for show_ei in info:
                if len(bucket[show_ei.idx - 1]) == 3:
                    bucket[show_ei.idx - 1].pop(2)
                bucket[show_ei.idx - 1].append(
                    (
                        show_ei.series_name,
                        show_ei.season_number,
                        show_ei.episode_number,
                        show_ei.special_name,
                    )
                )
            output = json.dumps(buckets, indent=2)
            open(json_path, "w").write(output)
            break
        except Exception as e:
            print(e)
            time.sleep(2)

output = json.dumps(buckets, indent=2)
open(json_path, "w").write(output)
# print(output)
