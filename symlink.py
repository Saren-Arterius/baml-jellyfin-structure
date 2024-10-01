import os.path
import json
import os
import shutil
import sys
base_dir = sys.argv[1]
if not base_dir.endswith("/"):
    base_dir += "/"

json_path = sys.argv[2]
data = json.loads(open(json_path).read())

def do_link(dry):
    for bucket in data:
        # print(bucket)
        # f = files[bucket.idx - 1]
        if len(bucket) == 1:
            episode = bucket[0]
            base, ext = os.path.splitext(episode[0])
            series_name, _, _, special_name = episode[2]
            # assume movie
            new_path = f"Movies/{series_name}/{series_name}"
            if special_name is not None:
                new_path += f"/extras/{series_name} {special_name}"
            link_path = f'{base_dir}{new_path}{ext}'
            print(f"{episode[0]} => {link_path}")
            if not dry:
                dir = os.path.dirname(link_path)
                os.makedirs(dir, exist_ok=True)
                try:
                    os.symlink(episode[0], link_path)
                except Exception as e:
                    print(e)
            for assoc in episode[1]:
                assoc_link_path = f'{base_dir}{new_path}{assoc}'
                print(f"{base}{assoc} => {assoc_link_path}")
                if not dry:
                    try:
                        os.symlink(f'{base}{assoc}', assoc_link_path)
                    except Exception as e:
                        print(e)
        else:
            for episode in bucket:
                series_name, season_number, episode_number, special_name = episode[2]
                base, ext = os.path.splitext(episode[0])
                if not season_number:
                    season_number = 1
                new_path = f"{series_name}/Season {season_number:02}/"
                if special_name is not None:
                    en = f"{episode_number:02}" if episode_number is not None else ""
                    new_path += f"extras/{series_name} S{season_number:02} {special_name}{en}"
                else:
                    if episode_number is None:
                        episode_number = 1
                    new_path += (
                        f"{series_name} S{season_number:02}E{episode_number:02}"
                    )
                link_path = f'{base_dir}{new_path}{ext}'
                print(f"{episode[0]} => {link_path}")
                if not dry:
                    dir = os.path.dirname(link_path)
                    os.makedirs(dir, exist_ok=True)
                    try:
                        os.symlink(episode[0], link_path)
                    except Exception as e:
                        print(e)
                for assoc in episode[1]:
                    assoc_link_path = f'{base_dir}{new_path}{assoc}'
                    print(f"{base}{assoc} => {assoc_link_path}")
                    if not dry:
                        try:
                            os.symlink(f'{base}{assoc}', assoc_link_path)
                        except Exception as e:
                            print(e)

do_link(True)
confirm = input('ok? y: ')
if confirm == 'y':
    shutil.rmtree(base_dir, True)
    do_link(False)
