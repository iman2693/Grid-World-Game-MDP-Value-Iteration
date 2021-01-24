# Author : Iman Kianian
# 1 January 2021
from State import State
from PyQt5 import QtCore, QtGui, QtWidgets
class gameboard(object):
    def setupUi(self, window,epsilon,gamma,livingreward,firereward,diamondreward):
        window.setObjectName("Form")
        self.Form=window
        Form = QtWidgets.QWidget(window)
        Form.setFixedHeight(5*100)
        Form.setFixedWidth(5*100)
        Form.setObjectName("centralwidget")
        Form.setStyleSheet("border:1px dashed black;")
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.maketable(epsilon,gamma,livingreward,firereward,diamondreward)
        window.setCentralWidget(Form)
        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Grid World Game - Game Board"))

    def maketable(self,epsilon,discount,livingreward,firereward,diamondreward):
        actions=['Right','Left','Up','Down']
        v=[]
        v_=[[],[],[]]
        def predictnext(rowindex,columnindex,direction): # predict next state after doing a work  ( Successor Function )
            if direction=='Right' and (columnindex==3 or (rowindex==1 and columnindex==0)) :
                return (rowindex,columnindex)
            elif direction=='Left' and (columnindex==0 or (rowindex==1 and columnindex==2)):
                return (rowindex,columnindex)
            elif direction=='Up' and (rowindex==0 or (rowindex==2 and columnindex==1)):
                return (rowindex,columnindex)
            elif direction=='Down' and (rowindex==2 or (rowindex==0 and columnindex==1)):
                return (rowindex,columnindex)
            elif direction=='Right':
                return (rowindex,columnindex+1)
            elif direction=='Left':
                return (rowindex,columnindex-1)
            elif direction=='Up':
                return (rowindex-1,columnindex)
            elif direction=='Down':
                return (rowindex+1,columnindex)

        def calculatemax(state,v): # find Optimal Action From a state
            P=[0.8,0.1,0.1]
            actionsu=[0 for i in actions]
            for i in range(len(actions)):
                if actions[i]=='Right' or actions[i]=='Left':
                    actionscan=[actions[i],'Down','Up']
                elif actions[i]=='Up' or actions[i]=='Down':
                    actionscan=[actions[i],'Right','Left']
                for j in range(len(actionscan)):
                    nextstate=predictnext(state.rowindex,state.columnindex,actionscan[j])
                    if nextstate[0]==0 and nextstate[1]==3:
                        actionsu[i]+=P[j]*(diamondreward+(discount*v[nextstate[0]][nextstate[1]]))
                    elif nextstate[0]==1 and nextstate[1]==3:
                        actionsu[i]+=P[j]*(firereward+(discount*v[nextstate[0]][nextstate[1]]))
                    else:
                        actionsu[i]+=P[j]*(livingreward+(discount*v[nextstate[0]][nextstate[1]]))
            maxindex=0
            maxvalue=actionsu[0]
            for j in range(1,len(actions)):
                if actionsu[j]>maxvalue:
                    maxvalue=actionsu[j]
                    maxindex=j
            return (maxvalue,actions[maxindex])

        # Initialize Variables -- Start

        for i in range(3):   ## making states
            for j in range(4):
                if i==0 and j==3:
                    v_[i].append(State(i,j,diamondreward,'Diamond'))
                elif i==1 and j==1:
                    v_[i].append(State(i,j,livingreward,'Block'))
                elif i==1 and j==3:
                    v_[i].append(State(i,j,firereward,'Fire'))
                else:
                    v_[i].append(State(i,j,livingreward))
        v=[[i.V for i in v_[0]],[i.V for i in v_[1]],[i.V for i in v_[2]]]

        Policy=[['none' for i in range(4)] for i in range(3)]  # For Save Action Policy for each state.
        iterations=0  # Counting iteration of while loop

        # Initialize Variables -- End

        # Value Iteration -- Start
        while True:
            iterations+=1
            delta=0
            v=[[i.V for i in v_[0]],[i.V for i in v_[1]],[i.V for i in v_[2]]]
            for i in range(3):
                for j in range(4):
                    if not ((i==0 and j==3) or (i==1 and j==3) or (i==1 and j==1)): 
                        temp=calculatemax(v_[i][j],v)
                        v_[i][j].V=temp[0]
                        Policy[i][j]=temp[1]
                        if abs(v_[i][j].V -v[i][j])>delta:
                            delta = abs(v_[i][j].V-v[i][j])
            if delta < (epsilon*(1-discount))/discount:
                break
        # Value Iteration -- End

        # Create graphical table -- Start
        for i in range(3):                
            for j in range(4):
                label = QtWidgets.QLabel(self.Form)
                label.setFixedWidth(100)
                label.setFixedHeight(100)
                if Policy[i][j]!='none':
                    label.setPixmap(QtGui.QPixmap(f"img/{Policy[i][j]}.png"))
                elif v_[i][j].role in (('Diamond', 'Fire')):
                    label.setPixmap(QtGui.QPixmap(f"img/{v_[i][j].role}.png"))
                else:
                    label.setStyleSheet('background-color:black;')
                self.gridLayout_2.addWidget(label, i, j, 1, 1)

        label = QtWidgets.QLabel(self.Form)
        label.setFixedHeight(50)
        label.setText(f'This is The Result After {iterations} iterations . ')
        label.setStyleSheet('font-size:20px;')
        self.gridLayout_2.addWidget(label, 3, 0, 1, 4)
        # Create graphical table -- End

        print(Policy,iterations)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    ui = gameboard()
    epsilon=0.00001
    discount=0.99
    livingreward=-1
    firereward=-1
    diamondreward=1
    ui.setupUi(Form,epsilon,discount,livingreward,firereward,diamondreward)
    Form.show()
    sys.exit(app.exec_())

