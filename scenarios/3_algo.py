import random
import xlrd
import matplotlib.pyplot as plt

workbook = xlrd.open_workbook('merged-mining-calculations.xlsx')
worksheet = workbook.sheet_by_index(0)

miningPower = []
difficulty = []
blockA = []

probabilityBlockATwo = []
probabilityBlockAFive = []
probabilityBlockATen = []

for y in range(worksheet.nrows):
    miningPower.append(worksheet.cell_value(y, 0))

for y in range(worksheet.nrows):
    difficulty.append(worksheet.cell_value(y, 1))

for y in range(worksheet.nrows):
    blockA.append(worksheet.cell_value(y, 2))

for y in range(worksheet.nrows):
    probabilityBlockATwo.append(worksheet.cell_value(y, 3))

for y in range(worksheet.nrows):
    probabilityBlockAFive.append(worksheet.cell_value(y, 4))

for y in range(worksheet.nrows):
    probabilityBlockATen.append(worksheet.cell_value(y, 5))

print(miningPower)
print(difficulty)
print(blockA)

print(probabilityBlockATwo)
print(probabilityBlockAFive)
print(probabilityBlockATen)

getRandomValuesTwoY = random.sample(probabilityBlockATwo, 10)
getRandomValuesFiveY = random.sample(probabilityBlockAFive, 10)
getRandomValuesTenY = random.sample(probabilityBlockATen, 10)
getRandomValuesX = random.sample(miningPower, 10)

plt.plot(getRandomValuesX, getRandomValuesTwoY)
plt.plot(getRandomValuesX, getRandomValuesFiveY)
plt.plot(getRandomValuesX, getRandomValuesTenY)
plt.xlabel("Mining Power %")
plt.ylabel("Probability of finding blocks in a row")
plt.title("A")
plt.show()

plt.plot(getRandomValuesX, getRandomValuesTwoY)
plt.xlabel("Mining Power")
plt.ylabel("Probability of finding blocks in a row using 2")
plt.title("A")
plt.show()

plt.plot(getRandomValuesX, getRandomValuesFiveY)
plt.xlabel("Mining Power")
plt.ylabel("Probability of finding blocks in a row using 5")
plt.title("A")
plt.show()

plt.plot(getRandomValuesX, getRandomValuesTenY)
plt.xlabel("Mining Power")
plt.ylabel("Probability of finding blocks in a row using 10")
plt.title("A")
plt.show()