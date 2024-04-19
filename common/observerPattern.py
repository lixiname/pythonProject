
from abc import abstractmethod, ABC
class Observable:
    def __init__(self):
        self.obsList = []

    def addObserver(self,obs):
        self.obsList.append(obs)
        print()

    def delObserver(self,obs):
        self.obsList.remove(obs)

    def notifyObservers(self,arg):
        for item in self.obsList:
            item.updates(arg)

class Observer(ABC):
    @abstractmethod
    def updates(self,arg):
        pass