var CLASSROOMS = null;
var RESULT_HEARDER = ""; // result的头部

// 13-14-2学期第一周周一开始时间
var START_MONTH = 9;
var START_DAY = 16;

// 响应初始化
$(document).ready(function() {
	// 查找按钮的点击响应
	$("#query").click(function(event) {
		var weekNum = $('[name="weekNum"]').val();
		var week = $('[name="week"]').val();
		var start = $('[name="start"]').val();
		var end = $('[name="end"]').val();

		$.ajax({
			url: '/queryEmptyClassrooms/query/',
			type: 'GET',
			dataType: 'json',
			data: {
				'classWeekNum': weekNum,
				'classWeek': week,
				'beginTime': start,
				'endTime': end
			},
			success: function(data) {
				// console.log(data);
				if (data) {
					CLASSROOMS = data; // javascript自动解析json
					var weekCN; // 将1-7转化为一～七
					if (week === "1") {
						weekCN = "一";
					} else if (week === "2") {
						weekCN = "二";
					} else if (week === "3") {
						weekCN = "三";
					} else if (week === "4") {
						weekCN = "四";
					} else if (week === "5") {
						weekCN = "五";
					} else if (week === "6") {
						weekCN = "六";
					} else if (week === "7") {
						weekCN = "日";
					} 
					RESULT_HEARDER = '<h3 class="text-center page-header">第 ' + weekNum 
						+ " 周 周" + weekCN + " " + start + "-" + end + " 节 <br/>空教室</h3>";
					showClassrooms($("#place").val());
				} else {
					CLASSROOMS = null; // 清空数据
					showClassrooms("全部校区"); // 清空结果
				}
			}
		});
	});

	// 处理校区选择的变化
	$('#place').change(function(event) {
		var place = $('#place').val();
		if (CLASSROOMS != null)
			showClassrooms(place);		
	});

	// 为输入框添加focus响应
	$('[name="weekNum"]').focusout(function(event) {
		if ($(this).val() === "")
			$(this).val("5");
	});
	$('[name="week"]').focusout(function(event) {
		if ($(this).val() === "")
			$(this).val("1");
	});
	$('[name="start"]').focusout(function(event) {
		if ($(this).val() === "")
			$(this).val("1");		
	});
	$('[name="end"]').focusout(function(event) {
		if ($(this).val() === "")
			$(this).val("3");
	});
	$('.input-data').focusin(function(event) {
		$(this).val("");		
	});

	// 查询今天与明天的响应
	$('#queryToday').click(function(event) {
		var today = new Date();
		changeInputValue(today);
		$('#query').click();
	});
	$('#queryTomorrow').click(function(event) {
		var tomorrow = new Date();
		tomorrow.setDate(tomorrow.getDate() + 1);
		changeInputValue(tomorrow);
		$('#query').click();
	});
});

// 根据选中的place改变显示的结果
function showClassrooms(place) {
	// 清空结果，提示错误
	if (CLASSROOMS === null) {
		$('#result').html("<h3 class='text-center page-header'><img src='../static/img/cry.gif'> " 
			+ "请正确输入(囧)..... <img src='../static/img/cry.gif'></h3>"); 
		return; // do nothing
	}

	var bAll = false; // 显示全部
	var html = RESULT_HEARDER 
		+ '<table class="table text-center"><tbody><tr class="text-center">';
	var roomNumPerLine = 5; // 每行显示的教室数量，随设备变化而改变
	var clientWidth = document.body.clientWidth; // 网页可见宽度

	// 修改每行显示的数量
	if (clientWidth <= 500) { 
		roomNumPerLine = 4;
	} else if (clientWidth <= 300) {
		roomNumPerLine = 3;
	}

	// 全部校区
	if (place === "全部校区") { 
		bAll = true;
	} 

	var j = 0; // 控制表格换行
	if (bAll || place === "四牌楼") {
		var arr = CLASSROOMS.SPL;
		var i;
		for (i = 0; i < arr.length; i++, j++) {
			html += '<td class="text-center">' + arr[i] + '</td>';
			if ((j + 1) % roomNumPerLine === 0) {
				html += '</tr><tr>';
			}
		}
	}

	if (bAll || place === "九龙湖") {
		var arr = CLASSROOMS.JLH;
		var i;
		for (i = 0; i < arr.length; i++, j++) {
			html += '<td class="text-center">' + arr[i] + '</td>';
			if ((j + 1) % roomNumPerLine === 0) {
				html += '</tr><tr>';
			}
		}
	}

	if (bAll || place === "丁家桥") {
		var arr = CLASSROOMS.DJQ;
		var i;
		for (i = 0; i < arr.length; i++, j++) {
			html += '<td class="text-center">' + arr[i] + '</td>';
			if ((j + 1) % roomNumPerLine === 0) {
				html += '</tr><tr>';
			}
		}
	}

	html += "</tr></table>";
	$("#result").html(html);
}

// 根据提供的日期修改输入框内容
function changeInputValue(day) {
	// 创建一个标识学期第一天的Date Object
	var startDate = new Date();
	startDate.setDate(START_DAY);
	startDate.setMonth(START_MONTH - 1);

	// 刷新要计算的日期，因为startDate对象后创建，为保证结果需更新
	day.setMinutes(startDate.getMinutes() + 1); 

	var dis = day - startDate; // 相差的毫秒数
	var daysGap = (dis / 1000.0 / 3600.0 / 24.0); // 相差的天数
	// console.warn(daysGap);
	$('[name="weekNum"]').val(Math.ceil(daysGap / 7)); // 设置第几周
	if (day.getDay() == 0) { // 设置星期几
		$('[name="week"]').val(7);
	} else {
		$('[name="week"]').val(day.getDay());
	}
}