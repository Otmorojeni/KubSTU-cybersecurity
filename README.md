# 🚩 KubSTU CTF 2026 Autumn Workspace

Рабочее пространство и база знаний для участия в соревновании по информационной безопасности **KubSTU CTF 2026 Autumn** (Jeopardy).

---

## ℹ️ Информация о хакатоне / соревновании

| Параметр | Значение |
| :--- | :--- |
| **Событие** | **KubSTU CTF 2026 Autumn** |
| **Платформа** | [ctf.kubstu-ctf.ru/games/3](https://ctf.kubstu-ctf.ru/games/3) |
| **Старт** | **10 октября 2026 г. в 10:00:00 (МСК)** |
| **Финиш** | **11 октября 2026 г. в 16:00:00 (МСК)** |
| **Длительность** | **30 часов нон-стоп** |
| **Формат** | **Jeopardy (Task-Based)**: решаем задачи, сдаем флаги |
| **Скоринг** | **Динамический** (чем меньше команд решило таск, тем выше его стоимость) |
| **Лимит команды** | До 5 человек |
| **Треки / Категории** | **6 категорий**, **50+ задач**: `Web`, `Crypto`, `Forensics`, `OSINT`, `Stegano`, `Misc` |
| **Зачеты** | **Students** (студенческий) и **Open** (общий). Единый скорборд на CTFtime |

### 🎓 Организаторы и партнеры
- **Организатор:** [Кубанский государственный технологический университет (КубГТУ)](https://kubstu.ru), Факультет информационных технологий и кибербезопасности (**ФИТК**), команда **Capybaras**.
- **Генеральные партнеры:**
  - **CyberCamp** ([Инфосистемы Джет](https://t.me/jetcybercamp)) — призовой фонд студенческого зачета.
  - **Standoff 365** ([Positive Technologies](https://standoff365.com)) — призовой фонд общего зачета (Open).
  - **Бастион** ([bastion-tech.ru](https://bastion-tech.ru)) — призовой фонд студенческого зачета.
- **Партнеры:** **Hackadvisor.io** (отзывы на Bug Bounty программы).

### 📞 Контакты и ссылки
- **Официальный сайт:** [kubstu-ctf.ru](https://kubstu-ctf.ru)
- **Telegram канал:** [@kubCTF](https://t.me/kubCTF)
- **Чат участников:** [t.me/+aBjfygkLWRcwZDMy](https://t.me/+aBjfygkLWRcwZDMy)
- **Email оргкомитета:** `ctf@kubstu.ru`

---

## 🧰 Каталог скилов проекта (Skills Catalog)

Все специализированные скилы скопированы и подготовлены в папке [`skills/`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills) и зарегистрированы для агента в [`.agent/skills/`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/.agent/skills).

### 1. Web Exploitation & Security
- [`backend-security-coder`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/backend-security-coder/SKILL.md) — анализ серверных уязвимостей (SQLi, IDOR, SSRF, command injection).
- [`frontend-security-coder`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/frontend-security-coder/SKILL.md) — поиск клиентских уязвимостей, DOM clobbering, CSP обходы.
- [`frontend-mobile-security-xss-scan`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/frontend-mobile-security-xss-scan/SKILL.md) — поиск и эксплуатация Cross-Site Scripting (XSS).
- [`auth-implementation-patterns`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/auth-implementation-patterns/SKILL.md) — аудит JWT, OAuth2, сессий, cookies, обход авторизации.
- [`security-auditor`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/security-auditor/SKILL.md) — комплексный аудит уязвимостей по OWASP Top 10.
- [`security-scanning-security-sast`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/security-scanning-security-sast/SKILL.md) — статический анализ исходного кода сервисов.

### 2. Cryptography
- [`ctf-crypto`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/ctf-crypto/SKILL.md) — чек-листы и атаки на RSA, AES (ECB/CBC/Padding Oracle), Diffie-Hellman, PRNG/MT19937, классические шифры, скрипты на Python/SageMath.
- [`solidity-security`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/solidity-security/SKILL.md) — аудит смарт-контрактов (Reentrancy, overflow, Web3 challenges).

### 3. Forensics & Network Analysis
- [`memory-forensics`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/memory-forensics/SKILL.md) — анализ дампов оперативной памяти с помощью Volatility, извлечение процессов и ключей.
- [`protocol-reverse-engineering`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/protocol-reverse-engineering/SKILL.md) — разбор сетевых дампов PCAP, Wireshark, реверс кастомных протоколов.
- [`malware-analyst`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/malware-analyst/SKILL.md) — статический и динамический анализ вредоносных вложений, распаковка.

### 4. Steganography
- [`ctf-steganography`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/ctf-steganography/SKILL.md) — анализ LSB (zsteg, StegSolve), steghide, починка IHDR/CRC в PNG, спектрограммы звука (Sonic Visualiser), полиглоты.

### 5. OSINT
- [`ctf-osint`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/ctf-osint/SKILL.md) — методики геолокации, реверс поиска по картинкам, поиск по никнеймам/почтам, git-форензика, веб-архивы.

### 6. Reverse Engineering & Binary Exploitation
- [`reverse-engineer`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/reverse-engineer/SKILL.md) — реверс бинарников, декомпиляция (Ghidra, IDA Pro, radare2), angr, pwntools.
- [`binary-analysis-patterns`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/binary-analysis-patterns/SKILL.md) — паттерны разбора скомпилированного кода и структур.
- [`anti-reversing-techniques`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/anti-reversing-techniques/SKILL.md) — обход антиотладки (anti-debugging, ptrace, obfuscation).
- [`firmware-analyst`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/firmware-analyst/SKILL.md) — распаковка и исследование прошивок (binwalk, squashfs).

### 7. Скриптинг, отладка и автоматизация (Misc & Solvers)
- [`python-pro`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/python-pro/SKILL.md) — написание быстрых солверов на Python (pwntools, requests, z3-solver, pycryptodome).
- [`bash-pro`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/bash-pro/SKILL.md) — CLI конвейеры, bash-скрипты, strings, grep, xxd, hexdump.
- [`c-pro`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/c-pro/SKILL.md) — разбор низкоуровневых исходников на Си.
- [`debugging-strategies`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/debugging-strategies/SKILL.md) и [`error-detective`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/error-detective/SKILL.md) — системная локализация багов.
- [`network-engineer`](file:///c:/Users/maksi/OneDrive/Рабочий%20стол/otmorojeni/KubSTU-cybersecurity/skills/network-engineer/SKILL.md) — сетевая топология, маршрутизация, DNS, сертификаты.

---

## 📁 Рекомендуемая структура решений

Для организованной работы во время хакатона создаем папки под категории:
```
KubSTU-cybersecurity/
├── challenges/
│   ├── web/
│   ├── crypto/
│   ├── forensics/
│   ├── osint/
│   ├── stegano/
│   └── misc/
├── skills/               # Папка со всеми скилами
├── .agent/skills/        # Системные скилы для AI ассистента
└── README.md
```
