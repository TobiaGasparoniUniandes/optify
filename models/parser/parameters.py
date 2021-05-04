import re

from models.utils.constants import *


def parse_parameters_explicit(parameters):
    """
    $profit\_a=6$\break
    $profit\_b=5$\break
    $tot\_units\_milk=5$\break
    $tot\_units\_choco=12$\break
    $choco\_a=3$\break
    $milk\_a=1$\break
    $choco\_b=2$\break
    $milk\_b=1$

    REGEX doc: https://regex101.com/r/K2PvT2/1
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
       https://regex101.com/delete/uZ1G4CUJWzgHR3VivYMIHXJx
    """
    # \$(\w+(?:\\_\w+)*)=(\d+)
    regex = re.compile(r"{}({})=({})".format(DOLLAR, VARIABLE, NUMBER))
    return regex.findall(parameters.replace(" ", ""))
