import re

KEY_WORDS = ('</', '<', '>', 'img', 'meta', 'hr', 'html', 'title', 'head', 'body', 'table', 'thead', 'tr', 'td', 'h1',
             'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'lang', 'charset', 'style', 'bgcolor', 'align', 'bordercolor', 'border',
             'width', "'", '`', '"', '=', '$')  # IF NOT EXISTS WE USE RegEx to find "[A-Za-z0-9- ]+" OR "[^<>''""]+"
phase_counter = 0


def get_rule(current_expression_part: str, last_stack_rule: str) -> list:
    case = (last_stack_rule, current_expression_part,)
    # перелік правил (ключ: значення)
    answer = {
        ("<вхідний тег>", "<",): ["<", "<тег>"],
        ("<cписок елементів>", "<",): ["<елемент>", "<список елементів>", ],
        ("<cписок елементів>", "</",): ["ε", ],
        ("<закритий тег>", "</",): ["</", "<ім'я подвійного тегу>", ">"],
        ("<елемент>", "<",): ["<вхідний тег>", ],
        ("<перелік атрибутів>", ">",): ["ε", ],
        ("<подвійний тег>", "</",): ["<закритий тег>", ],
        ("<подвійний тег>", "<",): ["<текст>", ],
        ("<текст>", "<"): ["<вхідний тег>"],

        ("<тег>", "img",): ["<одинарний тег>", ],
        ("<одинарний тег>", "img",): ["<ім'я одинарного тегу>", "<перелік атрибутів>", ">", ],
        ("<ім'я одинарного тегу>", "img",): ["img", ],

        ("<тег>", "meta",): ["<одинарний тег>", ],
        ("<одинарний тег>", "meta",): ["<ім'я одинарного тегу>", "<перелік атрибутів>", ],
        ("<ім'я одинарного тегу>", "meta",): ["meta", ],

        ("<тег>", "hr",): ["<одинарний тег>", ],
        ("<одинарний тег>", "hr",): ["<ім'я одинарного тегу>", "<перелік атрибутів>", ],
        ("<ім'я одинарного тегу>", "hr",): ["hr", ],

        ("<тег>", "html",): ["<подвійний тег>", ],
        ("<подвійний тег>", "html",): ["<відкритий тег>", ],
        ("<відкритий тег>", "html",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">",  "<текст>", "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "html",): ["html", ],

        ("<тег>", "head",): ["<подвійний тег>", ],
        ("<подвійний тег>", "head",): ["<відкритий тег>", ],
        ("<відкритий тег>", "head",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">",  "<текст>", "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "head",): ["head", ],

        ("<тег>", "body",): ["<подвійний тег>", ],
        ("<подвійний тег>", "body",): ["<відкритий тег>", ],
        ("<відкритий тег>", "body",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">",  "<текст>", "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "body",): ["body", ],

        ("<тег>", "table",): ["<подвійний тег>", ],
        ("<подвійний тег>", "table",): ["<відкритий тег>", ],
        ("<відкритий тег>", "table",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">",  "<текст>", "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "table",): ["table", ],

        ("<тег>", "thead",): ["<подвійний тег>", ],
        ("<подвійний тег>", "thead",): ["<відкритий тег>", ],
        ("<відкритий тег>", "thead",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">",  "<текст>", "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "thead",): ["thead", ],

        ("<тег>", "tr",): ["<подвійний тег>", ],
        ("<подвійний тег>", "tr",): ["<відкритий тег>", ],
        ("<відкритий тег>", "tr",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">",  "<текст>", "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "tr",): ["tr", ],

        ("<тег>", "th",): ["<подвійний тег>", ],
        ("<подвійний тег>", "th",): ["<відкритий тег>", ],
        ("<відкритий тег>", "th",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">", "<текст>",
                                     "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "th",): ["th", ],

        ("<тег>", "td",): ["<подвійний тег>", ],
        ("<подвійний тег>", "td",): ["<відкритий тег>", ],
        ("<відкритий тег>", "td",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">",  "<текст>", "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "td",): ["td", ],

        ("<тег>", "h1",): ["<подвійний тег>", ],
        ("<подвійний тег>", "h1",): ["<відкритий тег>", ],
        ("<відкритий тег>", "h1",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">", "<текст>",  "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "h1",): ["h1", ],

        ("<тег>", "h2",): ["<подвійний тег>", ],
        ("<подвійний тег>", "h2",): ["<відкритий тег>", ],
        ("<відкритий тег>", "h2",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">", "<текст>",  "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "h2",): ["h2", ],

        ("<тег>", "title",): ["<подвійний тег>", ],
        ("<подвійний тег>", "title",): ["<відкритий тег>", ],
        ("<відкритий тег>", "title",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">", "<текст>", "<подвійний тег>",],
        ("<ім'я подвійного тегу>", "title",): ["title", ],

        ("<тег>", "p",): ["<подвійний тег>", ],
        ("<подвійний тег>", "p",): ["<відкритий тег>", ],
        ("<відкритий тег>", "p",): ["<ім'я подвійного тегу>", "<перелік атрибутів>", ">", "<текст>", "<подвійний тег>", ],
        ("<ім'я подвійного тегу>", "p",): ["p", ],

        ("<перелік атрибутів>", "src",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "src",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "src",): ["src", ],

        ("<перелік атрибутів>", "lang",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "lang",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "lang",): ["lang", ],

        ("<перелік атрибутів>", "charset",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "charset",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "charset",): ["charset", ],

        ("<перелік атрибутів>", "style",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "style",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "style",): ["style", ],

        ("<перелік атрибутів>", "bgcolor",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "bgcolor",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "bgcolor",): ["bgcolor", ],

        ("<перелік атрибутів>", "align",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "align",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "align",): ["align", ],

        ("<перелік атрибутів>", "border",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "border",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "border",): ["border", ],

        ("<перелік атрибутів>", "bordercolor",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "bordercolor",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "bordercolor",): ["bordercolor", ],

        ("<перелік атрибутів>", "width",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "width",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "width",): ["width", ],

        ("<перелік атрибутів>", "height",): ["<визначений атрибут>", "<перелік атрибутів>", ],
        ("<визначений атрибут>", "height",): ["<ім'я атрибуту>", "=", "<значення атрибуту>", ],
        ("<ім'я атрибуту>", "height",): ["height", ],

        ("<значення атрибуту>", "'",): ["'", "<значення>", "'", ],
        ("<значення атрибуту>", '"',): ['"', "<значення>", '"', ],

        ("<список елементів>", "$",): ["ε", ],
        ("<закритий тег>", "$",): ["ε", ],
        ("<перелік атрибутів>", "$",): ["ε", ],
    }.get(case, ["exception"])
    if "exception" in answer:
        # match current_expression_part as [A-Za-z0-9- ]+ and [^<>''""]+
        element_pattern = '[^<>''""]+'
        text_pattern = '[A-Za-z0-9-. ]+'
        element = re.search(element_pattern, current_expression_part)
        text = re.search(text_pattern, current_expression_part)
        if last_stack_rule == '<список елементів>' and element:
            answer = ["<елемент>", "<список елементів>", ]
        elif last_stack_rule == '<елемент>' and element:
            answer = ["<текст>", ]
        elif last_stack_rule == '<текст>' and element:
            answer = [element.group(), ]
        elif last_stack_rule == '<значення>' and text:
            answer = [text.group(), ]
    return answer


# TODO замінити на аналогічну функцію з lexis.py, яка працює краще
def divide_into_parts(expression: str) -> list:
    # input 'id+id*id$'
    # output [ 'id', '+', 'id', '*', 'id', '$' ]
    # перевіряємо символ $ в кінці
    expression += '$' if expression[-1] != '$' else ''
    divided_expression = []

    # ділимо вираз на частини
    while expression != '$':
        if expression[0] == ' ':
            expression = expression[1:]
            continue
        flag = True
        # для кожного ключового слова
        for part in KEY_WORDS:
            # якщо ключове слово міститься в нашому виразу
            if part in expression:
                # якщо він є крайнім у списку
                if expression.index(part) == 0:
                    # додаємо в "поділений вираз" та вирізаємо з виразу
                    divided_expression.append(part)
                    expression = expression[len(part):]
                    flag = False
                    break
        if flag:
            min_index = 999999999
            for part in KEY_WORDS:
                if part in expression:
                    min_index = min(min_index, expression.index(part))
            divided_expression.append(expression[:min_index])
            expression = expression[min_index:]
    divided_expression.append('$')
    return divided_expression


def table_view(stack=None, input=None, output='') -> None:
    global phase_counter
    if phase_counter == 0:
        # ініціалізація таблички
        print(f'{" Phase":<10}|{" Stack":<100}|{" Input":<100}|{" Output":<30}')
    else:
        stack = "" if stack is None else "".join(stack)
        input = "" if input is None else "".join(input)
        print(f'{" "+str(phase_counter):<10}|{" "+stack:<100}|{" "+input:<100}|{" "+output:<30}')
    phase_counter += 1


def predictive_analyzer(expression: str) -> None:
    global phase_counter
    table_view()  # table init

    expression = divide_into_parts(expression)  # поділ на частини
    stack = ["$", "<вхідний тег>"]  # початковий стек. Чи має тут бути "<вхідний тег>"

    table_view(stack, expression)

    # для кожного останнього елементу стеку, поки він не є $ або першим елементом expression, який після всіх ітерацій
    # стане "$"
    # while stack[-1] != ("$" or expression[0]):
    while expression[0] != "$":
        # якщо останній елемент стеку та перший елемент виразу однакові - видаляємо і там, і там
        # example:  stack:  $E'T+        expression:  +id*id$
        if stack[-1] == expression[0]:
            # видаляємо
            stack = stack[:-1]
            expression = expression[1:]

            table_view(stack, expression)
            continue

        # зберігаємо це значення для table
        last_stack_element = stack[-1]

        # дістаємо правило, яким заміняємо останній елементу стеку
        new_rule = get_rule(expression[0], stack[-1])
        stack = stack[:-1]

        # перевіряємо на помилку
        if 'exception' in new_rule:
            print('EXCEPTION NOT RULE')
            print(f'stack[last] = "{last_stack_element}", expression[first] = "{expression[0]}"')
            print(stack)
            print(expression)
            break

        # в нашому випадку ε просто видаляє останній елемент стеку і нічого не додає
        if 'ε' not in new_rule:
            # тобто, якщо НЕ ε, то ми доповнюємо стек, але потрібно зробити реверс
            stack.extend(new_rule[::-1])

        table_view(stack, expression, last_stack_element+f"({expression[0]})" + " -> " + "".join(new_rule))

    # перезапускаємо лічильник для інших виразів
    phase_counter = 0
    print()


if __name__ == '__main__':
    predictive_analyzer("<h1 align='center'><img src='image.svg' height='380' width='1200'></h1>$")
