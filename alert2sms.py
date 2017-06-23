#!/usr/bin/env python

from urls.am_urls import url_handlers
from tornado import web, httpserver, ioloop
from tornado.options import options, define

define("host", default="0.0.0.0", help="Bind IP, ex: --host=0.0.0.0", type=str)
define(u"port", default=8081, help=u"Bind Port, ex: --port=8081", type=int)

if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(handlers=url_handlers)
    server = httpserver.HTTPServer(app)
    server.listen(options.port, options.host)

    ioloop.IOLoop.instance().start()
