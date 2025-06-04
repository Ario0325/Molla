import os
import re

# مسیر عکس‌ها
images_dir = r"D:\molla_ai\Molla\static\assets\images"

# ریشه پروژه برای جستجوی فایل‌هایی که ممکن است عکس در آن‌ها استفاده شده باشد
project_root = r"D:\molla_ai\Molla"

# پسوندهای فایل‌هایی که ممکن است تصویر در آن‌ها استفاده شده باشد
code_extensions = [".html", ".py", ".css", ".js"]

# پسوندهای معتبر عکس
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"]

# مرحله 1: پیدا کردن تمام فایل‌های تصویری
all_image_files = []
for root, _, files in os.walk(images_dir):
    for file in files:
        if os.path.splitext(file)[1].lower() in image_extensions:
            full_path = os.path.join(root, file)
            all_image_files.append(full_path)

# مرحله 2: پیدا کردن نام عکس‌های استفاده‌شده در کدها
used_images = set()
image_pattern = re.compile(r'/static/assets/images/([\w\-/]+?\.(?:jpg|jpeg|png|gif|svg|webp))', re.IGNORECASE)

for root, _, files in os.walk(project_root):
    for file in files:
        if os.path.splitext(file)[1].lower() in code_extensions:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = image_pattern.findall(content)
                    for match in matches:
                        used_images.add(os.path.basename(match).lower())
            except Exception as e:
                print(f"⚠️ خطا در خواندن {filepath}: {e}")

# مرحله 3: حذف عکس‌هایی که استفاده نشده‌اند
deleted_count = 0
for image_path in all_image_files:
    image_filename = os.path.basename(image_path).lower()
    if image_filename not in used_images:
        try:
            os.remove(image_path)
            print(f"❌ حذف شد: {image_filename}")
            deleted_count += 1
        except Exception as e:
            print(f"⚠️ خطا در حذف {image_filename}: {e}")

print(f"\n✅ تمام شد. {deleted_count} عکس بلااستفاده حذف شد.")
