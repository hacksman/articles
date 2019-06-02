**鸡仔说：**做大数据开发的朋友一定用过 Hadoop 这个工具，它是一款支持数据密集型的分布式应用程序。Hadoop 基于分布式档案系统和 MapReduce 技术，通过节点分工的模式把海量的数据处理工作分发至多台机器上，再将每台机器处理的结果汇总整合。虽然它的逻辑原理并不复杂（即简单的分治思想），但其中要攻克的技术难点却颇多，比如早期备受诟病的安全问题、文件存储压缩问题等。能开发出这样一个工具的人，必定有他的过人之处，那么接下来就跟鸡仔一起来了解被誉为 Hadoop 之父的 Doug Cutting，他到底是何许人也？又有哪些值得我们学习的地方呢？



#### 学计算机可以尽早还清贷款

Doug 来自加利福利亚纳帕谷的农村，1981 年他考上了斯坦福大学。虽然考上了大学，但家庭并不富裕的 Doug 却喜忧参半。只有借助贷款，他才能负担起学费

![640](/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640.jpeg)

斯坦福大学

在斯坦福，Doug 学习了语言学和计算机相关的课程。他觉得计算机课程很有趣，更重要的是，他发现学习计算机可以帮他尽早还清贷款。因此，临近毕业之际，他没有选择继续求学深造，而是在施乐公司（看过《乔布斯传》的朋友应该对这所公司有所了解，这家公司在当时非常有名，它的主要研究领域是印刷相关的技术。）找了一份薪水不错的工作，他的工作内容是进行自然语言处理和人工智能相关的研究，借此他也有幸参与了在当时比较新潮的一个领域——搜索

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (1).jpeg)](/Users/zhangfei/Desktop/640 (1).jpeg)

施乐的工作环境



#### 见证搜索行业的崛起

在谷歌之前，有不少公司曾对搜索领域做过探索，而这些公司在 Google 之后都被遗忘了。施乐就是其中的一员，它可以说是搜索领域的先驱。当然，他们对搜索的探索，重点围绕着自己的主业开展

我们都知道，施乐一直从事打印、复印相关的业务，他们当时研究的方向是如何将纸制品电子化。而纸制品电子化面临的主要问题，除了如何正确地识别纸制品上的文字外，还要保证如何快速检索这些已电子化的文件资料，Doug 当时从事的主要是后一项工作。这段时间的工作经验积累，让他在搜索技术的广度和深度上都得到了极大的提升

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (2).jpeg)](/Users/zhangfei/Desktop/640 (2).jpeg)

施乐的豆袋会议室

之后不久，随着网络时代到来，以雅虎为代表的基于网络搜索的公司如雨后春笋一样涌现出来。Doug 见证了整个搜索行业的崛起，当时，为了便于用户检索互联网信息，雅虎采用的方案是分类整合，就是说每当有人新建立一个网站，雅虎便将它添加到雅虎的网站库目录中，然后再将网站分成金融、新闻、体育、娱乐等板块

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (3).jpeg)](/Users/zhangfei/Desktop/640 (3).jpeg)

雅虎中国首页

雅虎的这个方案虽然能够帮助人们快速找到对应需求的站点，但无法精细地帮助用户找到自己的个性化需求。这时候谷歌出现了，它采用的是基于 PageRank 的搜索算法，可以精准地定位人们的检索目标，帮助人们找到想要的结果。就凭着这点关键的技术创新，谷歌搜索业务迎来了发展的飞跃期

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (4).jpeg)](/Users/zhangfei/Desktop/640 (4).jpeg)

PageRank算法简化图解



#### 两次练手收获两个开创性工具

Doug 虽然在施乐公司已积累了不少搜索技术的经验，但他探索的搜索技术都是基于离线环境的，因此数据量级不可能很大。Doug 感觉它的技术经验有点纸上谈兵。于是在 1997 年底，Doug 决定利用业余时间写一个开源项目，他在家以每周两天的时间投入开发，不久之后，便诞生了第一个开源文本搜索函数库——Lucene

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (5).jpeg)](/Users/zhangfei/Desktop/640 (5).jpeg)

Lucene logo

Google 的高速发展让 Doug 产生了危机，他担心日益减少的网络搜索引擎可能让信息检索行业出现新的商业垄断。Doug 于是着手与同事一起开发出了 Nutch，这是第一个与 Google 进行竞争的大型开源网络搜索引擎项目。Nutch 虽然开发出来了，但和之前一样，Nutch 工具依然没有经历过实战检验，Doug 接下来要做的，是在大量级的数据下，对 Nutch 进行压测。但大数据压测就意味着要采购大量的设备和数据。但 Doug 当时待业在家，并没有足够的财力购买这些设备和数据

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (6).jpeg)](/Users/zhangfei/Desktop/640 (6).jpeg)

