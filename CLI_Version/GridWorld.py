from State import State
actions=['Right','Left','Up','Down']
epsilon=0.00001
discount=0.99
livingreward=-2
firereward=-1
diamondreward=1
v=[]
v_=[[],[],[]]

def printfinalpolicy(Policy):
    for i in range(len(Policy)):
        for j in range(len(Policy[i])):
            if Policy[i][j]=='Right':
                print('%-4s'%'>',end='')
            elif Policy[i][j]=='Left':
                print('%-4s'%'<',end='')
            elif Policy[i][j]=='Up':
                print('%-4s'%'^',end='')
            elif Policy[i][j]=='Down':
                print('%-4s'%'v',end='')
            elif Policy[i][j]=='Block':
                print('%-4s'%'|',end='')
            else:
                print('%-4s'%Policy[i][j][0],end='')
        print()

def predictnext(rowindex,columnindex,direction):
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

def calculatemax(state,v):
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
    Policy[0][3]='Diamond'
    Policy[1][3]='Fire'
    Policy[1][1]='Block'
    if delta < (epsilon*(1-discount))/discount:
        break
printfinalpolicy(Policy)
input()