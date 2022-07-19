# Perceptron

def AND(x1, x2):
    w1 = 0.5
    w2 = 0.5
    theta = 0.7
    if w1 * x1 + w2 * x2 > theta:
        return 1
    else:
        return 0

def NAND(x1, x2):
    w1 = -0.5
    w2 = -0.5
    theta = -0.7
    if w1 * x1 + w2 * x2 > theta:
        return 1
    else:
        return 0

def OR(x1, x2):
    w1 = 0.5
    w2 = 0.5
    theta = 0.3
    if w1 * x1 + w2 * x2 > theta:
        return 1
    else:
        return 0

# 층이 하나 더 깊어져야됨.
# 이전까지는 선형적으로 풀이가 불가능 했던 문제를
# 층을 깊게 하므로서 해결함.
def XOR(x1, x2):
    return AND(NAND(x1, x2), OR(x1, x2))
