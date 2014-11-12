# -*- coding:utf-8 -*-

import json
from datetime import date, timedelta
import tornado.web

class QuickQueryHandler(tornado.web.RequestHandler):

	def get(self, campus, today_or_tomorrow, start_lesson, end_lesson):
		# constant @todo move to application layer
		term_id = '14152'
		start_year = 2014
		start_month = 9
		start_day = 22

		term_tail = term_id[-1:]

		if today_or_tomorrow not in ['today', 'tomorrow']:
			self.write(json.dumps([u'参数不对哦']))
			self.finish()

		# convert today_or_tomorrow to week and date
		start_date = date(start_year, start_month, start_day)
		check_date = date.today()
		if today_or_tomorrow == 'tomorrow':
			try:
				check_date = date(check_date.year, check_date.month, check_date.day + 1)
			except:
				# out of day
				try:
					check_date = date(check_date.year, check_date.month + 1, check_date.day)
				except:
					# out of month
					check_date = date(check_date.year + 1, check_date.month, check_date.day)

		delta = check_date - start_date
		week = delta.days / 7 + 1
		date = check_date.isoweekday()

		#@todo reuse following code
		# filter paramter
		try:
			# some default limitation
			week_low = 1
	    	week_high = 4
	    	date_low = 1
	    	date_high = 7
	    	start_lesson_low = 1
	    	start_lesson_high = 13
	    	end_lesson_low = 1
	        end_lesson_high = 13
	        campus_options = ['djq', 'spl', 'jlh']

	        # change limitation according to term_tail and campus
	        if term_tail == '-1':
	            pass
	        elif term_tail == '-2':
	            if campus == 'djq':
	                week_low = 5
	                week_high = 20
	            elif campus == 'jlh' or campus == 'spl':
	                week_high = 16
	        elif term_tail == '-3':
	            week_high = 16

	        # convert to integer
	        week_int = int(week)
	        date_int = int(date)
	        start_lesson_int = int(start_lesson)
	        end_lesson_int = int(end_lesson)
	    except:
	    	self.write(json.dumps([u'参数不对哦']))
	    	self.finish()

	    if campus in campus_options \
	    		and week_low <= week_int <= week_high \
	    		and date_low <= date_int <= date_high \
	    		and start_lesson_low <= start_lesson_int <= start_lesson_high \
	    		and end_lesson_low <= end_lesson_int <= end_lesson_high \
	    		and start_lesson_int <= end_lesson_int:
	    	# access db
	    	result = []

	    	self.write(json.dumps(result))
	    else:
	    	self.write(json.dumps([u'参数不对哦']))
		
		self.finish()

