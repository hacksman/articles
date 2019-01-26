#### 前言

人喜欢为自己的错误，找各种借口开脱。本周做算法题leetcode《394.字符串解码》的时候遇到了这样的问题，题目需要完成：s = "3[a]2[bc]", 返回 "aaabcbc"。实现的过程中，需要判断一个字符串是否为数字，几乎条件反射地，打算自己实现一个从0-9的字符串list，然后判断字符是否在里面。实现如下：



```python
num_check = list(map(lambda x: str(x), range(10)))

a = "3"

if a in num_check:
	print "this is num"
```



而python内置的库，已经帮你实现了这个功能了。最最最致命的是，我之前已经用过这个方法了，但是在实际使用的时候，我没有用上。我大可以说，这个是粗心，就和考试的时候一样，问什么数字平方等于4，我只写了个2，然后因此丢了-2那半分，但我知道，这其实就是基础不夯实的体现。是一种凭借直接经验获取知识的思维方式。毕竟python字符串判断方法，在日常开发中，用的比较少，因此被我忽视掉了。为了避免以后再犯类似的错误，就趁此机会捡起烂笔头。总结一下该知识点，防止以后再忘记



##### 1.startswith | 判断是否以某字符串开头



示例：

```bash
>>> "Brevity is the soul of wit".startswith("B")
True

>>> "Brevity is the soul of wit".startswith("Bre")
True

>>> "Brevity is the soul of wit".startswith("Ber")
False

# 支持元组等可迭代类型，其中有元素匹配上即可
>>> "Brevity is the soul of wit".startswith(("Bre", "Ber"))
True

# 判断索引[1, 3)中的元素，值是否为"re"
>>> "Brevity is the soul of wit".startswith("re", 1, 3)
True

```



##### 2.endswith | 判断是否以某字符串结尾



示例：

```bash
>>> "Brevity is the soul of wit".endswith("t")
True

>>> "Brevity is the soul of wit".endswith("T")
False

# 当存在索引匹配时，只根据索引位置进行匹配
>>> "Brevity is the soul of wit".endswith("re", 1, 3)
True

>>> "Brevity is the soul of wit".endswith("wi", -3, -1)
True

# 负数切片到0时，不会遵从整数规律，过0不会往初始位置移动
>>> "Brevity is the soul of wit".endswith("wit", -3, 0)
False

>>> "Brevity is the soul of wit".endswith("wi", -3, 0)
False

```



##### 3.isupper | 判断是否至少存在一个大写字母，且所有字母均大写



示例：

```
>>> "Brevity".isupper()
False

>>> "BREVITY".isupper()
True

>>> "BREVITY你好".isupper()
True

>>> "BREVITY你好\n".isupper()
True

>>> "BREVITY你好\n123".isupper()
True

>>> "BREVITY你好  \n123".isupper()
True

>>> "你好".isupper()
False

>>> "".isupper()
False

```



##### 4.islower | 判断是否至少存在一个小写字母，且所有字母均小写



示例：

```
>>> "Brevity".islower()
False

>>> "brevity".islower()
True

# 其他类似示例与isupper方法相仿，不再列举
```



##### 5.isdigit | 判断是否全部为非负整数



示例：

```bash
>>> "".isdigit()
False

>>> " 1".isdigit()
False

>>> "1".isdigit()
True

>>> "1.1".isdigit()
False

>>> "-1".isdigit()
False

>>> "12".isdigit()
True

>>> "0".isdigit()
True

>>> "1\n".isdigit()
False

>>> "一".isdigit()
False

>>> u"一".isdigit()
False

```



##### 6.isalpha | 判断是否全部为字母



示例：

```bash
>>> "a".isalpha()
True

>>> "Aa".isalpha()
True

>>> "A a".isalpha()
False

>>> "A\na".isalpha()
False

>>> "A你a".isalpha()
False

```



##### 7.isalnum | 判断是否全部为非负整数或字母（即 isdigit or isalpha）



示例：

```
>>> "a".isalnum()
True

>>> "1".isalnum()
True

>>> "A1".isalnum()
True

>>> "A 1".isalnum()
False

>>> "A\n1".isalnum()
False

>>> "-1".isalnum()
False

>>> "1.1".isalnum()
False

>>> "".isalnum()
False

```



##### 8.isspace | 判断是否全为空格（包含制表符）



示例：

```bash
>>> "a".isspace()
False

>>> " ".isspace()
True

>>> "".isspace()
False

>>> "a ".isspace()
False

>>> "\n ".isspace()
True

>>> "\n\t\r ".isspace()
True

>>> "\n\t\f ".isspace()
True

```



