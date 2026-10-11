# 🛡️ Mobile WAF 2 (WAF Gauntlet 100 Rounds)

- **Категория:** Web / Automation
- **Статус:** ✅ Решено
- **Флаг:** `kubstu{w4f_g4untl3t_100_r0unds_2c4ed716fd22}`

## Описание
> KeyVault Pro is an enterprise credential management platform built by SecureNest Solutions...
> Mobile WAF Gauntlet

## Решение
Испытание требовало автоматического прохождения 100 раундов тестирования Web Application Firewall.
Каждый раунд проверял устойчивость фильтров к обфусцированным атакам (SQLi, XSS, Path Traversal, RCE).
Был разработан скрипт `solve.py`, который:
1. Анализировал паттерны фильтрации текущего раунда.
2. Применял техники мутации пейлоадов (альтернативные кодировки, комментарии SQL `/**/`, конкатенацию строк, юникод-нормализацию).
3. Прошел 100 из 100 раундов и извлек валидный флаг.
