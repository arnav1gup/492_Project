# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define pov = Character("[povname]")

define n = Character("",  what_slow_cps=50, what_slow_abortable=False, image="nar")
# The game starts here.

label start:

    show bg welcome
    with fade
    n neutral"Welcome to the Game of Life!"

    n neutral"I am an AI assistant that will be guiding you through this simulation!" 

    n neutral"The purpose of this game is to show much our circumstances such as race, sex and the income we're born into and have no control on can unknowingly have an affect on our lives."

    n neutral"This game will take you through the multiple stages of becoming a software engineer all the way from high school to to a full time career!"

    n neutral"You will be assigned a Race, Gender, and Household Income. Then you shall maneuver through you career making decisions each step along the way that will be influenced by these factors! Good luck!"
    $ povname = renpy.input("To start the game, please enter your name: ", length=32)
    $ user.name = povname
    #show scene 
    n happy"Welcome [user.name]!"
    
    python:
        gender = user.getGender()
        race = user.getRace()

    n neutral"For this simulation you have been assigned the following attributes \n Income: [user.household_income], Race: [race], Gender: [gender]"
    n neutral"Keep these attributes in mind when making your choices!"
    #if time create some kind of stats panel

    n neutral"The first step of becoming a software engineer after high school, will be obtaining your degree." 
    
    n neutral "Go through each of the university options given
    , read the description and choose which ones you would like to apply." 
    
    n neutral "Remmember it is always reccomended to apply to more than one university!"

    jump uni_apply

default ivey_apply = False
default stateUni_apply = False
default community_apply = False

label uni_apply:

    show bg ivey_league
    with fade

    menu:
        n thinking "Would you Like to Apply to an Ivy League (or equivalent) University? Ivey League universities are extremely selective and usually only take in
        the best of candidates!"
        "Yes":
            $ ivey_apply = True
        
        "No":
            pass

    show bg state_uni
    with fade
    menu: 
        n thinking"Would you Like to Apply to an Local State University? State universities have acceptance rates ranging from 50-80\%"
        "Yes":
            $ stateUni_apply = True
        
        "No":
            pass
    show bg community
    with fade
    menu: 
        n thinking "Would you Like to Apply to a Community College? Community colleges are not selective and have acceptance rates of close to 100\%!"
        "Yes":
            $ community_apply = True
        
        "No":
            pass
    
    if not ivey_apply and not stateUni_apply and not community_apply:
        show bg restart
        n neutral "You must apply to at least one university!"
        jump uni_apply
    
    jump uni_decisions

    
default no_accept_unis = False

label uni_decisions:
    
    python:
        school_opts = []
        if(ivey_apply):
            school_opts.append(SchoolOptions.Ivey)
        if(stateUni_apply):
            school_opts.append(SchoolOptions.State)
        if(community_apply):
            school_opts.append(SchoolOptions.Community)
        
        accepted_unis = school_apply(user, school_opts)
        ivey_acept = SchoolOptions.Ivey in accepted_unis
        community_acept = SchoolOptions.Community in accepted_unis
        state_accept = SchoolOptions.State in accepted_unis

        #if accepted_unis empty then no_accept = true
        no_accept_unis = len(accepted_unis) == 0

    if no_accept_unis:
        jump no_uni
    if ivey_apply:
        if ivey_acept:
            n happy "Congratulations! You were accepted into an Ivey League University"
            show bg ivey_league
        else:
            show bg restart
            n sad "Unfortunately you were not accepted into an Ivey League University"
    if stateUni_apply:    
        if state_accept:
            show bg state_uni
            n happy "Congratulations! You were accepted into a Local State University"
        else:
            show bg restart
            n sad "Unfortunately you were not accepted into a Local State University"
    if community_apply:
        if community_acept:
            show bg community
            n happy "Congratulations! You were accepted into a Community College"
        else:
            show bg restart
            n sad "Unfortunately you were not accepted into a Community College"
        
    jump select_uni

label no_uni:
    show bg restart
    with fade
    n sad "Unfortunately you were not accepted into any universities, 
    you will have to take a gap year and reapply next year!"
    jump uni_apply

