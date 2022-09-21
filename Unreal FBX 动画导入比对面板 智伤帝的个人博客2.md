# Unreal FBX 动画导入比对面板 | 智伤帝的个人博客2
[](#前言 "前言")前言
--------------

>   前段时间协助动画组制作将动画 FBX 文件导入 Unreal 引擎里面，遇到很麻烦的问题。  
>   由于一些流程规范的问题，我们的动画需要添加修型，这个修型 K 帧的过程中有修改了时间滑块范围的情况。  
>   结果导致后续导出文件的数据和引擎里面的源动画数据匹配不上。  
>   这种问题检查起来就很麻烦了。  
>   当时由于赶时间，我们只好人工校对了，后来吸取教训，我觉得也可以在 Unreal 上开发工具， 借助 Unreal 的 Python API 来解决这些琐事。

[](#Unreal-Python-插件选择 "Unreal Python 插件选择")Unreal Python 插件选择
--------------------------------------------------------------

>   其实关于 Unreal 接入 Python 的插件是有两个选择的。  
>   一个是 Github 上已经有 1.6K 星星，已经经历常年开发，非常很成熟的插件 UnrealEnginePython [github 地址](https://github.com/20tab/UnrealEnginePython)  
>   然后 Epic 官方在 2018 年推出了 Unreal 内置的 Python 插件  
>   然后第三方插件的 readme 里面提到了关于和官方之间的纠葛，最后很可惜还是得不到官方的承认。  
>   所以我这里还是使用 官方的 Python 插件。

* * *

>   关于 Unreal 官方 Python 插件要如何使用，可以参照外国人做的一个教程 [B 站地址](https://www.bilibili.com/video/BV1b4411r7kX) [Youtube 地址](https://www.youtube.com/watch?v=RwWgC2xqk48&list=PLBLmKCAjA25Br8cOVzUroqi_Nwipg-IdP) [B 站国人重制版](https://www.bilibili.com/video/BV1PE411d7z8) [github 地址](https://github.com/AlexQuevillon/UnrealPythonLibrary)  
>   这套教程里面有很详细的 Python 操作教程，甚至还包括如何通过 C++ 开发蓝图节点，然后通过官方插件转换为 Python 调用。

* * *

>   由于目前项目用的 版本 为 4.22 ，所以有些功能和最新的不太一样，比如我最近开发遇到了 Python API 无法操作 Sequencer 导出 FBX  
>   这个命令在 [SequencerTools](https://docs.unrealengine.com/en-US/PythonAPI/class/SequencerTools.html?highlight=export_fbx#unreal.SequencerTools.export_fbx) 模块下面。  
>   但是我的 4.22 版本的插件下是无法调用，只能通过 C++ API 开发蓝图来调用。

[](#Unreal-Editor-Utility-开发 "Unreal Editor Utility 开发")Unreal Editor Utility 开发
--------------------------------------------------------------------------------

>   Editor Utility 是 Unreal 4.22 引入的新机制。  
>   通过这个可以借助 UMG 界面来开发引擎的工具界面，集成 Designer 组件拖拽开发，比较完善了。  
>   事件触发也支持蓝图，可以通过蓝图实现 Unreal 的自动化工具。  
>   具体的使用方法可以参照 官方 live ， 视频内容干货很多，很有参考价值。 [youtube 地址](https://www.youtube.com/watch?v=s_rt49atj0Y&t=2577s) [B 站地址](https://www.bilibili.com/video/BV1L4411T78y) [github 地址](https://github.com/bluevoidstudios/edutilexamples)  
>   这个视频里面也有提到如何在 4.22 中通过 蓝图 调用 Python。

>   下面就是我按钮点击触发 调用 Pyhton 方法。

[![](https://blog.l0v0.com/img/loading.gif)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/01.png)  
[![](https://blog.l0v0.com/img/loading.gif)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/02.png)

>   4.22 还没有直接执行 Python 脚本的蓝图，只能通过 `Execute Console Command` 调用 py 来变相执行 Python 脚本。  
>   这里我直接脚本前缀默认路径指向了蓝图的路径，然后只要输入相对蓝图路径的地址就可以执行相应的 Python 文件了。

[](#Unreal-对接-PySide "Unreal 对接 PySide")Unreal 对接 PySide
--------------------------------------------------------

>   Unreal 官方内置了 Python2 ， 简直就是为了影视工业的各个 DCC 软件所做的妥协。(当然不爽的话可以自己搭建一个 Python3 ，或者用 UnrealEnginePython 第三方插件也可以)  
>   目前 Python2 已经不再维护，还是希望整个行业的 Python 能够集体升级。

>   由于官方使用的是 Python2 所以只好接入比较过时的 PySide 包。  
>   安装方法很简单，因为 Unreal 的 Python 没有类似 Maya 的魔改，还是兼容传统的 Python2 编译器的。  
>   所以直接去网上安装一个 Python2 ，然后用 pip install PySide 即可，最后将包的路径添加到 Unreal python 的 sys.path 里面就可以用实现在 Unreal 里面调用 Qt 了。  
>   不过这里也有一些麻烦。  
>   图形化编程要保持窗口响应，进程需要挂起。

>   那么 Unreal 和 PySide 这两个会产生冲突。  
>   PySide 的 exec\_ 函数不好使，我之前有测试过，如果执行 QApplication 的 exec\_ 会导致 Unreal 卡死。  
>   好在油管那套 Unreal Python 教程有指点迷津， Unreal 自身有可以使用 register\_slate\_post\_tick\_callback 来提供无限回调的 tick 。  
>   教程通过 无限回调 来确保 Gui 窗口的持续相应的。  
>   不过经过我使用 PySide 的经验， 特别是年前开发 mpdb 模块的时候接触到的一些让 Qt GUI 持续响应的方法。  
>   其实不需要教程里那么麻烦，要记录存在的所有窗口并且还要不停触发 eventTick 函数来刷新 GUI 从而实现窗口响应。  
>   其实 QApplication 提供了 processEvents 来触发事件队列，所有的响应事件都是先插入到事件队列里面，然后通过 processEvents 来异步触发。  
>   这样的好处是 UI 刷新频率没有那么高，没有事件的话就不需要不断刷新重绘了。  
>   maya 的 evalDeferred 也是类似的事件队列机制。

>   下面就是我在 Unreal 里面初始化 PySide 的脚本，用了 Qt.py 来以防万一

```python
import os
import sys
DIR = os.path.dirname(__file__)
vendor = os.path.join(DIR, "vendor")
sys.path.insert(0, vendor) if vendor not in sys.path else None

FBX = os.path.join(DIR, "FBXImporter")
sys.path.insert(0, FBX) if FBX not in sys.path else None


import unreal
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui


def slate_deco(func):
    def wrapper(self, single=True, *args, **kwargs):
        
        if single:
            for win in QtWidgets.QApplication.topLevelWidgets():
                if win is self:
                    continue
                elif self.__class__.__name__ in str(type(win)):
                    win.deleteLater()
                    win.close()
        
        
        unreal.parent_external_window_to_slate(self.winId())
        return func(self, *args, **kwargs)
    return wrapper



def __QtAppTick__(delta_seconds):
    QtWidgets.QApplication.processEvents()
    
    QtWidgets.QApplication.sendPostedEvents()


def __QtAppQuit__():
    unreal.unregister_slate_post_tick_callback(tick_handle)



unreal_app = QtWidgets.QApplication.instance()
if not unreal_app:
    unreal_app = QtWidgets.QApplication([])
    tick_handle = unreal.register_slate_post_tick_callback(__QtAppTick__)
    unreal_app.aboutToQuit.connect(__QtAppQuit__)

    
    QtWidgets.QWidget.show = slate_deco(QtWidgets.QWidget.show)
```

>   `__QtAppTick__`原本只需要添加 `processEvents` 就可以了，但是根据官方文档，这个操作无法执行组件删除事件。  
>   这会导致我的 Qt 窗口越来越多，而不会触发回收删除。  
>   进一步查了文档可以知道 `deleteDeferred` 事件可以通过 `sendPostedEvents` 函数触发。

>   另外借助 Python 动态特性 用装饰器 重写了 QWidget 的 show 函数。  
>   这样我的窗口组件执行 show 确保只有一个窗口。  
>   `parent_external_window_to_slate` 这个操作是在官方论坛里面学到的 [链接](https://forums.unrealengine.com/unreal-engine/unreal-studio/1526501-how-to-get-the-main-window-of-the-editor-to-parent-qt-or-pyside-application-to-it)，加入这个之后 PySide 生成的窗口就是依附到 Unreal 里面了。  
>   窗口不会和 Unreal 分开，不会导致 Unreal 的界面将窗口盖住的问题。  
>   由于几乎所有的 Qt 组件都是继承自 QWidget 的，所以几乎所有的 `show` 方法都会重载到这个装饰器上，一劳永逸，方便快捷。

>   最后就是通过蓝图连接到 Editor Utility 上，确保启动插件的窗口自动执行上面的初始化脚本。

[![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/03.png)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/03.png)

>   有了这一步初始化之后，就可以像 Maya 一样来写 Qt 界面了。

[](#Qt-界面编写 "Qt 界面编写")Qt 界面编写
-----------------------------

>   这一次 Qt 编写的要求还是有点高的，毕竟需要实现对比效果。  
>   而且最好是直观的，一目了然的。  
>   下面是界面写好的效果，通过点击我的 Editor Utility 的界面启动。

[![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/04.gif)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/04.gif)

>   基本的界面交互如上图所示，基本就是两个列表同步滚动和选择。  
>   导入的话可以利用按钮打开选择窗口进行导入，也可以通过拖拽直接将 FBX 文件拖拽到 ListWidget 上。

[![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/05.gif)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/05.gif)

>   导入 FBX 会使用 Autodesk 提供的 FBX Python SDK 读取 FBX 文件中的时间数据，经过换算获取帧数，然后比对是否和隔壁列表的 AnimSequence 有同名对象。  
>   如果名称匹配则比较帧数是否统一，如果帧数统一就打勾，帧数不统一打叉。

[![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/06.png)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/06.png)

>   如果没有匹配额的则放到列表最下面提示感叹号。

>   右键菜单可以将选择的 item 进行删除和批量导入 FBX 动画。

### [](#ListWidget-同步 "ListWidget 同步")ListWidget 同步

>   这次界面开发比较大难点就是两个 ListWidget 的 同步问题。

>   滚动同步其实参考 Stack Overflow 的回答 [链接地址](https://stackoverflow.com/questions/57481521/pyqt-syncing-scroll-in-2-different-qlistwidgets)  
>   选择同步也可以利用类似的方法去做，但是选择前首先需要清空当前的选择项。  
>   清空操作也会触发 signal，直接导致 signal 重复调用变成永动机 _(:з」∠)_  
>   后面写了个同步类，通过 protected 保护变量来防止死循环调用。

>   代码整合到了 QtLib 里面 [链接地址](https://github.com/FXTD-ODYSSEY/QtLib/blob/master/QtLib/widget/list_syncer.py)

### [](#Splitter-组件 "Splitter 组件")Splitter 组件

>   我发现 PySide 的 Splitter 没有明显的 Gui 表示进行区分。  
>   这让我很不爽，于是网上搜了一下，发现有方法可以将 Splitter 做成类似 Houdini 带按钮的 Splitter 效果。 [Stack Overflow 链接](https://stackoverflow.com/questions/21997090/pyqt-qt4-how-to-add-a-tiny-arrow-collapse-button-to-qsplitter)  
>   于是就学着自己改良了一个 Splitter 组件。

[github 链接](https://github.com/FXTD-ODYSSEY/QtLib/blob/master/QtLib/widget/splitter.py)

[![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/07.gif)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/07.gif)

>   支持轴向和横向，双击 splitter 可以自动平均分配。

[](#Unreal-Python-API-调用 "Unreal Python API 调用")Unreal Python API 调用
--------------------------------------------------------------------

>   Unreal Python API 网上的材料极少，出了寥寥无几的论坛文章之外，就只有 Youtube 的那套教程是比较好的了。  
>   剩下就是在 Python API 文档里面查方法的说明了，好在大部分常用的操作视频教程都涵盖了。

[![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/08.png)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/08.png)

>   另外使用 Python API 之前，相关的 Scripting 插件都要统统开启， Unreal 的官方 Python 插件本质上是调用 Unreal 的蓝图节点功能。  
>   我之前就是没有开启 `Sequencer Scripting` 插件，结果 Sequencer 相关的命令都是空的，我一度怀疑是官方插件出 Bug 了，后来试着试着才知道是我没加载 _(:з」∠)_

### [](#Unreal-获取选中的资源目录 "Unreal 获取选中的资源目录")Unreal 获取选中的资源目录

>   Python API 目前依然是各种不完善，比如无法直接获取到 Content Browser 的文件夹，只能获取到选中的资源。  
>   所以我只好通过选中的资源获取目录，然后通过目录获取目录下所有的资源.

```python
import unreal
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
if len(selected_assets) == 0:
    return
asset = selected_assets[0]
directory = unreal.Paths.get_path(asset.get_path_name())

assets = unreal.EditorAssetLibrary.list_assets(directory)
```

### [](#Unreal-Cotent-Browser-跳转到选中资源 "Unreal Cotent Browser 跳转到选中资源")Unreal Cotent Browser 跳转到选中资源

[![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/09.png)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/09.png)

>   一开始以为这个功能挺难实现的，没想到 Unreal 已经封装好了。  
>   直接传入 unreal 引用路径就可以自动同步。

```python

def sync_assets(self):
    path_list = [item.text() for item in self.selectedItems()]
    unreal.EditorAssetLibrary.sync_browser_to_objects(path_list)
```

### [](#导入-FBX-动画 "导入 FBX 动画")导入 FBX 动画

>   这个操作就遇到了大坑了，  
>   因为 上面的教程只提供了 骨骼动画蒙皮全部一起导入的方案。  
>   但是没有提供只导入动画这种方案。  
>   后来我踩了很多坑之后，在论坛上上找到了解决方案。  
>   就是导入 task 的 FbxImportUI options 需要设置 `automated_import_should_detect_type` 为 False

```python
def buildImportTask(self, filename='', destination_path='', skeleton=None):

    options = unreal.FbxImportUI()
    options.set_editor_property("skeleton", skeleton)
    
    options.set_editor_property("import_animations", True)
    options.set_editor_property("import_as_skeletal", False)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("import_rigid_mesh", False)
    options.set_editor_property("create_physics_asset", False)
    options.set_editor_property(
        "mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    
    options.set_editor_property(
        "automated_import_should_detect_type", False)

    task = unreal.AssetImportTask()
    task.set_editor_property("factory", unreal.FbxFactory())
    
    task.set_editor_property("automated", True)
    task.set_editor_property("destination_name", '')
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("filename", filename)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", False)
    task.options = options

    return task

def import_items(self):
    
    tasks = []
    for fbx_item in self.selectedItems():
        fbx_path = fbx_item.toolTip()
        if not fbx_path:
            continue
        
        fbx_path = fbx_path.split("\n")[0]
        row = self.row(fbx_item)
        asset_item = self.asset_list.item(row)
        asset_path = os.path.dirname(asset_item.text())
        skeleton = asset_item.asset.get_editor_property('skeleton')

        task = self.buildImportTask(fbx_path, asset_path, skeleton)
        tasks.append(task)

        
        fbx_item.setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
        asset_item.setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))

    
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
```

[](#FBX-Python-SDK "FBX Python SDK")FBX Python SDK
--------------------------------------------------

>   我们插件面板获取到了 FBX 的文件路径，但是还需要通过 Python 来读取 FBX 的数据。  
>   这要如何实现呢？  
>   其实方法不止有一种，比如存储 FBX 的 ASCII 模式，那就是纯文本编辑，甚至可以用正则表达式匹配数据。  
>   但是如果凑巧导出的是 Binary 格式，那就操作不了了。  
>   所以我网上查了一下，比较靠谱的方法就是使用 Autodesk 官方提供的 FBX Python SDK

>   FBX 是 Autodesk 公司开发的一种通用三维数据存储格式，极大解决了不同软件的数据互通问题。(现在有 USD 这种更好的解决方案了，我还没有时间研究这个 _(:з」∠)_)  
>   我感觉这个东西推出来主要原因是 Autodesk 收购了太多三维软件了，每个软件用的标准都不统一。  
>   推出这个格式，可以解决动捕软件对接主流三维软件的问题，所以它并不是一种工业标准的格式。  
>   FBX 格式算是比较早期支持相对完整的通用格式了，至今依然是游戏行业的通用标准。影视的流程比较复杂，目前大都用 Alembic 或者 ass 等各种缓存。  
>   USD 没用过，传闻听了很多，希望生态能够成熟起来，实现数据格式的大一统。

* * *

>   回到这里讨论的主题， FBX 的 Python SDK 如何使用。具体可以从官网了解 [链接](https://www.autodesk.com/products/fbx/overview)  
>   Autodesk 提供了 C++ 的 SDK ， 类似 Unreal Unity 这些游戏引擎大概率也是引入了这个模块实现 FBX 的解析。  
>   我们要用 Python 操作 FBX ，首先需要安装 Python SDK ，可以去官网下载并安装 [链接](https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-1)

>   下载运行 exe 安装完成，可以去到安装目录找到 FBX 的 python 包。

[![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/10.png)
](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/post_img/a999f0c/10.png)

>   lib 文件夹有对应不同 Python 平台的 fbx 库，已经编译好，是可以直接 Python 调用的 pyd 文件，还有一个为了简化操作而写的 FbxCommon.py  
>   而 samples 目录下则有一些 Python 操作的案例，可以参考学习。  
>   这个 SDK 操作网上也找不到多少使用资料，基本看官方的材料足矣。

>   这里主要参考了 ImportScene 里面 DisplayAnimation 的一些数据。  
>   通过 ImportScene.py 的操作可以知道， FBX SDK 需要 `FbxCommon.InitializeSdkObjects` 初始化 manager 和 scene 对象。  
>   然后通过 `FbxCommon.LoadScene` 来加载 FBX 场景。  
>   最初我们的动画是带修型的，所以记载模型的数据就特别特别慢，我在想 难道 FBX SDK 不可以只读取部分数据来加速吗？  
>   于是又去翻阅 FBX 的官方文档以及 FBX C++ API 文档，没错这个 API 和 OpenMaya 1.0 一样只有 C++ 文档，不过用起来差不多。 [官方文档地址](http://help.autodesk.com/view/FBX/2020/ENU/) [C++ 文档地址](http://help.autodesk.com/view/FBX/2020/ENU/?guid=FBX_Developer_Help_cpp_ref_annotated_html)  
>   文档也是用同一个生成器生成的。

```python
def read_fbx_frame(self, fbx_file):
    
    manager, scene = FbxCommon.InitializeSdkObjects()
    
    s = manager.GetIOSettings()
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Material", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Texture", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Audio", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Audio", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Shape", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Link", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Gobo", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Animation", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Character", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Global_Settings", True)
    manager.SetIOSettings(s)

    result = FbxCommon.LoadScene(manager, scene, fbx_file)
    if not result:
        raise RuntimeError("%s load Fail" % fbx_file)

    setting = scene.GetGlobalSettings()
    time_span = setting.GetTimelineDefaultTimeSpan()
    time_mode = setting.GetTimeMode()
    frame_rate = fbx.FbxTime.GetFrameRate(time_mode)
    duration = time_span.GetDuration()
    second = duration.GetMilliSeconds()
    
    frame_count = round(second/1000*frame_rate) + 1
    return frame_count
```

>   读取 FBX 遇到最大的坑就是 设置 IOsettings 属性  
>   在 C++ 官方文档的说明里面明明是有 `IMP_FBX_MATERIAL` `IMP_FBX_TEXTURE` 这些可以通过 SetBoolProp 来设置的 [链接](http://help.autodesk.com/view/FBX/2020/ENU/?guid=FBX_Developer_Help_importing_and_exporting_a_scene_io_settings_html)  
>   但是 fbx 模块并没有直接提供这些属性，只有 EXP 相关的属性。  
>   结果我就不知道怎样才可以设置导入场景的设置。  
>   后来想到可以打印一些 已有 的 EXP 相关属性的类型，结果发现这些原来都是字符串。  
>   于是又深入查了 C++ 文档，但是 C++ 文档各种变量串在一起，查询起来非常非常混乱。  
>   后来我研究了一下怎么讲 IOSettings 里面相关的字符串全部打印出来，通过 C++ 文档的方法和自己的测试，总算实现了这个效果。

[FBX Python SDK 打印 IOSettings 包含的 Property 属性](https://github.com/FXTD-ODYSSEY/MayaScript/blob/430e9194da85d884d0304b141706bae44460dd8a/_FBXDemo/property/list_property.py)  
[输出的属性整理出的 md 文件](https://github.com/FXTD-ODYSSEY/MayaScript/blob/430e9194da85d884d0304b141706bae44460dd8a/_FBXDemo/property/IOProperty.md)

>   通过上面输出打印的 IOSettings 可以看到 SetBoolRrop 可以填写控制导入的物体的字符串。  
>   通过这个导入限定，FBX 的读取速度就非常快了。

[](#总结 "总结")总结
--------------

>   这次 Unreal 的工具开发，深度结合了 Python Qt 界面开发和 Unreal 内置的 API ，还额外研究 FBX Python SDK 的 API 使用。  
>   学习到了很多新的东西，不过感觉这些东西没有太多深度，就是资料太少，需要有查文档踩坑的过程。  
>   近期特效给我安排了一个任务，需要将 Unreal 的 Sequencer 里的东西自动导出进行处理。  
>   但是最近查了 Sequencer 的 API ，貌似支持非常不友好，比如无法直接获取到当前 Sequencer 界面所使用的 LevelSequence  
>   所以后续需要研究一下 Unreal 插件开发，通过 C++ 蓝图插件开发来解决这些问题。

版权声明: 本博客所有文章除特别声明外，均采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可协议。转载请注明来自 [智伤帝的个人博客](https://blog.l0v0.com/)！

打赏

*   [![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/img/wechatimg.jpg)
    ](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/img/wechatimg.jpg)
    
    微信
    
*   [![](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/img/alipayimg.jpg)
    ](https://cdn.jsdelivr.net/gh/FXTD-odyssey/FXTD-odyssey.github.io@master/img/alipayimg.jpg)
    
    支付宝
    

* * *