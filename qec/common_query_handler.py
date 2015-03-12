# -*- coding:utf-8 -*-

import json
import tornado.web
from qec.utils import filter_common, get_free_classrooms

class CommonQueryHandler(tornado.web.RequestHandler):

	def get(self, campus, week, date, start_lesson, end_lesson):
		# filter paramter
		filter_result = filter_common(campus, week, date, start_lesson, end_lesson)

		if filter_result is None:
			self.write(json.dumps(['BAD_PARAMETER']))
		else:
			# access db
			result = get_free_classrooms(
				filter_result[0], filter_result[1], filter_result[2], filter_result[3], filter_result[4])
			self.write(json.dumps(result))

		self.finish()
