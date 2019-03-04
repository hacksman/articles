

2019年03月02日 天气晴 



今天是我来到这个世界的第9557天，也是单身的第9557天。今年回家见老妈，被下了死命令，今年再不带一个回去，我可能要就要露宿街头了。



![WechatIMG1409](/Users/zhangfei/growing/articles/imgs/WechatIMG1409.png)



平时就蓬头垢面写代码，哪有时间撩妹啊。现在已经到三月份了，看了下公司的需求，已经排到了7月中旬，照这个趋势看，脱单？是不可能脱单的！这辈子都不可能脱单的！！！旁友那哥们为这事焦头烂额，就给我介绍一软件：一周CP，🤩打开新世界大门，里面有好多小姐姐，关键我没时间玩啊。不过我转念一想，找对象不过就是个算术题嘛，接触的人越多，找到对象的概率越大。所以，这周末，不吃饭也得把软件破解了，只要破解了加密算法，就可以让它自动给小姐姐点赞，增加自己的曝光率，想来靠谱，上，怼它。为脱单奋斗！



#### 工具环境

- 语言：Python
- 编辑器：Pycharm
- 数据库：MongoDB
- 工具：Charles、apktool、dex2jar、JD-GUI



#### 实现思路

思路非常简单，我们首先需要登录账户（你得注册一个），然后到达广场页面，在软件的推荐栏目下，实现对不同的小姐姐进行点赞。上面已经介绍过了，我们只需要增加自己的曝光，不要对别人进行私信打扰，一方面容易被封号，另外一方面如果你的主页有内容，你点赞别人，别人对你感兴趣进而主动联系你，你的脱单的成功率会更高。（备注：建议自己的主页分享点你的兴趣爱好，展现你自己是个有趣的童鞋吧）

![image-20190304084641206](/Users/zhangfei/growing/articles/脱单日记：一周CP反爬虫破解点赞小姐姐/imgs/image-20190304084641206.png)



首先你需要获取账号登录过程中的关键信息，一般加密无外乎token、sign、cookies这些信息，我们通过Charles挂一下代理看看登录过程中的信息，搜索一下关键词token，就发现token和其他一些关键参数啦



![WechatIMG1415](/Users/zhangfei/growing/articles/脱单日记：一周CP反爬虫破解点赞小姐姐/imgs/WechatIMG1415.png)



接下来我们深入分析，在点击广场页面，分析网页发出了核心需求，我们多试几个接口就发现，里面有两个几个核心的参数，一个是请求时，request请求头上的Token字段，经过比对我们发现这个是登录的时候给出的access_token字段



![WechatIMG1413](/Users/zhangfei/growing/articles/脱单日记：一周CP反爬虫破解点赞小姐姐/imgs/WechatIMG1413.png)



接下来我们发现一个特殊的字段sign。这个字段每一次请求时，都在不断的变化，因此我猜测这个是在服务端进行了加密，然后每次请求的时候需要进行加密计算。这里我们进行反编译，然后查看它的混淆代码，发现果不其然，这部分在服务端进行了加密。具体的实现步骤限于篇幅就先不介绍了，毕竟涉及别人的机密，我这里实现了一个接口供大家调用，大家关注公众号：鸡仔说，回复【cp】关键词可获得唯一的破解校验码，然后你可以通过请求接口http://wx.zxiaoji.com/cp， 并传入你刚才获得的唯一校验码，自己的 secret_key、access_token、以及调用时参数，就可以拿到sign参数对小姐姐进行点赞，并引起小姐姐的关注啦



#### show me the code

```python
def get_moment_list(self):
    self.log.info("开始采集动态页")
    params = {
        "num": 20,
        "start": 0,
        "timestamp": int(time.time()),
        "type": "recommend",
        "user_id": self.user_id,
        "last_object_id": "",
    }
	
    # 获取sign
    sign = self.__get_sign(params)
    if not sign:
        return
    params["sign"] = sign
    # 这里的 self.__START_URL 就是刷新首页的请求
    resp = self.request.get(self.__START_URL, params=params, verify=False)
    resp_json = resp.json()
    return resp_json
```



这里我们实现了一个简单的功能——刷新广场页，来自五湖四海的小姐姐都是从这个入口进来的，所以你可以每次在这里刷新页面，然后对小姐姐们进行点赞



```python
def like_sex(self, post_data, sex=2, exclude_cp=True):
    """
    :param fid: 文章id
    :param sex: 性别，默认2，即性别为女
    :return:
    """
	# 如果是cp组，则不进行点赞
    is_cp = post_data.get('left_user', None)
    if exclude_cp and is_cp:
        self.log.info("过滤掉cp组")
        return False
    # 如果是话题栏，也不进行点赞
    category = post_data.get("category")
    if category == "topic":
        self.log.info("过滤掉话题..")
        return False
	
    # 文章唯一id
    fid = post_data.get("fid")
    # 用户昵称
    nick_name = post_data["user"].get("nickname")
    # 发布的文字
    post_text = post_data["payload"].get("text")

    # 如果在 mongo 已经找到这条数据，说明你已经对这条动态进行过点赞，不再点赞
    mongo_exists = self.__update_like_mongo(fid, nick_name, post_text)
    if mongo_exists == -1:
        self.log.info("之前已对这条数据点过赞了，跳过...")
        return False

    raw_sex = post_data["user"].get('sex')

    if raw_sex == sex:
        fid_params = {
            "cancel": "0",
            "fid": fid,
            "timestamp": "0",
            "user_id": self.user_id,
        }
        sign = self.__get_sign(fid_params)
        if not sign:
            return False
        fid_params["sign"] = sign
        # 发起对小姐姐进行点赞的请求
        resp = self.request.get(self.__LIKE_PID_URL, params=fid_params, verify=False)
        resp_json = resp.json()
        if resp_json.get("message") == "success":
            nick_name = post_data["user"].get("nickname")
            post_text = post_data["payload"].get("text")
            self.log.info("给用户({})发布的【{}】点赞成功".format(nick_name, post_text))
            return True
```



