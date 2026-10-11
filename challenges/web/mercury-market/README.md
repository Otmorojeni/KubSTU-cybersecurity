# 🛒 Game SHOP / Mercury Market (Shift-Left, Brain-Right)

- **Категория:** Web (236 pts)
- **Статус:** ✅ Решено
- **Флаг:** `KubSTU{un10n_s3l3ct_pr0m0_100_p3rc3nt}`

## Описание
> Game SHOP
> http://159.194.250.157:8080/ http://45.153.189.92:8080/ http://155.212.216.201:8080/

## Анализ и Решение
Сервис представляет собой интернет-магазин игровых предметов и VIP-аккаунтов. В магазине продавался закрытый лот за 250 000 ₽: «Closed access: Mercury Market seller panel».
Начальный баланс пользователя составлял 500 ₽.

### Авторские ловушки (Red Herrings):
Автор заложил множество фейковых флагов для отсева автоматических сканеров:
- Заголовок `X-Mercury-Notice` и HTML-комментарии: `KubSTU{m1rr0r_d3c0y_n0t_th3_r34l_fl4g}`
- Файл `/.env.example`: `KubSTU{3nv_f1l3_w4s_n3v3r_th3_fl4g}`
- Карта скриптов `/static/js/mk.js.map`: `KubSTU{s0urc3m4p_l34k_w4s_4_tr4p}`
- Комментарии в `/static/js/mk.js`: `KubSTU{d3v_byp4ss_l3ft_1n_pr0d}`

### Эксплуатация уязвимости:
В обработчике формы применения промокодов была обнаружена SQL-инъекция:
```sql
SELECT discount_percent FROM promo_codes WHERE code = '{user_input}'
```
Внедрив пейлоад:
```text
' UNION SELECT 100 -- -
```
удалось применить 100% скидку к заказу на VIP-панель. Окончательная стоимость составила 0.00 ₽. Заказ успешно завершился, и в описании приобретённого товара («Goods from the seller») отобразился реальный флаг:
`KubSTU{un10n_s3l3ct_pr0m0_100_p3rc3nt}`
