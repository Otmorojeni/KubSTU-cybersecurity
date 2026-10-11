# 🛡️ KubSTU Cybersecurity CTF 2026 — Solutions & Writeups

Репозиторий решений и отчётов (writeups) команды **DemClub-200** с межвузовского хакатона по кибербезопасности **КубГТУ CTF 2026** (10–11 октября 2026).

<div align="center">

| 🏆 Место | 🎯 Счёт | 🏁 Решено заданий | 🏅 Статус команды |
| :---: | :---: | :---: | :---: |
| **#24** | **6948** | **45** | **DemClub-200 (STUDENTS)** |

**MVP команды:** `awesome` (Otmorojeni) *(закрыто большинство заданий во всех категориях)*

</div>

---

## 📊 Навигация по категориям и задачам

### 🔐 Cryptography & Math
| # | Задача | Статус | Флаг | Описание и техника |
| :-: | :--- | :-: | :--- | :--- |
| 1 | [01-decimal-stream](challenges/crypto/01-decimal-stream/README.md) | ✅ | `KubSTU{d3c1m4l_15_my_l4n6u4g3}` | Декодирование числового потока ASCII кодов |
| 2 | [02-rsa-out-of-the-box](challenges/crypto/02-rsa-out-of-the-box/README.md) | ✅ | `KubSTU{r54_ag41n_b47_1_lik3_17_aft3r_411_1t5_n0t_7ha7_h4rd}` | Факторизация модулей RSA без сохранения настроек |
| 3 | [03-caesar-cipher](challenges/crypto/03-caesar-cipher/README.md) | ✅ | `KubSTU{c43s4r_w0uld_b3_pr0ud}` | Классический шифр Цезаря со сдвигом |
| 4 | [04-aes-is-secure-right](challenges/crypto/04-aes-is-secure-right/README.md) | ✅ | `KubSTU{c3rt1f1c4t3_r3v0k3d}` | Эксплуатация логики отзыва сертификатов AES |
| 5 | [05-the-deterministic-fog](challenges/crypto/05-the-deterministic-fog/README.md) | ✅ | `KubSTU{lw3_574nd5_f0r_l0v3ly_w153_c4pyb4r4}` | Постквантовая LWE криптосистема, атака на детерминированный шум |
| 6 | [06-params-l-knapsack](challenges/crypto/06-params-l-knapsack/README.md) | ✅ | `KubSTU{y0u_n33d_70_6e_4_re41_d373ct1ve_7o_5o1v3_7h15}` | Рюкзачный шифр Меркла-Хеллмана, атака на решётки через LLL |
| 7 | [07-perelman-ricci-flow](challenges/crypto/07-perelman-ricci-flow/README.md) | ✅ | `KubSTU{45_a_m4773r_...}` | Восстановление кривой из каскада потоков Риччи |
| 8 | [08-curve-ball-ctf111](challenges/crypto/08-curve-ball-ctf111/README.md) | ✅ | `KubSTU{45_f0r_311ip71c_...}` | Дискретный логарифм на эллиптической кривой (Pohlig-Hellman, PARI/GP) |

### 🌐 Web & WAF
| # | Задача | Статус | Флаг | Описание и техника |
| :-: | :--- | :-: | :--- | :--- |
| 1 | [calculator-ssti](challenges/web/calculator/README.md) | ✅ | `kubstu{cl34rl1n3_t3mpl4t3_1nj3ct_983a0807}` | Server-Side Template Injection (SSTI) в Jinja2 через строковую подстановку |
| 2 | [cry-node-vm-escape](challenges/web/cry-node-vm-escape/README.md) | ✅ | `kubstu{vm_1s_n0t_a_s4ndb0x_pr0t0typ3_p0llut10n_2_rce}` | Побег из песочницы Node.js `vm` через Prototype Pollution в RCE |
| 3 | [mercury-market](challenges/web/mercury-market/README.md) | ✅ | `KubSTU{un10n_s3l3ct_pr0m0_100_p3rc3nt}` | SQLi в промокодах `PWN100`, байпас стоимости VIP-лота и ловушек |
| 4 | [mobile-waf](challenges/web/mobile-waf/README.md) | ✅ | `kubstu{w4f_g4untl3t_100_r0unds_2c4ed716fd22}` | Автоматизированный байпас 100 раундов WAF Gauntlet |
| 5 | [bankiro-telegram](challenges/web/bankiro-telegram/README.md) | ⏳ | *В процессе* | Telegram Mini App банкинг, анализ `tgWebAppData` и статуса CAPY+ |
| 6 | [vibecoding-php](challenges/web/vibecoding-php/README.md) | ⏳ | *В процессе* | PHP эксплойт обхода фильтрации путей |

