
在日常开发的时候，我们经常会遇到时间处理的问题，代码示例爬虫过来的时间处理，代码示例对库内的数据进行时间维度的统计等。虽然是个很简单的东西，但每次用的时候都难免要再查一查，其实这就是基础不夯实的表现。趁着今天有空，总结一下开发过程中，最最最常见的日期时间格式和操作



#### 常见日期时间类型

| 类型      | 格式         | 示例                |
| --------- | ------------ | :------------------ |
| time      | 时间格式     | 17:54:03            |
| date      | 日期格式     | 2019-01-09          |
| datetime  | 日期时间格式 | 2019-01-09 17:54:03 |
| timestamp | 时间戳格式   | 1547035707.229842   |

<center>右滑可看到示例</center>





#### 日期时间对象的格式

- 对象格式（即struct_time对象格式）

```bash
>>> import time

>>> t_struct = time.gmtime(1547036431)

>>> t_struct

time.struct_time(tm_year=2019, tm_mon=1, tm_mday=9, tm_hour=12, tm_min=20, tm_sec=31, tm_wday=2, tm_yday=9, tm_isdst=0)
```



- 字符串格式：

```bash
>>> import time
>>> t = time.strftime("%H:%M")
>>> t
'20:56'
```



- 浮点数格式：

```bash
>>> import time

>>> t = time.time()

>>> t

1547206269.212508

>>> t.__class__

<type 'float'>
```





#### 常见操作

我们一观察便知，其实struct_time对象和浮点数格式，都不是面向人类友好的格式，一般我们会将它们往字符串形式转换



##### 格式转换：

- 将struct_time转换成字符串形式

```bash
>>> import time

>>> localtime = time.localtime(time.time())

>>> localtime

time.struct_time(tm_year=2019, tm_mon=1, tm_mday=9, tm_hour=21, tm_min=12, tm_sec=15, tm_wday=2, tm_yday=9, tm_isdst=0)

>>> t_format = time.strftime("%Y-%m-%d %H:%M:%S", localtime)

>>> t_format

'2019-01-09 21:12:15'
```



- 将浮点数格式转换成字符串形式
  因为时间戳仅包含当前时间数据，不包括日期数据，因此我们要借用datetime实现这一转换

```bash
>>> import time

>>> t_float = time.time()

>>> from datetime import datetime

>>> t = datetime.fromtimestamp(t_float)

>>> t

datetime.datetime(2019, 1, 9, 21, 25, 27, 296692)

>>> t_format = t.strftime("%Y-%m-%d %H:%M:%S")

>>> t_format

'2019-01-09 21:25:27'
```



##### 时间运算：

时间计算无非是比较差值。照理说比较差值比较简单，无非是加减算法，但因为格式不一样，就增加了很多不必要的麻烦。当然前人已经帮我们踩了很多的坑，代码示例我们官方的datetime包，就对此做了很好的支持，我们要转换成统一的格式，就只需要将调用datetime下的strptime即可

```bash
>>>from datetime import datetime

>>>t1 = datetime.strptime("2019/01/11 20:26:45", "%Y/%m/%d %H:%M:%S")

>>>t2 = datetime.strptime("2019-01-11 21:26:45", "%Y-%m-%d %H:%M:%S")

>>>t_delta = t2 - t1

>>>type(t1)

<type 'datetime.datetime'>

>>>t_delta

datetime.timedelta(0, 3600)

>>>t_delta.seconds

3600
```



值得一提的是datetime中的timedelta函数，可以很方便的计算日期时间，代码示例我们一直现在的日期，想要知道一周后的日期，就可以通过它来实现

```bash
>>> import datetime

>>> t_now = datetime.datetime.now()

>>> t_now

datetime.datetime(2019, 1, 11, 20, 39, 42, 15616)

>>> delta = datetime.timedelta(days=7)

>>> t_future = t_now + delta 

t_future

>>> datetime.datetime(2019, 1, 18, 20, 39, 42, 15616)
```



#### 第三方干货库

虽然官方给出的两个库已经满足了大部分的需求，但随着时间的推移，业务需求越来越复杂，官方的库，可能无法满足我们的项目需求。这时候就需要引入一些第三方库了，常见的有Maya、Arrow和Dateutil，一般我用Arrow就已经足够了，另外两个功能大同小异，有兴趣的朋友可以自己探索



我们经常因为业务的需要统计月度，季度或者年度的指标数据，这个时候用arrwo就非常方便了，他里面有三个重要的函数，第一个是floor，表示头部，第二个是tail，表示尾部，我们用它们可以很方便地得到日、周、月、季度、年度的开始和结尾；另外一个是shift，它则可以更加灵活地以日、周、月、季、年为单位得获取时间

```bash
>>> import arrow

>>> now = arrow.utcnow().to("local")

>>> now

<Arrow [2019-01-11T20:53:40.411946+08:00]>

>>> now.floor("day")

<Arrow [2019-01-11T00:00:00+08:00]>

>>> now.ceil("day")

<Arrow [2019-01-11T23:59:59.999999+08:00]>

>>> now.floor("month")

<Arrow [2019-01-01T00:00:00+08:00]>

>>> now.floor("year")

<Arrow [2019-01-01T00:00:00+08:00]>

>>> now.shift(days=-3)

<Arrow [2019-01-08T20:53:40.411946+08:00]>

>>> now.shift(days=-3).strftime("%Y-%m-%d %H:%M:%S")

'2019-01-08 20:53:40'

>>> now.shift(months=-3).strftime("%Y-%m-%d %H:%M:%S")

'2018-10-11 20:53:40'
```



#### 其他有趣补充

在探索日期时间的功能时，我发现有timedelta字段，觉得这个命名很有趣，于是查了下这个的delta，直译过来是三角洲的意思，一查维基是：



![python_datetime_9.png](/Users/zhangfei/growing/articles/python中最常用的日期时间/imgs/pic_1.png)



Delta（大写Δ，小写δ，中文音译：德尔塔、德耳塔）



Delta 是三角洲的英文，源自三角洲的形状像三角形，如同大写的“Δ”



发现非常有趣，原来命名是跟着人的感觉走的



#### 小结

![pic2](/Users/zhangfei/growing/articles/python中最常用的日期时间/imgs/pic_2.png)



1. 在学习的时候对自己不懂得东西，要花时间归纳总结，尤其是那些每次遇到都会卡壳的小问题，虽然每次花时间不多，但积累起来就浪费了大量的时间
2. 学习的过程中，可以对自己的好奇部分，花一点时间探索，有时候可能会收获意想不到的惊喜，代码示例这次的delta命名。但要注意时间的控制



#### 参考资料

[Converting Strings to datetime in Python](https://stackabuse.com/converting-strings-to-datetime-in-python/)

[time date datetme timestamp 傻傻分不清楚](https://cloud.tencent.com/developer/article/1378717)

[python 获取当年、季度、月、日的开始和结束时间](https://blog.csdn.net/tengdazhang770960436/article/details/79100931)

[Δ](https://zh.wikipedia.org/wiki/%CE%94)