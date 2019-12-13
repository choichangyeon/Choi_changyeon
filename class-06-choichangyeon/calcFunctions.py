from math import factorial as fact

def factorial(numStr):
    try:
        n = int(numStr)
        r = str(fact(n))
    except:
        r = 'Error!'
    return r

def decToBin(numStr):
    try:
        n = int(numStr)
        r = bin(n)[2:]
    except:
        r = 'Error!'
    return r

def binToDec(numStr):
    try:
        n = int(numStr, 2)
        r = str(n)
    except:
        r = 'Error!'
    return r

def decToRoman(numStr):
    try:
        n = int(numStr)
    except:
        return 'Error!'

    if n >= 4000:
        return 'Error!'

    # numberBreaks = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    # letters ={
    #     1000: 'M', 900:'CM', 500:'D', 400:'CD',
    #     100:'C', 90:'XC', 50:'L', 40:'XL',
    #     10:'X', 9:'IX', 5:'V', 4:'IV',
    #     1:'I'
    # }
    # result = ''
    # for value in numberBreaks:
    #     while n >= value:
    #         result += letters[value]
    #         n -= value

    romans = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'),
        (1, 'I')
    ]

    result = ''
    for value, letters in romans:
        while n >= value:
            result += letters
            n -= value

    return result

def romanToDec(numStr):
    try:
        if numStr.isdigit():
            return 'Error!'
        l = ["0"] * len(numStr)
        for word in range(len(numStr)):
            l[word] = numStr[word]
    except:
        return 'Error!'

    romans = [('M', 1000), ('D', 500), ('C', 100), ('L', 50), ('X', 10), ('V', 5), ('I', 1)]

    for i in range(len(l)):
        for word, value in romans:
            if l[i] == word:
                l[i] = value
    sum = 0

    for k in range(len(l)-1):
        if int(l[k]) < int(l[k+1]):
            l[k] = -int(l[k])

    for j in range(len(l)):
        sum += int(l[j])


    return sum







