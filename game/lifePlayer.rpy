init python:    
    class LifePlayer:
        # randomly assign race, gender. Then household income.
        def __init__(self):
            self.yoe = 0
            self.race = Race(randint(1, 4))
            self.gender = Gender(randint(1, 3))
            self.race_bias = RaceBiases[self.race][self.gender]
            self.household_income = Race.income(self.race)
            self.school = SchoolOptions.No_School
            self.school_name = "No School"
            self.job_hops = 0
            self.promotions = 0
            self.jobs = []
            self.salaries = []

        #getter methods

        def getRace(self):
            if self.race.value == 1:
                return "White"
            elif self.race.value == 2:
                return "Black"
            elif self.race.value == 3:
                return "Hispanic"
            else:
                return "Asian"
        
        def getGender(self):
            if self.gender.value == 1:
                return "Man"
            elif self.gender.value == 2:
                return "Woman"
            else:
                return "Non-binary"


        def getIncome(self):
            return self.household_income
        

        # p is probability the thing happens. 0 <= p <= 1.
        # return true if it happens, false otherwise.
        def biased_flip(self, p):
            return random() <= p
        
## This is how a LifePlayer Class is created.
default user = LifePlayer()
default IS_DEBUG = False