label select_uni:

    if no_accept_unis:
        jump no_uni

    show bg question
    with fade
    menu:
        n neutral"Which school would you like to select to attend?"

        "Ivey League (Cost 50,000 per year)" if ivey_acept and not financial_aid_apply:
            if user.household_income < 75000:
                jump financial_aid
            else:
                $ school_select(user, SchoolOptions.Ivey)
            #if this option is chosen, check if household income is more than 75,000. If yes then okay,
            #otherwise send to financial aid section
        
        "Local State University (Cost 30,000 per year)" if state_accept:
            $ school_select(user, SchoolOptions.State)

        "Community College (Cost 10,000 per year)" if community_acept:
            $ school_select(user, SchoolOptions.Community)

    if user.school == SchoolOptions.Ivey:
        show bg ivey_league
        with fade
    elif user.school == SchoolOptions.State:
        show bg state_uni
        with fade
    elif user.school == SchoolOptions.Community:
        show bg community
        with fade
    hide narrator thinking
    n happy "Congratulations [user.name] you are going to [user.school_name]!"

    jump during_uni

default financial_aid_apply = False

label financial_aid:

    show bg application
    with fade

    menu:
        n sad"Unforutnately, you do not have enough money to attend an Ivey League University without financial aid. Would you like to apply for financial aid?"

        "Yes":
            $ recieved = financial_aid(user)
            if (recieved):
                n happy "Congratulations! You have recieved financial aid!"
                $ school_select(user, SchoolOptions.Ivey)
                show bg ivey_league
                with fade
                n happy "Congratulations [user.name] you are going to [user.school_name]!"
                jump during_uni

            else:
                show bg restart
                with fade
                n sad "Unfortunately you did not recieve financial aid, please choose another university to attend"
                $ financial_aid_apply = True
                $ accepted_unis.remove(SchoolOptions.Ivey)
                if len(accepted_unis) == 0:
                    $ no_accept = True
                jump select_uni

        "No, I do not want to apply for financial aid":
            jump select_uni
    
label during_uni:
    scene bg three years
    pause 1      
    # show 3 years later screen

    if user.school == SchoolOptions.Ivey:
        show bg ivey_league
        with fade
    elif user.school == SchoolOptions.State:
        show bg state_uni
        with fade
    elif user.school == SchoolOptions.Community:
        show bg community
        with fade


    n neutral "Wow time really flew by looks like you are in your last year of university and its time to get an internship to add some
    work experience to your resume!"
    
    n neutral "A strong internship can do wonders for a fulltime career so go through the options and apply carefully!"

    show bg faang
    with fade

    menu:
        n thinking "Would you Like to Apply to a FAANG SWE internship? FAANG jobs have competitve pay, and require high skill! They are highly selective and only 
        accept the best of the best and only hire the best!"
        "Yes":
            $ faang_intern_apply = True
        
        "No":
            $ faang_intern_apply = False
    
    show bg local_it
    with fade 
    menu:
        
        n thinking "Would you Like to Apply to a Local IT Company? Local IT companies require medium skill and are fairly selective"
        "Yes":
            $ local_intern_apply = True
        
        "No":
            $ local_intern_apply = False
    
    show bg startup 
    with fade
    menu:
        
        n thinking "Would you Like to Apply to a Tech Startup? Tech Startups require medium-low skill and is the best way for a begginer to get work experience in the tech industry!"
        "Yes":
            $ startup_intern_apply = True
        
        "No":
            $ startup_intern_apply = False
    
    show bg minimum_wage
    with fade
    menu: 
        n thinking "Would you Like to Apply to a Minimum wage job? Minimum wage jobs typically require little to no prior or skill knowledge"
        "Yes":
            $ minimum_intern_apply = True
        
        "No":
            $ minimum_intern_apply = False
    
    jump after_intern_apply

