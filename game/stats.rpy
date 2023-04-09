screen gameUI:
    imagebutton:
        xalign 1.0
        yalign 0.0
        xoffset -30
        yoffset 30
        auto "UI/stats_%s.png"
        action ShowMenu("StatsUI")
        
## Stats UI
screen StatsUI():
    tag statsUI
    add "UI/bg peach.png"
    hbox:
        ## left frame
        ## Right frame
        ## Notice that we're using selectedCharacter to show the variables here.
        frame:
            ysize 1080
            xsize 1280
            vbox:
                xoffset 20
                yoffset 20
                text "Name: [user.name]"
                text "Blood Type: [user.race]"
                text "Major: [user.school_name]"
                text "Affection"
                ## We're creating a bar with the max affection of 10
                ## You can change the max affection to 100 or whatever value you want.
            #     bar value StaticValue(selectedCharacter.affection, 10) xsize 300 xoffset 80
            # add selectedCharacter.imageName xalign 1.0 yalign 0.5

style stats_button_text:
    xalign 0.5