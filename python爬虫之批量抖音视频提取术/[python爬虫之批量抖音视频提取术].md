
假期正好有空闲时间，终于可以整理自己的笔记啦。整理到抖音视频的时候，就好麻烦，每次都要先把视频导出到本地，再给微信的文件管理助手，再下载传到印象笔记，一来二去浪费不少时间，想想这事不正好适合爬虫去干吗？于是就有了以下这篇内容

### 工具环境
- 语言：Python3.6
- 编辑器：Pycharm
- 数据库：MongoDB
- 工具：Charles

### 前言：
在使用Charles，你需要做一些基础的配置，将你的手机的网络代理到本地电脑，以便做进一步的抓包分析，以下两篇文章可能对你有所帮助

1. [https://www.jianshu.com/p/a3f005628d07][1]
2. [https://www.jianshu.com/p/68684780c1b0][2]

### 爬取思路
爬取站点：[https://www.douyin.com/ ][3]

这里的爬取思路非常简单，以至于我会觉得这篇文章会有些空洞。当你抓包正确配置好环境后，打开抖音软件，做一些简单的操作，Charles就会给你返回如下的数据，这些数据其实就是服务端给你返回的数据，里面包含所有我们需要的信息。比如我们今天要下载的自己点击过的，喜欢的视频链接等

你操作软件时，看一下Charles中每条数据的变化情况，你会发现，你个人主页下面的链跟videos、feed和likes和这三条数据有关，每一次你做相应的操作，下面就会多出一些请求链接


那我们别的先不管，看下每个请求中的数据，有没有我们想要的数据，随便看一下某个链接中的返回数据

可以看到这里有play\_add，再一看链接中有video字样，基本八九不离十了。因为我已经验证过了，这里的信息就是如我们猜测的那样，包含视频的全部信息

那我们其实就需要模拟这里的请求链接即可，先看下请求中都包含哪些必要的信息，你多看几个就发现，真正变化的就几个固定的参数，其中红线以上的部分都是和设备相关的信息和app信息，真正核心加密的参数就只有，mas，as和ts。这里我先自己网上找了下有没有相关的轮子可用，索性狗屎运比较好，正好找到了，地址在这：[https://github.com/AppSign/douyin][4]

套用即可，而且这位大佬的所有破解，都是和字节跳动有关的，我有点觉得这个就是官方让员工自己放出来的。按尼胃，我们拿到了加密的参数的实现之后，后面就太简单了

看上面那位大佬的代码提取视频那里，跟视频相关的关键参数就是这个aweme\_id，我们拿到它之后，后面直接构造提取原视频的请求即可。

那么废话不说，上码走起


### show me the code

#### 核心请求：


    def grabfavorite(self, userid, maxcursor=0):
        favoriteparams = self.FAVORITEPARAMS
        favoriteparams'userid'] = userid
        favoriteparams'maxcursor'] = maxcursor
        queryparams = {favoriteparams, self.commonparams}
        sign = getSign(self.gettoken(), queryparams)
        params = {queryparams, sign}
        resp = requests.get(self.FAVORITEURL,
                            params=params,
                            verify=False,
                            headers=self.HEADERS)

        favoriteinfo = resp.json()

        hasmore = favoriteinfo.get('hasmore')
        maxcursor = favoriteinfo.get('maxcursor')

        videoinfos = favoriteinfo.get('awemelist')

        for pervideo in videoinfos:
            authornickname = pervideo'author'.get("nickname")
            authoruid = pervideo'author'.get('uid')
            videodesc = pervideo.get('desc')
            downloaditem = {
                "authornickname": authornickname,
                "videodesc": videodesc,
                "authoruid": authoruid,
            }
            awemeid = pervideo.get("awemeid")
            self.downloadfavoritevideo(awemeid, downloaditem)
            time.sleep(5)

        return hasmore, maxcursor


这里我们将设备参数，app信息，用户一起用作查询参数，再与获得的token一起，发送给getSign函数，构造加密数据，最后把这些数据组合成的字典放在一起，请求我们的喜欢的链接（https://aweme.snssdk.com/aweme/v1/aweme/favorite/
）即可拿到对应的response数据。大家可能会发现，我这里漏掉了一个max\_cursor参数，这是因为，第一次发送请求时，这里的参数是0，之后我们请求了数据后，如果返回的has\_more是1，就代表有数据，那么下一次我们请求的时候，就需要带上上一次的max\_cursor。就可以理解为我们刷数据，往下翻页吧

所以这也就是为什么我在这个地方做了返回，就是为了方便上一层调用，看下这里如果有数据的话，我们就继续翻页下载

#### 翻页：

__FAVORITE_URL              = ""
    def grabfavoritemain(self, userid):
        count = 1
        self.logger.info("当前正在爬取第 👉 {} 👈 页内容...".format(count))
        hasmore, maxcursor = self.grabfavorite(userid)
        while hasmore:
            count += 1
            self.logger.info("当前正在爬取第 👉 {} 👈 页内容...".format(count))
            hasmore, maxcursor = self.grabfavorite(userid, maxcursor)


我们在第一次请求后得到是否有数据的状态和max\_cursor参数，那就简单了，如果我们发现有更多数据，就继续请求即可

#### 视频下载

    def grabfavoritemain(self, userid):
        count = 1
        self.logger.info("当前正在爬取第 👉 {} 👈 页内容...".format(count))
        hasmore, maxcursor = self.grabfavorite(userid)
        while hasmore:
            count += 1
            self.logger.info("当前正在爬取第 👉 {} 👈 页内容...".format(count))
            hasmore, maxcursor = self.grabfavorite(userid, maxcursor)
    def downloadfavoritevideo(self, awemeid, videoinfos):
        videocontent = self.downloadvideo(awemeid)
        authornickname = videoinfos.get("authornickname")
        authoruid = videoinfos.get("authoruid")
        videodesc = videoinfos.get("videodesc")
        videoname = "".join(authornickname, authoruid, videodesc)

        self.logger.info("downloadfavoritevideo 正在下载视频 {} ".format(videoname))

        if not videocontent:
            self.logger.warn("你正在下载的视频，由于某种神秘力量的作用，已经凉凉了，请跳过...")
            return

        with open("../videos/{}.mp4".format(videoname), 'wb') as f:
            f.write(videocontent)

    def downloadvideo(self, awemeid, retrytimes=0):
        queryparams = self.commonparams
        queryparams'awemeid'] = awemeid

        sign = getSign(self.gettoken(), queryparams)
        params = {queryparams, sign}

        postdata = {
            "awemeid": awemeid
        }

        resp = requests.get(self.VIDEODETAILURL,
                            params=params,
                            data=postdata,
                            verify=False,
                            headers=self.HEADERS)
        respresult = resp.json()
        playaddrraw = respresult'awemedetail']'video''playaddr''urllist'

        content = requests.get(playaddr).content

        return content


类似的，我们构造了sign签名之后，请求视频获取链接，传入对应的aweme\_id即可拿到我们想要的视频数据，最后直接以二进制的形式写入文件即可。文件名我这里是用的用户昵称、用户唯一id和视频描述，如果觉得太长，大家也可以自己改成自己想要的文件名

最后开启爬虫，就可以得到如下结果


以上实现爬取自己抖音喜欢过的所有视频的步骤，小伙伴们可以自己完整走一遍过程，或者直接拷贝我在github上的代码地址，注意user\_id要改成你自己的哦，
另外后续我这个仓库会增加更多有趣实用的爬虫，欢迎大家给星，有什么问题可以向我反馈，一起学习进步



[1]:	https://www.jianshu.com/p/a3f005628d07
[2]:	https://www.jianshu.com/p/68684780c1b0
[3]:	http://www.dytt8.net/
[4]:	https://github.com/AppSign/douyin
