# -*- coding:utf-8 -*-

import json
from datetime import date, timedelta
from qec.utils import filter_quick
import tornado.web

class QuickQueryHandler(tornado.web.RequestHandler):

	def get(self, campus, today_or_tomorrow, start_lesson, end_lesson):
		filter_result = filter_quick(
			campus, today_or_tomorrow, start_lesson, end_lesson)

		if filter_result is None:
			self.write(json.dumps([u'参数不对哦']))
		else:
			# access db
			result = ['j1-111']
			self.write(json.dumps(result))

		self.finish()

