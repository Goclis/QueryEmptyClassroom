# -*- coding:utf-8 -*-

import json
from datetime import date, timedelta
from qec.utils import filter_quick
import tornado.web

class QuickQueryHandler(tornado.web.RequestHandler):

	def get(self, campus, today_or_tomorrow, start_lesson, end_lesson):
		# constant @todo move to application layer
		term_id = '14152'
		start_year = 2014
		start_month = 9
		start_day = 22

		term_tail = term_id[-1:]

		filter_result = filter_quick(
			campus, today_or_tomorrow, start_lesson, end_lesson, term_tail,
			start_year, start_month, start_day)

		if filter_result is None:
			self.write(json.dumps([u'参数不对哦']))
		else:
			# access db
			result = ['j1-111']
			self.write(json.dumps(result))

		self.finish()

