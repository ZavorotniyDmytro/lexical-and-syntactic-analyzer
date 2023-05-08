import re

HTML_FILE_PATH = 'index.html'

# Задаємо регулярні вирази для токенів
TAG_REGEX = r"<\s*([a-zA-Z0-9]+)([^>]*)>"
END_TAG_REGEX = r"</\s*([a-zA-Z0-9]+)\s*>"
ATTRIBUTE_REGEX = r"([a-zA-Z0-9_-]+)\s*=\s*['\"](.*?)['\"]"
TEXT_REGEX = r"[^<]+"


def tokenize_html(html):
    tokens = []
    while html:
        # Шукаємо початковий тег
        match = re.match(TAG_REGEX, html)
        if match:
            tag_name = match.group(1)
            attributes_str = match.group(2)
            attributes = []
            # Шукаємо атрибути
            for attr_match in re.finditer(ATTRIBUTE_REGEX, attributes_str):
                attr_name = attr_match.group(1)
                attr_value = attr_match.group(2)
                attributes.append((attr_name, attr_value))
            tokens.append(('TAG_START', tag_name, attributes))
            html = html[match.end():]
        # Шукаємо закриваючий тег
        match = re.match(END_TAG_REGEX, html)
        if match:
            tag_name = match.group(1)
            tokens.append(('TAG_END', tag_name))
            html = html[match.end():]
        # Шукаємо текстовий контент
        match = re.match(TEXT_REGEX, html)
        if match:
            text = match.group(0)
            tokens.append(('TEXT', text))
            html = html[match.end():]
        # Якщо не знайшли жодного токена, кидаємо виключення
        if not match:
            raise ValueError('Invalid HTML')
    return tokens


def show_current_element(type_token='Тип токену', lexeme='Лексема', start='Початок', length='Довжина'):
    print(f'{f" {type_token}":<15}|'
          f'{f" {lexeme}":<15}|'
          f'{f" {start}":<15}|'
          f'{f" {length}":<15}')


def html_parse(file_path):
    show_current_element()
    print(f'{"-" * 57}')
    f = open(file_path, 'r', encoding='utf-8')
    d = dict()
    length = 0
    for line in f:
        if line != '\n':
            match_tags = re.findall(r'<[^<>]+>', line)
            # match_content = re.findall(r'>[^<>]+<', line)
            for item in match_tags:
                # print(match_tags)
                # print(item)
                show_current_element('Start of tag', "<", str(length), "1")
                split_item = item[1:-1].split(' ')
                # print(split_item)
                if len(split_item) == 1:
                    # print(item)
                    show_current_element("Tag", item[1: len(item) - 1], str(line.index(item)+length+1),
                                         str(len(split_item[0])))
                else:
                    show_current_element("Tag", str(split_item[0]), str(line.index(split_item[0]) + length + 1),
                                         str(len(split_item[0])))
                    # print(split_item[1:])
                    for sub_tags in split_item[1:]:
                        # print('sub = ' + sub_tags)
                        attr, value = sub_tags.split('=')
                        show_current_element("Attribute", str(attr), str(
                            line.index(attr) + length + 1), str(len(attr)))
                        show_current_element("Value", str(value[1:-1]), str(line.index(value) + length + 2),
                                             str(len(value) - 2))

                show_current_element(
                    "End of tag", ">", str(length + len(item)+1), "1")
                length += (len(line)+1)


if __name__ == '__main__':
    html2 = '<html><head><title>Інформація про мене</title></head><body><h1>Чудовий тег h1</h1><h2>Заворотній Дмитро Олександрович, 202 група</h2><table><caption>Результати моїх тестів</caption><thead><tr><th>Тест</th><th>Результат</th><th>Посилання на тест</th></tr></thead><tr><th>Моя майбутня професія</th><th>Людина-природа</th><th>https://onlinetestpad.com/ru/testview/12319-vasha-budushhaya-professiya</th></tr><tr><th>Тест на уважність</th><th>33%</th><th>https://onlinetestpad.com/ru/testview/53800-test-na-vnimatelnost</th></tr></table><img height="380" src="img.jpg" width="1200"/><p>А й правда, крилатим ґрунту не треба<br/>Землі немає, то буде небо.<br/>Немає поля, то буде воля.<br/>Немає пари, то будуть хмари.</p></body></html>'

    tokens = tokenize_html(html2)
    print(tokens)
    # html_parse(HTML_FILE_PATH)
