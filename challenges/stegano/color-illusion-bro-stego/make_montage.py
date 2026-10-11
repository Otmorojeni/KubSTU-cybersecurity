import os, glob
from PIL import Image, ImageDraw, ImageFont

def make_montage(folder, output_img, cols=6):
    files = sorted(glob.glob(os.path.join(folder, '*.jpg')))
    if not files:
        print('No files in', folder)
        return
    
    tile_w, tile_h = 256, 256
    rows = (len(files) + cols - 1) // cols
    
    montage = Image.new('RGB', (cols * tile_w, rows * tile_h), color=(0, 0, 0))
    draw = ImageDraw.Draw(montage)
    
    for idx, f in enumerate(files):
        try:
            im = Image.open(f)
            r = idx // cols
            c = idx % cols
            x = c * tile_w
            y = r * tile_h
            montage.paste(im, (x, y))
            
            # Label with basename (lat_lon)
            base = os.path.basename(f)
            parts = base.split('_')
            label = f"{parts[0]}_{parts[1]}" if len(parts) >= 2 else base[:15]
            draw.text((x + 5, y + 5), f"{idx}: {label}", fill=(255, 255, 0))
        except Exception as e:
            pass
            
    montage.save(output_img, quality=85)
    print(f'Saved montage {output_img} with {len(files)} tiles')

if __name__ == '__main__':
    make_montage('kirova_tiles', 'montage_kirova.jpg')
