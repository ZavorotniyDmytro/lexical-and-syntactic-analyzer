from lexis import *
from syntax import *

HTML_FILE_PATH = 'index.html'

if __name__ == '__main__':
    # html_string = file_to_html(HTML_FILE_PATH)
    # expression = lexis_analyzer(html_string)
    # print(expression)
    # predictive_syntax_analyzer(expression)

    expression = lexis_analyzer('<h2 align="right">Заворотній Дмитро Олександрович, 202 група</h2>')
    print(expression)
    predictive_syntax_analyzer(expression)


