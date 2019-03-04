



假设你去面试 Python 开发岗，面试官如果对基础比较看重的话，那么很可能会问你这样的问题



“谈谈你对 Python 中的浅拷贝和深拷贝的理解？”



若平时你在开发中像我一样，过度使用 deepcopy，以至于忘记了浅拷贝（shallow copy）和深拷贝（deep copy）的区别，那很可能要栽大跟头了。建议在读这篇文章之前，看下我之前写的文章[《你真的理解Python中的赋值、传参吗？》](http://www.zxiaoji.com/?p=473)，它有助于你更快的理解本文



#### Python 的引用计数

首先我们要知道，Python 内不可变对象的内存管理方式是引用计数。因此，我们在谈论拷贝时，其实谈论的主要特点都是基于可变对象的。我们来看下面这段代码



![carbon.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon.png)



输出如下



![carbon_1.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon (1).png)

![pic_1.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/image-20190217160609047.png)

因为我们这里操作的是不可变对象，Python 用引用计数的方式管理它们，所以 Python 不会对值相同的不可变对象，申请单独的内存空间。只会记录它的引用次数



#### 浅拷贝

我们先来比较一下浅拷贝和赋值在可变对象上的区别



![carbon_2.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon (2).png)

输出结果

![carbon_3.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon (3).png)

![pic_2.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/image-20190217162327378.png)

发现没有，赋值就是对物体进行贴标签操作，作用于同一物体。而浅拷贝则会创建一个新的对象，至于对象中的元素，它依然会引用原来的物体，我们再来看一段例子



![carbon_4.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon (4).png)

输出如下

![carbon_5.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon (5).png)



![pic_3.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/image-20190217170908126.png)



操作不可变对象时，由于引用计数的特性，被拷贝的元素改变时，就相当于撕掉了原来的标签，重新贴上新的标签一样，对于我们已拷贝的元素没有任何影响。因此在操作不可变对象时，浅拷贝和深拷贝是没有区别的



![carbon_6.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon (6).png)

输出结果

![carbon_7.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon (7).png)

![pic_4.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/image-20190217175458807.png)

由于浅拷贝会使用原始元素的引用（内存地址）。所以在在操作被拷贝对象内部的可变元素时，其结果是会影响到拷贝对象的



#### 深拷贝



深拷贝遇到可变对象，则又会进行一层对象创建，所以你操作被拷贝对象内部的可变对象，不影响拷贝对象内部的值



![carbon_8.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon (8).png)

输出如下

![carbon_9.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/carbon (9).png)

![pic_5.png](https://raw.githubusercontent.com/hacksman/articles/master/5张图彻底理解Python中的浅拷贝与深拷贝/imgs/image-20190217181758479.png)

#### 总结

因此，在下次我们遇到这类问题时，我们说出以下关键点，基本就很稳了

1. 由于 Python 内部引用计数的特性，对于不可变对象，浅拷贝和深拷贝的作用是一致的，就相当于复制了一份副本，原对象内部的不可变对象的改变，不会影响到复制对象
2. 浅拷贝的拷贝。其实是拷贝了原始元素的引用（内存地址），所以当拷贝可变对象时，原对象内可变对象的对应元素的改变，会在复制对象的对应元素上，有所体现
3. 深拷贝在遇到可变对象时，又在内部做了新建了一个副本。所以，不管它内部的元素如何变化，都不会影响到原来副本的可变对象



#### 参考资料

[图解python中赋值、浅拷贝、深拷贝的区别](https://www.cnblogs.com/eczhou/p/7860668.html)

[Python中 copy, deepcopy 的区别及原因](https://iaman.actor/blog/2016/04/17/copy-in-python#copydifference)