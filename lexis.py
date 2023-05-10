import re

HTML_FILE_PATH = 'index.html'

# Задаємо регулярні вирази для токенів
ALL_TAG_REGEX = r"<\s*([a-zA-Z0-9]+)([^>]*)>"
TAG_REGEX = r'<([/]?\w+)[^>]*>'
END_TAG_REGEX = r"</\s*([a-zA-Z0-9]+)\s*>"
ATTRIBUTE_REGEX = r"([a-zA-Z0-9_-]+)\s*=\s*['\"](.*?)['\"]"
TEXT_REGEX = r">([^><]+)<"
CLEAR_HTML_REGEX = r'[\n\t]'
SPACE_REGEX = r'\s+'


def open_html_file(path):
    return open(path, 'r', encoding='utf-8')


def clean_html_string(html_string):
    clean_string = re.sub(CLEAR_HTML_REGEX, '', html_string)
    clean_string = re.sub(SPACE_REGEX, ' ', clean_string)
    return clean_string.strip()


def show_current_element(type_token='Тип токену', lexeme='Лексема', start='Початок', length='Довжина'):
    print(f'{f" {type_token}":<15}|'
          f'{f" {lexeme}":<15}|'
          f'{f" {start}":<15}|'
          f'{f" {length}":<15}')


# TODO щось схоже має бути реалізовано у html_parse, який потім це все віддать синтаксичному аналізатору
def concat(tag: str, attributes: list, text:list):
    expression = []
    expression.extend(['<', tag, ])
    for attr, content in attributes:
        expression.extend([attr, '=', "'", content, "'"])
    expression.append('>')
    expression.extend(text)
    # expression.extend(['</', tag, '>'])
    return expression


def html_parse(file):
    expression = []
    show_current_element()
    print(f'{"-" * 57}')

    length = 0
    for line in file:
        if line != '\n':
            match_tags = re.findall(r'<[^<>]+>', line)
            content = re.findall(TEXT_REGEX, line)
            for item in match_tags:

                tag = re.search(TAG_REGEX, item)
                attributes = re.findall(ATTRIBUTE_REGEX, item)  # only content r'\s*=\s*["\']?([^"\'>\s]+)'
                print(concat(tag.group(1), attributes, content))



                show_current_element('Start of tag', "<", str(length), "1")
                split_item = item[1:-1].split(' ')

                if len(split_item) == 1:
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


def file_content_to_html(file):
    html = file.read()
    return clean_html_string(html)


def html_parse_v2(html):
    length = 0
    expression = []
    tags = re.findall(r'<[^<>]+>', html)
    content = re.findall(TEXT_REGEX, html)

    show_current_element()
    while html != "":
        if len(tags) != 0:
            tag = tags[0]
            if html.index(tag) == 0:
                html = html[len(tag):]
                name_tag = re.search(TAG_REGEX, tag).group(1)
                attributes = re.findall(ATTRIBUTE_REGEX, tag)
                if name_tag[0] == '/':
                    expression.extend(['</', name_tag[1:], '>'])
                else:
                    expression.extend(['<', name_tag])
                    for attribute in attributes:
                        expression.extend([attribute[0], '=', "'", attribute[1], "'"])
                    expression.append('>')
                tags = tags[1:]
                continue

        if len(content) != 0:
            text = content[0]
            if html.index(text) == 0:
                if text == ' ':
                    content = content[1:]
                    html = html[1:]
                    continue
                expression.append(text)
                html = html[len(text):]
                content = content[1:]





if __name__ == '__main__':
    # html_parse(open_html_file(HTML_FILE_PATH))

    html_parse_v2(file_content_to_html(open_html_file(HTML_FILE_PATH)))
