# -*- coding:utf-8 -*-

#@todo 增加对数据库访问异常的返回提醒

import sys
sys.path.insert(0, '../crawler')  # 为了导入配置信息

import crawlerconfig as settings
import MySQLdb

# api_1: /query/[spl, djq, jlh]/[which week]/[which day]/[start class]/[end class]
# api_2: /query/[spl, djq, jlh]/[today, tomorrow]/[start class]/[end class]
# api_2 可以通过当前时间计算好后转换为 api_1，所以这里只实现 api_1


# 负责根据学期和校区对参数选项进行过滤
#
# 以下根据学期对参数进行合法界定：
# 1. xx-xx-1 学期
#   (a) jlh
#       week [1~4]
#       date [1~7]
#       start_lesson[1~13]
#       end_lesson[1~13]
#       start_lesson <= end_lesson
#   (b) spl
#       同 (a)
#   (c) djq
#       似乎没课，暂时同 (a)
#
# 2. xx-xx-2 学期
#   (a) jlh
#       week [1~16]
#       date [1~7]
#       start_lesson[1~13]
#       end_lesson[1~13]
#       start_lesson <= end_lesson
#   (b) spl
#       同 (a)
#   (c) djq
#       week [5~20]
#       date [1~7]
#       start_lesson[1~13]
#       end_lesson[1~13]
#       start_lesson <= end_lesson
#
# 3. xx-xx-3 学期
#   (a) jlh
#       week [1~16]
#       date [1~7]
#       start_lesson[1~13]
#       end_lesson[1~13]
#       start_lesson <= end_lesson
#   (b) spl
#       同 (a)
#   (c) djq
#       同 (a)
#
# 除此之外，参数应该满足如下类型：
# campus - string
# week, date, start_lesson, end_lesson - integer
def front_filter(campus, week, date, start_lesson, end_lesson):
    term_id = settings.course_term_id
    term_tail = term_id[-1:]
    try:
        # limit parameters
        week_low = 1
        week_high = 4
        date_low = 1
        date_high = 7
        start_lesson_low = 1
        start_lesson_high = 13
        end_lesson_low = 1
        end_lesson_high = 13
        campus_options = ['djq', 'spl', 'jlh']

        # 根据 term 和 campus 修改限制参数
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

        # 检查参数是否合理
        week_int = int(week)
        date_int = int(date)
        start_lesson_int = int(start_lesson)
        end_lesson_int = int(end_lesson)
    except:
        print 'Invalid Parameters'
        return [] # No need to notify error.
    if campus in campus_options \
            and week_low <= week_int <= week_high \
            and date_low <= date_int <= date_high \
            and start_lesson_low <= start_lesson_int <= start_lesson_high \
            and end_lesson_low <= end_lesson_int <= end_lesson_high \
            and start_lesson_int <= end_lesson_int:
        return get_free_classrooms(campus, week_int, date_int, start_lesson_int, end_lesson_int)
    else:
        return []
    


