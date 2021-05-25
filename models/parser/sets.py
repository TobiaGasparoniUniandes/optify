import re

from models.utils.constants import *


def parse_sets_explicit(sets):
    """
    REGEX DOC:  https://regex101.com/r/jj4JdD/1
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
       https://regex101.com/delete/8nAjBoIj2xAApldjcIaOi1uN
    """
    # \$(\w+(?:\\_\w+)*)=\\\{((?:\w+(?:\\_\w+)*,?)+)\\\}\$

    regex = re.compile(r"\$(\w+(?:\\_\w+)*)=\\\{((?:\w+(?:\\_\w+)*,?)+)\\\}\$")
    matches = regex.findall(sets.replace(" ", ""))
    dictionaries = {}
    for match in matches:
        dictionaries[match[0]] = {ele for ele in match[1].split(',')}
    return dictionaries
