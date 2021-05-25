import re
from models.utils.constants import *


def parse_indexes_explicit(indexes):
    '''
    REGEX DOC: https://regex101.com/r/9CQldC/1
    https://regex101.com/delete/IeGKEeA2JaZGUUXJqj6KH3bE
    '''

    # \$\w+(?:\\_\w+)*=\[\d+,...,\d+\]
    regex = re.compile(r"\$([a-z])\\in(\w+)\$\\break")
    return regex.findall(indexes.replace(" ", ""))
