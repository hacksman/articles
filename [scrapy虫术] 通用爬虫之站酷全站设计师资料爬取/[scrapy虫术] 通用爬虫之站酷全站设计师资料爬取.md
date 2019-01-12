
我们写多几个爬虫就会发现，其实有很多相同的模块，比如翻页，比如网络错误重试等。scrapy内部已经有非常完美的处理模块，我们只需要简单配置即可使用，还是接上一节我们的爬虫，这一次我们将它封装地更加强大。这次，我们做一个通用爬虫，实现随机请求头和换ip功能，除此之外将实现可配置化爬虫，也就是说，我们要爬取一个站点，只需要写必要的链接筛选和解析规则即可，而无需像之前那样写很多冗余的代码块。黑喂狗\~

### 工具环境
- 语言：python3.6
- 编辑器：Pycharm
- 数据库：MongoDB
- 框架：scrapy1.5.1

### 温馨提示：
阅读此文可能需要对scrapy框架有基本的了解，对xpath解析有一个基本的了解

### 爬取思路
爬取站点：[https://www.zcool.com.cn/ ][1]

我们需要的是每一个设计师的资料页面的信息，如下所示：

逻辑其实很简单：
1. 找到尽可能多的设计师
2. 找到他们的主页（作为跳板）
3. 点开详情页资料，开始爬取信息

	如果你有看过上一节的爬虫介绍，其实发现这一点也不难，不过是通过rule配置进行页面追踪，这里我们主需要找到尽可能的的设计师，这里我事先做过简单的调研，这里就不详细我找设计的过程了，最后是在更多，设计师那里找到的，加上首页每个作品的设计师，也有4000个，当然这里可能有很多重复的，但和全量设计师，我当时有爬过一次，当时好像是有公开设计师的总量，不知道是25W还是250W的注册设计师，这样算来的话，其实这4000设计师和25W根本不是一个量级的。那么我们就需要找别的入口，看哪里还尽可能可以找到很多的设计师

	这里有我已经发现的地方
- 第一个是设计师页面的不同类型的选项，还有按照城市区分的
- 设计师首页或作品也下面的访客和留言
- 每个设计师的关注对象和粉丝

我最后选择的是每个设计的关注和粉丝，因为对于第一个，我可能需要将每个城市的id记录在案，然后再进行了详细的拆分，生成根据城市和类型的自由组合，然后再将这些组合的url作为初始链接进行爬虫，相当于爬取之前要进行一步预处理，不太适合scrapy通用爬取的方法

访客和留言，大家可以通过调度页面分析功能，发现它其实并没有在html中实时展示，而是通过动态加载的方式调取信息，爬取的时候同样有限制，可能涉及解析json，考虑到要做通用爬虫，所以没有选择此种方式

最后每个设计师的关注对象和粉丝的方法，就非常简单直接，可能会丢失一些从来不关注的用户。只要是有关注别人基本可以找到


### show me the code

核心的功能模块我是照着大才哥的教程学习的，传送门丢给大家：

[https://juejin.im/post/5b026d53518825426b277dd5][2]

大家可以看一下大才哥的教程一步步实现，在此基础上，我增加了一个自动换请求头的功能和换代理的功能

#### 1. 随机请求头:

import random
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
class RandomUserAgentMiddleware(UserAgentMiddleware):
"""This middleware allows spiders to override the useragent"""

def init(self, settings, useragent='Scrapy'):
    super(RandomUserAgentMiddleware, self).init()
    self.useragent = useragent
    useragentfile = settings.get('USERAGENTLIST')
    if not useragentfile:
        ua = settings.get('USERAGENT', useragent)
        self.useragentlist = ua
    else:
        with open(useragentfile, 'r') as f:
            self.useragentlist = i.strip() for i in f.readlines()

@classmethod
def fromcrawler(cls, crawler):
    o = cls(crawler.settings)
    crawler.signals.connect(o.spideropened, signal=signals.spideropened)
    return o

def spideropened(self, spider):
    self.useragent = getattr(spider, 'useragent', self.useragent)

def processrequest(self, request, spider):
    useragent = random.choice(self.useragentlist)
    if self.useragent:
        request.headers.setdefault(b'User-Agent', useragent)


核心思路就是在settings内得到的user-agent的文件路径之地，之后再每次请求的时候，随机再其中抽取一个，如果没有拿到的话，就默认选择配置中的默认请求头

#### 2. 随机代理ip
类似的，我们在发起请求之前，先获得自己搭建好的ip代理服务，获得可用代理ip，我们只需要继承HttpProxyMiddleware模块的功能，替换ip即可，HttpProxyMiddleware已经为我们贴心地实现了诸如需要使用账号密码，http和https的使用等

完成它们之后，我们只需要根据要求，实现对应的items.py(需要提取的字段对象)、rules.py(对页面追踪逻辑的规则定义)、loaders.py(解析页面的处理)即可，如果要使用动态的url，例如初始需要指定多页面，那就需要配置一下urls.py

对应站酷网，核心的思路在上面的思路中已经结束，代码注释中有每一步的追踪步骤，不在赘述


'zcool': (
    # 追踪下一页
    Rule(LinkExtractor(restrictxpaths='//a@class="laypagenext"]')),
    # 提取如 https://www.zcool.com.cn/u/15472001 样式的页面
    Rule(LinkExtractor(allow='.www.zcool.com.cn\/u\/\d+$')),
    # 追踪 https://www.zcool.com.cn/designer 页面设计师主页的链接
    Rule(LinkExtractor(restrictxpaths='//a@z-st="usercontentcard1username"]')),
    # 追踪 https://www.zcool.com.cn/designer 筛选 | 推荐设计师 栏目的分页
    Rule(LinkExtractor(restrictxpaths='//astarts-with(@z-st, "desingerfilterrecommend")]')),
    # 追踪 https://www.zcool.com.cn/designer 筛选 | 不限职业 栏目的分页
    Rule(LinkExtractor(restrictxpaths='//astarts-with(@z-st, "desingerfilterprofession")]')),
    # 本来准备使用访客和留言来追踪的，后来发现页面是动态加载的，提取收到该信息，遂弃用
    # Rule(LinkExtractor(restrictxpaths='//a@class="usernick"')),
    # Rule(LinkExtractor(restrictxpaths='//a@class="visitor-name"')),
    # 追踪 粉丝页面
    Rule(LinkExtractor(allow='.?fans.')),
    # 追踪 关注页面
    Rule(LinkExtractor(allow='.?follow.')),
    # 追踪 设计师资料页，并回调给parseitem函数处理
    Rule(LinkExtractor(allow='.?profile.'), callback='parseitem'),
)


至此，一个通用的母体爬虫便制作完毕，之后如果用来爬反爬虫不是特别强的网站，一个爬虫也不过就是分析网站和做页面解析费点时间，做好这个之后，一个简单的页面爬虫，我初略估计不会超过半小时即可

现在我的爬虫还在提取中，目前单机采集速度大概在日采集5-6万的样子，如果要提速可以自己在配置中增加并发

[1]:	http://www.dytt8.net/
[2]:	https://juejin.im/post/5b026d53518825426b277dd5