Nutch 架构示意图



#### Hadoop 比 Webmap 快 33 倍

就在 Doug 为测试困扰时，Google 随即发布了一份研究报告，报告中介绍了两款 Google 为了支持自家产品而研发的软件平台，一个是 GFS（即 Google File System），用于存储不同设备产生的海量数据。另外一个是 MapReduce，它在 GFS 上工作，用于分布式大规模数据处理。基于这两个平台，Doug 开发出了大名鼎鼎的 Hadoop

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (7).jpeg)](/Users/zhangfei/Desktop/640 (7).jpeg)

Hadoop logo



这就解决了困扰 Doug 很久的压测问题，之前可能需要一台超级计算机才能完成的工作，现在只需要将任务分布在几台廉价的计算机上同样可以完成。Doug 对 Google 的开源大加赞赏「我们开始设想用 4-5 台电脑来实现这个项目，但在实际运行中牵涉了大量繁琐的步骤需要靠人工来完成。Google 的平台让这些步骤得以自动化，为我们实现整体框架打下了良好的基础。」

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (8).jpeg)](/Users/zhangfei/Desktop/640 (8).jpeg)

MapReduce 工作流简化图



出于时间成本的考虑，Doug 决定结束自己的自由职业生涯。以此来进一步完善他的 Hadoop 项目。他先找了 IBM ，但 IBM 对他早期的 Lucene 项目更感兴趣。就在此时，雅虎的负责人 Raymie Stata 热情邀请他加入雅虎公司并马上对搜索业务项目进行优化改造。加入雅虎后，Doug 如虎添翼，他有一支一百人的团队帮他完善 Hadoop 项目，这大大加速了 Hadoop 项目的发展。不久之后，雅虎就将它的搜索业务架构迁移到 Hadoop 上来。两年后，雅虎启动了基于 Hadoop 的第一项目 Webmap——一个用来计算网页间链接关系的算法。迁移项目至 Hadoop 的成效立竿见影，在相同的硬件环境下，基于 Hadoop 的 Webmap 的反应速度是之前系统的 33 倍



#### 新身份，新征程

虽然 Hapdoop 极大地提高了雅虎的搜索性能，但当时的雅虎是热锅上的蚂蚁。内部管理，产品定位，技术服务等诸多问题无法得到解决，雅虎的局面实在是江河日下了。由于公司只关注产品，却不想在技术上有过多的投入，Doug 于是跳槽到了 Cloudera

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (9).jpeg)](/Users/zhangfei/Desktop/640 (9).jpeg)

Cloudera logo

Cloudera 是为某些公司提供技术服务和咨询的平台，它的客户多来自传统行业。传统行业的客户有大量的数据，但不知道如何合理地使用它们，这正好与 Doug 想在 Hadoop 平台处理更大量的数据的想法不谋而合，在这里他有大量的客户业务数据，辅助他更好地完善 Hadoop 项目。值得一提的是，在 Doug 服务传统企业的过程中，越来越多的互联网巨头也开始加入了 Hadoop 的队伍（如 Facebook、eBay、LinkedIn 等），Hadoop 的团队无形之中被进一步扩大了

目前， 除了作为 Hadoop 之父外，Doug 还有另外一个身份——Cloudera 首席架构师。Cloudera 可以说是 Hadoop 生态圈最知名的公司了，它的核心产品是为客户搭建基于 Hadoop 的大数据平台，帮助企业安装、配置、运行 Hadoop 以便处理海量的数据

![640 (/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/640 (10).jpeg)](/Users/zhangfei/Desktop/640 (10).jpeg)

Cloudera 版本衍化



谈到目前 Hadoop 的发展趋势，Doug 很是意外 「我从没有想过，Hadoop 除了搜索引擎，还能在其它方面发挥作用，它如今的受关注程度，已经完全超过了我之前的想象。」

![faces.dougcutting24180.web_](/Users/zhangfei/growing/articles/Hadoop 之父：普通程序员到顶级公司 CTO 的进阶之路/imgs/faces.dougcutting24180.web_.jpg)

Doug Cutting

谈及他的成功事迹，Doug 觉得主要归功于两点：热情。他喜欢攻克技术难题带来的成就感，他非常享受自己的程序被千万人使用的感觉。另外一个就是脚踏实地。Doug 的所有成就都是他一点一滴积累来的，头顶青天脚踏实地，时间会给人最好的嘉奖

希望 Doug Cutting 的故事对你能有所启发。最后邀请你思考一下 👇👇👇



\- 今日互动 -

**正如 Doug 所言，成功是源于对技术的热情**

**那么我们在日常的工作中，又该如何保持热情呢？**



欢迎在评论区发表你的看法

 撰文 | 张小吉

 校稿 | 小麦童鞋