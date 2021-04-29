# %% 
import re

'''
Constants
'''

# REGEX
NO_MATTER = r"?:"
VARIABLE = r"\w+(?:\\_\w+)*"
MIN_MAX = r"(MIN|MAX)"
DOLLAR = r"\$"
OPERANDS = r"[*+]"
NUMBER = r"\d+"
IN = r"\\in"

MATHBB = r"\\mathbb"
N = r"N"
OPEN_BRACKETS = r"\{"
CLOSE_BRACKETS = r"\}"
OPEN_SQUARE = r"\["
CLOSE_SQUARE = r"\]"
SPACES = r"\s*"
DOTS= r"..."
LEQ = r"\\leq"


'''
Functions for parsing input model
'''

def parse_sets(sets):
    '''
    REGEX DOC:  https://regex101.com/r/e5EPiz/1
    '''

def parse_indexes(indexes):
    '''
    REGEX DOC: https://regex101.com/r/JKDmgO/1
    '''

    # \$\w+(?:\\_\w+)*=\[\d+,...,\d+\]
    regex = re.compile(r"{}{}={}{},{},{}{}".format(DOLLAR, VARIABLE, OPEN_SQUARE, NUMBER, DOTS, NUMBER, CLOSE_SQUARE))
    return regex.findall(indexes.replace(" ", ""))

print(parse_indexes("$p = [1 , ... , 8]  $p=[1,...,8]"))
