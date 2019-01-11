from collections import deque

def search(lines, pattern, history=5):
    pervious_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, pervious_lines  # 使用生成器函数生成一个可迭代对象
        pervious_lines.append(line)

if __name__ == '__main__':
    with open(__file__, 'r') as f:
        for line, perv_lines in search(f, 'def'):
            for perv_line in perv_lines:
                print(perv_line, end='')
            print(line, end='')
            print('-' * 20)
