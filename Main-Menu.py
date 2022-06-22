"""
3D Object Viewer
Ondřej Sojka, I. ročník
zimní semestr 2021/2022
Programování - NPRG030 - Zápočtový program
"""


#_______________Hide_Console_____________________
import win32gui, win32con

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)


#Main UI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QIcon
import sys, res 
import Settings

#MsgBox/File Select
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename

#Other
import os
import Viewport
import Exporter
import FullView

objname = ""
new_objname = ""
path = ""
size = 0
#Fixing Messagebox - When msgbox is called tkinter wants to open default window as well
def MessageboxFix(type,heading,text):
        #I'll call the default window
        root = Tk()
        root.overrideredirect(1)
        root.withdraw()
        if type == "info":
                messagebox.showinfo(heading,text)
        elif type == "error":
                messagebox.showerror(heading,text)
        elif type == "warning":
                messagebox.showwarning(heading,text)
        #And then destroy it
        root.destroy()
#Passing variables for export
def ExportData():
        v_data, f_data = Viewport.ExportData()
        Exporter.main(v_data,f_data)
def Exit():
        Viewport.quit() #Because of IDLE bug that is caused by calling sys.exit() before pygame.quit()
        sys.exit()
def ShowSettings():
        FormSettings.show()
def OpenFile():
        global path
        #Getting "Open" file dialog and then getting path from it, which we will use in opening
        #Then I pass the path and get just a Name of the file
        Tk().withdraw() 
        path = askopenfilename(filetypes=[("3D Object File", ".obj")]) 
        name = os.path.basename(path)
        global objname
        objname = name
        #Reseting UI because of the label "Selected Object"
        Form.close()
        ui.setupUi(Form)
        Form.show()
        Viewport.objname = path
        

def ShowFullView():
        #new_objname - Like I said, I'm loading everything here, so I'm also passing objname into new varible
        #Which I'm again using in ShowInfo()
        #Checking if file ends with .obj
        if objname[-3:] == "obj":
                FullView.main()
        else:
                MessageboxFix("error","Error: Wrong File!","You have to select a file *.obj!")
#Just Try|Catch and calling main function from Viewport.py which is explained there
def ShowWireFrame():
        global size
        global new_objname
        #Loading size file if already selected, if not pass to Msgbox Error
        #I load file size here and not in OpenFileDialog because this is also the "Load function"
        #Which loads all the informations about the object, so I thought that it would make much more sense
        try:
                size = os.path.getsize(path)
        except:
                pass
        #new_objname - Like I said, I'm loading everything here, so I'm also passing objname into new varible
        #Which I'm again using in ShowInfo()
        new_objname = objname
        Viewport.quit()
        #Checking if file ends with .obj
        if objname[-3:] == "obj":
                try:
                        Viewport.main()
                except:
                        MessageboxFix("error","Error: mtl File Missing!", "To load object you need to have mtl file in the same directory as the object")
        else:
                MessageboxFix("error","Error: Wrong File!","You have to select a file *.obj!")
#Function for showing all informations about the object
def ShowInfo():
        #The main string which appears
        #Shows new_objname, then calls Statictics from Viewport.py and getting file size which I converted to Kb
        objinfo = "{} has:\n{}\nFile size: {}Kb".format(new_objname,Viewport.Statistics(Viewport.count_vertex,Viewport.faces),round(size/1000,1))
        #Exception for pressing button before selecting a file
        if new_objname == "":
                MessageboxFix("error","Error: Couldn't read object","Program couldn't read object statictics, please make sure that you first loaded object by clicking on one of the buttons above!")
        else:
                MessageboxFix("info","Object info",objinfo)




