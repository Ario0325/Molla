# cleanup_project.py

import os
import sys
import shutil
from PIL import Image

# ——————————————————————————————————————————————————————
# ۱. تنظیم BASE_DIR (شبیه settings.py جنگو)
# ریشه‌ی پروژه همان مسیری است که این فایل در آن قرار دارد:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# محل پوشه‌ی استاتیک تصاویر
IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'assets', 'images')

# پسوندهای مجاز برای بهینه‌سازی تصاویر
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# حداقل کیفیت (برای JPEG) – هرچه این عدد کمتر باشد، حجم کمتر ولی کیفیت پایین‌تر
JPEG_QUALITY = 80

# ——————————————————————————————————————————————————————
# ۲. تابع حذف تمامی پوشه‌های __pycache__ و فایل‌های *.pyc
def remove_pycache_and_pyc(root_path):
    removed_count = 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        # حذف پوشه‌های __pycache__
        if '__pycache__' in dirnames:
            cache_dir = os.path.join(dirpath, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                print(f"❌ پوشه حذف شد: {cache_dir}")
                removed_count += 1
            except Exception as e:
                print(f"⚠️ خطا در حذف {cache_dir}: {e}")

        # حذف فایل‌های .pyc
        for file in filenames:
            if file.endswith('.pyc'):
                file_path = os.path.join(dirpath, file)
                try:
                    os.remove(file_path)
                    print(f"❌ فایل حذف شد: {file_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️ خطا در حذف {file_path}: {e}")

    print(f"\n✅ عملیات حذف __pycache__/.pyc تمام شد. تعداد حذف‌شده: {removed_count}\n")


# ——————————————————————————————————————————————————————
# ۳. تابع برای بهینه‌سازی (فشرده‌سازی) تصاویر در پوشه‌ی IMAGES_DIR
def optimize_images(images_dir):
    if not os.path.isdir(images_dir):
        print(f"❌ پوشه تصاویر پیدا نشد: {images_dir}")
        return

    optimized_count = 0
    for dirpath, dirnames, filenames in os.walk(images_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in IMAGE_EXTENSIONS:
                continue

            img_path = os.path.join(dirpath, filename)
            try:
                # باز کردن تصویر
                img = Image.open(img_path)

                # برای JPEG:
                if ext in {'.jpg', '.jpeg'}:
                    img.save(img_path, format='JPEG', optimize=True, quality=JPEG_QUALITY)

                # برای PNG:
                elif ext == '.png':
                    img.save(img_path, format='PNG', optimize=True)

                optimized_count += 1
                print(f"🔧 بهینه‌سازی شد: {img_path}")

            except Exception as e:
                print(f"⚠️ خطا در بهینه‌سازی {img_path}: {e}")
                continue

    print(f"\n✅ عملیات بهینه‌سازی تصاویر تمام شد. تعداد بهینه‌شده: {optimized_count}\n")


# ——————————————————————————————————————————————————————
# ۴. تابع اصلی که دو مرحله را اجرا می‌کند
def main():
    print("\n🔹 شروع حذف __pycache__ و فایل‌های .pyc ...\n")
    remove_pycache_and_pyc(BASE_DIR)

    print("\n🔹 شروع بهینه‌سازی تصاویر ...\n")
    optimize_images(IMAGES_DIR)

    print("🏁 همهٔ عملیات به پایان رسید. حجم پروژه کاهش خواهد یافت!\n")

# اجرای مستقیم اسکریپت
if __name__ == '__main__':
    main()
