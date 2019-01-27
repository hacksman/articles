#### 什么是GraphQL



GraphQL 是一种面向 API 的查询语言。在互联网早期，互联网的需求都以 Web 为主，那时候数据和业务需求都不复杂，所以用 RestAPI 的方式完全可以满足需求。但是随着互联网的发展，数据量增大，业务需求多变。还有各种客户端需要接口适配，基于 RestAPI 的方式，显得越来呆板，因此 GraphQL 便应运而生。它至少可以提供以下三个方面的优势



1. GraphQL 提供更方便的 API 查询

不同的客户端有时候需要返回的数据格式不同，之前使用 RestAPI 的方式，需要后端针对每一个客户端提供单独的接口。随着业务需求的增加，维护的成本随机呈指数级跃升。而使用 GraphQL 就比较开心了，只需要写一套接口即可



2. 解决前后端过于依赖

在开发的过程中，前端需要和后端反反复复确认各个字段，防止到时候开发到一半，因为没有对好字段，要大块大块地改代码。现在有 GraphQL 就比较方便了，你需要什么类型的字段，就自己写对应的查询语法



3. 节约网络和计算机内存资源

之前通过 RestAPI 的方式写接口，有一个很大的问题在于，对于接口的定义，需要前期做大量的工作，针对接口做各种力度的拆分，但即使这样，也没办法应对需求的风云突变。有时候需要返回的仅仅是某个用户的某一类型的数据，但不得不把该用户的其他信息也一并返回来，这既浪费了网络的资源，也消耗了计算机的性能。显然不够优雅，GraphQL 再一次证明了它的强大，它能够提供 DIY 获取所需要的数据，用多少，拿多少，可以说是相当环保了



PS : 更多 GraphQL 的介绍可以看文末的参考资料



#### 介绍



这篇文章，我将用一个具体的 Todo List 实例，和大家一起，一步步手动搭建一个 GraphQL + MongoDB 的项目实例。我们将会在其中用到以下库，开始之前需要提前安装好：



1. graphene_mongo
2. graphene
3. mongoengine
4. flask_graphql
5. Flask



在开始之前，我们来梳理一下我们的核心需求，我们要建立一个 Todo List 产品，我们核心的表只有两个，一个是用户表，存储所有的用户信息，另外一个是任务表，存储着所有用户的任务信息。任务表通过用户 id 与对应的用户关联。表结构对应的是一对多的关系，核心的数据字段如下： 



task表

```json
{ 
    "_id" : ObjectId("5c353fd8771502a411872712"), 
    "_in_time" : "2019-01-09 08:26:53", 
    "_utime" : "2019-01-09 09:26:39", 
    "task" : "read", 
    "start_time" : "2019-01-09 08:26:53", 
    "end_time" : "2019-01-09 08:26:53", 
    "repeat" : [
        "Wed"
    ], 
    "delete_flag" : NumberInt(0), 
    "user" : "1"
}
```



user表

```
{ 
    "_id" : "1", 
    "_in_time" : "2019-01-09 08:39:16", 
    "_utime" : "2019-01-09 09:23:25", 
    "nickname" : "xiao hong", 
    "sex" : "female", 
    "photo": "http://xh.jpg",
    "delete_flag" : NumberInt(0)
}
```



#### 项目结构



一图胜千言，为更清晰的了解项目的整体结构，我将项目的整体目录结构打印下来，小伙伴们可以参照着目录结构，看接下来的搭建步骤



```
----task_graphql\
    |----api.py
    |----database\
    |    |----__init__.py
    |    |----base.py
    |    |----model_task.py
    |    |----model_user.py
    |----requirements.txt
    |----schema.py
    |----schema_task.py
    |----schema_user.py
```

![pic_1](/Users/zhangfei/growing/articles/GraphQL搭配MongoDB入门项目实战/imgs/pic_1.png)



- user_model 和 task_model 定义数据模块，直接数据库 mongo 对接
- 上层定义的 schema 操作 shema_user 和 schema_task 对数据 model 进行增删改查操作
- 最后 flask 搭建对外的 api 服务实现和外界的请求交互



#### 创建数据模型



我们的数据模型结构非常简单

- user_model 列出所有的用户信息
- task_model 列出所有的任务信息，通过user字段与用户表关联，表示该任务归属于哪一个用户

![pic_2](/Users/zhangfei/growing/articles/GraphQL搭配MongoDB入门项目实战/imgs/pic_2.png)





##### base.py

```python
from mongoengine import connect

connect("todo_list", host="127.0.0.1:27017")
```

