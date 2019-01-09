"""
测试 Python 和 C 的速度。

    $ python3 test.sample.py
    3.1415926535897922
    纯 Python 10000 次循环    : 1.3527750968933105
    3.1415926535897922
    C 10000 次循环，Python 调用: 0.0003681182861328125
"""
import time
import sample

def calc_pi(n):
    '''http://www.pi314.net/eng/bellard.php'''
    pi = 0.0
    for i in range(int(n+1)):
        pi += (-1)**i / 2**(10*i) * (-32/(4*i+1) - 1/(4*i+3) + 256/(10*i+1) - 64/(10*i+3) - 4/(10*i+5) - 4/(10*i+7) + 1/(10*i+9))
    pi *= 1 / 64
    return pi

if __name__ == '__main__':
    sample.gcd(35, 7)
    sample.divide(42, 8)

    now = time.time()
    loop_time = 10000
    print(calc_pi(loop_time))
    print('纯 Python ' + str(loop_time) + ' 次循环    :', (time.time() - now))

    now = time.time()
    print(sample.calc_pi(int(loop_time)))
    print('C ' + str(loop_time) + ' 次循环，Python 调用:', (time.time() - now))
