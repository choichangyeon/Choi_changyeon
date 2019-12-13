numPadList = [
    '7', '8', '9',
    '4', '5', '6',
    '1', '2', '3',
    '0', '.', '=',
]

operatorList = [
    '*', '/',
    '+', '-',
    '(', ')',
    'C',
]

constantList = [
    'pi',
    '빛의 이동 속도 (m/s)',
    '소리의 이동 속도 (m/s)',
    '태양과의 평균 거리 (km)',
]

from calcFunctions import *

functionMap = [
    ('factorial (!)', factorial),
    ('-> binary', decToBin),
    ('binary -> dec', binToDec),
    ('-> roman', decToRoman),
    ('roman -> dec', romanToDec)
]

functionList = [x[0] for x in functionMap]
