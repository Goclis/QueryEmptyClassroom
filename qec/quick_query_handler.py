# -*- coding:utf-8 -*-

import json
from datetime import date, timedelta
from qec.utils import filter_quick, get_free_classrooms
import tornado.web

class QuickQueryHandler(tornado.web.RequestHandler):

	def get(self, campus, today_or_tomorrow, start_lesson, end_lesson):
		filter_result = filter_quick(
			campus, today_or_tomorrow, start_lesson, end_lesson)

		if filter_result is None:
			self.write(json.dumps(['BAD_PARAMETER'], ensure_ascii=False))
		else:
			# access db
			result = get_free_classrooms(
				filter_result[0], filter_result[1], filter_result[2], filter_result[3], filter_result[4])
			
			self.write(json.dumps(result, ensure_ascii=False))

		self.finish()

