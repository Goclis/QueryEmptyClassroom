# -*- coding:utf-8 -*-

import json
import tornado.web
from qec.utils import filter_common

class CommonQueryHandler(tornado.web.RequestHandler):

	def get(self, campus, week, date, start_lesson, end_lesson):
		# constant @todo move to application layer
		term_id = '14152'

		term_tail = term_id[-1:]

		# filter paramter
		filter_result = filter_common(campus, week, date, start_lesson, end_lesson, term_tail)

		if filter_result is None:
			self.write(json.dumps([u'参数不对哦']))
		else:
			# access db
			result = ['j1-111']
			self.write(json.dumps(result))

		self.finish()
