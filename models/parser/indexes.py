import re
from models.utils.constants import *


def parse_indexes_explicit(indexes):
    '''
    REGEX DOC: https://regex101.com/r/JKDmgO/1
    '''

    # \$\w+(?:\\_\w+)*=\[\d+,...,\d+\]
    regex = re.compile(r"{}{}={}{},{},{}{}".format(DOLLAR, VARIABLE, OPEN_SQUARE, NUMBER, DOTS, NUMBER, CLOSE_SQUARE))
    return regex.findall(indexes.replace(" ", ""))
