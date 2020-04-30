#coding:utf-8
# __init__:负责对象的初始化，但其实在执行该方法之前，对象就已经创建存在了
# __new__:该方法一般不会被重写，它作为构造函数用于创建对象，是一个工厂函数，专用于生产实例对象。如果是考虑到单例模式，可以通过此方法来实现
# __call__:涉及到可调用对象(callable),我们平时自定义的函数，内置函数和类都是属于可调用对象,但凡是可以把一对括号()应用到某一个对象身上的都可
#          称之为可调用对象，可以用函数callable来判断对象是否可调用 print(callablei(object)):

class A:
    def __init__(self):
        print("__init__")
        super(A, self).__init__()

    def __new__(cls):
        print("__new_")
        return super(A, cls).__new__(cls)

    def __call__(self):
        print("__call__")


class Counter:
    def __init__(self, fun):
        self.fun = fun
        self.count = 0

    def __call__(self, *arg, **kwargs):
        self.count += 1
        return self.fun(*arg, **kwargs)


@Counter
def foo():
   print('=========') 

#foo()
#print(foo.count)
A()

