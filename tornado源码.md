* Tornado并发能力强
    tornado优秀的并发能力得益于它的web server从底层实现了一整套基于epoll的单线程异步架构（其他python web框架
    的自带server基本是基于wsgi写的简单服务器，并没有自己实现底层架构）
    https://segmentfault.com/a/1190000005659237

    ** epoll的原理（epoll是一个可扩展的linux I/O事件通知机制） https://www.zhihu.com/topic/19594919/top-answers
       epoll的patch源码：http://www.xmailserver.org/linux-patches/nio-improve.html


* Future

  Future会封装异步执行的结果，在同步执行中，Future常常会去等待线程或者进程的执行结果，但是
  在tornado中，他会配合 '.IOLoop.add_future' 或者 yield(需配合.gen.coroutine) 使用

* tornado AsyncHTTPClient 实现

    Example usage:
    ```
    def handle_request(response):
        if response.error:
            print "Error", response.error
        elif:
            print response.body

    http_client = AsyncHTTPClient()
    http_client.fetch("http://www.google.com/", handle_request)
    ```
    fetch方法:

    ```
    def fetch(self, request, callback=None, **kwargs):
        if self._closed:
            raise RuntimeError("fetch() called on closed AsyncHTTPClient")
        if not isinstance(request, HTTPRequest):
            request = HTTPRequest(url=request, **kwargs)
        # We may modify this (to add Host, Accept-Encoding, etc),
        # so make sure we don't modify the caller's object.  This is also
        # where normal dicts get converted to HTTPHeaders objects.
        request.headers = httputil.HTTPHeaders(request.headers)
        request = _RequestProxy(request, self.defaults)
        # 先创建Future，TracebackFuture 继承 Future
        future = TracebackFuture()
        if callback is not None:
            callback = stack_context.wrap(callback)

            def handle_future(future):
                exc = future.exception()
                if isinstance(exc, HTTPError) and exc.response is not None:
                    response = exc.response
                elif exc is not None:
                    response = HTTPResponse(
                        request, 599, error=exc,
                        request_time=time.time() - request.start_time)
                else:
                    response = future.result()
                self.io_loop.add_callback(callback, response)
            # 给future注册回调方法 handle_future,
            future.add_done_callback(handle_future)

        def handle_response(response):
            if response.error:
                future.set_exception(response.error)
            else:
                future.set_result(response)
        self.fetch_impl(request, handle_response)
        return future

    def fetch_impl(self, request, callback):
        raise NotImplementedError()
    ```
