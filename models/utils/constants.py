# DOC TYPES
LATEX = 'latex'

# REGEX
NO_MATTER_GROUP = r"?:"
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
DOTS = r"..."
LEQ = r"\\leq"

# TEXT
MINIMIZE = "minimize"
MAXIMIZE = "maximize"
MAX = "MAX"
MIN = "MIN"
CONCRETE_MODEL = "ConcreteModel"
POSITIVE_INTEGERS = "PositiveIntegers"

# API RESULT KEYS

NAME = 'name'
VARIABLES = 'variables'
INDEX = 'index'
KEY = 'key'
LOWER = 'lower'
VALUE = 'value'
UPPER = 'upper'
FIXED = 'fixed'
STALE = 'stale'
DOMAIN = 'domain'
ACTIVE = 'active'
SIZE = 'size'
BODY = 'body'
CONSTRAINTS = 'constraints'
OBJECTIVES = 'objectives'
ELEMENTS = 'elements'