label after_intern_apply:
    
    python:
        intern_opts = []
        if(faang_intern_apply):
            intern_opts.append(JobOptions.FAANG)
        if(local_intern_apply):
            intern_opts.append(JobOptions.Local_IT_Company)
        if(startup_intern_apply):
            intern_opts.append(JobOptions.Startup)
        if(minimum_intern_apply):
            intern_opts.append(JobOptions.Minimum_Wage)

        accepted_interns = intern_apply(user, intern_opts)
        faang_acept_intern = JobOptions.FAANG in accepted_interns
        local_acept_intern = JobOptions.Local_IT_Company in accepted_interns
        startup_accept_intern = JobOptions.Startup in accepted_interns
        minimum_accept_intern =  JobOptions.Minimum_Wage in accepted_interns
        no_accept_intern = len(accepted_interns) == 0

    if no_accept_intern:
        show bg restart
        n sad "Unfortunately you were accepted to no internships. You'll have better luck for your fulltime career!"
        $ select_intern(user, JobOptions.Unemployed)
        jump after_uni

    if faang_intern_apply:
        if faang_acept_intern:
            show bg faang
            n happy "Congratulations! You were selected for a FAANG SWE Internship"
        else:
            show bg restart
            n sad "Unfortunately you were not selected for a FAANG SWE Internship"

    if local_intern_apply:
        if local_acept_intern:
            show bg local_it
            n happy "Congratulations! You were selected for a Local IT Company"
        else:
            show bg restart
            n sad "Unfortunately you were not selected for a Local IT Company"

    if startup_intern_apply:
        if startup_accept_intern:
            show bg startup
            n happy "Congratulations! You were selected to work for a Startup"
        else:
            show bg restart
            n sad "Unfortunately you were not selected to work for a Startup"

    if minimum_intern_apply:
        if minimum_accept_intern:
            show bg minimum_wage
            n happy "Congratulations! You were selected to work for a Minimum Wage Job"
        else:
            show bg restart
            n sad "Unfortunately you were not selected to work for a Minimum Wage Job"
        

    show bg question
    menu:
        n neutral "Which internship would you like to select?"

        "FAANG SWE Internship (Pay: $8000 per month)" if faang_acept_intern:
            $ select_intern(user, JobOptions.FAANG)
        
        "Local IT Company Internship (Pay: $5000 per month)" if local_acept_intern:
            $ select_intern(user, JobOptions.Local_IT_Company)

        "Tech Startup (Pay: $3000 per month)" if startup_accept_intern:
            $ select_intern(user, JobOptions.Startup)

        "Minimum Wage job (Pay: $1500 per month)" if minimum_accept_intern:
            $ select_intern(user, JobOptions.Minimum_Wage)
    
    $ job = jobDetails[user.jobs[0]]['name']
    n happy "Congratulations [user.name] you are going to work as [job] for the summer!"

    jump after_uni

label after_uni(show_intro=True):
    
    if show_intro:
        show bg grad
        with fade
        n happy "Congratulations on completing your university. It is now time to find a fulltime job! Read the options and apply!"
    
    show bg faang
    with fade
    menu:
        
        n thinking "Would you Like to Apply to a FAANG SWE full time role? FAANG jobs have competitve pay, and require high skill"
        "Yes":
            $ faang_apply = True
        
        "No":
            $ faang_apply = False
    show bg local_it
    with fade

    menu:
         
        n thinking"Would you Like to Apply to a Local IT Company full time SWE role? Local IT companies require medium skill"
        "Yes":
            $ local_apply = True
        
        "No":
            $ local_apply = False
    show bg startup
    with fade

    menu: 
        
        n thinking"Would you Like to Apply to a Tech Startup full time SWE role? Tech Startups require medium-low skill"
        "Yes":
            $ startup_apply = True
        
        "No":
            $ startup_apply = False
    
        
    jump after_job_apply
    
