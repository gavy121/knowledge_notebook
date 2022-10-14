# 谷歌翻译为何退出中国？被迫的还是主动的？该如何恢复 Chrome 翻译功能？ | 零度解说 - 零度解说
下面是获取可用 IP 地址以及修改 Windows 系统和 macOS 系统 hosts 文件的自动化脚本代码：

只需一键即可完成所有修改步骤。

脚本托管在 [GitHub Gist](https://www.freedidi.com/go.php?url=aHR0cHM6Ly9naXN0LmdpdGh1Yi5jb20vYm9va2ZlcmUvYzliYWYxZDAzZDZmNDg4YzcwMzNlZmZiZDU0MWU2Mjg=) 上，你也可以通过以下链接直接下载到本地使用。

把代码保存为bat’文件，最后以管理员身份运行脚本即可完成!



```
:: Copyright (c)2022 https://bookfere.com
:: This is a batch script for fixing Google Translate and making it available
:: in the Chinese mainland. If you experience any problem, visit the page below:
:: https://bookfere.com/post/1020.html

@echo off
setlocal enabledelayedexpansion
chcp 437 >NULL

set "source\_domain=google.cn"
set "target\_domain=translate.googleapis.com"

set "hosts\_file=C:\\Windows\\System32\\drivers\\etc\\hosts"
for /f "skip=4 tokens=2" %%a in ('"nslookup %source\_domain% 2>NUL"') do set ip=%%a
set "old\_rule=null"
set "new\_rule=%ip% %target\_domain%"
set "comment=# Fix Google Translate CN"

for /f "tokens=\*" %%i in ('type %hosts\_file%') do (
    set "line=%%i"
    :: Retrieve the rule If the target domain exists.
    if not "!line:%target\_domain%=!"=="%%i" set "old\_rule=%%i"
)

if not "%old\_rule%"=="null" (
    echo A rule has been added to the hosts file. 
    echo \[1\] Update \[2\] Delete
    set /p action="Enter a number to choose an action: "
    if "!action!"=="1" (
        if not "%old\_rule%"=="%new\_rule%" (
            echo Deleting the rule "%old\_rule%"
            echo Adding the rule "%new\_rule%"
            set "new\_line=false"
            for /f "tokens=\*" %%i in ('type %hosts\_file% ^| find /v /n "" ^& break ^> %hosts\_file%') do (
                set "rule=%%i"
                set "rule=!rule:\*\]=!"
                if "%old\_rule%"=="!rule!" set "rule=%new\_rule%"
                if "!new\_line!"=="true" >>%hosts\_file% echo.
                >>%hosts\_file% <NUL set /p="!rule!"
                set "new\_line=true"
            )
        ) else (
            echo The rule already exists, nothing to do.
        )
    )
    if "!action!"=="2" (
        echo Deleting the rule "%old\_rule%"
        set "new\_line=false"
        for /f "tokens=\*" %%i in ('
            type "%hosts\_file%" ^| findstr /v /c:"%comment%" ^| findstr /v "%target\_domain%" ^| find /v /n "" ^& break ^> "%hosts\_file%"
        ') do (
            set "line=%%i"
            set "line=!line:\*\]=!"
            if "!new\_line!"=="true" >>%hosts\_file% echo.
            >>%hosts\_file% <NUL set /p="!line!"
            set "new\_line=true"
        )
    )
) else (
    echo Adding the rule "%new\_rule%"
    echo.>>%hosts\_file%
    echo %comment%>>%hosts\_file%
    <NUL set /p="%new\_rule%">>%hosts\_file%
)

echo Done.
pause

```

### 如果你用的是 macOS 系统

打开“**终端**”，拷贝以下命令并将其粘贴到终端上，按回车，输入你的系统密码，再按回车。注意，输入密码时是不显示任何信息的，只要确保输入的密码是正确的就可以。

sudo bash -c "$(curl -skL https://fere.link/ow3cld)"

sudo bash -c "$(curl -skL https://fere.link/ow3cld)"

```
sudo bash -c "$(curl -skL https://fere.link/ow3cld)"
```

如果看到如下所示提示，表示规则添加成功，也就可以正常使用 Chrome 的谷歌翻译功能了。

```
Adding the rule "142.250.70.195 translate.googleapis.com"
Done.
```

\* 提示：终端打开的方式为，打开“**访达（Finder）**”，在左侧边栏找到并进入“**应用程序（Applications）**”文件夹，在里面找到并进入“**实用工具（Utilities）**”文件夹，在这里面就可以找到“**终端（Terminal）**”，双击打开。

​\* 注意：​由于代码是托管在 GitHub 的，因此在请求 URL 的时候可能会遇到网络不通畅的情况，如果运行命令后长时间没反应，建议按 Ctrl + C 中止运行，​然后再重新运行一遍上面的命令，一般最多尝试两三次。

此命令可以重复使用。添加规则后再次使用时会出现交互提示信息，输入 **1** 会尝试更新已添加规则的 IP 地址，如果没有变化则不做任何修改，输入 **2** 会删除已添加的规则。

Github 开源项目地址：https://gist.github.com/bookfere

[![](https://www.freedidi.com/wp-content/uploads/logo.png)
](https://bittly.cc/Surfshark)