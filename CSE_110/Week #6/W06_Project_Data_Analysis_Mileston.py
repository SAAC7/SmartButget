# Entity,         Code,   Year,     Life expectancy (years)
# Afghanistan,    AFG,    1950,     27.638


max_life = None
min_life = None
with open("CSE_110/Week #6/life-expectancy.csv") as database:
    for line in database:
        try:
            life_exp=float(line.strip().split(",")[3])
        except ValueError:
            continue
        if max_life==None or life_exp > max_life:
            max_life = life_exp
        if min_life==None or life_exp < min_life:
            min_life = life_exp 
print(f"The highest value for life expectancy is: {max_life}")
print(f"The lowest value for life expectancy is: {min_life}")

