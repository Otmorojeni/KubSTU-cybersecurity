# 📄 Last Chance / Cave (PDF Forensic Stegano)

- **Категория:** Steganography / Forensics
- **Статус:** ✅ Решено
- **Флаг:** `KubSTU{part1_f4k3_s1g_metadata_stitching_is_fun_abe8776b}`

## Описание
> Imagine you’re wandering through a cave, without any light. Or maybe you’re an explorer? Flag format: KubSTU{...}

## Решение
1. Парсинг структуры файла `last chance.pdf` через `qpdf`, `pdfdetach` и Python.
2. Анализ скрытых потоков данных (FlateDecode), потоков метаданных XMP и подписей.
3. Сшивка фрагментов метаданных и извлечение валидного флага.
