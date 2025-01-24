def check_option(options):
    not_error = True
    input_value = ""
    while (not_error):
        input_value = input("Write an option: ")
        if (input_value.lower() in [item.lower() for item in options]):
            not_error = False
        else:
            print(f"Enter a correct option")
    return input_value.capitalize()
print(        
    f"Welcome to 'The last survivor'"
    f"You are waking up but do not recognize this place."
    f"What are you going to do?"
      )
options = ["walk","scream","wait"]
print(f"options : {options}")
choise = check_option(options)
# Walk
if (choise.lower() == options[0].lower()):
    print("You decide to walk down a dark hallway. The walls are wet, and you hear faint whispers.")
    print("What do you do?")
    options = ["explore", "turn back", "hide"]
    print(f"options : {options}")
    choise = check_option(options)
    # Walk > Explore
    if (choise.lower() == options[0].lower()):
        print("You push further into the unknown, finding a bloodied door.")
        print("What do you do?")
        options = ["open the door", "turn back", "search for another path"]
        print(f"options : {options}")
        choise = check_option(options)
    # Walk > Turn Back
    elif (choise.lower() == options[1].lower()):
        print("You decide to retreat, but the whispers grow louder, and you feel a presence behind you.")
        print("What do you do?")
        options = ["run", "confront the presence", "freeze in fear"]
        print(f"options : {options}")
        choise = check_option(options)
    # Walk > Hide
    else:
        print("You find a small cabinet and hide inside. The whispers stop, but you hear heavy breathing nearby.")
        print("What do you do?")
        options = ["stay hidden", "peek outside", "burst out and run"]
        print(f"options : {options}")
        choise = check_option(options)
# Scream      
elif (choise.lower() == options[1].lower()):
    print("Your scream echoes through the desolate place. Suddenly, you hear hurried footsteps.")
    print("What do you do?")
    options = ["run", "stay quiet", "fight"]
    print(f"options : {options}")
    choise = check_option(options)
    # Scream > Run
    if (choise.lower() == options[0].lower()):
        print("You start running blindly down a dark corridor. Suddenly, the ground crumbles beneath you.")
        print("What do you do?")
        options = ["grab a ledge", "brace for impact", "try to climb back up"]
        print(f"options : {options}")
        choise = check_option(options)
    # Scream > Stay quiet
    elif (choise.lower() == options[1].lower()):
        print("You stay quiet, hoping the footsteps pass you by. But they stop right next to you.")
        print("What do you do?")
        options = ["hold your breath", "attack", "plead for mercy"]
        print(f"options : {options}")
        choise = check_option(options)
    # Scream > Fight
    else:
        print("You prepare to fight as a shadowy figure appears in the distance.")
        print("What do you do?")
        options = ["charge at it", "find a weapon", "wait for it to approach"]
        print(f"options : {options}")
        choise = check_option(options)
        
# Wait
else:
    print("You stay still, hoping something or someone will help you.")
    print("After a few moments, you hear a faint growl approaching.")
    print("What do you do?")
    options = ["hide", "investigate", "run"]
    print(f"options : {options}")
    choise = check_option(options)
    # Wait > Hide
    if (choise.lower() == options[0].lower()):
        print("You duck behind a broken table as the growling gets louder.")
        print("What do you do?")
        options = ["stay hidden", "peek", "run"]
        print(f"options : {options}")
        choise = check_option(options)
    # Wait > Investigate
    elif (choise.lower() == options[1].lower()):
        print("You cautiously move toward the growl and see a pair of glowing red eyes in the darkness.")
        print("What do you do?")
        options = ["approach", "run", "shout to scare it off"]
        print(f"options : {options}")
        choise = check_option(options)
    # Wait > Run
    else:
        print("You sprint in the opposite direction, but the growl turns into a deafening roar, and something starts chasing you.")
        print("What do you do?")
        options = ["hide", "keep running", "try to fight"]
        print(f"options : {options}")
        choise = check_option(options)

     
