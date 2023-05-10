import re

# регулярні вирази для токенів
TAG_REGEX = r'<([/]?\w+)[^>]*>'
ATTRIBUTE_REGEX = r"([a-zA-Z0-9_-]+)\s*=\s*['\"](.*?)['\"]"
TEXT_REGEX = r">([^><]+)<"
CLEAR_HTML_REGEX = r'[\n\t]'
SPACE_REGEX = r'\s+'


def clean_html_string(html_string: str) -> str:
    clean_string = re.sub(CLEAR_HTML_REGEX, '', html_string)
    clean_string = re.sub(SPACE_REGEX, ' ', clean_string)
    return clean_string.strip()


def show_current_element(type_token='Тип токену', lexeme='Лексема', start='Початок', length='Довжина'):
    print(f'{f" {type_token}":<15}|'
          f'{f" {start}":<10}|'
          f'{f" {length}":<10}|'          
          f'{f" {lexeme}":<15}')


def file_to_html(path: str) -> str:
    file = open(path, 'r', encoding='utf-8')
    html = file.read()
    return clean_html_string(html)


def lexis_analyzer(html: str) -> list:
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
                    show_current_element('Start of tag', "</", str(length), "2")
                    show_current_element('Tag', name_tag[1:], str(length+1), str(len(name_tag[1:])))
                    length += len(tag)
                    expression.extend(['</', name_tag[1:], '>'])
                else:
                    show_current_element('Start of tag', "<", str(length), "1")
                    show_current_element('Tag', name_tag[:], str(length + 1), str(len(name_tag[:])))
                    length += len(name_tag) + 2
                    expression.extend(['<', name_tag])
                    for attribute in attributes:
                        show_current_element('Attribute', attribute[0], str(length), str(len(attribute[0])))
                        length += len(attribute[0]) + 2
                        show_current_element('Value', attribute[1], str(length), str(len(attribute[1])))
                        length += len(attribute[1]) + 2
                        expression.extend([attribute[0], '=', "'", attribute[1], "'"])
                    length -= 1
                    expression.append('>')
                tags = tags[1:]
                show_current_element("End of tag", ">", str(length), "1")
                length += 1
                continue

        if len(content) != 0:
            text = content[0]
            if html.index(text) == 0:
                if text == ' ':
                    content = content[1:]
                    html = html[1:]
                    continue
                show_current_element("Text", text, str(length), str(len(text)))
                length += len(text)
                expression.append(text)
                html = html[len(text):]
                content = content[1:]
    return expression
