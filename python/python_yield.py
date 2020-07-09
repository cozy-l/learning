"""

"""

class Fab(object):

    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n += 1
            return r
        raise StopIteration()


"""
一个带有 yield 的函数就是一个 generator，它和普通函数不同，生成一个 generator 看起来像函数调用，
但不会执行任何函数代码，直到对其调用 next()（在 for 循环中会自动调用 next()）才开始执行。
虽然执行流程仍按函数的流程执行，但每执行到一个 yield 语句就会中断，并返回一个迭代值，
下次执行时从 yield 的下一个语句继续执行。看起来就好像一个函数在正常执行的过程中被 yield 中断了数次，
每次中断都会通过 yield 返回当前的迭代值。

yield 的好处是显而易见的，把一个函数改写为一个 generator 就获得了迭代能力，比起用类的实例保存状态来计算下一个 next() 的值，
不仅代码简洁，而且执行流程异常清晰。
"""


def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield a
        a, b = b, a+b
        n += 1


"""
yield 在文件读取方面也有很好的用处，因为如果直接对文件对象调用read()方法， 会导致不可预测的内存占用
好的方法是利用固定长度的缓冲区来不断读取文件内容，通过yield我们可以更容易实现，而不再需要编写读文件的迭代类
"""


def read_file(fpath):
    BLOCK_SIZE = 512
    with open(fpath, 'r') as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if block:
                yield block
            else:
                return


if __name__ == '__main__':
    # for i in Fab(5):
    #     print(i)
    # print(type(fab(5)))
    # for _ in fab(5):
    #     print(_)
    fpath = "../record"
    for _ in read_file(fpath):
        print('*****************************************')
        print(_)