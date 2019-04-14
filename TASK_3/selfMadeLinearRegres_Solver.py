import sys
import re
import operator
import numpy as np
import subprocess


def matchPa(text):
    return text.count('b')

def x_kerps(listX):
    krList = []
    for i in listX:
        krList.append(matchPa(i))
    return krList

def load_train_data(fileName):
    # ps = subprocess.Popen(('xzcat', fileName), stdout=subprocess.PIPE)
    # linesInFile = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
    # linesInFile = int(str(linesInFile, "utf-8"))
    # for i in range(1, linesInFile):
    #     if(i == 3):
    #         break
    #     oC = subprocess.check_output(('head', '-n ', str(i)), stdin=ps.stdout)
    #     outCmd = subprocess.check_output(('tail', '-n 1', str(nr)), stdin=oC.stdout)
    fileIn = open(fileName, 'r')
    listX = []
    listY = []
    for lf in fileIn.readlines():
        rawData = lf.split("\t")
        yearTrain = int(rawData[0].split(".")[0])
        dataTrain = rawData[-1]
        listX.append(dataTrain)
        listY.append(yearTrain)
    return listX, listY

def load_data(fileName):
    fileIn = open(fileName, 'r')
    listText = []
    for lf in fileIn.readlines():
        listText.append(lf)
    return listText

# Funkcja liniowa jednej zmiennej
def hhh(theta, x):
    toReturn = theta[0] + theta[1] * x
    return toReturn if toReturn >= 1814 and toReturn <= 2014 else 1914

def h(theta, x):
    return theta[0] + theta[1] * x
# ********************************************

# Funkcja licząca błąd średniokwadratowy
def J(h, theta, x, y):
    m = len(y)
    return 1.0 / (2 * m) * sum((h(theta, x[i]) - y[i])**2 for i in range(m))
# ********************************************

# Gradient Descent
def gd(h, costfun, theta, x, y, alpha, eps):
    current_cost = costfun(h, theta, x, y)
    log = [[current_cost, theta]]
    m = len(y)
    max_itern = 1200000
    count_itern = 0
    while True:
        count_itern += 1
        new_theta = [
        theta[0] - alpha/float(m) * sum(h(theta, x[i]) - y[i] for i in range(m)),
        theta[1] - alpha/float(m) * sum((h(theta, x[i]) - y[i]) * x[i] for i in range(m))
        ]
        theta = new_theta
        try:
            current_cost, prev_cost = costfun(h, theta, x, y), current_cost
            # print("diff: ",prev_cost - current_cost)
        except OverflowError:
            break

        if abs(prev_cost - current_cost) <= eps:
            break
        log.append([current_cost, theta])

        if count_itern == max_itern:
            break
    #     print(current_cost, prev_cost)
    # print(log[-1])
    return log
# ********************************************

# Funkcja sterująca
def main():
    print("ALGORITHM-TASK-SOLVER")
    listX, listY = load_train_data(sys.argv[1])
    listXkerp = x_kerps(listX)
# **************** TRAIN ****************************
    print("> TRAIN ALGORITHM")
    prev_cost = gd(h, J, [0, 0], listXkerp, listY, alpha=0.000001, eps=1000)
    bestTheta = prev_cost[-1][1]
# ***************************************************
    loadTrainDataToProcessing = load_data(sys.argv[2])
    print("> SAVE OUT")
    countMatch = 0
    countGD = 0
    with open(sys.argv[3], "w") as f:
        for tdtp in loadTrainDataToProcessing:
            yearSet = set()
            wordList = tdtp.split(" ")
            for w in wordList:
                match = re.match(r'[1-2][0-9][0-9][0-9]', w)
                if match is not None:
                    if (int(match.group()) >= 1814) and (int(match.group()) <= 2014):
                        yearSet.add(match.group())
            if len(yearSet) != 0:
                f.write(yearSet.pop() + ".0\n")
                countMatch += 1
            else:
                f.write(str(int(hhh(bestTheta, matchPa(tdtp)))) + "\n")
                countGD += 1
    print("INFO:\ncountMatch: ", countMatch, " countGD: ", countGD)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("MORE ARGS!!")
        print("python3 selfMadeLinearRegres_Solver.py train.tsv in.tsv out.tsv")
        exit()
    main()