#**************UI*****************#
class Ui_MainWindow(object):
#Everywhere it's the same
#Setting main things for widgets like:
#Geometry (Width, Height, X,Y coords)
#Font family(Font, size, style)
#Cursor Hover
#And some CSS(QtSS - but it's almost the same) for button visual
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(704, 396)
        MainWindow.setMinimumSize(QtCore.QSize(704, 396))
        MainWindow.setMaximumSize(QtCore.QSize(704, 396))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_Select = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Select.setGeometry(QtCore.QRect(260, 40, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(1)
        self.btn_Select.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Select.setFont(font)
        self.btn_Select.setStyleSheet("QPushButton{\n"
"  border-radius: 15px;\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:transparent;\n"
"  color: white;\n"
"  font-size: 25px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:white;\n"
"  color: black;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgba(255,255,255,155);\n"
"border:1px solid rgb(0,0,0);\n"
"}\n"
"")
        self.btn_Select.setObjectName("btn_Select")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 711, 401))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setPixmap(QtGui.QPixmap(":/Images/bg.png"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.btn_WireFrame = QtWidgets.QPushButton(self.centralwidget)
        self.btn_WireFrame.setGeometry(QtCore.QRect(260, 140, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(1)
        self.btn_WireFrame.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_WireFrame.setFont(font)
        self.btn_WireFrame.setStyleSheet("QPushButton{\n"
"  border-radius: 15px;\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:transparent;\n"
"  color: white;\n"
"  font-size: 23px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:white;\n"
"  color: black;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgba(255,255,255,155);\n"
"border:1px solid rgb(0,0,0);\n"
"}\n"
"")
        self.btn_WireFrame.setObjectName("btw_WireFrame")
        self.btn_FullView = QtWidgets.QPushButton(self.centralwidget)
        self.btn_FullView.setGeometry(QtCore.QRect(260, 200, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(1)
        self.btn_FullView.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_FullView.setFont(font)
        self.btn_FullView.setStyleSheet("QPushButton{\n"
"  border-radius: 15px;\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:transparent;\n"
"  color: white;\n"
"  font-size: 23px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:white;\n"
"  color: black;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgba(255,255,255,155);\n"
"border:1px solid rgb(0,0,0);\n"
"}\n"
"")
        self.btn_FullView.setObjectName("btw_FullView")
        self.btn_Info = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Info.setGeometry(QtCore.QRect(260, 260, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setFamily("Segoe UI Light")
        self.btn_Info.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Info.setFont(font)
        self.btn_Info.setStyleSheet("QPushButton{\n"
"  border-radius: 15px;\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:transparent;\n"
"  color: white;\n"
"  font-size: 23px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:white;\n"
"  color: black;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgba(255,255,255,155);\n"
"border:1px solid rgb(0,0,0);\n"
"}\n"
"")
        self.btn_Info.setObjectName("btw_Info")
        self.btn_Save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Save.setGeometry(QtCore.QRect(200, 330, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(1)
        self.btn_Save.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Save.setFont(font)
        self.btn_Save.setStyleSheet("QPushButton{\n"
"  border-radius: 15px;\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:transparent;\n"
"  color: white;\n"
"  font-size: 23px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:white;\n"
"  color: black;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgba(255,255,255,155);\n"
"border:1px solid rgb(0,0,0);\n"
"}\n"
"")
        self.btn_Save.setObjectName("btw_Save")
        self.btn_Exit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Exit.setGeometry(QtCore.QRect(380, 330, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(1)
        self.btn_Exit.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Exit.setFont(font)
        self.btn_Exit.setStyleSheet("QPushButton{\n"
"  border-radius: 15px;\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:transparent;\n"
"  color: white;\n"
"  font-size: 23px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:white;\n"
"  color: black;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgba(255,255,255,155);\n"
"border:1px solid rgb(0,0,0);\n"
"}\n"
"")
        self.btn_Exit.setObjectName("btn_Exit")
        self.btn_Settings = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Settings.setGeometry(QtCore.QRect(480, 28, 50, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(1)
        self.btn_Settings.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Settings.setFont(font)
        self.btn_Settings.setStyleSheet("QPushButton{\n"
"  border-radius: 20px;\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:transparent;\n"
"  color: white;\n"
"  font-size: 23px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  border:1px solid rgb(255,255,255);\n"
"  background-color:white;\n"
"  color: black;\n"
"}\n"
"QPushButton:pressed {\n"
"background-color: rgba(255,255,255,155);\n"
"border:1px solid rgb(0,0,0);\n"
"}\n"
"")
        self.btn_Settings.setObjectName("btn_Settings")
        self.btn_Settings.setIcon(QIcon("Images/settings.png"))
        self.btn_Settings.setIconSize(QtCore.QSize(25,25))
        self.lb_Selcted = QtWidgets.QLabel(self.centralwidget)
        self.lb_Selcted.setGeometry(QtCore.QRect(200, 90, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.lb_Selcted.setFont(font)
        self.lb_Selcted.setStyleSheet("color:White;\n"
"border-bottom: 1px solid white;\n"
"border-radius: 0px")
        self.lb_Selcted.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_Selcted.setObjectName("lb_Selcted")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 20, 371, 361))
        self.label_2.setStyleSheet("background: rgba( 255, 255, 255, 0.25 );\n"

"border-radius: 10px;\n"
"border: 1px solid rgba( 255, 255, 255, 0.18 );")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        #Packing the widgets
        self.label.raise_()
        self.label_2.raise_()
        self.btn_WireFrame.raise_()
        self.btn_Save.raise_()
        self.btn_Info.raise_()
        self.btn_FullView.raise_()
        self.btn_Exit.raise_()
        self.btn_Settings.raise_()
        self.btn_Select.raise_()
        self.lb_Selcted.raise_()
#Button Events (Functions)
        self.btn_Exit.clicked.connect(Exit)
        self.btn_Select.clicked.connect(OpenFile)
        self.btn_WireFrame.clicked.connect(ShowWireFrame)
        self.btn_Info.clicked.connect(ShowInfo)
        self.btn_Settings.clicked.connect(ShowSettings)
        self.btn_Save.clicked.connect(ExportData)
        self.btn_FullView.clicked.connect(ShowFullView)
        #Set up the text
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

#This Function is mainly used for more languages in UI, but I used that for setting up text and changing "Selected Object" label
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "3D Object Viewer"))
        self.btn_Select.setText(_translate("MainWindow", "Select .obj File"))
        self.btn_WireFrame.setText(_translate("MainWindow", "Show WireFrame"))
        self.btn_FullView.setToolTip(_translate("MainWindow", "<html><head/><body><p>Wasn\'t planned to do, doesn\'t work with every object</p></body></html>"))
        self.btn_FullView.setText(_translate("MainWindow", "Show Full View"))
        self.btn_Info.setText(_translate("MainWindow", "Object Info"))
        self.btn_Save.setText(_translate("MainWindow", "Export"))
        self.btn_Exit.setText(_translate("MainWindow", "Exit"))
        if(objname == ""):
                self.lb_Selcted.setText(_translate("MainWindow", "Selected Object"))
        else:
                self.lb_Selcted.setText(_translate("MainWindow", objname))

#Main function which puts everything together
if __name__ == "__main__":
        #Setting up the UI
        app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        ui = Ui_MainWindow()
        ui.setupUi(Form)
        Form.show()
        FormSettings = QtWidgets.QWidget()
        UiSettings = Settings.Ui_SettingWindow()
        UiSettings.setupUi(FormSettings)
        sys.exit(app.exec_())
        
