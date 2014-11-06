QueryEmptyClassroom
===================

查询空教室


Tornado版本预计实现的优化：

1. 程序启动时直接缓存所有的教室列表，将每次请求两次查询减少为一次。
2. 尝试使用Asynchronous mysql driver。
