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
    if spisok:
        for i in spisok:
            musik_mass.append(i.name_musiks)
        mass_random = []
        for i in range(11):
            mass_random.append(random.choice(musik_mass))
        #print(mass_random)
        return mass_random
    else:
        return musik_mass

def photo_val(file_name):
    mass = file_name.split(".")
    if mass[-1] not in ['png','jpeg','jpg','PNG']:
        return "no"
    else:
        return "yes"