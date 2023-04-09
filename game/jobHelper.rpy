##Helper file for all the code related to job application calculations is declared and defined.

init python:
    # use google's data
    # https://about.google/belonging/diversity-annual-report/2022/
    # 2022 hiring percentages:
    # white (male): 25.4%
    # white (female): 14.8%
    # black (male): 5.0%
    # black (female): 4.3%
    # asian (male): 28.9%
    # asian (female): 17.4%
    # hispanic (male): 5.8%
    # hispanic (female): 3.2%
    # again, no non-binary data. Will group that with women.
    # we will use these raw probabilities for our computations bc
    # while it is not the true probability of the group getting a job at Google,
    # it helps illustrate the implicit biases we would likely see in the hiring process
    # due to a lack of diversity in the current workforce.
    def compute_faang_acceptance_prob(player):
        if player.race == Race.White and player.gender == Gender.Man:
            return 0.254
        elif player.race == Race.White and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.148
        elif player.race == Race.Black and player.gender == Gender.Man:
            return 0.05
        elif player.race == Race.Black and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.043
        elif player.race == Race.Asian and player.gender == Gender.Man:
            return 0.289
        elif player.race == Race.Asian and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.174
        elif player.race == Race.Hispanic and player.gender == Gender.Man:
            return 0.058
        elif player.race == Race.Hispanic and (player.gender == Gender.Woman or
                                            player.gender == Gender.Nonbinary):
            return 0.032


    # based on Uber's workforce data. It's not really a startup...
    # but it's closer in culture than a Google would be.
    # though, note that companies with shit diversity would never post their numbers.
    # so what we're seeing is really as good as it gets in terms of diversity...
    # white (male): 23.2%
    # white (female): 17.1%
    # black (male): 5.4%
    # black (female): 4.0%
    # asian (male): 20.7%
    # asian (female): 15.3%
    # hispanic (male): 5.7%
    # hispanic (female): 4.2%
    def compute_other_acceptance_prob(player):
        if player.race == Race.White and player.gender == Gender.Man:
            return 0.232
        elif player.race == Race.White and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.171
        elif player.race == Race.Black and player.gender == Gender.Man:
            return 0.054
        elif player.race == Race.Black and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.04
        elif player.race == Race.Asian and player.gender == Gender.Man:
            return 0.207
        elif player.race == Race.Asian and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.153
        elif player.race == Race.Hispanic and player.gender == Gender.Man:
            return 0.057
        elif player.race == Race.Hispanic and (player.gender == Gender.Woman or
                                            player.gender == Gender.Nonbinary):
            return 0.042


    # a little bonus we add to prob of getting a job based on the school.
    # less impact the longer since graduating.
    # based on data pulled from LinkedIn:
    # https://www.linkedin.com/company/google/people/?facetSchool=166688%2C4695%2C1646%2C3173
    # in sample size of 3817 Google employees, we have
    # 1657 Harvard
    # 789 Princeton
    # 689 Michigan State
    # 682 Ohio State
    # so 64% ivey, 36% state
    def school_job_bonus(player):
        job_count = player.job_hops + player.promotions
        bonus_factor = 0.5
        if job_count > 0:
            bonus_factor = bonus_factor ** job_count
        
        bonus = 0.0
        if player.school == SchoolOptions.Ivey:
            bonus = 0.64
        elif player.school == SchoolOptions.State:
            bonus = 0.36

        return bonus * bonus_factor

    def job_history_bonus(player):
        c = 0
        for n in player.jobs:
            c += n.value
        c += player.promotions * 2
        c += player.yoe

        if c <= 3:
            return 0
        elif c <= 6:
            return 0.1
        elif c <= 10:
            return 0.2
        elif c <= 15:
            return 0.4
        elif c <= 20:
            return 0.6
        elif c <= 28:
            return 0.8
        else:
            return 1

    # https://www.eeoc.gov/special-report/diversity-high-tech
    # tech jobs percent in management by race.
    # 20.5% women, 79.5% men.
    # white (male): 60.8%
    # white (female): 15.7%
    # black (male): 3.3%
    # black (female): 0.8%
    # asian (male): 10.3%
    # asian (female): 2.7%
    # hispanic (male): 3.9%
    # hispanic (female): 1.0%
    def compute_promo_prob(player):
        if player.race == Race.White and player.gender == Gender.Man:
            return 0.608
        elif player.race == Race.White and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.157
        elif player.race == Race.Black and player.gender == Gender.Man:
            return 0.033
        elif player.race == Race.Black and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.008
        elif player.race == Race.Asian and player.gender == Gender.Man:
            return 0.103
        elif player.race == Race.Asian and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.027
        elif player.race == Race.Hispanic and player.gender == Gender.Man:
            return 0.039
        elif player.race == Race.Hispanic and (player.gender == Gender.Woman or
                                            player.gender == Gender.Nonbinary):
            return 0.01

    # just returns the 'best' option.
    # now we consider school, race, gender.
    def intern_apply(player, job_opts):
        player.yoe += 1
        res = []
        for job in job_opts:
            p = 0.0
            if job == JobOptions.FAANG:
                p = compute_faang_acceptance_prob(player) + school_job_bonus(player)
            elif job == JobOptions.Startup:
                p = compute_other_acceptance_prob(player) + school_job_bonus(player)
            elif job == JobOptions.Local_IT_Company:
                p = compute_other_acceptance_prob(player) + school_job_bonus(player)
            elif job == JobOptions.Minimum_Wage:
                p = 1

            if IS_DEBUG:
                print('\t', job, p)

            if player.biased_flip(p):
                res.append(job)

        if IS_DEBUG:
            print('\t', res)
        return res

    def select_job(player, job, isPromoOrSwitch=False, useCurrent=False):
        player.jobs.append(job)
        if isPromoOrSwitch:
            salary = player.salaries[-1] * jobDetails[job]['promo'] * player.race_bias
            player.salaries.append(salary)
        elif useCurrent:
            salary = player.salaries[-1] * player.race_bias
            player.salaries.append(player.salaries[-1])
        else:
            salary = jobDetails[job]['salary'] * player.race_bias
            player.salaries.append(salary)

    def select_intern(player, job):
        player.jobs.append(job)
 
    def get_job_name(job):
        if job == JobOptions.FAANG:
            return 'a FAANG SWE'
        elif job == JobOptions.Startup:
            return 'a Startup SWE'
        elif job == JobOptions.Local_IT_Company:
            return 'a Local IT Company SWE'
        elif job == JobOptions.Minimum_Wage:
            return 'a Minimum Wage Job'

    def job_apply(player, job_opts):
        # tier the jobs.
        # only return a job > the cur job.

        # for earlier iterations, weight the school and internship more heavily.
        player.yoe += 1
        res = []
        for job in job_opts:
            p = 0.0
            if job == JobOptions.FAANG:
                p = compute_faang_acceptance_prob(player) + school_job_bonus(player)
            elif job == JobOptions.Startup:
                p = compute_other_acceptance_prob(player) + school_job_bonus(player)
            elif job == JobOptions.Local_IT_Company:
                p = compute_other_acceptance_prob(player) + school_job_bonus(player)
            elif job == JobOptions.Minimum_Wage:
                p = 1

            if IS_DEBUG:
                print('\t', job, p)

            if player.biased_flip(p):
                res.append(job)

        if IS_DEBUG:
            print('\t', res)
        return res

    # return true if promoted, else false.
    def job_promotion(player):
        player.yoe += 1
        p = compute_promo_prob(player)
        p_2 = job_history_bonus(player)
        p = min(1, p+p_2)

        res = player.biased_flip(p)
        if res:
            player.promotions += 1
        return res

    #returns true if switched, else false.
    def job_switch(player, job):
        player.yoe += 1
        res = []
        
        p = 0.0
        if job == JobOptions.FAANG:
            p = compute_faang_acceptance_prob(player)
        elif job == JobOptions.Startup:
            p = compute_other_acceptance_prob(player)
        elif job == JobOptions.Local_IT_Company:
            p = compute_other_acceptance_prob()
        elif job == JobOptions.McDonalds:
            p = 1

        p_2 = job_history_bonus(player)
        if IS_DEBUG:
            print('\t', p_2)
        p = min(1, p+p_2)

        if IS_DEBUG:
            print('\t', job, p)

        did_get = player.biased_flip(p)
        if did_get:
            player.job_hops += 1
        return did_get
    
    def financial_aid(player):
        p = 0
        if player.household_income <= 70000:
            p = 1
        elif player.household_income <= 80000:
            p = 0.8
        elif player.household_income <= 90000:
            p = 0.76
        elif player.household_income <= 100000:
            p = 0.74
        elif player.household_income <= 110000:
            p = 0.72
        elif player.household_income <= 120000:
            p = 0.69
        elif player.household_income <= 130000:
            p = 0.66
        elif player.household_income <= 140000:
            p = 0.63
        elif player.household_income <= 150000:
            p = 0.59
        elif player.household_income <= 160000:
            p = 0.54
        elif player.household_income <= 170000:
            p = 0.49
        elif player.household_income <= 180000:
            p = 0.43
        elif player.household_income <= 190000:
            p = 0.28
        elif player.household_income <= 200000:
            p = 0.24
        else:
            p = 0.0

        return player.biased_flip(p)


    def summary(player):
        job_count = player.promotions + player.job_hops
        final_salary = SalaryBands.L3.value
        if job_count == 1:
            final_salary = SalaryBands.L4.value
        elif job_count == 2:
            final_salary = SalaryBands.L5.value
        elif job_count == 3:
            final_salary = SalaryBands.L6.value
        elif job_count == 4:
            final_salary = SalaryBands.L7.value
        elif job_count == 5:
            final_salary = SalaryBands.L8.value

        return {
            'final_salary': final_salary,
            'promotions': player.promotions,
            'job_hops': player.job_hops,
        }