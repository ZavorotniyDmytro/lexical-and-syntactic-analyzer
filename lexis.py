import re

HTML_FILE_PATH = 'index.html'

# Задаємо регулярні вирази для токенів
TAG_REGEX = r"<\s*([a-zA-Z0-9]+)([^>]*)>"
END_TAG_REGEX = r"</\s*([a-zA-Z0-9]+)\s*>"
ATTRIBUTE_REGEX = r"([a-zA-Z0-9_-]+)\s*=\s*['\"](.*?)['\"]"
TEXT_REGEX = r">([^><]+)<"


def show_current_element(type_token='Тип токену', lexeme='Лексема', start='Початок', length='Довжина'):
    print(f'{f" {type_token}":<15}|'
          f'{f" {lexeme}":<15}|'
          f'{f" {start}":<15}|'
          f'{f" {length}":<15}')


def html_parse(file_path):
    show_current_element()
    print(f'{"-" * 57}')
    f = open(file_path, 'r', encoding='utf-8')
    length = 0
    for line in f:
        if line != '\n':
            match_tags = re.findall(r'<[^<>]+>', line)
            match_content = re.findall(TEXT_REGEX, line)
            match_attributes = re.findall(ATTRIBUTE_REGEX, line)  # only content r'\s*=\s*["\']?([^"\'>\s]+)'
            print(match_attributes)
            print(match_content)
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
    html_parse(HTML_FILE_PATH)
