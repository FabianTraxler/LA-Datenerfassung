from abc import ABCMeta, abstractmethod

class Discipline(metaclass=ABCMeta):

    @abstractmethod
    def load_athlete_achievements(self, athlete_number):
        pass
    
    @abstractmethod
    def save_athlete_achievement(self, athlete_number, achievement):
        pass

    @abstractmethod
    def load_group_achievements(self, group_name):
        pass