##### 9.istitle | 判断是否为首字母大写（忽略非字母字符）



示例：

```bash
>>> "Brevity is the soul of wit".istitle()
False

>>> "Brevity Is The Soul Of Wit".istitle()
True

>>> "Brevity 1Is The Soul Of Wit".istitle()
True

>>> "Brevity 1234Is The Soul Of Wit".istitle()
True

>>> "Brevity你1234Is The Soul Of Wit".istitle()
True

>>> "Brevity你1234is The Soul Of Wit".istitle()
False

>>> "Brevity你1234Is a The Soul Of Wit".istitle()
False

>>> "Brevity Is The Soul Of WIT".istitle()
False

```



##### 10.isdecimal | 判断是否全为阿拉伯数字非负整数（只接受unicode形式输入）



示例：

```bash
>>>"1".isdecimal()
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'str' object has no attribute 'isdecimal'

>>> b"1".isdecimal()
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'str' object has no attribute 'isdecimal'

>>> u"1".isdecimal()
True

# 支持全角输入识别
>>> u"１".isdecimal()
True

>>> u"一".isdecimal()
False

>>> u"Ⅳ".isdecimal()
False

>>> u"2²".isdecimal()
False

>>> u"2 ".isdecimal()
False

>>> u"-1".isdecimal()
False

>>> u"⅕".isdecimal()
False

```



##### 11.isnumeric | 判断是否全为非负整数（只接受unicode形式输入）



示例：

```bash
>>> "1".isnumeric()
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'str' object has no attribute 'isnumeric'

>>> b"1".isnumeric()
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'str' object has no attribute 'isnumeric'

>>> u"1".isnumeric()
True

>>> u"1²".isnumeric()
True

>>> u"⅕".isnumeric()
True

>>> u"一".isnumeric()
True

>>> u"Ⅳ".isnumeric()
True

>>> u"-1".isnumeric()
False

>>> u"一千".isnumeric()
True

>>> u"壹仟".isnumeric()
True

>>> u"六十兆柒仟三百二十一".isnumeric()
True

>>> u"三".isnumeric()
True

>>> u"三 ".isnumeric()
False

```



以上就是python2中的字符判断函数集合，python3中引入了两个新的字符判断函数，让字符判断功能更加强大



##### 12.isidentifier | 判断是否为python内部关键字或有效标志符



示例：

```bash
>>> "def".isidentifier()
True

>>> "with".isidentifier()
True

>>> "Brevity".isidentifier()
True

>>> "_Brevity".isidentifier()
True

>>> "__Brevity".isidentifier()
True

>>> "___Brevity".isidentifier()
True

>>> "Brevity is".isidentifier()
False

>>> " is".isidentifier()
False

>>> " ".isidentifier()
False

>>> "".isidentifier()
False

```



##### 13.isprintable | 判断是否可打印（包括空字符串）



示例：

```
>>>"".isprintable()
True

>>>" ".isprintable()
True

>>>" \b".isprintable()
False

>>>" \n".isprintable()
False

>>>" \t".isprintable()
False

>>>"1 000".isprintable()
True

>>>"1, 000".isprintable()
True

```



##### 14.isascii() | 判断是否为ascii码【American Standard Code for Information Interchange (美国信息交换标准码)】



延展阅读：[维基百科-ASCII](https://zh.wikipedia.org/wiki/ASCII)



示例：

```bash
>>> "1".isascii()
True

>>> u"1".isascii()
True

>>> b"1".isascii()
True

>>> "1,000".isascii()
True

>>> "1 000".isascii()
True

>>> "1.1".isascii()
True

>>> "二".isascii()
False

>>> "`".isascii()
True

>>> "】".isascii()
False

>>> "]".isascii()
True
```



#### 参考资料

- [The Python Standard Library » String Methods](https://docs.python.org/3/library/stdtypes.html#str.upper)

- [python内置字符串处理变量整理](https://blog.csdn.net/qq_34857250/article/details/78808824)
- [Python: isdigit() vs. isdecimal()](https://www.webucator.com/blog/2015/02/python-isdigit-vs-isdecimal/)
- [python中str函数isdigit、isdecimal、isnumeric的区别](https://www.cnblogs.com/jebeljebel/p/4006433.html)
- [Python 的内置字符串方法（收藏专用）](https://segmentfault.com/a/1190000004598007#articleHeader38)

