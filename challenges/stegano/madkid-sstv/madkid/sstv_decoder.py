import wave
import struct
import math
from PIL import Image

def decode_sstv(wav_path, output_path="sstv_output.png"):
    print(f"[+] Открываю файл: {wav_path}")
    with wave.open(wav_path, 'rb') as w:
        params = w.getparams()
        channels = params.nchannels
        sampwidth = params.sampwidth
        framerate = params.framerate  # Исправлено здесь
        nframes = params.nframes
        
        if channels != 1:
            print("[-] Ошибка: Нужен МОНО файл (1 канал). Перекодируйте его через ffmpeg!")
            return

        raw_data = w.readframes(nframes)
        
    print(f"[+] Частота: {framerate} Гц, Всего фреймов: {nframes}")
    
    # Читаем амплитуды звука
    fmt = {1: 'b', 2: 'h', 4: 'i'}[sampwidth]
    samples = [f[0] for f in struct.iter_unpack(fmt, raw_data)]
    
    print("[+] Декодирую частоты сигнала...")
    freqs = []
    last_zero = 0
    for i in range(1, len(samples)):
        if (samples[i-1] < 0 and samples[i] >= 0) or (samples[i-1] > 0 and samples[i] <= 0):
            period = i - last_zero
            if period > 0:
                freq = framerate / (period * 2)
                freqs.append(freq)
            last_zero = i

    # Стандартный размер для большинства тасков (Martin 1 / Scottie)
    width = 320
    height = 256
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    
    print(f"[+] Создаю изображение {width}x{height}...")
    
    idx = 0
    for y in range(height):
        for x in range(width):
            if idx < len(freqs):
                f = freqs[idx]
                # Маппинг частоты SSTV (1500-2300 Гц) в цвет (0-255)
                val = int(max(0, min(255, (f - 1500) * 255 / 800)))
                pixels[x, y] = (val, val, val)
                idx += 1

    img.save(output_path)
    print(f"[+] Готово! Результат сохранен в {output_path}")

if __name__ == "__main__":
    import sys
    file_to_decode = sys.argv[1] if len(sys.argv) > 1 else "fixed_sound.wav"
    decode_sstv(file_to_decode)