# 现实情况分析
# 东大为一年三学期，分别以 -1, -2, -3 对学期进行结尾
# -1 为 4 周，-2 和 -3 都为 16 周，但又因为校区的不同，有所差异
# 
# Exception: 丁家桥（djq）不区分 -1 和 -2，将两者合并在一起，因而排课时，没有短学期的课，
# 但对于 -2，学期，它们的课是从 1 - 20 周，其中 1 - 4 其实就是短学期的课程，
# 因此，在获取 -2 学期的课时，存在一些课是 5 - 20 周的，鉴于丁家桥同学们的使用
# 习惯，保留 5 - 20 周这样的查询行为
#
# 另外两个校区貌似没有这样的问题
#
# 显然，由于这样的一些问题，需要一个前端的过滤器根据不同的学期对参数进行不同
# 的过滤行为乃至修改（djq -2），再传给本函数
#
# 本函数接受过滤修改以及转换过后的参数，只进行检查的查表及返回操作
# @campus : string
# @date : int
# @week : int
# @start_lesson : int
# @end_lesson : int
# @return : [] - 出错也返回 []
def get_free_classrooms(campus, week, date, start_lesson, end_lesson):
    # Todo: 替换成安全的查询， = = 防止过滤不干净
    connection = MySQLdb.connect(
        host=settings.db_host, user=settings.db_username, passwd=settings.db_password,
        db=settings.db_name, charset='utf8')
    cursor = connection.cursor()

    classrooms = []
    ALL_CLASSROOM_SQL = 'SELECT DISTINCT course_place FROM course_schedule WHERE course_place LIKE %s'
    cursor.execute(ALL_CLASSROOM_SQL, ['%-%'])
    rs = cursor.fetchall()
    for r in rs:
        classrooms.append(r[0])
    # 判断单双周
    if week % 2 == 0:
        search_course_type = 1 # 双周，设置为单周
    else:
        search_course_type = 2 # 单周，设置为双周

    CLASSROOM_USING_SQL = 'SELECT DISTINCT course_place FROM course_schedule WHERE ' \
            + '((course_type != %s) ' \
            + "AND (course_date = %s) " \
            + "AND (course_start_week <= %s AND course_end_week >= %s)" \
            + "AND ((%s - course_end_lesson) * (%s - course_start_lesson) <= 0))"
    
    cursor.execute(CLASSROOM_USING_SQL, 
        [search_course_type, date, week, week, start_lesson, end_lesson])
    rs = cursor.fetchall()
    for r in rs:
        if classrooms.__contains__(r[0]):
            classrooms.remove(r[0])

    # Exceptions:
    try:
        classrooms.remove(u"九龙湖其它-大活322")
    except:
        pass

    jlh = []
    djq = []
    spl = []


    # 根据各大校区教室名称特征区分
    for room in classrooms:
        if room.find(u'教') != -1:
            jlh.append(room)
        elif room.find(u'基') != -1 \
                or (room.find(u'综合') != -1 and room.find(u'综合楼') == -1) \
                or room.find(u'公卫') != -1:
            djq.append(room)
        else:
            spl.append(room)
    if campus == 'jlh':
        return sort_classroom_by_CN(jlh)
    elif campus == 'djq':
        return djq 
    elif campus == 'spl':
        return spl
    else:
        return []


# 根据中文顺序对列表排序，返回排好序的列表
def sort_classroom_by_CN(l):
    # 将九龙湖的教室进行排序，花费空间节省时间
    tmpJLH = []
    for room in l:
        if room.find(u"教一") != -1:
            tmpJLH.append(room.replace(u"教一", "J1"))
        if room.find(u"教二") != -1:
            tmpJLH.append(room.replace(u"教二", "J2"))
        if room.find(u"教三") != -1:
            tmpJLH.append(room.replace(u"教三", "J3"))
        if room.find(u"教四") != -1:
            tmpJLH.append(room.replace(u"教四", "J4"))
        if room.find(u"教五") != -1:
            tmpJLH.append(room.replace("教五", "J5"))
        if room.find(u"教六") != -1:
            tmpJLH.append(room.replace(u"教六", "J6"))
        if room.find(u"教七") != -1:
            tmpJLH.append(room.replace(u"教七", "J7"))
        if room.find(u"教八") != -1:
            tmpJLH.append(room.replace(u"教八", "J8"))

    tmpJLH.sort()
    l = []
    for room in tmpJLH:
        if room.find("J1") != -1:
            l.append(room.replace("J1", u"教一"))
        if room.find("J2") != -1:
            l.append(room.replace("J2", u"教二"))
        if room.find("J3") != -1:
            l.append(room.replace("J3", u"教三"))
        if room.find("J4") != -1:
            l.append(room.replace("J4", u"教四"))
        if room.find("J5") != -1:
            l.append(room.replace("J5", u"教五"))
        if room.find("J6") != -1:
            l.append(room.replace("J6", u"教六"))
        if room.find("J7") != -1:
            l.append(room.replace("J7", u"教七"))
        if room.find("J8") != -1:
            l.append(room.replace("J8", u"教八"))
    return l