这里的逻辑也很简单，就是对指定性别的人进行点赞（默认是小姐姐），这里也过滤掉了CP组，当然你也可以自己额外开发新的功能，自己拓展，丰衣足食



```python
def start(self, *args, **kwargs):
    count = 0
    like_count = 0
    while True:
        count += 1
        moment_data = self.get_moment_list()
        like_count_batch = 0
        for per_post in moment_data["data"]["list"]:
            like_succeed = self.like_sex(per_post)
            if like_succeed:
                like_count_batch += 1
                like_count += 1
            time.sleep(random.randint(1, 2))
            if like_count % 100 == 0:
                self.log.info("当前已经对 {} 位小姐姐点过赞了...".format(like_count))
        self.log.info("当前已经遍历了第 {} 次动态".format(count))
        time.sleep(random.randint(7*like_count_batch, 10*like_count_batch))
        now = datetime.datetime.now()
        # 晚上 2点至6 点之间不进行点赞
        if now.hour in range(2, 6):
            time.sleep(random.randint(3600, 4000))
```



这里的逻辑就是不断的刷新主页信息，然后对广场上的异性（也可以设置为同性）进行疯狂点赞。如果因此获得了幸福，请毫不客气地回来给我打钱，哈哈哈，小伙伴们加油



你可以自己改造功能，当然也可以直接调用项目，传入指定的参数即可



核心参数如下

```python
# 通过登录时抓包获取，以下为示范数据，与真实数据可能有些许差异
secret_key = "423dabf849172d8a15342710cc3211220"

# 通过登录时抓包获取，以下为示范数据，与真实数据可能有些许差异
token = "1576511283920896_6364131_1573704298_86dbaf32dc852651de5c8a5bfcac7bc7"

# 通过登录时抓包获取，以下为示范数据，与真实数据可能有些许差异
user_id = "7314332"

# 通过关注公众号【鸡仔说】回复【cp】获取，以下为示范数据，与真实数据可能有些许差异
check_code = "odyvBt5OiGhR72FBF2AnMnCa_Dt3"
```

![image-20190304090633590](/Users/zhangfei/growing/articles/脱单日记：一周CP反爬虫破解点赞小姐姐/imgs/image-20190304090633590.png)

![image-20190304192610608](/Users/zhangfei/growing/articles/脱单日记：一周CP反爬虫破解点赞小姐姐/imgs/image-20190304192610608.png)



在Python3.6版本（或以上版本），终端下输入命令行👇👇👇

```python
python lanuch_cp_spider.py --secrite_key 423dabf849172d8a15342710cc3211220 --token 1576511283920896_6364131_1573704298_86dbaf32dc852651de5c8a5bfcac7bc7 --user_id 7314332 --check_code odyvBt5OiGhR72FBF2AnMnCa_Dt3
```

输出如下

```bash
2019-03-01 09:16:07,680 INFO yizhoucp_crawl.py get_moment_list:80 开始采集动态页
2019-03-01 09:16:08,712 INFO yizhoucp_crawl.py like_sex:141 给用户(不甜。)发布的【今天杭州有太阳！！】点赞成功
2019-03-01 09:16:10,920 INFO yizhoucp_crawl.py like_sex:141 给用户(会是你好友吗)发布的【早上好啊啊啊！！！】点赞成功
2019-03-01 09:16:15,170 INFO yizhoucp_crawl.py like_sex:141 给用户(九九)发布的【💔 
男人的嘴骗人的鬼💔 
我现在很崩溃💔 
我现在只想大哭一场💔】点赞成功
2019-03-01 09:16:16,547 INFO yizhoucp_crawl.py like_sex:141 给用户(好难)发布的【  我对你就算再好，在你眼里都认为并不重要。回首去看你以往的感情经历，反而那些玩弄你感情的人，你在以后的岁月里遇到好狗，继续吃你喜欢的东西。】点赞成功
2019-03-01 09:16:17,885 INFO yizhoucp_crawl.py like_sex:141 给用户(哈娜)发布的【☀️晴天        
                      ————周杰伦】点赞成功
2019-03-01 09:16:19,071 INFO yizhoucp_crawl.py like_sex:141 给用户(无言)发布的【哼╭(╯^╰)╮
都没有一个真心谈恋爱的小哥哥
我要沉迷学习无法自拔了……】点赞成功
2019-03-01 09:16:23,329 INFO yizhoucp_crawl.py like_sex:141 给用户(你会剥石榴么)发布的【早🤭】点赞成功
2019-03-01 09:16:25,586 INFO yizhoucp_crawl.py like_sex:141 给用户(X)发布的【奔现成功🏃
正式官宣❤】点赞成功
2019-03-01 09:16:26,587 INFO yizhoucp_crawl.py like_sex:107 过滤掉cp组
2019-03-01 09:16:29,820 INFO yizhoucp_crawl.py like_sex:141 给用户(Charon)发布的【反正你没女朋友 叫我声宝贝怎么了】点赞成功
```



看👆👆👆，至此已经实现对小姐姐进行点赞【PS：如果要对小哥哥进行点赞，需要自己改一下日志和性别项哦】， 记住，找对象就是个算术题，你曝光的越多，就越容易引起小姐姐的注意，早日脱单。不说了，我先去撩妹叻~



完整的项目请移步GitHub查看，如果项目对小伙伴们有帮助或启发，请在GitHub上给了star支持下吧，先谢过啦！



