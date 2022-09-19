def setUpAnim(dispTime):
    userInputDispTime = int(dispTime)

    #create master GRP to collect asset cmb's in render context
    grp = ix.cmds.CreateObject("group", "Group")
    ix.cmds.RenameItem(str(grp),"MASTER_grp")
    ix.cmds.SetValues(["project://env_master/env/assets/MASTER_grp.inclusion_rule[0]"], ["project://env_master/env/render/*cmb"])

    #REFRESH SCENE TOO UPDATE THE GROUP NODE -> THIS GETS FILTERED RESULTS
    ix.application.check_for_events()

    grp = ix.get_item("project://env_master/env/assets/MASTER_grp")
    # Get the attribute that contain the result objects of a group
    masterCmbList =  grp.get_attribute("references")


    ### MAIN VARIBALES SET UP ###
    fps = ix.application.get_prefs().get_double_value("animation", "frames_per_second") # get the frame rate from prefs
    displayTimePerAsset = userInputDispTime/fps
    startFrameInSecs = 1001/fps
    lastFrame  = (len(masterCmbList) * (displayTimePerAsset*fps))+(1001)
    rotYLastFrameInSecs = (1001 + 4)/fps
    StartFrame = 1001


    for i in range(masterCmbList.get_value_count()):

        #ATTRIBUTE NAMES
        strAssetName = str(masterCmbList.get_object(i))
        rotYPramName = strAssetName + ".rotate[1]"
        hidePramName= strAssetName +".unseen_by_renderer"
        visPramName=strAssetName +".display_visible"
        #ROTATE Y KEYFRAMES
        ix.cmds.SetKey([str(rotYPramName)], startFrameInSecs,[0.0], 0)
        ix.cmds.SetKey([str(rotYPramName)], rotYLastFrameInSecs,[360.0], 0)

        #VIEWPORT VISABILITY KEYFRAMES
        ix.cmds.SetKey([str(visPramName)], startFrameInSecs-(1/fps),[0.0], 1)
        ix.cmds.SetKey([str(visPramName)], startFrameInSecs,[1.0], 1)
        ix.cmds.SetKey([str(visPramName)], startFrameInSecs+displayTimePerAsset,[0.0], 1)

        #RENDER VISABILITY KEYFRAMES
        ix.cmds.SetKey([str(hidePramName)], startFrameInSecs-(1/fps),[1.0], 1)# set invisibaleKey
        ix.cmds.SetKey([str(hidePramName)], startFrameInSecs,[0.0], 1)# set visable key
        ix.cmds.SetKey([str(hidePramName)], startFrameInSecs+displayTimePerAsset,[1.0], 1)

        print "startFrameInSecs - 1 {0}".format(((startFrameInSecs)-(1/fps))*fps)
        print "startFrameInSecs {0}".format((startFrameInSecs)*fps)
        print "startFrameInSecs+dispTime {0}".format((startFrameInSecs+displayTimePerAsset)*fps)

        #LOOP COUNT / MATH
        startFrameInSecs = startFrameInSecs + displayTimePerAsset
        rotYLastFrameInSecs = rotYLastFrameInSecs + displayTimePerAsset

    #SET FRAME RANGE
    frameRange = ix.cmds.SetCurrentFrameRange(1001.0, lastFrame)
    ix.cmds.SetCurrentFrame(1001)

#LIST ALL IMAGE PASSES

#REMOVING ANIMATION AND DELLETING KEYFRAMES
def restoreScene():
    grp = ix.get_item("project://env_master/env/assets/MASTER_grp")
    masterCmbList =  grp.get_attribute("references")
    for i in range(masterCmbList.get_value_count()):
        strAssetName = str(masterCmbList.get_object(i))
        ix.cmds.RemoveFCurve([strAssetName +".display_visible[0]"])
        ix.cmds.RemoveFCurve([strAssetName +".unseen_by_renderer[0]"])
        #ix.cmds.RemoveFCurve([strAssetName +"
        ix.cmds.RemoveFCurve([strAssetName +".rotate[1]"])
        ix.cmds.SetValues([strAssetName+".display_visible"], ["1"])
        #ix.cmds.SetKey([strAssetName], startFrameInSecs,[1.0], 0)

    ix.cmds.DeleteItems(["project://env_master/env/assets/MASTER_grp"])

### WINDOW SETUP ###
class MyLineEdit(ix.api.GuiLineEdit):
    def __init__(self, parent, x, y, w, h,label):
        ix.api.GuiLineEdit.__init__(self, parent, x, y, w, h, label)
        self.connect(self, 'EVT_ID_LINE_EDIT_CHANGED', self.enter_text)

    def enter_text(self, sender, evtid):
        ix.log_info(self.get_text() )

class MyButtonA(ix.api.GuiPushButton):
    def __init__(self, parent, x, y, w, h, label):
        ix.api.GuiPushButton.__init__(self, parent, x, y, w, h, label)
        self.connect(self, 'EVT_ID_PUSH_BUTTON_CLICK', self.on_click)

    def on_click(self, sender, evtid):
        setUpAnim(lineEdit.get_text())

class MyButtonB(ix.api.GuiPushButton):
    def __init__(self, parent, x, y, w, h, label):
        ix.api.GuiPushButton.__init__(self, parent, x, y, w, h, label)
        self.connect(self, 'EVT_ID_PUSH_BUTTON_CLICK', self.on_click)

    def on_click(self, sender, evtid):
        restoreScene()

window = ix.api.GuiWindow(ix.application, 300, 100, 400, 240, "Multi Asset Previewer")

panel = ix.api.GuiPanel(window, 0, 0, window.get_width(), window.get_height())
panel.set_constraints(ix.api.GuiWidget.CONSTRAINT_LEFT,
                      ix.api.GuiWidget.CONSTRAINT_TOP,
                      ix.api.GuiWidget.CONSTRAINT_RIGHT,
                      ix.api.GuiWidget.CONSTRAINT_BOTTOM);

lineEdit = MyLineEdit(panel, 5, 40, 360, 20, "dispaly time per asset (frames)")
button = MyButtonA(panel, 50, 100, 140, 22, "create set up")
button = MyButtonB(panel, 50, 150, 140, 22, "restore")

window.show()
while window.is_shown(): ix.application.check_for_events()