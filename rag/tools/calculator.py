import math


def calculator(expression):

    expression = expression.strip().lower()

    if expression.startswith("sqrt(") and expression.endswith(")"):
        number = float(expression[5:-1])
        return str(math.sqrt(number))

    return str(eval(expression))