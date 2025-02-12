
people = [
    "Stephanie 30",
    "John 29",
    "Emily 20",
    "Gretchen 54",
    "Noah 12",
    "Penelope 32",
    "Michael 20",
    "Jacob 1"
]
youngest_age = None
name = None
for line in people:
    age = int(line.split()[1])
    if youngest_age == None:
        youngest_age=age
        name = line.split()[0]
    if youngest_age > age:
        youngest_age=age
        name = line.split()[0]

print(f"The youngest person is: {name} with an age of {youngest_age}")
