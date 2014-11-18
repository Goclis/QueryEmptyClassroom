# -*- coding:utf-8 -*-

from qec.common_query_handler import CommonQueryHandler
from qec.quick_query_handler import QuickQueryHandler
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):

	def __init__(self):
		handlers = [
			(r'/query/([a-z]{3})/(\d{1,2})/(\d)/(\d{1,2})/(\d{1,2})', CommonQueryHandler),
			(r'/query/([a-z]{3})/([a-z]{1,8})/(\d{1,2})/(\d{1,2})', QuickQueryHandler)
		]

		tornado.web.Application.__init__(self, handlers, debug=True)


if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