### 🔍 Forensics & Incident Response
| # | Задача | Статус | Флаг | Описание и техника |
| :-: | :--- | :-: | :--- | :--- |
| 1 | [not-to-give-not-to-take](challenges/forensics/not-to-give-not-to-take/README.md) | ✅ | `KubSTU{local_headers_lie_central_directory_does_not}` | Восстановление оборванного ZIP-архива с Data Descriptors и битым Central Directory |
| 2 | [smart-building-modbus-ics](challenges/forensics/smart-building-modbus-ics/README.md) | ✅ | `KubSTU{modbus_echoes_keep_the_secret}` | Поиск скрытого канала в Modbus TCP ICS дампах сетевого трафика |
| 3 | [workstation-infection-chain](challenges/forensics/workstation-infection-chain/README.md) | ✅ | `KubSTU{InvoiceViewer.exe\|198.51.100.23:4444\|...}` | Реконструкция цепочки заражения: фишинг, C2 и маскировка RuntimeBroker |
| 4 | [last-export](challenges/forensics/last-export/README.md) | ✅ | `KubSTU{aU70p5y_D3l373d_P3_4nd_r3v3r53}` | Carving удалённого бинарника `sync_7D3.exe` из образа флешки |
| 5 | [heartbleed-tls-reassembly](challenges/forensics/heartbleed-tls-reassembly/README.md) | ✅ | `KubSTU{heartbleed_reassembled_the_private_key_and_tls_fell}` | Сборка закрытого RSA ключа из кучи Heartbleed и расшифровка TLS в Wireshark |
| 6 | [ctf-repo-git-leak](challenges/forensics/ctf-repo-git-leak/README.md) | ✅ | *Завершено* | Поиск утечек ключей в `git reflog` и висячих коммитах |
| 7 | [hydro-incident-triages](challenges/forensics/hydro-incident-triages/README.md) | ✅ | *Завершено (10/10)* | Комплексное расследование Medusa Locker (Joomla вебшелл, GPO, PS 4104) |
| 8 | [uav-gas-pipeline](challenges/forensics/uav-gas-pipeline/README.md) | ⏳ | *В процессе* | Анализ образа SD-карты разбившегося БПЛА, фильтрация decoy-флагов |

### ⚙️ Reverse Engineering
| # | Задача | Статус | Флаг | Описание и техника |
| :-: | :--- | :-: | :--- | :--- |
| 1 | [fw-risc](challenges/reverse/fw-risc/README.md) | ✅ | `KubSTU{tr4ps_4r3_th3_r34l_c0ntr0l_fl0w}` | Эмуляция прошивки RISC архитектуры LC-3 и разбор TRAP-векторов |
| 2 | [chronos](challenges/reverse/chronos/README.md) | ✅ | `KubSTU{k3y3d_by_1ts_0wn___t3xt_s3ct10n}` | Реверс Mach-O бинарника с самошифрованием через хеш секции `__text` |

### 🎨 Steganography & Hardware
| # | Задача | Статус | Флаг | Описание и техника |
| :-: | :--- | :-: | :--- | :--- |
| 1 | [color-illusion-bro-stego](challenges/stegano/color-illusion-bro-stego/README.md) | ✅ | *Завершено* | Анализ аномалий и знаков частотных всплесков в блоках $8\times 8$ 2D-DCT |
| 2 | [transmission-audio](challenges/stegano/transmission-audio/README.md) | ✅ | `kubstu{h34r_th3_pictur3_8a72}` | Извлечение спектрограммы скрытого текста из аудио `transmission.wav` |
| 3 | [last-chance-pdf](challenges/stegano/last-chance-pdf/README.md) | ✅ | `KubSTU{part1_f4k3_s1g_metadata_stitching_is_fun_abe8776b}` | Сшивка фрагментов метаданных XMP и потоков PDF |
| 4 | [madkid-sstv](challenges/stegano/madkid-sstv/README.md) | ✅ | *Завершено* | Декодирование аналогового сигнала любительского телевидения SSTV |

### 📦 Misc
| # | Задача | Статус | Флаг | Описание и техника |
| :-: | :--- | :-: | :--- | :--- |
| 1 | [subway-3-coin-runs](challenges/misc/subway-3-coin-runs/README.md) | ✅ | `kubstu{1t5_r3a1_subww3i}` | 24 видеозаписи Subway Surfers, количество монет = ASCII код символа |
| 2 | [matryoshka](challenges/misc/matryoshka/README.md) | ✅ | `kubstu{t3n_l4y3rs_d33p_991939c0}` | Автоматическая распаковка 10 уровней вложенных разноформатных архивов |
| 3 | [subway-2-temple](challenges/misc/subway-2-temple/README.md) | ⏳ | *В процессе* | Анализ NAL-юнитов H.265/HEVC и ловушек автора (`GROB-DECOY`) |

