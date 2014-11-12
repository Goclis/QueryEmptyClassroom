# -*- coding:utf-8 -*-

# two filter
from datetime import date as datelib, timedelta
import config


# @brief filter parameters of common query.
#
# @return if parameter is ok, return the tuple (campus, week, date, start_lesson, end_lesson),
#	else return None.
def filter_common(campus, week, date, start_lesson, end_lesson):
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

		term_tail = config.TERM_ID[-1:]

		# change limitation according to term_tail and campus
		if term_tail == '1':
			pass
		elif term_tail == '2':
			if campus == 'djq':
				week_low = 5
				week_high = 20
			elif campus == 'jlh' or campus == 'spl':
				week_high = 16
		elif term_tail == '3':
			week_high = 16

		# convert to integer
		week_int = int(week)
		date_int = int(date)
		start_lesson_int = int(start_lesson)
		end_lesson_int = int(end_lesson)
	except:
		return None

	if campus in campus_options \
			and week_low <= week_int <= week_high \
			and date_low <= date_int <= date_high \
			and start_lesson_low <= start_lesson_int <= start_lesson_high \
			and end_lesson_low <= end_lesson_int <= end_lesson_high \
			and start_lesson_int <= end_lesson_int:
		return (campus, week_int, date_int, start_lesson_int, end_lesson_int)

	return None

# @brief filter paramters of quick query.
#
# @return if parameter is ok, return the tuple (campus, week, date, start_lesson, end_lesson),
#	else return None.
def filter_quick(campus, today_or_tomorrow, start_lesson, end_lesson):
	if today_or_tomorrow not in ['today', 'tomorrow']:
		return None

	# convert today_or_tomorrow to week and date
	start_date = datelib(config.START_YEAR, config.START_MONTH, config.START_DAY)
	check_date = datelib.today()
	if today_or_tomorrow == 'tomorrow':
		try:
			check_date = datelib(check_date.year, check_date.month, check_date.day + 1)
		except:
			# out of day
			try:
				check_date = datelib(check_date.year, check_date.month + 1, check_date.day)
			except:
				# out of month
				check_date = datelib(check_date.year + 1, check_date.month, check_date.day)

	delta = check_date - start_date
	week = delta.days / 7 + 1
	date = check_date.isoweekday()

	return filter_common(campus, week, date, start_lesson, end_lesson)



