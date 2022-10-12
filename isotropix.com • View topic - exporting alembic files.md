# isotropix.com • View topic - exporting alembic files
        isotropix.com • View topic - exporting alembic files                

Isotropix Forums
================

[**FORUM INDEX**](./index.php?sid=d73a1894d157920dabb5f763f18322a8) **‹** [Isotropix Community Forums](./viewforum.php?f=3&sid=d73a1894d157920dabb5f763f18322a8) **‹** [Scripting](./viewforum.php?f=21&sid=d73a1894d157920dabb5f763f18322a8)

[exporting alembic files](./viewtopic.php?f=21&t=3586&sid=d73a1894d157920dabb5f763f18322a8)
-------------------------------------------------------------------------------------------

Clarisse Scripting related topics  

[Post a reply](./posting.php?mode=reply&f=21&t=3586&sid=d73a1894d157920dabb5f763f18322a8 "Post a reply")

 https://forum.isotropix.com/viewtopic.php?p=14758   

[First unread post](#unread) • 5 posts • Page **1** of **1**

### [exporting alembic files](#p14717)

[![](./styles/isotropix2016/imageset/icon_post_target_unread.gif)
](./viewtopic.php?p=14717&sid=d73a1894d157920dabb5f763f18322a8#p14717)by **[megavotch](./memberlist.php?mode=viewprofile&u=8436&sid=d73a1894d157920dabb5f763f18322a8)** » Tue Nov 07, 2017 3:20 am

I'm getting a crash when trying to export alembic files in a loop using python.  
  
I'm creating an alembic export object and setting the options. And then executing ix.api.IOHelpers.export\_to\_alembic(options).  
  
This works great for the first object exported in the loop.  
But when exporting the next object Clarisse crashes with this error...  
  
error: Cannot create a new instance of AbcInputArchiveManager: there is already one.  
  
Any Idea what could be causing this?

[megavotch](./memberlist.php?mode=viewprofile&u=8436&sid=d73a1894d157920dabb5f763f18322a8)

**Posts:** 151

**Joined:** Mon Nov 18, 2013 8:20 pm

[Top](#wrap "Top")

* * *

### [Re: exporting alembic files](#p14721)

[![](./styles/isotropix2016/imageset/icon_post_target_unread.gif)
](./viewtopic.php?p=14721&sid=d73a1894d157920dabb5f763f18322a8#p14721)by **[bvaldes](./memberlist.php?mode=viewprofile&u=13171&sid=d73a1894d157920dabb5f763f18322a8)** » Tue Nov 07, 2017 10:07 am

Hi,  
  
You should maybe use the export button of your Alembic export item instead of using the IOHelper function:  

#### python code

```
exporter = CreateObject("alembic_export", "ProcessAlembicExport") # Create the item
# Here set all the options like you probably did
exporter.call_action("run_process") # Click on the Run Process button
```

  
That should avoid your issues. Regards

Benoit VALDES  
Isotropix  
Clarisse QA

[![](./download/file.php?avatar=13171_1481033212.png)
](./memberlist.php?mode=viewprofile&u=13171&sid=d73a1894d157920dabb5f763f18322a8)  
[bvaldes](./memberlist.php?mode=viewprofile&u=13171&sid=d73a1894d157920dabb5f763f18322a8)

**Posts:** 384

**Joined:** Mon Sep 26, 2016 10:44 am

[Top](#wrap "Top")

* * *

### [Re: exporting alembic files](#p14758)

[![](./styles/isotropix2016/imageset/icon_post_target_unread.gif)
](./viewtopic.php?p=14758&sid=d73a1894d157920dabb5f763f18322a8#p14758)by **[megavotch](./memberlist.php?mode=viewprofile&u=8436&sid=d73a1894d157920dabb5f763f18322a8)** » Sat Nov 11, 2017 2:07 am

I'm not able to make this work, when I create a ProcessAlembicExport node I'm not able to set the attrs.  
  
Interestingly the node that is created is grayed out and I'm not able to manually set the attrs either. What am I missing?

[megavotch](./memberlist.php?mode=viewprofile&u=8436&sid=d73a1894d157920dabb5f763f18322a8)

**Posts:** 151

**Joined:** Mon Nov 18, 2013 8:20 pm

[Top](#wrap "Top")

* * *

### [Re: exporting alembic files](#p14763)

[![](./styles/isotropix2016/imageset/icon_post_target_unread.gif)
](./viewtopic.php?p=14763&sid=d73a1894d157920dabb5f763f18322a8#p14763)by **[bvaldes](./memberlist.php?mode=viewprofile&u=13171&sid=d73a1894d157920dabb5f763f18322a8)** » Mon Nov 13, 2017 10:52 am

Hi,  
  
I am really sorry for my previous post. Indeed this object doesn't exist so you can't use it.  
I made a simple test to export some ABC and I didn't get any error.  

#### python code

```
options = ix.api.AbcExportOptions(ix.application)
for item in ["box", "sphere", "cylinder"]:
    ix.selection.select("project://"+item)
     
    options.export_mode = ix.api.AbcExportOptions.EXPORT_MODE_SELECTION
    options.filename = ix.api.CoreString("/Users/bvaldes/Desktop/Bazard/" + item + ".abc")
    ix.api.IOHelpers.export_to_alembic(options)
```

  
To make the test working I created 3 geo in the work context and set the export mode to selection. In the loop i simply select the item that I want to export. If you are working in context mode, you can do the same thing and set the current context in the loop (don't forget to set the export mode to EXPORT\_MODE\_CONTEXT)  
  
I hope that can solve your issue. Once again sorry for the previous post. Regards

Benoit VALDES  
Isotropix  
Clarisse QA

[![](./download/file.php?avatar=13171_1481033212.png)
](./memberlist.php?mode=viewprofile&u=13171&sid=d73a1894d157920dabb5f763f18322a8)  
[bvaldes](./memberlist.php?mode=viewprofile&u=13171&sid=d73a1894d157920dabb5f763f18322a8)

**Posts:** 384

**Joined:** Mon Sep 26, 2016 10:44 am

[Top](#wrap "Top")

* * *

### [Re: exporting alembic files](#p14767)

[![](./styles/isotropix2016/imageset/icon_post_target_unread.gif)
](./viewtopic.php?p=14767&sid=d73a1894d157920dabb5f763f18322a8#p14767)by **[megavotch](./memberlist.php?mode=viewprofile&u=8436&sid=d73a1894d157920dabb5f763f18322a8)** » Tue Nov 14, 2017 12:00 am

Thank you for clarifying Benoit,  
  
I'm still getting the crash. I suspect it's because I have a much more complex setup. I'll try and reproduce the crash in a simple scene.

[megavotch](./memberlist.php?mode=viewprofile&u=8436&sid=d73a1894d157920dabb5f763f18322a8)

**Posts:** 151

**Joined:** Mon Nov 18, 2013 8:20 pm

[Top](#wrap "Top")

* * *

Display posts from previous: All posts1 day7 days2 weeks1 month3 months6 months1 year Sort by AuthorPost timeSubject AscendingDescending 

* * *

[Post a reply](./posting.php?mode=reply&f=21&t=3586&sid=d73a1894d157920dabb5f763f18322a8 "Post a reply")

5 posts • Page **1** of **1**

[Return to Scripting](./viewforum.php?f=21&sid=d73a1894d157920dabb5f763f18322a8)

Jump to: Select a forum \------------------ Isotropix Community Forums    Get Clarisse iFX PLE Now!    News and Announcements       Clarisse 5.5 Early Access       Clarisse 5          Clarisse Olympus Archive       Clarisse iFX 4.0       Clarisse iFX 3.6       Clarisse iFX 3.5          Clarisse iFX Daedalus Archive       Clarisse iFX 3.0          Clarisse iFX Pegasus Archive       Clarisse iFX 2.0          Clarisse iFX Hyperion Archive       Clarisse iFX 1.6       Clarisse iFX 1.5       Clarisse iFX 1.0    General Discussion    Angie    Finished Work    Work In Progress    Tutorials    Tips and Tricks    Expressions    Scripting       Useful Community Scripts    Feature Requests       Feature Requests Archives    Bugs       Bugs Archive    Jobs       Video Tutorials    Get Procedurally Creative Challenge