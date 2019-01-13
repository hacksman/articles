
在日常开发的时候，我们经常会遇到时间处理的问题，代码示例爬虫过来的时间处理，代码示例对库内的数据进行时间维度的统计等。虽然是个很简单的东西，但每次用的时候都难免要再查一查，其实这就是基础不夯实的表现。趁着今天有空，总结一下开发过程中，最最最常见的日期时间格式和操作



# 常见日期时间类型

| 类型      | 格式         | 示例                |
| --------- | ------------ | :------------------ |
| time      | 时间格式     | 17:54:03            |
| date      | 日期格式     | 2019-01-09          |
| datetime  | 日期时间格式 | 2019-01-09 17:54:03 |
| timestamp | 时间戳格式   | 1547035707.229842   |

<center>右滑可看到示例</center>





# 日期时间对象的格式

- 对象格式（即struct_time对象格式）


==代码示例==：

![code_1.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/code_1.png)



- 字符串格式：


==代码示例==：

![code_2.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/code_2.png)



- 浮点数格式：

==代码示例==：

![code_3.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/code_3.png)





# 常见操作

我们一观察便知，其实struct_time对象和浮点数格式，都不是面向人类友好的格式，一般我们会将它们往字符串形式转换



## 格式转换：

- 将struct_time转换成字符串形式

==代码示例==：

![code_4.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/code_4.png)



- 将浮点数格式转换成字符串形式
  因为时间戳仅包含当前时间数据，不包括日期数据，因此我们要借用datetime实现这一转换

==代码示例==：

![code_5.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/code_5.png)



## 时间运算：

时间计算无非是比较差值。照理说比较差值比较简单，无非是加减算法，但因为格式不一样，就增加了很多不必要的麻烦。当然前人已经帮我们踩了很多的坑，代码示例我们官方的datetime包，就对此做了很好的支持，我们要转换成统一的格式，就只需要将调用datetime下的strptime即可

==代码示例==：

![code_6.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/code_6.png)



值得一提的是datetime中的timedelta函数，可以很方便的计算日期时间，代码示例我们一直现在的日期，想要知道一周后的日期，就可以通过它来实现

==代码示例==：

![code_7.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/code_7.png)



# 第三方干货库

虽然官方给出的两个库已经满足了大部分的需求，但随着时间的推移，业务需求越来越复杂，官方的库，可能无法满足我们的项目需求。这时候就需要引入一些第三方库了，常见的有Maya、Arrow和Dateutil，一般我用Arrow就已经足够了，另外两个功能大同小异，有兴趣的朋友可以自己探索



我们经常因为业务的需要统计月度，季度或者年度的指标数据，这个时候用arrwo就非常方便了，他里面有三个重要的函数，第一个是floor，表示头部，第二个是tail，表示尾部，我们用它们可以很方便地得到日、周、月、季度、年度的开始和结尾；另外一个是shift，它则可以更加灵活地以日、周、月、季、年为单位得获取时间

==代码示例==：

![code_8.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/code_8.png)



# 其他有趣补充

在探索日期时间的功能时，我发现有timedelta字段，觉得这个命名很有趣，于是查了下这个的delta，直译过来是三角洲的意思，一查维基是：



![pic_1.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/pic_1.png)



Delta（大写Δ，小写δ，中文音译：德尔塔、德耳塔）

Delta 是三角洲的英文，源自三角洲的形状像三角形，如同大写的“Δ”



发现非常有趣，原来命名是跟着人的感觉走的



# 小结

![pic_2.png](https://raw.githubusercontent.com/hacksman/articles/master/python中最常用的日期时间/imgs/pic_2.png)

1. 在学习的时候对自己不懂得东西，要花时间归纳总结，尤其是那些每次遇到都会卡壳的小问题，虽然每次花时间不多，但积累起来就浪费了大量的时间
2. 学习的过程中，可以对自己的好奇部分，花一点时间探索，有时候可能会收获意想不到的惊喜，代码示例这次的delta命名。但要注意时间的控制



# 参考资料

1. Converting Strings to datetime in Python
2. time date datetme timestamp 傻傻分不清楚
3. python 获取当年、季度、月、日的开始和结束时间
4. Δ