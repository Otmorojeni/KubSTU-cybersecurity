# 🏦 Bankiro (Telegram Web App Banking)

- **Категория:** Web / Telegram Mini Apps
- **Статус:** ⏳ В процессе / Не завершено
- **Цель:** `t.me/bankiro2_bot` (`bank2.kubstu-ctf.ru`)

## Описание
> We are a modern bank. We have decided to integrate into Telegram. This is safe, you see.
> t.me/bankiro2_bot

## Исследование
Интерфейс мобильного банка развернут в виде Telegram Mini App.
В магазине доступна покупка флага за виртуальную валюту, однако для совершения покупки требуется привилегированный статус **CAPY+**.
Было выполнено внедрение кастомного UserScript в веб-клиент Telegram (`web.telegram.org/k/`) для изучения трафика между фреймом и бэкендом, а также реверс параметров `tgWebAppData` и хеша подписи сессии. До окончания таймера соревнований подделать авторизационную подпись не удалось.
