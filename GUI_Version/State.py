class State:
    def __init__(self,rind,cind,Reward,Role='Normal',v=0,w='null'):
        self.rowindex=rind
        self.columnindex=cind
        self.V=0
        self.role=Role
        self.reward=Reward
        self.work=w
    def printindex(self):
        print(self.rowindex , self.columnindex)
    