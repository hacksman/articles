#### 前言

人喜欢为自己的错误，找各种借口开脱。本周做算法题leetcode《394.字符串解码》的时候遇到了这样的问题，题目需要完成：s = "3[a]2[bc]", 返回 "aaabcbc"。实现的过程中，需要判断一个字符串是否为数字，几乎条件反射地，打算自己实现一个从0-9的字符串list，然后判断字符是否在里面。实现如下：



![code_0.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (0).png)



而python内置的库，已经帮你实现了这个功能了。最最最致命的是，我之前已经用过这个方法了，但是在实际使用的时候，我没有用上。我大可以说，这个是粗心，就和考试的时候一样，问什么数字平方等于4，我只写了个2，然后因此丢了-2那半分，但我知道，这其实就是基础不夯实的体现。是一种凭借直接经验获取知识的思维方式。毕竟python字符串判断方法，在日常开发中，用的比较少，因此被我忽视掉了。为了避免以后再犯类似的错误，就趁此机会捡起烂笔头。总结一下该知识点，防止以后再忘记



##### 1.startswith | 判断是否以某字符串开头



示例：

![code_1.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (1).png)



##### 2.endswith | 判断是否以某字符串结尾



示例：

![code_2.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (2).png)



##### 3.isupper | 判断是否至少存在一个大写字母，且所有字母均大写



示例：

![code_3.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (3).png)



##### 4.islower | 判断是否至少存在一个小写字母，且所有字母均小写



示例：

![code_4.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (4).png)



##### 5.isdigit | 判断是否全部为非负整数



示例：

![code_5.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (5).png)



##### 6.isalpha | 判断是否全部为字母



示例：

![code_6.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (6).png)



##### 7.isalnum | 判断是否全部为非负整数或字母（即 isdigit or isalpha）



示例：

![code_7.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (7).png)



##### 8.isspace | 判断是否全为空格（包含制表符）



示例：

![code_8.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (8).png)



##### 9.istitle | 判断是否为首字母大写（忽略非字母字符）



示例：

![code_9.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (9).png)



##### 10.isdecimal | 判断是否全为阿拉伯数字非负整数（只接受unicode形式输入）



示例：

![code_10.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (10).png)



##### 11.isnumeric | 判断是否全为非负整数（只接受unicode形式输入）



示例：

![code_11.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (11).png)



以上就是python2中的字符判断函数集合，python3中引入了三个新的字符判断函数，让字符判断功能更加强大



##### 12.isidentifier | 判断是否为python内部关键字或有效标志符



示例：

![code_12.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (12).png)



##### 13.isprintable | 判断是否可打印（包括空字符串）



示例：

![code_13.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (13).png)



##### 14.isascii() | 判断是否为ascii码【American Standard Code for Information Interchange (美国信息交换标准码)】



延展阅读：[维基百科-ASCII](https://zh.wikipedia.org/wiki/ASCII)



示例：

![code_14.png](https://raw.githubusercontent.com/hacksman/articles/master/一文详解Python字符串条件判断方法/imgs/carbon (14).png)



#### 参考资料

- [The Python Standard Library » String Methods](https://docs.python.org/3/library/stdtypes.html#str.upper)

- [python内置字符串处理变量整理](https://blog.csdn.net/qq_34857250/article/details/78808824)
- [Python: isdigit() vs. isdecimal()](https://www.webucator.com/blog/2015/02/python-isdigit-vs-isdecimal/)
- [python中str函数isdigit、isdecimal、isnumeric的区别](https://www.cnblogs.com/jebeljebel/p/4006433.html)
- [Python 的内置字符串方法（收藏专用）](https://segmentfault.com/a/1190000004598007#articleHeader38)

