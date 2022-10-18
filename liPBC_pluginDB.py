from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class LiPBC_pluginDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'LiPBC-Bulid',
            self.OK|self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            

        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Apply')
        frame = FXHorizontalFrame(self, 0, 0,0,0,0, 0,0,0,0)

        comboLen=10    
        self.RootComboBox_1 = AFXComboBox(p=frame, ncols=0, nvis=1, text='ModelName:', tgt=form.ModelNameKw, sel=0)
        names = mdb.models.keys()
        names.sort()
        for name in names:
            self.RootComboBox_1.appendItem(name)
            comboLen = len(name) if len(name) > comboLen else comboLen

        self.RootComboBox_1.setMaxVisible(comboLen)
        if not form.ModelNameKw.getValue() in names and names:
            form.ModelNameKw.setValue(names[0])
        msgCount = 6
        form.ModelNameKw.setTarget(self)
        form.ModelNameKw.setSelector(AFXDataDialog.ID_LAST + msgCount)
            
        fileName = os.path.join(thisDir, 'LiPBC_icon.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=self, text='', ic=icon)

        self.form = form
    
    def show(self):
        AFXDataDialog.show(self)
        if mdb.models.keys():
            self.currentModelName = mdb.models.keys()[0]
        else:
            self.currentModelName = ''
        self.form.ModelNameKw.setValue(self.currentModelName)

    
    def hide(self):
        AFXDataDialog.hide(self)
