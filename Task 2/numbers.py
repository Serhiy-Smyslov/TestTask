def div_five(num: int) -> bool:
    return True if num % 5 == 0 else False


def div_three(num: int) -> bool:
    return True if num % 3 == 0 else False


if __name__ == '__main__':
    for number in range(11, 80):
        if div_three(number) and div_five(number):
            print('$$@@', end=' ')
        elif div_three(number):
            print('$$', end=' ')
        elif div_five(number):
            print('@@', end=' ')
        else:
            print(number, end=' ')