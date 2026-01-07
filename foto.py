import os
import sys
from PIL import Image


FOTO_WIDTH = 354  
FOTO_HEIGHT = 472 
A4_WIDTH_PX = 2480
A4_HEIGHT_PX = 3508


def cm_to_px(cm):
return int(cm * 300 / 2.54)

SPACING_CM = 0.2
MARGIN_CM = 0.5


MARGIN_TOP = cm_to_px(MARGIN_CM)
MARGIN_LEFT = cm_to_px(MARGIN_CM)
SPACING_X = cm_to_px(SPACING_CM)
SPACING_Y = cm_to_px(SPACING_CM)


SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png')


def crop_to_3x4_ratio(image):
    """
    Memotong gambar ke rasio 3:4 dengan fokus di tengah.
    """
    width, height = image.size
    target_ratio = 3 / 4 
    current_ratio = width / height
    
    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        right = left + new_width
        top = 0
        bottom = height
    else:
        new_height = int(width / target_ratio)
        left = 0
        right = width
        top = (height - new_height) // 2
        bottom = top + new_height
    
    return image.crop((left, top, right, bottom))


def process_image(image_path):
    """
    Memproses gambar: crop ke rasio 3:4 dan resize ke 354x472 piksel.
    """
    try:
        with Image.open(image_path) as img:
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            

            cropped = crop_to_3x4_ratio(img)
            
            resized = cropped.resize((FOTO_WIDTH, FOTO_HEIGHT), Image.Resampling.LANCZOS)
            
            return resized
    except Exception as e:
        print(f"[!] Gagal memproses {image_path}: {e}")
        return None


def find_all_images(root_dir):
    """
    Mencari semua file gambar secara rekursif di dalam folder.
    """
    images = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                full_path = os.path.join(dirpath, filename)
                images.append(full_path)
    
    
    images.sort()
    return images


def calculate_layout():
    """
    Menghitung berapa banyak foto yang bisa muat dalam satu halaman A4.
    """
 
    available_width = A4_WIDTH_PX - (2 * MARGIN_LEFT)
    available_height = A4_HEIGHT_PX - (2 * MARGIN_TOP)
    
  
    cols = (available_width + SPACING_X) // (FOTO_WIDTH + SPACING_X)
    rows = (available_height + SPACING_Y) // (FOTO_HEIGHT + SPACING_Y)
    
    return int(cols), int(rows)


def create_a4_page_with_photos(photos, start_index, cols, rows):
    """
    Membuat satu halaman A4 dengan foto-foto yang telah diproses.
    Returns: PIL Image dari halaman A4
    """
  
    page = Image.new('RGB', (A4_WIDTH_PX, A4_HEIGHT_PX), 'white')
    
    photos_per_page = cols * rows
    photos_placed = 0
    
    for i in range(photos_per_page):
        photo_index = start_index + i
        if photo_index >= len(photos):
            break
        
        photo = photos[photo_index]
        if photo is None:
            continue
        
    
        row = i // cols
        col = i % cols
        
        x = MARGIN_LEFT + col * (FOTO_WIDTH + SPACING_X)
        y = MARGIN_TOP + row * (FOTO_HEIGHT + SPACING_Y)
        
     
        page.paste(photo, (x, y))
        photos_placed += 1
    
    return page, photos_placed


def create_pdf(processed_photos, output_path):
    """
    Membuat file PDF dari foto-foto yang telah diproses.
    """
    if not processed_photos:
        print("[X] Tidak ada foto yang berhasil diproses!")
        return None
    

    cols, rows = calculate_layout()
    photos_per_page = cols * rows
    
    print(f"[*] Layout: {cols} kolom x {rows} baris = {photos_per_page} foto per halaman")
    
 
    pages = []
    current_index = 0
    
    while current_index < len(processed_photos):
        page, placed = create_a4_page_with_photos(processed_photos, current_index, cols, rows)
        pages.append(page)
        current_index += photos_per_page
        print(f"[*] Halaman {len(pages)} dibuat dengan {placed} foto")
    

    if pages:
        pages[0].save(
            output_path,
            'PDF',
            resolution=300.0,
            save_all=True,
            append_images=pages[1:] if len(pages) > 1 else []
        )
        return output_path
    
    return None


def main():
    if len(sys.argv) != 2:
        print("[X] Penggunaan: python foto.py <path_ke_folder>")
        print("    Contoh: python foto.py C:\\Users\\Foto")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    

    if not os.path.isdir(root_dir):
        print(f"[X] Folder tidak ditemukan: {root_dir}")
        sys.exit(1)
    
    print(f"[*] Mencari gambar di: {root_dir}")
    print("=" * 60)
    
    
    image_paths = find_all_images(root_dir)
    
    if not image_paths:
        print("[X] Tidak ada file gambar (.jpg, .jpeg, .png) yang ditemukan!")
        sys.exit(1)
    
    print(f"[*] Ditemukan {len(image_paths)} gambar")
    print("-" * 60)
    
 
    processed_photos = []
    for i, path in enumerate(image_paths, 1):
        print(f"[{i}/{len(image_paths)}] Memproses: {os.path.basename(path)}")
        processed = process_image(path)
        if processed:
            processed_photos.append(processed)
    
    print("-" * 60)
    print(f"[OK] {len(processed_photos)} dari {len(image_paths)} gambar berhasil diproses")
    print("-" * 60)
    
   
    output_filename = "Foto_3x4_Final.pdf"
    output_path = os.path.join(root_dir, output_filename)
    
 
    print("[*] Membuat file PDF...")
    result_path = create_pdf(processed_photos, output_path)
    
    if result_path:
        abs_path = os.path.abspath(result_path)
        print("=" * 60)
        print("[SELESAI]")
        print(f"File PDF disimpan di:")
        print(f"   {abs_path}")
        print("=" * 60)
    else:
        print("[X] Gagal membuat file PDF!")
        sys.exit(1)


if __name__ == "__main__":
    main()
