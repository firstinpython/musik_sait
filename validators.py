import random
def mp_val(file_name):
    file = file_name.split(".")
    print(file)
    if file[-1] != "mp3":
        return "no"
    else:
        return "yes"

def random_musik(spisok):
    musik_mass = []
    for i in spisok:
        musik_mass.append(i.name_musiks)
    mass_random = []
    for i in range(11):
        mass_random.append(random.choice(musik_mass))
    print(mass_random)
    return mass_random