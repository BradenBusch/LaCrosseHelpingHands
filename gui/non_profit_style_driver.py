import os

class Colors:
    main_theme = '#ABABFB'
    secondary = '#ABD3FB'

def style_sheet():
    file = open(os.path.abspath(os.path.dirname(__file__) + '\\non_profit_style.qss'))
    try:
        qcss = file.read().format(
            main_theme=Colors.main_theme,
            secondary=Colors.secondary
        )
    except KeyError:
        qcss = ""
    file.close()
    return qcss
