def mp_val(file_name):
    file = file_name.split(".")
    print(file)
    if file[-1] != "mp3":
        return "no"
    else:
        return "yes"