from enum import Enum


class TokenType(Enum):

    ENDFILE = 0 #'$'
    ELSE = 1 #'else'
    IF = 2#'if'
    INT = 3#'int'
    RETURN =4 #'return'
    VOID = 5#'void'
    WHILE = 6#'while'
    PLUS = 7#'+'
    MINUS = 8#'-'
    MULTIPLICATION = 9#'*'
    SLASH = 10#'/'
    LESS_THAN = 11#'<'
    LESS_EQUAL = 12#'<='
    GREATER_THAN = 13#'>'
    GREATER_EQUAL = 14#'>='
    EQUAL = 15#'=='
    DIFFERENT = 16#'!='
    ASSIGNMENT = 17#'='
    SEMICOLON  = 18#';'
    COMMA  = 19#','
    OPEN_PARENTHESIS = 20#'('
    CLOSE_PARENTHESIS = 21#')'
    OPEN_BRACKETS = 22#'['
    CLOSE_BRACKETS = 23#']'
    OPEN_KEYS = 24#'{'
    CLOSE_KEYS = 25#'}'
    OPEN_COMMENT = 26#'/*'
    CLOSE_COMMENT = 27#'*/'
    ID = 28
    NUM = 29
