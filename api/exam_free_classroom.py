# -*- coding:utf-8 -*-

# api: exam/[spl, djq, jlh]/year/month/day/start/end

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0, '../crawler')  # 为了导入配置信息


import crawlerconfig as settings
import MySQLdb


# 负责过滤参数
#
# 参数合法边界如下：
# campus - [spl, jlh, djq]
# year - > 2000
# month - [1~12]
# day - [1-31]
# start - [1~3] 1 for morning, 2 for afternoon, 3 for evening
# end - same as start
# start <= end
def front_filter(campus, year, month, day, start, end):
    campus_options = ['djq', 'jlh', 'spl']
    try:
        year_int = int(year)
        month_int = int(month)
        day_int = int(day)
        start_int = int(start)
        end_int = int(end)
    except:
        print 'Invalid Parameters.'
        return []

    if year_int > 2000 \
            and 1 <= month_int <= 12 \
            and 1 <= day_int <= 31 \
            and 1 <= start_int <= 3 \
            and 1 <= end_int <= 3 \
            and start_int <= end_int \
            and campus in campus_options:
        return get_free_classroom(campus, year_int, month_int, day_int, start_int, end_int)
    else:
        return []
    


def get_free_classroom(campus, year, month, day, start, end):
    time_range = range(start - 1, end - start + 1)

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

    exam_term = settings.exam_term
    exam_date = str(year)
    if month < 10:
        exam_date += '0'
    exam_date += str(month)
    if day < 10:
        exam_date += '0'
    exam_date += str(day)
    try:
        exam_date = int(exam_date)
    except:
        return []


    CLASSROOM_USING_SQL = "SELECT DISTINCT exam_place FROM exam_schedule WHERE exam_term = %s"\
        + "AND exam_date = %s AND exam_time = %s"
    for t in time_range:
        cursor.execute(CLASSROOM_USING_SQL, [exam_term, exam_date, t])
        rs = cursor.fetchall()
        for r in rs:
            try:
                classrooms.remove(r[0])
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
        return sortClassroomsByCN(jlh)
    elif campus == 'djq':
        return djq 
    elif campus == 'spl':
        return spl
    else:
        return []


# 根据中文顺序对列表排序，返回排好序的列表
def sortClassroomsByCN(l):
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
