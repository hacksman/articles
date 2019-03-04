说明：本文主要以理解 Python 中的赋值、参数传递运行机制为主，可能其中的观点不一定严谨，如果有不对的地方，还望指出，先谢过啦



在学习编程的过程我们都会遇到很多定义，之前在遇到这些定义的时候，我有一种强迫症。就是不搞清楚每一个字的含义，不善罢甘休。但是每次都会尽兴而来，失望而归。多次之后我学乖了，就是不纠结实际每一个字的含义，用自己能懂的方式理解他们，比如今天要说的引用传递和值传递



官方的定义是这样的



值传递：

> 值传递是指在调用函数时将实际参数复制一份传递到函数中，这样在函数中如果对参数进行修改，将不会影响到实际参数 —— via：百度百科



> 引用传递：
>
> 引用传递是指在调用函数时将实际参数的地址传递到函数中，那么在函数中对参数所进行的修改，将影响到实际参数—— via：百度百科



这种每一个字我都认识，但连起来我就不知道啥意思的感觉，已经伴随了我这个9年+4年教育生涯，至此对它深恶痛绝。



#### 赋值



回到正题，我们暂时抛开两个概念，我们先来说下 Python 中的赋值，以我的理解，其实就是下定义的步骤，如果大家看过《武林外传》中第二十九集《吕圣人智斗姬无命 佟掌柜火拼展红绫》，就更容易理解以下的概念了



![pic_1.png](https://raw.githubusercontent.com/hacksman/articles/master/你真的理解Python中的赋值、传参吗？/imgs/53e050f9ececd14d2a3b4d1f84b2f820c1efd892.jpg)



赋值这个操作，其实可以理解成给物体贴标签，或者可以理解为给物体命名，既然是名称，就像《武林外传》中的一样，你可以叫“姬无命”，我也可以叫“姬无命”。重要的是这个物体，而不是标签。其中，这个标签（或者名称），我们在计算机中把它叫做变量，物体就是实际的值



我们知道，在计算机中，值会占用一定的空间去存储，而计算机为了方便找到它，则会给它一个地址，方便我们找到它

![pic_2.png](https://raw.githubusercontent.com/hacksman/articles/master/你真的理解Python中的赋值、传参吗？/imgs/image-20190216173433318.png)





我们写段代码理解下



```bash
>>> zxj = "张小鸡"
>>> jwm = zxj
>>> print(id(zxj))
4334207504
>>> print(id(jwm))
4334207504
```

![pic_3.png](https://raw.githubusercontent.com/hacksman/articles/master/你真的理解Python中的赋值、传参吗？/imgs/image-20190216174843243.png)



看图理解很简单，这里的物体是字符“张小鸡”，我们把它贴上标签“zxj”，第二个地方赋值就相当于再贴一个标签“jwm”。就是上面说的，你可以叫“张小鸡”，我也可以叫“张小鸡”，看后面，他们实际上的内存地址都是一样的



#### 参数传递



在理解了上面的过程，我们再来看看 Python 中调用函数传递参数的过程。先说结论，Python 中参数的传递就是赋值的过程。我们来看下这段代码



```python
a = "张小鸡"

def foo(b):
    print ">>> before id(b):", id(b)
    b = "姬无命"
    print ">>> after id(b):", id(b)

print ">>> before id(a):", id(a)
foo(a)
print ">>> after id(a):", id(a)
```

这一段的输出如下

```bash
>>> before id(a): 4301385520
>>> before id(b): 4301385520
>>> after id(b): 4301385040
>>> after id(a): 4301385520
```



![pic_4.png](https://raw.githubusercontent.com/hacksman/articles/master/你真的理解Python中的赋值、传参吗？/imgs/image-20190216181026372.png)

我们在赋值时，其实就相当于把函数的形参b这个标签又贴在了“张小鸡”物体上。后面我们再执行b=“姬无命”时，就相当于把b这个标签从“张小鸡”这个物体上撕下来，放到“姬无命”这个物体上



#### 可变和不可变对象



Python 内部对对象进行了区分，即为可变对象和不可变对象，类型如下

 

int、str、float、tuple等为不可变对象

list、dict、set等为可变对象



不可变对象我们上面已经说过他的赋值的特点，我们这里主要看可变对象。对于可变对象，我们可以简单的理解为做了个包装盒。我们在赋值的时候，这个标签是贴在了这个包装盒子上。计算机会记录这个盒子的地址，里面每一个物体的地址，计算机也仍然会记录



![pic_5.png](https://raw.githubusercontent.com/hacksman/articles/master/你真的理解Python中的赋值、传参吗？/imgs/image-20190216182413554.png)





```python
a = ["张小鸡"]

def foo(b):
    print(">>> before id(b):", id(b))
    b[0] = "姬无命"
    b.append("Tom")
    print(">>> after id(b):", id(b))

print(">>> before value(a):", a)
print(">>> before id(a):", id(a))
foo(a)
print(">>> after value(a):", a)
print(">>> after id(a):", id(a))
```

输出如下

```bash
>>> before value(a): ['张小鸡']
>>> before id(a): 4518129480
>>> before id(b): 4518129480
>>> after id(b): 4518129480
>>> after value(a): ['姬无命', 'Tom']
>>> after id(a): 4518129480
```

我们将盒子里面的“张小鸡”替换为“姬无命”，又再盒子里面添加了“Tom”，自始至终，因为我们没有动过盒子本身，所以他的地址不会发生变化



![pic_6.png](https://raw.githubusercontent.com/hacksman/articles/master/你真的理解Python中的赋值、传参吗？/imgs/image-20190217084946345.png)



结合上图来看下，我们修改一下代码，再深入看下盒子和盒子里面物体的地址的变化

```python
a = ["张小鸡"]

def foo(b):
    b[0] = "姬无命"
    b.append("Tom")

print(">>> before id(a): ", id(a))
print(">>> before id(a[:]): ", [id(_) for _ in a])
foo(a)
print(">>> after id(a): ", id(a))
print(">>> after id(a[:]): ", [id(_) for _ in a])
```

输出如下

```bash
>>> before id(a):  4471127880
>>> before id(a[:]):  [4472230896]
>>> after id(a):  4471127880
>>> after id(a[:]):  [4472230992, 4472127648]
```



看，我们的盒子（即id(a)）自始至终都没有变化，而内部因为更换过物体，所以里面的地址都不一样了



#### 拓展思考

```python
def foo(a, b=[]):
    b.append(a)
    return b

print(foo(1))
print(foo(1))
print(foo(1))
```

上面这段代码的输出结果是

```bash
>>> [1]
>>> [1, 1]
>>> [1, 1, 1]
```



能说说为什么会发生这样的怪现象吗？并想一想这个特性的应用场景有哪些？欢迎评论留言给我



#### 参考资料



[Python参数传递，既不是传值也不是传引用](https://zhuanlan.zhihu.com/p/35959581)

[python函数传参是传值还是传引用？](https://www.cnblogs.com/loleina/p/5276918.html)

[python可变和不可变对象](https://www.jianshu.com/p/c5582e23b26c)

