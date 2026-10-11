# 💔 Heartbleed & TLS Private Key Reassembly

- **Категория:** Forensics / Network
- **Статус:** ✅ Решено
- **Флаг:** `KubSTU{heartbleed_reassembled_the_private_key_and_tls_fell}`

## Описание
> During the incident at xxx.xxx.lab, the attacker allegedly exploited some CVE. The response team was left with a network dump and heap memory fragments. Your goal is to reconstruct the chain of compromise and extract the flag.

## Решение
1. В дампах памяти обнаружена утечка приватного ключа сервера через уязвимость OpenSSL Heartbleed (CVE-2014-0160).
2. Из фрагментов кучи реконструирована ASN.1 структура закрытого RSA ключа.
3. Закрытый ключ импортирован в Wireshark для расшифровки сессионных ключей TLS в сетевом дампе.
4. Расшифрован защищенный HTTPS-запрос с получением флага.
