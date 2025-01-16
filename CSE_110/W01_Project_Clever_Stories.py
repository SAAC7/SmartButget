print(f"Welcome, are you ready to enjoy and laugh with a Mad Libs?\nSo now all you have to do is enter the following information: ")
print(f"--------------------------------------------------------------")
adjective=input("Adjetive: ").lower()
animal=input("Animal: ").lower()
verb1=input("Verb: ").lower()
exclamation=input("Exclamation: ").capitalize()
verb2=input("Verb: ").lower()
verb3=input("Verb: ").lower()
print(f"--------------------------------------------------------------")
story = (
    f"\nThe other day, I was really in trouble. It all started when I saw a very"
    f"\n{adjective} {animal} {verb1} down the hallway. \"{exclamation}!\" I yelled. But all"
    f"\nI could think to do was to {verb2} over and over. Miraculously,"
    f"\nthat caused it to stop, but not before it tried to {verb3}"
    f"\nright in front of my family.\n"
)
print(story)