label after_job_apply:
    
    python:
        first_job_opts = []
        if(faang_apply):
            first_job_opts.append(JobOptions.FAANG)
        if(local_apply):
            first_job_opts.append(JobOptions.Local_IT_Company)
        if(startup_apply):
            first_job_opts.append(JobOptions.Startup)

        accepted_jobs = job_apply(user, first_job_opts) #will return array of all possible accepted jobs
        faang_accept_full = JobOptions.FAANG in accepted_jobs
        local_accept_full = JobOptions.Local_IT_Company in accepted_jobs
        startup_accept_full = JobOptions.Startup in accepted_jobs
        no_accept_full = len(accepted_jobs) == 0

    if no_accept_full:
    # Decide what to do about full time rejection
        show bg restart
        n sad "Unfortunately you were accepted to no fulltime jobs"
        jump no_job

    if faang_apply:
        if faang_accept_full:
            show bg faang
            n happy "Congratulations! You were selected for a SWE Fulltime role at FAANG"
        else:
            show bg restart
            n sad "Unfortunately you were not selected for a SWE Fulltime role at FAANG"

    if local_apply:
        if local_accept_full:
            show bg local_it
            n happy "Congratulations! You were selected for a SWE Fulltime role at Local IT Company"
        else:
            show bg restart
            n sad "Unfortunately you were not selected for a SWE Fulltime role at Local IT Company"

    if startup_apply:
        if startup_accept_full:
            show bg startup
            n happy "Congratulations! You were selected to work for a SWE Fulltime role at a Startup"
        else:
            show bg restart
            n sad "Unfortunately you were not selected to work for a SWE Fulltime role at a Startup"


    show bg question
    with fade
    
    menu:
        n neutral"Which full time role would you like to select?"

        "FAANG SWE (Pay: $170000 per year)" if faang_accept_full:
            $ select_job(user, JobOptions.FAANG)
        
        "Local IT Company (Pay: $110000 per month)" if local_accept_full:
            $ select_job(user, JobOptions.Local_IT_Company)

        "Tech Startup (Pay: $95000 per month)" if startup_accept_full:
            $ select_job(user, JobOptions.Startup)
    
    $ current_job = user.jobs[-1]
    n happy"Congratulation [user.name] you are going to work as [current_job] for your full time job!"

    jump after_first_job

label no_job:
    $ job_loop += 1
    n sad "Unfortunately, you could not get a job for Year [job_loop]. You are currently unemployed. Try again next year!"
    $ select_job(user, JobOptions.Unemployed)
    call after_uni(False)
    

default job_loop = 0
default promotion_apply = False
default switch_jobs = False

label after_first_job:

    scene bg one year
    pause 1  

    $ job_loop += 1
    if job_loop == 5:
        jump end_game
    if user.jobs[-1] == JobOptions.Unemployed:
        show bg application
        with fade
    if user.jobs[-1] == JobOptions.FAANG:
        show bg faang
        with fade
    if user.jobs[-1] == JobOptions.Local_IT_Company:
        show bg local_it
        with fade
    if user.jobs[-1] == JobOptions.Startup:
        show bg startup
        with fade 
    $ currjob = jobDetails[user.jobs[-1]]['name']
    $ currsalary = user.salaries[-1]
    n happy "Congratulations on your completing Year [job_loop] of your fulltime career! You are working as [currjob] and are earning $[currsalary]. Since it's been a year at this position and this job, you can make the decision of whether you would like to 
    change jobs or apply for a promotion to increase your pay!"

    menu:
        n thinking "What would you like to do?"

        "Apply for a promotion":
            $ promotion_apply = True
            jump promotion

        "Switch Jobs":
            $ switch_jobs = True
            jump job_switch
    
        
label promotion:

    show bg application
    n thinking"Did you get a promotion?"
    $ did_get = job_promotion(user)

    if did_get:
        n happy"Congratulations! You were selected for a promotion!"
        $ select_job(user, user.jobs[-1], isPromoOrSwitch=True)
    else:
        n sad "Unfortunately you were not selected for a promotion! Try again next year!"
        $ select_job(user, user.jobs[-1])

