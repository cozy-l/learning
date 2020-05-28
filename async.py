import tornado
from tornado.httpclient import AsyncHTTPClient
import time, sys


def http_callback_way(url1, url2):
    http_client = AsyncHTTPClient()
    start = time.time()
    count = [0]

    def handle_result(response, url):
        print('%d handler response:%s' % (time.time(), url))
        count[0] += 1
        if count[0] == 2:
            cost = time.time() - start
            print('cost:%d' % cost)
            # 退出程序,
            # sys.eixt() 会抛出一个异常SystemExit 如果捕获可以在程序退出时 做一些清场工作，sys.exit(0) 正常退出
            # os.exit() 直接终止 退出
            sys.exit(0)

    future1 = http_client.fetch(url1, lambda res, url=url1: handle_result(res, url))
    print('%d No wait' % time.time())
    future2 = http_client.fetch(url2, lambda res, url=url2: handle_result(res, url))
    print(future1, future2)


url_list = ['http://xlambda.com/gevent-tutorial/', 'https://www.bing.com']

if __name__ == '__main__':
    http_callback_way(*url_list)
    io_loop = tornado.ioloop.IOLoop.instance()
    print('io_loop:', io_loop)
    # 打印发现，这里实际上返回的是KQueueIOLoop, 路径: tornado.platform.kqueue.KQueueIOLoop
    # mac平台返回KQueueIOLoop， 若是linux则返回EPollIOLoop 都是高效I/O多路复用的实现方式
    io_loop.start()
