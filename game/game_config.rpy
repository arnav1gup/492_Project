init python: 
    from enum import Enum
    from random import randint, random

    class Race(Enum):
        White = 1
        Black = 2
        Hispanic = 3
        Asian = 4
        All_Races = 5 # not an option for game.

        # https://www.census.gov/content/dam/Census/library/visualizations/2022/demo/p60-276/figure2.pdf
        # median household income by race.
        def income(race):
            if race == Race.White:
                return 78000
            elif race == Race.Black:
                return 48000
            elif race == Race.Hispanic:
                return 58000
            elif race == Race.Asian:
                return 101000
            elif race == Race.All_Races:
                return 78000
            else:
                raise ValueError('Invalid race')


    class Gender(Enum):
        Man = 1
        Woman = 2
        Nonbinary = 3


    class SchoolOptions(Enum):
        Ivey = 1
        State = 2
        Community = 3
        No_School = 4

    class JobOptions(Enum):
        FAANG = 4
        Startup = 3
        Local_IT_Company = 2
        Minimum_Wage = 1
        Unemployed = 0

        def __lt__(self, other):
            return self.value < other.value
        
        def __le__(self, other):
            return self.value <= other.value


    # from levels.fyi
    class SalaryBands(Enum):
        L3 = 140000
        L4 = 170000
        L5 = 210000
        L6 = 240000
        L7 = 280000
        L8 = 330000
    
    jobDetails = {
        JobOptions.Unemployed:{
            'salary': 0,
            'name': 'Unemployed',
            'promo':0
        },
        JobOptions.FAANG: {
            'salary': 170000,
            'name': 'a FAANG SWE',
            'promo': 1.25
        },
        JobOptions.Startup: {
            'salary': 95000,
            'name': 'a Startup SWE',
            'promo': 1.07
        },
        JobOptions.Local_IT_Company: {
            'salary': 110000,
            'name': 'a Local IT Company SWE',
            'promo': 1.15
        },
        JobOptions.Minimum_Wage: {
            'salary': 0,
            'name': 'a Minimum Wage Worker',
            'promo': 0
        }
    }

    #Race biases from the follwoing article: 
    #https://www.emergingtechbrew.com/stories/2021/05/24/report-finds-tech-racial-gender-pay-disparities-narrowing-still-present
    #Non binary data from the following article
    # https://www.codecademy.com/resources/blog/gender-pay-gap-in-tech/
    RaceBiases = {
        Race.White: {
            Gender.Man: 1,
            Gender.Woman: 0.92,
            Gender.Nonbinary: 0.7
        },
        Race.Asian: {
            Gender.Man: 1.01,
            Gender.Woman: 0.95,
            Gender.Nonbinary: 0.707
        },
        Race.Black: {
            Gender.Man: 0.89,
            Gender.Woman: 0.90,
            Gender.Nonbinary: 0.623
        },
        Race.Hispanic: {
            Gender.Man: 0.96,
            Gender.Woman: 0.90,
            Gender.Nonbinary: 0.672
        }
    }