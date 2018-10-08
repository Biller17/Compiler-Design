from enum import Enum



#tokentype class with all enum tokens
class TokenType(Enum):

    ENDFILE = '$'
    ELSE = 'else'
    IF = 'if'
    INT ='int'
    RETURN ='return'
    VOID ='void'
    WHILE ='while'
    PLUS ='+'
    MINUS ='-'
    ASTERISK ='*'
    SLASH = '/'
    LESS_THAN = '<'
    LESS_THAN_EQUAL_TO = '<='
    GREATER_THAN = '>'
    GREATER_THAN_EQUAL_TO = '>='
    EQUAL = '=='
    DIFFERENT = '!='
    ASSIGNMENT = '='
    SEMICOLON  = ';'
    COMMA  = ','
    OPEN_PARENTHESIS = '('
    CLOSE_PARENTHESIS = ')'
    OPEN_BRACKETS = '['
    CLOSE_BRACKETS = ']'
    OPEN_KEYS = '{'
    CLOSE_KEYS = '}'
    ID = ''
    NUM = ''
    ERROR = 'error'
