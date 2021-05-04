def convert_data(string):
    """
    :param string: value in string format
    :return: the value in its original format
    """
    if string == 'None':
        return None
    elif string == 'True':
        return True
    elif string == 'False':
        return False
    elif isint(string):
        return int(float(string))
    elif isfloat(string):
        return float(string)
    else:
        return string


# Function adapted from
# https://stackoverflow.com/questions/15357422/python-determine-if-a-string-should-be-converted-into-int-or-float
def isfloat(x):
    try:
        float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True


# Function taken from
# https://stackoverflow.com/questions/15357422/python-determine-if-a-string-should-be-converted-into-int-or-float
def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b