只需要通过调用 mongoengine 的 connect 指定对应的数据库链接信息和数据库即可，后面直接引入至Flask模块会自动识别连接



##### model_user.py

```python
import sys
sys.path.append("..")

from mongoengine import Document
from mongoengine import (StringField, IntField)
from datetime import datetime


class ModelUser(Document):

    meta = {"collection": "user"}

    id = StringField(primary_key=True)
    _in_time = StringField(required=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    _utime = StringField(required=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    nickname = StringField(required=True)
    sex = StringField(default="unknown", required=True)
    delete_flag = IntField(default=0, required=True)
```

所要定义的数据文档都通过 mongoengine 的 Document 继承，它可以将对应字段转换成类属性，方便后期对数据进行各种操作，meta 字段指定对应的你需要链接的是哪张 mongo 表



##### model_task.py

```python
import sys
sys.path.append("..")

from mongoengine import Document
from mongoengine import (StringField, ListField, IntField, ReferenceField)

from .model_user import ModelUser
from datetime import datetime


class ModelTask(Document):

    meta = {"collection": "task"}
    
    _in_time = StringField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), required=True)
    _utime = StringField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), required=True)
    task = StringField(default="", required=True)
    start_time = StringField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), required=True)
    end_time = StringField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), required=True)
    repeat = ListField(StringField(required=True))
    delete_flag = IntField(default=0, required=True)
    user = ReferenceField(ModelUser, required=True)
```

其中 required 表示这个字段是必须字段，default 可以设置该字段的默认值。ReferenceField 可以指定和哪个模型相关联，这里指定的是 ModelUser 字段，关联默认为对应 mongo 表中的 _id 字段



#### 创建GraphQL查询

现在我们已经将数据库和模型部分的连接功能完成了，接下来创建 API 部分，在我们的 task_graphql 目录下，有两个文件，schema_task.py 和 schema_user.py 分别将 model_task 和 model_user 类映射成 Graphene schema对象



##### schema_task.py

```python
from database.model_task import ModelTask
from graphene_mongo import MongoengineObjectType

import graphene
import schema_user

from datetime import datetime


class TaskAttribute:
    id = graphene.ID()
    _in_time = graphene.String()
    _utime = graphene.String()
    task = graphene.String()
    start_time = graphene.String()
    end_time = graphene.String()
    repeat = graphene.List(graphene.String)
    delete_flag = graphene.Int()
    user = graphene.String()


class Task(MongoengineObjectType):

    class Meta:
        model = ModelTask


class TaskNode(MongoengineObjectType):
    class Meta:
        model = ModelTask
        interfaces = (graphene.relay.Node, )
```



##### schema_user.py

```python
from database.model_task import ModelTask
from graphene_mongo import MongoengineObjectType

import graphene

from datetime import datetime

class TaskAttribute:
    id = graphene.ID()
    _in_time = graphene.String()
    _utime = graphene.String()
    task = graphene.String()
    start_time = graphene.String()
    end_time = graphene.String()
    repeat = graphene.List(graphene.String)
    delete_flag = graphene.Int()
    user = graphene.String()

class Task(MongoengineObjectType):

    class Meta:
        model = ModelTask

class TaskNode(MongoengineObjectType):
    class Meta:
        model = ModelTask
        interfaces = (graphene.relay.Node, )
```



现在我们创建一个 schema.py 的文件，把刚才定义好的 schema_task.py 和 schema_user.py 文件引入进来，定义两个对外访问的接口

- tasks: 查询所有任务信息，返回一个list
- users: 查询所有用户信息，返回一个list

```python
import schema_user
import schema_task
import graphene
from graphene_mongo.fields import MongoengineConnectionField


class Query(graphene.ObjectType):

    node = graphene.relay.Node.Field()

    tasks = MongoengineConnectionField(schema_task.TaskNode)

    users = MongoengineConnectionField(schema_user.UserNode)

schema = graphene.Schema(query=Query)
```



#### 创建 Flask 应用

在主目录下创建一个 api.py 文件，将我们之前定义好的数据库连接和 schema 引入进来，用 Flask 的 add_url_rule 方法将两者关联起来，为了方便访问，我们通过引入 flask_graphql 的 GraphQLView 方法，将接口可视化出来，方便调试



```python
from flask import Flask
from schema import schema
from flask_graphql import GraphQLView
from database.base import connect
from logger import AppLogger

log = AppLogger("task_graphql.log").get_logger()

app = Flask(__name__)
app.debug = True

app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
```



