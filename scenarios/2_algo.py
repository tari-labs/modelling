import random
import xlrd
import matplotlib.pyplot as plt

workbook = xlrd.open_workbook('merged-mining-calculations.xlsx')
worksheet = workbook.sheet_by_index(1)

miningPower = []
difficulty = []
blockA = []
blockB = []

probabilityBlockATwo = []
probabilityBlockAFive = []
probabilityBlockATen = []

probabilityBlockBTwo = []
probabilityBlockBFive = []
probabilityBlockBTen = []

for y in range(worksheet.nrows):
    miningPower.append(worksheet.cell_value(y, 0))

for y in range(worksheet.nrows):
    difficulty.append(worksheet.cell_value(y, 1))

for y in range(worksheet.nrows):
    blockA.append(worksheet.cell_value(y, 2))

for y in range(worksheet.nrows):
    blockB.append(worksheet.cell_value(y, 3))

for y in range(worksheet.nrows):
    probabilityBlockATwo.append(worksheet.cell_value(y, 4))

for y in range(worksheet.nrows):
    probabilityBlockAFive.append(worksheet.cell_value(y, 5))

for y in range(worksheet.nrows):
    probabilityBlockATen.append(worksheet.cell_value(y, 6))

for y in range(worksheet.nrows):
    probabilityBlockBTwo.append(worksheet.cell_value(y, 7))

for y in range(worksheet.nrows):
    probabilityBlockBFive.append(worksheet.cell_value(y, 8))

for y in range(worksheet.nrows):
    probabilityBlockBTen.append(worksheet.cell_value(y, 9))

print(miningPower)
print(difficulty)
print(blockA)
print(blockB)

print(probabilityBlockATwo)
print(probabilityBlockAFive)
print(probabilityBlockATen)

print(probabilityBlockBTwo)
print(probabilityBlockBFive)
print(probabilityBlockBTen)

getRandomValuesATwoY = random.sample(probabilityBlockATwo, 10)
getRandomValuesAFiveY = random.sample(probabilityBlockAFive, 10)
getRandomValuesATenY = random.sample(probabilityBlockATen, 10)

getRandomValuesBTwoY = random.sample(probabilityBlockBTwo, 10)
getRandomValuesBFiveY = random.sample(probabilityBlockBFive, 10)
getRandomValuesBTenY = random.sample(probabilityBlockBTen, 10)

getRandomValuesX = random.sample(miningPower, 10)

# Plotting Line Chart for Probability Block A
plt.plot(getRandomValuesX,getRandomValuesATwoY, label="2")
plt.plot(getRandomValuesX,getRandomValuesAFiveY, label="5")
plt.plot(getRandomValuesX,getRandomValuesATenY, label="10")
plt.xlabel("Mining Power")
plt.ylabel("Probability of finding blocks in a row using")
plt.title("A")
plt.show()

# Plotting Line Chart for Probability Block B
plt.plot(getRandomValuesX,getRandomValuesBTwoY, label="2")
plt.plot(getRandomValuesX,getRandomValuesBFiveY, label="5")
plt.plot(getRandomValuesX,getRandomValuesBTenY, label="10")
plt.xlabel("Mining Power")
plt.ylabel("Probability of finding blocks in a row using")
plt.title("B")
plt.show()

# Plotting Line Chart for Comparison of A B at 2 Blocks
plt.plot(getRandomValuesX,getRandomValuesATwoY)
plt.plot(getRandomValuesX,getRandomValuesBTwoY)
plt.xlabel("Mining Power")
plt.ylabel("Probability of finding blocks in a row using 2")
plt.title("Comparison of A B at 2 Blocks")
plt.show()

# Plotting Line Chart for Comparison of A B at 2 Blocks
plt.plot(getRandomValuesX,getRandomValuesAFiveY)
plt.plot(getRandomValuesX,getRandomValuesBFiveY)
plt.xlabel("Mining Power")
plt.ylabel("Probability of finding blocks in a row using 5")
plt.title("Comparison of A B at 5 Blocks")
plt.show()

# Plotting Line Chart for Comparison of A B at 10 Blocks
plt.plot(getRandomValuesX,getRandomValuesATenY)
plt.plot(getRandomValuesX,getRandomValuesBTenY)
plt.xlabel("Mining Power")
plt.ylabel("Probability of finding blocks in a row using 10")
plt.title("Comparison of A B at 10 Blocks")
plt.show()