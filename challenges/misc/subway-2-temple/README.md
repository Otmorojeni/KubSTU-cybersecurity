# 🏃 Subway 2 (The continuation of the legendary task)

- **Категория:** Misc / Video Stego
- **Статус:** ⏳ В процессе

## Описание
> The continuation of the legendary task Do you see the flag in its open form?
> temple.mp4

## Анализ
В видеопотоке H.265/HEVC и метаданных обнаружены намеренные ловушки автора:
- Бокс `uuid` в MP4 с текстом дразнилки `GROBTAUNT`.
- SEI NAL с фейковым флагом `GROB-DECOY v0` (`KubSTU{l00k_harder_...}`).
- На спектрограмме аудиопотока — маркер `NOT-THE-KEY` на частоте 9–11.5 кГц.
