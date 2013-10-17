# encoding: UTF-8
''' Main View '''
import sys
import classroomUtil # 数据库操作模块
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

reload(sys)
sys.setdefaultencoding('utf8')

# 首页
def index(request):
	return render_to_response('query.html')

# 方便记忆的链接
def shortIndex(request):
	return HttpResponseRedirect('/queryEmptyClassrooms/index/')

# 关于
def about(request):
	return render_to_response('about.html')

# 响应查询空教室
def queryEmptyClassrooms(request):
	try:
		classWeek = int(request.GET['classWeek']) # 星期几
		classWeekNum = int(request.GET['classWeekNum']) # 第几周
		beginTime = int(request.GET['beginTime']) # 开始时间
		endTime = int(request.GET['endTime']) # 结束时间
		if not ((1 <= classWeekNum <= 16) \
			and (1 <= classWeek <= 7) \
			and (1 <= beginTime <= 13) \
			and (1 <= endTime <= 13)
			and (beginTime <= endTime)):
			return HttpResponse(json.dumps(""), mimetype="text/json")
	except:
		return HttpResponse(json.dumps(""), mimetype="text/json")

	classrooms = classroomUtil.getEmptyClassrooms(classWeek, classWeekNum, beginTime, endTime)

	# 将教室分校区
	JiuLongHu = []
	SiPaiLou = []
	DingJiaQiao = []
	for room in classrooms:
		if room.find('教') != -1:
			JiuLongHu.append(room)
		elif room.find('基') != -1 or (room.find('综合') != -1 and room.find('综合楼') == -1):
			DingJiaQiao.append(room)
		else:
			SiPaiLou.append(room)
	JiuLongHu = classroomUtil.sortClassroomsByCN(JiuLongHu)

	return HttpResponse(json.dumps({'SPL': SiPaiLou, 'JLH': JiuLongHu, 'DJQ': DingJiaQiao}), mimetype="text/json")