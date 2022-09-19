import os
import sys
from os import walk
import datetime

def logAndImportAssets():

    def createLogFile(searchUserDefPath,saveUserDefPath):
        #get a timestamp for the name of the log file to be created
        DT = datetime.datetime.now()
        timeStamp = "_{0:02d}{1:02d}{2}_{3:02d}{4:02d}".format(DT.day,DT.month,DT.year,DT.hour,DT.minute)
        #set file path name for the log with timestamp
        abcLogRefPath = str(saveUserDefPath)
        abcLogRefPath = abcLogRefPath.replace(".txt","")
        abcLogRefPath = abcLogRefPath+timeStamp+".txt"

        #search this path
        filePath = str(searchUserDefPath)
        if os.path.isdir(varB) == True:

            #write and .abc's under user dinaed path to this log
            file_object = open(abcLogRefPath,"w+")
            for dirpath, dirnames, filenames in walk(filePath, followlinks=False):
                for file in filenames:
                    if file.endswith(".abc"):
                        abcPath = os.path.sep.join((dirpath,file))
                        #print "**** path: {0}".format(abcPath)
                        file_object.write(abcPath+'\n')
            file_object.close()


            fileObject = open(abcLogRefPath,"r")
            count = len(open(abcLogRefPath).readlines(  ))
            print count
            geoPathList = fileObject.readlines()
            #return(geoPathList)


            #geometryPathList = createLogFile()
            for i  in geoPathList:
                i = i.strip("\n")
                ix.cmds.CreateFileReference("project://env_master/env/assets", [i])
        else:   ix.application.message_box("File path to search from doens't exist", "Information", ix.api.AppDialog.ok(),ix.api.AppDialog.STYLE_OK)
            pass

    class MyLineEditA(ix.api.GuiLineEdit):
        def __init__(self, parent, x, y, w, h,label):
            ix.api.GuiLineEdit.__init__(self, parent, x, y, w, h, label)
            self.connect(self, 'EVT_ID_LINE_EDIT_CHANGED', self.enter_text)

        def enter_text(self, sender, evtid):
            ix.log_info(self.get_text() )

    class MyLineEditB(ix.api.GuiLineEdit):
        def __init__(self, parent, x, y, w, h,label):
            ix.api.GuiLineEdit.__init__(self, parent, x, y, w, h, label)
            self.connect(self, 'EVT_ID_LINE_EDIT_CHANGED', self.enter_text)

        def enter_text(self, sender, evtid):
            ix.log_info(self.get_text() )


    class MyButton(ix.api.GuiPushButton):
        def __init__(self, parent, x, y, w, h, label):
            ix.api.GuiPushButton.__init__(self, parent, x, y, w, h, label)
            self.connect(self, 'EVT_ID_PUSH_BUTTON_CLICK', self.on_click)

        def on_click(self, sender, evtid):
            createLogFile(lineEditA.get_text(),lineEditB.get_text())


    window = ix.api.GuiWindow(ix.application, 300, 100, 540, 200, "log'n'load")

    panel = ix.api.GuiPanel(window, 0, 0, window.get_width(), window.get_height())
    panel.set_constraints(ix.api.GuiWidget.CONSTRAINT_LEFT,
                          ix.api.GuiWidget.CONSTRAINT_TOP,
                          ix.api.GuiWidget.CONSTRAINT_RIGHT,
                          ix.api.GuiWidget.CONSTRAINT_BOTTOM);

    lineEditA = MyLineEditA(panel, 5, 40, 460, 20, "Find All Alembics Under This Path:")
    lineEditB = MyLineEditB(panel, 5, 70, 460, 20, "Path to Save Location abd Log:")
    button = MyButton(panel, 50, 100, 270, 22, "Create Log and Import")

    window.show()
    while window.is_shown(): ix.application.check_for_events()

logAndImportAssets()