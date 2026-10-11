# 💾 Last Export (Восстановление удаленного PE файла)

- **Категория:** Forensics
- **Статус:** ✅ Решено
- **Флаг:** `KubSTU{aU70p5y_D3l373d_P3_4nd_r3v3r53}`

## Описание
> One of the temporary exports has disappeared from the portable storage device in the materials preparation department. The employee claims that he managed to copy the results before leaving and cleared the workspace, but the transfer log appears to be incomplete.

## Решение
1. Анализ образа файловой системы `last_export.img` через Autopsy / TestDisk / binwalk.
2. Carving удаленного исполняемого файла `sync_7D3.exe`.
3. Статический и динамический реверс алгоритма шифрования утилиты и получение флага.
