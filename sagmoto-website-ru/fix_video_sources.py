import re

# Read video_list.html
with open('video_list.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Mapping: old CDN URLs -> local video files
# Order matters: replace longest URLs first
replacements = [
    # video 1: X6s Fuel Tanker
    ('https://omo-oss-video110.thefastvideo.com/portal-saas/new2023032811535752050/cms/vedio/746b829d-9068-43f2-a210-a407ec94590b.mp4', 'videos/video1.mp4'),
    # video 2: X3s | Shining!
    ('https://omo-oss-video110.thefastvideo.com/portal-saas/new2023032811535752050/cms/vedio/16266d11-2e17-4261-8891-3155ec43c9d8.mp4', 'videos/video2.mp4'),
    # video 3: SAGMOTO i9 electric light truck
    ('https://omo-oss-video110.thefastvideo.com/portal-saas/new2023032811535752050/cms/vedio/5043fd1c-de74-41b5-8368-a420f4e98e2e.mp4', 'videos/video3.mp4'),
    # video 4: SAGMOTO X9 Cleaning sweeper truck
    ('https://omo-oss-video110.thefastvideo.com/portal-saas/new2023032811535752050/cms/vedio/56f1f1c3-a466-4d7c-b16e-a49ba21564d6.mp4', 'videos/video4.mp4'),
    # video 5: X9 2120 4X4 Dumper
    ('https://omo-oss-video110.thefastvideo.com/portal-saas/new2023032811535752050/cms/vedio/90e97676-6dfc-4eff-a452-174d48fda8ec.mp4', 'videos/video5.mp4'),
    # video 6: X9 1995 Lorry
    ('https://omo-oss-video110.thefastvideo.com/portal-saas/new2023032811535752050/cms/vedio/aea91ed1-9dfd-4166-9552-d896a9a1ca54.mp4', 'videos/video6.mp4'),
    # video 7: SAGMOTO Embracing World
    ('https://omo-oss-video110.thefastvideo.com/portal-saas/new2023032811535752050/cms/vedio/c89e4896-5569-4bc3-a197-dff0c6e6c18b.mp4', 'videos/video7.mp4'),
    # video 8: X3s 6x4 Stiff boom crane
    ('https://omo-oss-video110.thefastvideo.com/portal-saas/new2023032811535752050/cms/vedio/28f19a5e-ca71-412d-a279-d63c4fecd68e.mp4', 'videos/video8.mp4'),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"Replaced: {old.split('/')[-1]} -> {new}")
    else:
        print(f"NOT FOUND: {old.split('/')[-1]}")

with open('video_list.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDone! {count} URLs replaced.")

# Verify
print("\n--- Verification ---")
for old, new in replacements:
    if old in content:
        print(f"STILL HAS OLD: {old.split('/')[-1]}")
    if new in content:
        print(f"OK: {new} found")
