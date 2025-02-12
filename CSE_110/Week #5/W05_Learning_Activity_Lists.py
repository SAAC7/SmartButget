friends = []
while True:
    name = input("Type the name of a friend: ")
    if name.lower() == "end":
        break
    friends.append(name.title())

print(f" Your Friends are: ")
for friend in friends:
    print(friend)