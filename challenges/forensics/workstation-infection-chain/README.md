# 💻 Workstation Infection Chain

- **Категория:** Forensics
- **Статус:** ✅ Решено
- **Флаг:** `KubSTU{InvoiceViewer.exe|198.51.100.23:4444|RuntimeBroker.exe}`

## Описание
> While the employee was distracted by a meeting, you obtained an image of their workstation. Your task is to reconstruct the infection chain, determine what exactly happened, and answer questions related to the incident.

## Решение
1. Восстановлен первоначальный вектор атаки (фишинговый файл `InvoiceViewer.exe`).
2. Найден сетевой артефакт соединения с C2-сервером атакующего: `198.51.100.23:4444`.
3. Определен закрепленный в автозагрузке вредоносный бинарник, маскирующийся под системный процесс Windows: `%APPDATA%\Microsoft\OneDrive\RuntimeBroker.exe`.
