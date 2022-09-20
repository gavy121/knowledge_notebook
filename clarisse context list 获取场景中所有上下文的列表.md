# clarisse context list 获取场景中所有上下文的列表
[获取场景中所有上下文的列表](https://forum.isotropix.com/viewtopic.php?f=21&t=3929&sid=5f50434cd43b7257c9efb473f5eb51a5)
-----------------------------------------------------------------------------------------------------------

https://forum.isotropix.com/viewtopic.php?f=21&t=3929

如何使用python列出场景中存在的所有上下文？  
问候..

[1111](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=15328&sid=5f50434cd43b7257c9efb473f5eb51a5)

**帖子：**  1

**加入时间：**  2017 年 12 月 24 日星期日 9:42 pm

* * *

### [回复：获取场景中所有上下文的列表](#p16347)

[![](https://forum.isotropix.com/styles/isotropix2016/imageset/icon_post_target_unread.gif)
](https://forum.isotropix.com/viewtopic.php?p=16347&sid=5f50434cd43b7257c9efb473f5eb51a5#p16347)通过**[bvaldes](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=13171&sid=5f50434cd43b7257c9efb473f5eb51a5)** » 2018 年 5 月 3 日星期四下午 4:15

您好，

抱歉回复晚了。看看这个代码片段：

#### 蟒蛇代码

```
def getSubContext(context = ix.get\_current\_context(), recursive = True):   
 """  
 此函数返回包含在作为参数的上下文中的所有上下文的列表。  
 如果 'context' 参数为空，则起点是当前Clarisse 中的上下文 @arg context: 搜索的起点。如果你想为整个项目提供 'project:/' 作为参数  
 @arg recusive: 如果你想在 sub 的子上下文中查找，请将其设置为 True -context。如果你只想要第一个孩子，设置为False @return：找到的所有上下文的列表。 示例：  
 getSubContext() => 将返回当前上下文中的所有上下文。还包括子上下文  
 getSubContext('project:/') => 将返回整个项目中的所有上下文  
 getSubContext('project:/', False) => 将返回 'project:/' 中包含的第一级上下文  
 """   
 result = \[\]   
 context = ix.get\_item(str(context))   
 sub\_contexts = \[\]   
 for i in range(context.get\_context\_count()):   
 result.append(context.get\_context(i))   
 sub\_contexts.append(context.get\_context(i) )  
 如果递归：  
 while len(sub\_contexts)>0:   
 workOn = sub\_contexts   
 sub\_contexts = \[\]   
 for context in workOn:   
 for i in range(context.get\_context\_count()):  
 sub\_contexts.append(context.get\_context(i))   
 result.append(context.get\_context(i))  
 返回结果 
```

如果您需要帮助，请随时提出。问候，

Benoit VALDES  
Isotropix  
Clarisse QA

[![](https://forum.isotropix.com/download/file.php?avatar=13171_1481033212.png)
](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=13171&sid=5f50434cd43b7257c9efb473f5eb51a5)  
[巴尔德斯](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=13171&sid=5f50434cd43b7257c9efb473f5eb51a5)

**帖子：**  384

**加入时间：**  2016 年 9 月 26 日星期一上午 10:44

* * *

### [回复：获取场景中所有上下文的列表](#p18893)

[![](https://forum.isotropix.com/styles/isotropix2016/imageset/icon_post_target_unread.gif)
](https://forum.isotropix.com/viewtopic.php?p=18893&sid=5f50434cd43b7257c9efb473f5eb51a5#p18893)通过**[jeroendesmet](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=10694&sid=5f50434cd43b7257c9efb473f5eb51a5)** » 2019 年 1 月 30 日，星期三 7:10 pm

你好！

所以我尝试使用这个 getSubContext 函数，乍一看似乎工作正常......

我想检查一个特定的上下文是否已经存在，如果不存在，则创建该上下文。  
如果它确实存在，请不要创建它。这是为了避免让 Clarisse 创建一个具有不同名称的新上下文（如 context、 context2  
等）

列表...它不起作用。

代码：[全选](#)

`contexts = getSubContext("project://ASSETS")

######## THIS WORKS #########  
for c in contexts:  
    print c

####### THIS DOESN'T ########  
testList = ['project://ASSETS/context1', 'project://ASSETS/context2']

for t in testList:  
    if t in contexts:  
        print ("context exists >> " + t)  
    else:  
        print ("context doesn\'t exist >> " + t)

`

所以在我的场景中，我创建了一个上下文“资产”，并在其中创建了 2 个上下文：“上下文 1”和“上下文 2”。  
所以：[project://ASSETS/context1](project://ASSETS/context1) [project://ASSETS/context2](project://ASSETS/context2)有了这个设置，我正在运行上面的脚本......它应该打印一个“上下文存在”，因为它在testList ......但是它没有不。任何想法？我在这里想念什么？谢谢！！J。

  

[杰罗恩德斯梅特](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=10694&sid=5f50434cd43b7257c9efb473f5eb51a5)

**帖子：**  19

**加入时间：**  2014 年 11 月 15 日星期六晚上 9:08

* * *

### [回复：获取场景中所有上下文的列表](#p18896)

[![](https://forum.isotropix.com/styles/isotropix2016/imageset/icon_post_target_unread.gif)
](https://forum.isotropix.com/viewtopic.php?p=18896&sid=5f50434cd43b7257c9efb473f5eb51a5#p18896)通过**[ayanik](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=10734&sid=5f50434cd43b7257c9efb473f5eb51a5)** » 2019 年 1 月 30 日，星期三 8:00 pm

Hoi Jeroen，

看起来您正在将字符串与 OfContext 对象进行比较。我的工具包中有两个脚本，类似于上面发布的脚本，一个用于递归上下文，一个用于项目。下面我修改了我的脚本以满足您的需求。我现在无法测试它，因为我不在我的电脑和手机上。

代码：[全选](#)

`def get_sub_contexts(ctx, search="", max_depth=0, current_depth=0):  
    """Gets all subcontexts."""  
    current_depth += 1  
    results = []  
    for i in range(ctx.get_context_count()):  
        sub_context = ctx.get_context(i)  
        results.append(sub_context)  
        # 0 is infinite  
        if current_depth <= max_depth or max_depth == 0:  
            for result in get_sub_contexts(sub_context, name, max_depth, current_depth):  
                if result not in results:  
                    results.append(result)  
    if search:  
        for sub_ctx in results:  
            if str(sub_ctx) == search:  
                return sub_ctx  
        return []  
    return results

def get_items(ctx, kind=(), max_depth=0, current_depth=0, return_first_hit=False):  
    """Gets all items recursively."""  
    result = []  
    items = ix.api.OfItemVector()  
    sub_ctxs = get_sub_contexts(ctx, max_depth=max_depth, current_depth=current_depth)  
    sub_ctxs.insert(0, ctx)  
    for sub_ctx in sub_ctxs:  
        if sub_ctx.get_object_count():  
            objects_array = ix.api.OfObjectArray(sub_ctx.get_object_count())  
            flags = ix.api.CoreBitFieldHelper()  
            sub_ctx.get_all_objects(objects_array, flags, False)  
            for i_obj in range(sub_ctx.get_object_count()):  
                if kind:  
                    for k in kind:  
                        if objects_array[i_obj].is_kindof(k):  
                            if return_first_hit:  
                                return objects_array[i_obj]  
                            items.add(objects_array[i_obj])  
                else:  
                    items.add(objects_array[i_obj])  
    for item in items:  
        result.append(item)  
    return result

`

[阿亚尼克](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=10734&sid=5f50434cd43b7257c9efb473f5eb51a5)

**帖子：**  91

**加入时间：**  2014 年 11 月 26 日，星期三 9:10 pm

* * *

### [回复：获取场景中所有上下文的列表](#p18897)

[![](https://forum.isotropix.com/styles/isotropix2016/imageset/icon_post_target_unread.gif)
](https://forum.isotropix.com/viewtopic.php?p=18897&sid=5f50434cd43b7257c9efb473f5eb51a5#p18897)通过**[jeroendesmet](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=10694&sid=5f50434cd43b7257c9efb473f5eb51a5)** » 2019 年 1 月 30 日，星期三 8:15 pm

你好！

谢谢回复。今天晚些时候我会看看。

似乎我也可以通过创建一个新列表并将每个项目（或 OfContext-object，无论是什么）作为字符串附加到该列表来修复它：

代码：[全选](#)

`contexts=[]  
for c in getSubContext("project://ASSETS"):  
    contexts.append(str(c))  
print contexts`

打印“上下文”会给我一个正确的列表。耶！

[杰罗恩德斯梅特](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=10694&sid=5f50434cd43b7257c9efb473f5eb51a5)

**帖子：**  19

**加入时间：**  2014 年 11 月 15 日星期六晚上 9:08

* * *

### [回复：获取场景中所有上下文的列表](#p18900)

[![](https://forum.isotropix.com/styles/isotropix2016/imageset/icon_post_target_unread.gif)
](https://forum.isotropix.com/viewtopic.php?p=18900&sid=5f50434cd43b7257c9efb473f5eb51a5#p18900)通过**[ayanik](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=10734&sid=5f50434cd43b7257c9efb473f5eb51a5)** » 2019 年 1 月 30 日，星期三 11:10 pm

是的，您可以将它们转换为字符串并将它们放在另一个列表中。那也行。

[阿亚尼克](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=10734&sid=5f50434cd43b7257c9efb473f5eb51a5)

**帖子：**  91

**加入时间：**  2014 年 11 月 26 日，星期三 9:10 pm

* * *

### [回复：获取场景中所有上下文的列表](#p18906)

[![](https://forum.isotropix.com/styles/isotropix2016/imageset/icon_post_target_unread.gif)
](https://forum.isotropix.com/viewtopic.php?p=18906&sid=5f50434cd43b7257c9efb473f5eb51a5#p18906)通过**[bvaldes](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=13171&sid=5f50434cd43b7257c9efb473f5eb51a5)** » 2019 年 1 月 31 日星期四上午 10:02

嗨，

几年前我做了一些有用的功能。如果需要，您可以使用它们：

#### 蟒蛇代码

```
def getSubContext(context = ix.get\_current\_context(), recursive = True):   
 result = \[\]   
 context = ix.get\_item(str(context))   
 sub\_contexts = \[\]   
 for i in range(context.get\_context\_count()):   
 result.append (context.get\_context(i))   
 sub\_contexts.append(context.get\_context(i))  
 如果递归：  
 while len(sub\_contexts)>0:   
 workOn = sub\_contexts   
 sub\_contexts = \[\]   
 for context in workOn:   
 for i in range(context.get\_context\_count ()):   
 sub\_contexts.append(context.get\_context(i))   
 result.append(context.get\_context(i))  
 返回结果def getItems(context = ix.get\_current\_context(), kind = None, recursive=True):   
 result = \[\]   
 workOn = \[ix.get\_item(str(context))\]   
 vItems = ix.api.OfItemVector()  
 如果递归：  
 对于getSubContext 中的 subContext(workOn\[0\], recursive = True):   
 workOn.append(subContext) 用于 workOn 中的上下文：  
 if (context.get\_object\_count()):   
 objects\_array = ix.api.OfObjectArray(context.get\_object\_count())  
 上下文。 get\_objects(objects\_array)   
 for i\_obj in range(context.get\_object\_count()):   
 if kind is not None:   
 if objects\_array\[i\_obj\].is\_kindof(kind):  
 vItems.add(objects\_array\[i\_obj\])   
 else:   
 vItems.add(objects\_array\[i\_obj\])for item in vItems:   
 result.append(item.get\_full\_name())  
 返回结果 
```

我希望这能帮到您。

问候

Benoit VALDES  
Isotropix  
Clarisse QA

[![](https://forum.isotropix.com/download/file.php?avatar=13171_1481033212.png)
](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=13171&sid=5f50434cd43b7257c9efb473f5eb51a5)  
[巴尔德斯](https://forum.isotropix.com/memberlist.php?mode=viewprofile&u=13171&sid=5f50434cd43b7257c9efb473f5eb51a5)

**帖子：**  384

**加入时间：**  2016 年 9 月 26 日星期一上午 10:44

* * *

* * *