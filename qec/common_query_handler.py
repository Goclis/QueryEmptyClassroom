# -*- coding:utf-8 -*-

import json
import tornado.web
from qec.utils import filter_common

class CommonQueryHandler(tornado.web.RequestHandler):

	def get(self, campus, week, date, start_lesson, end_lesson):
		# filter paramter
		filter_result = filter_common(campus, week, date, start_lesson, end_lesson)

		if filter_result is None:
			self.write(json.dumps([u'参数不对哦']))
		else:
			# access db
			result = ['j1-111']
			self.write(json.dumps(result))

		self.finish()
