import os

files = os.listdir("male1")
startIndex = 2501
endIndex = 7500

for index, i in enumerate(files):
    os.rename("male1/" + i, "male1/massMale" + str(index + startIndex) + ".mhm")
    print("male1/" + i + " -> " + "male1/massMale" + str(index + startIndex) + ".mhm")