label job_switch:
    if user.jobs[-1] == JobOptions.FAANG:
        menu:
            n thiking "Which job can would you like to apply to switch to (You can only pick one so pick wisely!)"
            
            "Other FAANG SWE (25\% higher than current job)":
                $ accepted_switch = job_switch(user, JobOptions.FAANG)
                if (accepted_switch):
                    show bg faang
                    n happy "Congratulations! You were selected to work for a new FAANG SWE!"
                    $ select_job(user, JobOptions.FAANG, isPromoOrSwitch=True)
                else:
                    n sad "Unfortunately you were not selected to work for a new FAANG SWE! Try again next year!"
                    $ select_job(user, JobOptions.FAANG, useCurrent=True)

    if user.jobs[-1] == JobOptions.Local_IT_Company:
        menu:
            n thinking "Which job can would you like to apply to switch to (You can only pick one so pick wisely!)"
            
            "FAANG SWE (Pay: 25\% higher than current job)":
                $ accepted = job_switch(user, JobOptions.FAANG)
                if (accepted_switch):
                    show bg faang
                    n happy"Congratulations! You were selected to work for a new FAANG SWE!"
                    $ select_job(user, JobOptions.FAANG, isPromoOrSwitch=True)
                else:
                    n sad "Unfortunately you were not selected to work for a new FAANG SWE! Try again next year!"
                    $ select_job(user, JobOptions.Local_IT_Company, useCurrent=True)
            
            "Other Local IT Company SWE (Pay: 15\% higher than current job)":
                $ accepted = job_switch(user, JobOptions.Local_IT_Company)
                if (accepted_switch):
                    show narrator happy
                    n happy"Congratulations! You were selected to work for a new Local IT Company SWE!"
                    $ select_job(user, JobOptions.Local_IT_Company, isPromoOrSwitch=True)
                else:
                    show narrator sad
                    n sad "Unfortunately you were not selected to work for a new Local IT Company SWE! Try again next year!"
                    $ select_job(user, JobOptions.Local_IT_Company, useCurrent=True)

    if user.jobs[-1] == JobOptions.Startup:
        menu:
            n thiking "Which job can would you like to apply to switch to (You can only pick one so pick wisely!)"
            
            "FAANG SWE (Pay: 25\% higher than current job)":
                $ accepted = job_switch(user, JobOptions.FAANG)
                if (accepted):
                    show bg faang
                    n happy "Congratulations! You were selected to work for a new FAANG SWE!"
                    $ select_job(user, JobOptions.FAANG, isPromoOrSwitch=True)
                else:
                    n sad "Unfortunately you were not selected to work for a new FAANG SWE! Try again next year!"
                    $ select_job(user, JobOptions.Local_IT_Company, useCurrent=True)

            "Local IT Company SWE (Pay: 15\% higher than current job)": 
                $ accepted = job_switch(user, JobOptions.Local_IT_Company)
                if (accepted):
                    show bg local_it
                    n happy "Congratulations! You were selected to work for a new Local IT Company SWE!"
                    $ select_job(user, JobOptions.Local_IT_Company, isPromoOrSwitch=True)
                else:
                    n sad "Unfortunately you were not selected to work for a new Local IT Company SWE! Try again next year!"
                    $ select_job(user, JobOptions.Local_IT_Company, useCurrent=True)
            "Other Startup SWE Role (Pay: $10000 higher than current job)":
                $ accepted = job_switch(user, JobOptions.Startup)
                if (accepted):
                    n happy "Congratulations! You were selected to work for a new Startup SWE!"
                    $ select_job(user, JobOptions.Startup, isPromoOrSwitch=True)
                else:
                    n sad "Unfortunately you were not selected to work for a new Local IT Company SWE! Try again next year!"
                    $ select_job(user, JobOptions.Startup, useCurrent=True)
    jump after_first_job

define n1 = nvl_narrator

label ending:

        n1 "Congratulations on completing your career!"
        "Here is the summary of your game!"
        #nvl-menu
        
        "University Attended: [user.school_name]"
        "Summer Internship: [user.jobs[0]]"
        "For your first year you worked as a [user.jobs[1]] and earnered $[user.salaries[0]]"
        "For your second year you worked as a [user.jobs[2]] and earnered $[user.salaries[1]]"
        "For your third year you worked as a [user.jobs[3]] and earnered $[user.salaries[2]]"
        "For your fourth year you worked as a [user.jobs[4]] and earnered $[user.salaries[3]]"
        "For your fifth year you worked as a [user.jobs[5]] and earnered $[user.salaries[4]]"

        $ retirement_salary = user.salaries[0] + user.salaries[1] + user.salaries[2] + user.salaries[3] + user.salaries[4]
        "Final Salary: [user.salary]"

        #Analysis of different nationalities

        "Thank you for playing! We hope this game has taught you something about the role that factors you have no control
        over such as your race, gender and financial conditions can have on your career and life! Make sure to play this game
        a few times to see how different choices and attributes assigned to you can affect your career!"

        return