### 🎲 Blockchain & Web3
| # | Задача | Статус | Флаг | Описание и техника |
| :-: | :--- | :-: | :--- | :--- |
| 1 | [sepolia-casino](challenges/blockchain/sepolia-casino/README.md) | ✅ | `KubSTU{bad_randomness_same_tx}` | Эксплуатация уязвимости псевдослучайности (`block.timestamp` / `blockhash`) |

### 🗺️ OSINT
| # | Задача | Статус | Флаг | Описание и техника |
| :-: | :--- | :-: | :--- | :--- |
| 1 | [carsharing-krasnodar](challenges/osint/carsharing-krasnodar/README.md) | ⏳ | *В процессе* | Геолокация машины по фото в центре Краснодара через тайлы панорам |

---

## 💡 Топ интересных решений (Highlights)

### 1. [Not to give, not to take (Forensics)](challenges/forensics/not-to-give-not-to-take/README.md)
* **Проблема:** Файл архива аварийно оборвался при копировании: Central Directory полностью отсутствовал, а в локальных заголовках стоял флаг `0x0008` (Data Descriptor), обнуляющий размеры файлов. Стандартный 7-Zip выдавал ошибку повреждения.
* **Решение:** Написали скрипт [`repair_and_extract.py`](challenges/forensics/not-to-give-not-to-take/repair_and_extract.py), который потоково распарсил локальные блоки, вычислил границы сжатых потоков по маркерам `PK\x07\x08`, заново собрал Central Directory с валидными смещениями и EOCD-записью, вытащив заветный `secret.txt`. Флаг был сдан за 37 минут до конца соревнований!

### 2. [Shift-Left, Brain-Right / Mercury Market (Web)](challenges/web/mercury-market/README.md)
* **Проблема:** Магазин игровых лотов с ловушками-приманками (fake flags в комментариях, `.env.example`, `.map` файлах). На балансе 500 ₽, а VIP-лот стоит 250 000 ₽.
* **Решение:** Нашли точку инъекции в поле применения промокодов (`' UNION SELECT 100 -- -`), переопределили скидку до 100%, оформили заказ за 0 ₽ и забрали настоящий закрытый конфиг продавца с флагом.

### 3. [Subway 3 (Misc)](challenges/misc/subway-3-coin-runs/README.md)
* **Проблема:** Дано 24 MP4-видео с геймплеем Subway Surfers.
* **Решение:** Заметили, что дублирующиеся видео в точности совпадают с повторяющимися буквами в префиксе `kubstu{`. Число собранных монет в каждом забеге в точности равнялось десятичному ASCII-коду символа флага.

### 4. [The Deterministic Fog (Crypto)](challenges/crypto/05-the-deterministic-fog/README.md)
* **Проблема:** Постквантовая криптосистема на основе Learning With Errors (LWE).
* **Решение:** Генератор шума оказался детерминированным. По короткому диагностическому следу калибровки полностью восстановили состояние генератора, вычли векторы шума и решили линейную систему уравнений над конечным полем.

### 5. [Зашифрованные передачи L (Crypto)](challenges/crypto/06-params-l-knapsack/README.md)
* **Проблема:** Блоки текста зашифрованы суммированием элементов открытого ключа (рюкзак Меркла-Хеллмана).
* **Решение:** Построили решётку Клоза размерности $(n+1) \times (n+1)$ и с помощью LLL-редукции (алгоритм Ленстры–Ленстры–Ловаса) нашли кратчайший неколлинеарный вектор с координатами $\{0, 1\}$, мгновенно восстановив сообщение.

---

## 🛠️ Использованный инструментарий
- **Языки:** Python 3.12+, Solidity 0.8.28, PARI/GP (GP64), Bash.
- **Криптоанализ & Математика:** `pycryptodome`, `gmpy2`, `sympy`, PARI/GP (`elllog`, `ellorder`, `factor`), LLL Lattice reduction.
- **Форензика & Сеть:** Wireshark, TShark, Autopsy, Volatility, struct/zlib бинарные парсеры, `qpdf`, `exiftool`.
- **Реверс:** IDA Pro, Ghidra, radare2, objdump, LC-3 custom emulators.
- **Веб-эксплойты:** Requests, BeautifulSoup, Burp Suite, Prototype Pollution гаджеты, SSTI payloads.

---

## 👥 Команда DemClub-200
* `awesome` (Otmorojeni) — Lead Solver / MVP
* `zan_ezz`
* `mak_ros`
* `cikapu_ka`
