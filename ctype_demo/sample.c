/* 编译为动态库：
 * $ gcc-8 sample.c -fPIC -shared -o libsample.so
 * -shared 选项指定生成动态连接库
 * -fPIC 表示编译为位置独立代码（position-independent code）
 */

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
