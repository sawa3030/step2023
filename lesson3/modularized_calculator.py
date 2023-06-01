#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def read_start_brackets(line, index):
    token = {'type': 'START_BRACKETS'}
    return token, index + 1

def read_end_brackets(line, index):
    token = {'type': 'END_BRACKETS'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_start_brackets(line, index)
        elif line[index] == ')':
            (token, index) = read_end_brackets(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

# calculate multiply and divide
def calculate_multiply_and_divide(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLY':
                tokens[index-2]['number'] *= tokens[index]['number']
                del tokens[index - 1: index+1]
                index -= 1
                continue
            elif tokens[index - 1]['type'] == 'DIVIDE':
                tokens[index-2]['number'] /= tokens[index]['number']
                del tokens[index - 1: index+1]
                index -= 1
                continue
        index += 1
    return tokens

# calculate plus and minus
def calculate_plus_and_minus(tokens):
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    answer = 0
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def evaluate_inside_brackets(tokens):
    tokens = calculate_multiply_and_divide(tokens) # 掛け算、割り算の計算を先に行う
    answer = calculate_plus_and_minus(tokens) # 足し算、引き算の計算
    return answer

def calculate(tokens):
    while True:
        # import pdb;pdb.set_trace()
        start_brackets = 0
        end_brackets = 0
        index = 0

        # 最も優先度の高いカッコを見つける
        while index < len(tokens):
            if tokens[index]['type'] == 'START_BRACKETS':
                start_brackets = index
            elif tokens[index]['type'] == 'END_BRACKETS':
                end_brackets = index
                break
            # カッコがなくなればそのまま計算して答えを返す
            if index == len(tokens) - 1:
                answer = evaluate_inside_brackets(tokens)
                return answer
            index += 1
        
        # カッコの中を計算
        in_brackets_answer = evaluate_inside_brackets(tokens[start_brackets+1: end_brackets])

        # カッコの計算結果でカッコの中身を置き換え
        del tokens[start_brackets: end_brackets+1]
        tokens.insert(start_brackets, {'type': 'NUMBER', 'number': in_brackets_answer})

def test(line):
    tokens = tokenize(line)
    actual_answer = calculate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2")
    test("1+2.0")
    test("1.0+2.0")
    test("1.00+2.0")
    test("1.0+2.1-3")
    test("1.0-2.1-5")
    test("1.0-2.1-10.00")
    test("1+0")
    test("0+0")
    test("10000000000+10000000000000000")
    test("3*5*7")
    test("3.0*5*7")
    test("3.0*5.0*7.0")
    test("3/5*7")
    test("3.0*5.0/7.0")
    test("3.0/5.0/7.0")
    test("0/5.0/7.0")
    test("10000000*10000000000/99999999")
    test("3.0+4*2-1/5")
    test("3.0+4.1*2.1-1.1/5.1")
    test("3.0+0*2-0.000/5")
    test("(3.0+4*(2-1))/5")
    test("(3.0+4.9*(2.2-1.1))/5.4")
    test("(3.0+(6.0-3.0)*(2-1))/5")
    test("(3.0+(2.0*3.0-10)*(2-1))/5")
    test("(3.0-(2.0*3.0-10)*(2-1))/5")
    test("(3.0-(2.0*3.0-6)*(2-1))/5")
    test("3*5*(-7)")
    test("((1000.0*100000000000.0-600000)*(200000000-10000000))/500000000")
    test("0")
    test("1")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = calculate(tokens)
    print("answer = %f\n" % answer)
