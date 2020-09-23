'''
Retrieves the style sheet and reads in the information stored in it.

Authors: Braden Busch, Kaelan Engholdt, Alex Terry
Version: 03/01/2020

'''

import os


# holds the colors and themes to be used in the application
class Colors:
    main_theme = '#ABABFB'
    secondary = '#ABD3FB'


# opens the style sheet and reads in all information
def style_sheet():
    '''
    :return : the styled style sheet information read in from the style sheet file
        :type : str
    '''
    
    # open the style sheet
    file = open(os.path.abspath(os.path.dirname(__file__) + '\\non_profit_style.qss'))
    
    # attempt to read in the style sheet
    try:
        qcss = file.read().format(
            main_theme=Colors.main_theme,
            secondary=Colors.secondary
        )
    except KeyError:
        qcss = ""
    
    # close the style sheet
    file.close()
    
    return qcss
