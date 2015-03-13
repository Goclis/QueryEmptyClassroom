QueryEmptyClassroom
===================
本项目提供了查询空教室的API供其他应用程序使用。

## 1. API
### 1.1. 通用查询
__URL__

```
/query/[校区]/[第几周]/[周几]/[第几节开始]/[第几节结束]
```

__PARAMETERS__

- `校区`：可选值为[jlh, djq, spl]，分别代表九龙湖，丁家桥，四牌楼。
- `第几周`：可选值范围取决于当前所处学期。
	- `xx-xx-1`：1-4。
	- `xx-xx-2`：1-16，对于丁家桥为5-20（有人说他们习惯这样...）。
	- `xx-xx-3`：1-16。
- `周几`：可选值为1-7。
- `第几节开始`：可选值为1-13。
- `第几节结束`：可选值为1-13。


__EXCEPTIONS__

- 当参数不正确时，会返回`[BAD_PARAMETER]`。
- 当访问数据库出错时，会返回`[DB_ERROR]`。

### 1.2. 快速查询
提供便捷查询今天/明天的空教室。

__URL__

```
/query/[天]/[第几节开始]/[第几节结束]
```

__PARAMTERS__

- `天`：可选值为[today, tomorrow]，分别代表今天，明天。
- 其他参数同`1.1`。

__EXCEPTIONS__

同`1.1`。

### 1.3. 考试周空教室查询
数据已获取，暂未实现API。

## 2. 运行环境
- Linux (Ubuntu 12.04 & 14.04)
- MySQL
- Tornado
- Python Libs
	- MySQLdb

运行中的计算（如今天是几号）依赖于系统时间，因此，需要保证机器时间准确，起码不要有天这一级别上错误。

__爬虫额外依赖__

- Python Libs
	- lxml
	- requests

## 3. 项目内容
项目主要包含两部分，一为python实现的获取数据的爬虫，二为基于tornado框架的http server。

__项目文件夹结构__

- QueryEmptyClassroom
	- config
	- crawler
	- qec
	- sql
	- main.py

### 3.1. sql
空教室是通过从`所有教室列表`中去除掉`占用教室`得到的。而占用教室是通过使用调用API时的信息查询数据库获取的，`sql/all.sql`中包含了对数据库中表的描述。

### 3.2. config
无论是查询数据库还是获取数据库，都需要关于数据库的信息，比如说`host`、`username`、`password`以及`db_name`等等，这些均在`config/config.py`文件中定义了，作为一个配置模块存在。

除数据库信息外，其还包含着学期的信息，以下为具体描述。

- 学期信息
	- `course_term`：哪个学期，格式为学年加学期，如`14-15-1`。
	- `course_term_id`：学期的对应ID，即course_term去掉`-`，如`14151`。
	- `exam_term`：考试信息的学期，格式同course_term，如`13-14-3`。
	- `start_year`：本学期第一周周一对应的年。
	- `start_month`：本学期第一周周一对应的月。
	- `start_day`：本学期第一周周一对应的日。
- 数据库信息
	- `db_host`：数据库所在主机。
	- `db_username`：数据库用户名。
	- `db_password`：数据库密码。
	- `db_name`：数据库名。

### 3.3. crawler
`crawler/get_info.py`为用于获取数据的爬虫，获取到的数据将保存到数据库中，因此，在使用前需要设置好`config/config.py`中关于数据库信息的内容。

__使用__

```
工具简介：获取上课教室及考试教室数据的爬虫
    
用法：get_info.py [cmd]
    
cmd：（所有的更新命令都会清空原表，请注意备份）
	-ua, --update-all 更新所有的表
    -uc, --update-course 更新和上课教室相关的表
    -ue, --update-exam 更新和考试教室相关的表
    -h, --help 打印帮助信息
```

__执行结果__

执行完后除了更新了数据库外，还会产生相应的log，日志中以`ERROR`开头的为发生错误的SQL语句，日志的结尾有汇总。

__注意__

在该脚本中通过使用了相对路径`../config`将配置信息所在文件夹加入到了`sys.path`中，因此，在执行此脚本时需要将工作目录切到与脚本同一文件夹下，如下的使用可能会出错。

```
$ pwd
/path/QueryEmptyClassroom
$ crawler/get_info.py -ue
```

另外，在执行时可能会因为`locale`的问题导致`UnicodeError`的发生，请确保`locale`为`xxx.UTF-8`（xxx使用`en_US`或者`zh_CN`都可以）。测试机通过在`.zshrc`中加入`export LC_ALL=en_US.UTF-8`解决了此问题。

__数据来源__

上课数据来源于[全校课表](http://xk.urp.seu.edu.cn/jw_service/service/academyClassLook.action)。

考试数据来源于[全校考试安排](http://xk.urp.seu.edu.cn/jw_service/service/runAcademyClassDepartmentQueryAction.action)。

### 3.4. qec
因为http server是基于tornado的，对于URL，是映射到某个Handler上的。qec文件夹里提供了两个Handler分别对应于`1.1`和`1.2`描述的API，分别如下。

- `qec/common_query_handler.py`：CommonQueryHandler。
- `qec/quick_query_handler.py`：QuickQueryHandler。

这两个Handler都依赖于该文件夹下的另外一个文件`utils.py`，这个文件中提供了一系列的方法，如检查参数是否合理的方法，另外获取空教室的方法也在其中。

由于要获取空教室是要查询数据库的，`utils.py`同样也依赖于`3.2`中的配置文件。

### 3.5. main.py
主程序，包含建立URL到Handler的映射以及监听的端口等内容，执行此文件即启动了http server，如下。

```
$ python main.py
```

打开浏览器，[访问](http://localhost:8000/query/today/1/3)。

或者执行如下命令。

```
$ curl http://localhost:8000/query/today/1/3
```

## 4. 部署
### 4.1. 数据库
最好创建个新的数据库，进去后使用`source`命令把`sql/all.sql`给执行以下初始化数据库。

接下来创建一个新的用户，只给这个用户新数据库的权限。

把以上的信息都写入配置文件。

### 4.2. 更新数据库内容
见`5. 更新`。

### 4.3. tornado的部署
原先服务器咋部署tornado的，这个依旧处理就好了。

**注意**：由于查数据库是阻塞的，最好不要和那些有异步能力的API混合在一起，独立起一个比较好。

## 5. 更新
上课的信息每个学期都在变，甚至一个学期在选课前后也会大改不少，因此，数据库是需要不断更新的，使用爬虫脚本可以简化更新过程，但更新时仍要注意一些事情，这里大概给出步骤。

__修改配置文件__

取决于要更新的内容，比如说不打算更新考试周教室信息，就没必要在意`exam_term`。

__选择性备份__

这个自行选择是否备份要更新的数据表。

__执行脚本__

首先，当前工作目录必须和脚本相同。其次，根据要更新的内容选用合适的命令行参数，使用`-h`参数查看帮助。

__查看脚本结果__

脚本执行完毕后会有相应的log产生在同一目录下，查看其中的`ERROR`行，看看原因及是否影响了数据准确性。原因极有可能是bug。

## 6. 可能的扩展
1. 关于配置文件。由于配置文件是在程序启动时读取的，当修改后面临着重启程序，可以考虑做成动态读取的。
2. 关于爬虫。不一定需要人为的去执行，当服务器有相应的环境的情况下，可以写个定时脚本，每天半夜的时候更新一次。

## Todos
1. 测试代码是否可用。