到这里，我们就已经用 graphql 成功创建了一个可查询的 Todo List 接口，接下来。我们可以用它来测试一下查询接口吧。然后在开始查询之前大家需要自己 mock 点数据到 mongo 里面



![image-20190127112537893](/Users/zhangfei/growing/articles/GraphQL搭配MongoDB入门项目实战/imgs/pic_3.png)



我们访问接口地址(http://127.0.0.1:5000/graphql)，来查询一下看看效果

![pic_4](/Users/zhangfei/growing/articles/GraphQL搭配MongoDB入门项目实战/imgs/pic_4.png)



#### 添加 GraphQL 更新方法（mutation）

GraphQL 官方将更新创建操作，全部整合在 mutation 下，它包含了插入和更新数据功能，接下来我们就继续上面的操作，将这部分功能完善



##### schema_task.py

```python
from database.model_task import ModelTask
from graphene_mongo import MongoengineObjectType

import graphene

from datetime import datetime


class TaskAttribute:
    id = graphene.ID()
    _in_time = graphene.String()
    _utime = graphene.String()
    task = graphene.String()
    start_time = graphene.String()
    end_time = graphene.String()
    repeat = graphene.List(graphene.String)
    delete_flag = graphene.Int()
    user = graphene.String()


class Task(MongoengineObjectType):

    class Meta:
        model = ModelTask


class TaskNode(MongoengineObjectType):
    class Meta:
        model = ModelTask
        interfaces = (graphene.relay.Node, )


class CreateTaskInput(graphene.InputObjectType, TaskAttribute):
    pass


class CreateTask(graphene.Mutation):

    task = graphene.Field(lambda: TaskNode)

    class Arguments:
        input = CreateTaskInput(required=True)

    def mutate(self, info, input):
        task = ModelTask(**input)
        task.save()
        return CreateTask(task=task)


class UpdateTask(graphene.Mutation):

    task = graphene.Field(lambda: TaskNode)

    class Arguments:
        input = CreateTaskInput(required=True)

    def mutate(self, info, input):
        id = input.pop("id")
        task = ModelTask.objects.get(id=id)
        task._utime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task.update(**input)
        task.save()
        return UpdateTask(task=task)
```



##### schema_user.py

```python
from database.model_user import ModelUser
from graphene_mongo.types import MongoengineObjectType
import graphene
from datetime import datetime


class UserAttribute:
    id = graphene.String()
    _in_time = graphene.String()
    _utime = graphene.String()
    nickname = graphene.String()
    photo = graphene.String()
    sex = graphene.String()
    delete_flag = graphene.Int()


class User(MongoengineObjectType):

    class Meta:
        model = ModelUser


class UserNode(MongoengineObjectType):

    class Meta:
        model = ModelUser
        interfaces = (graphene.relay.Node, )


class CreateUserInput(graphene.InputObjectType, UserAttribute):
    pass


class CreateUser(graphene.Mutation):

    user = graphene.Field(lambda: UserNode)

    class Arguments:
        input = CreateUserInput(required=True)

    def mutate(self, info, input):
        user = ModelUser(**input)
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):

    user = graphene.Field(lambda: UserNode)

    class Arguments:
        input = CreateUserInput(required=True)

    def mutate(self, info, input):
        id = input.pop("id")
        user = ModelUser.objects.get(id=id)
        user._utime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user.update(**input)
        user.save()
        return UpdateUser(user=user)
```

一看代码便知，我们将需要添加的信息，通过input传入进来，然后将对应的参数进行映射即可。我们再通过实例看下创建数据的效果

![pic_5](/Users/zhangfei/growing/articles/GraphQL搭配MongoDB入门项目实战/imgs/pic_5.png)



我们再来试下修改数据的操作，like this

 

![pic_6](/Users/zhangfei/growing/articles/GraphQL搭配MongoDB入门项目实战/imgs/pic_6.png)



bingo！！！



至此，我们通过 GraphQL 搭配 MongoDB 的操作就完美收关了。

完整项目请查看 github: https://github.com/hacksman/task_graphql_demo

以上都是自己一路踩过了很多坑之后总结出的方法，如有疏漏，还望指正



#### 参考资料

- [Flask-Graphene-SQLAlchemy](https://github.com/alexisrolland/flask-graphene-sqlalchemy)
- [[译] 我经常听到的 GraphQL 到底是什么？](https://juejin.im/post/58fd6d121b69e600589ec740)
- [Explaining GraphQL Connections](https://blog.apollographql.com/explaining-graphql-connections-c48b7c3d6976)
- [GraphQL & Relay 初探](https://juejin.im/post/5aaba1b86fb9a028cb2d645a)







