/* 编译为动态库：
 * $ gcc-8 sample.c -fPIC -shared -o libsample.so
 * -shared 选项指定生成动态连接库
 * -fPIC 表示编译为位置独立代码（position-independent code）
 */

#include <math.h>
#include "sample.h"

/* Compute the greatest common divisor */
int gcd(int x, int y) {
    int g = y;
    while (x > 0) {
        g = x;
        x = y % x;
        y = g;
    }
    return g;
}

/**
 * 一个返回多个值的C函数例子，
 * 其中有一个是通过指针参数的方式。
 */
int divide(int a, int b, int *remainder)
{
    int quot = a / b;
    *remainder = a % b;
    return quot;
}

double calc_pi(int n)
{
    double pi = 0.0;
    int i = 0;
    for( ; i <= n; i++)
    {
        pi += pow(-1, i) / pow(2, 10*i) * (-32.0/(4.0*i+1) - 1.0/(4.0*i+3) + 256.0/(10.0*i+1) - 64.0/(10.0*i+3.0) - 4.0/(10.0*i+5.0) - 4.0/(10.0*i+7.0) + 1.0/(10.0*i+9.0));
    }
    pi *= 0.015625;
    return pi;
}
