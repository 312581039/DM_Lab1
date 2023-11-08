"""
Description     : Simple Python implementation of the Apriori Algorithm
Modified from:  https://github.com/asaini/Apriori
Usage:
    $python apriori.py -f DATASET.csv -s minSupport

    $python apriori.py -f DATASET.csv -s 0.15
"""

import sys
import time
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """calculates the support for items in the itemSet and returns a subset
    of the itemSet each of whose elements satisfies the minimum support"""
    _itemSet = set()
    localSet = defaultdict(int)
    
    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def returnItemsWithMinSupportAndClosed(itemSet, transactionList, minSupport, closedFreqSet, prevCount=None):
    _itemSet = set()
    countDict = defaultdict(int)
    localSet = defaultdict(int)
    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                localSet[item] += 1
    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)
            countDict[item] = count  
    if prevCount and countDict:
        for prev, count_ in prevCount.items():  # k   : count_
            Closed = True
            for current, count in countDict.items():    # k+1 : count
                if prev.issubset(item):
                    if int(count) > int(count_):
                        Closed = False
                        break
            if Closed:
                closedFreqSet[prev] = float(count_) / len(transactionList)
    return _itemSet, countDict


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))  # Generate 1-itemSets
            
    return itemSet, transactionList


def frequent_itemset(data_iter, minSupport):
    itemSet, transactionList = getItemSetTransactionList(data_iter)
    freqSet = defaultdict(int)
    largeSet = dict()

    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
    currentLSet = oneCSet
    k = 2
    info = ''
    while currentLSet != set([]):    
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet= returnItemsWithMinSupport(
            currentLSet, transactionList, minSupport, freqSet
        )
        info += f"{k-1}\t{len(currentLSet)}\t{len(currentCSet)}\n"
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    return toRetItems, info


def frequent_closed_itemset(data_iter, minSupport):

    itemSet, transactionList = getItemSetTransactionList(data_iter)
    closedFreqSet = defaultdict(int)
    largeSet = dict()

    oneCSet, countDict = returnItemsWithMinSupportAndClosed(itemSet, transactionList, minSupport, closedFreqSet)
    prevCount = countDict
    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet, prevCount = returnItemsWithMinSupportAndClosed(
            currentLSet, transactionList, minSupport, closedFreqSet, prevCount=prevCount
        )
        currentLSet = currentCSet
        k = k + 1

    return closedFreqSet


def printResults(items):
    """prints the generated itemsets sorted by support """
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))


def to_str_results(items):
    """prints the generated itemsets sorted by support"""
    i = []
    for item, support in sorted(items, key=lambda x: x[1]):
        x = "item: %s , %.3f" % (str(item), support)
        i.append(x)
    return i


def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    with open(fname, "r") as file_iter:
        for line in file_iter:
            record = frozenset(line.strip().split(" ")[3:])
            yield record


def runTask(file, minS, path):
    print(f"-> Mining \033[31m{file}\033[0m with minS \033[32m{minS} ({minS/100}%)\033[0m")
    
    print("-> Start mining Frequent Itemset (Task 1)...")
    inFile = dataFromFile(path)
    task1_start = time.time()
    items, info = frequent_itemset(inFile, minS/100)
    task1_end = time.time()
    saveFreq(items, path[-6], minS)
    saveIterInfo(info, path[-6], minS, len(items))
    
    print("-> Start mining Frequent Closed Itemset (Task 2)...")
    inFile = dataFromFile(path)
    task2_start = time.time()
    items = frequent_closed_itemset(inFile, minS/100)
    task2_end = time.time()
    saveFreqClosed(items, path[-6], minS, len(items))
    
    Task1_time = task1_end - task1_start
    Task2_time = task2_end - task2_start
    print("Execute time - Task 1: \033[31m{:.5f}\033[0m".format(Task1_time))
    print("Execute time - Task 2: \033[31m{:.5f}\033[0m".format(Task2_time))
    print("Ratio of computation time (Task 2 / Task 1 * 100%): \033[31m{:.5f} %\033[0m".format(Task2_time/Task1_time*100))
    

def saveFreq(items, filename, minS):
    sort_itemset = sorted(items, key=lambda item: item[1], reverse=True)
    with open(f'./output/step2_task1_dataset{filename}_{minS}_result1.txt', 'w') as f:
        for freq in sort_itemset:
            info = str(round(freq[1]*100, 1)) + '\t{' + ",".join(freq[0]) + '}\n'
            f.write(info)

def saveIterInfo(info, filename, minS, total):
    with open(f'./output/step2_task1_dataset{filename}_{minS}_result2.txt', 'w') as f:
        f.write(str(total) + '\n')
        f.write(info)

def saveFreqClosed(dict, filename, minS, total):
    sort_itemset = sorted(dict.items(), key=lambda item: item[1], reverse=True)
    with open(f'./output/step2_task2_dataset{filename}_{minS}_result1.txt', 'w') as f:
        f.write(str(total) + '\n')
        for freq in sort_itemset:
            info = str(round(freq[1]*100, 1)) + '\t{' + ",".join(freq[0]) + '}\n'
            f.write(info)


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option(
        "-f",  "--inputFile",
        dest="input",
        help="filename containing csv",
        default=['A.data', 'B.data', 'C.data']
    )
    optparser.add_option(
        "-s", "--minSupport",
        dest="minS",
        help="minimum support value",
        default=[[1.0, 0.5, 0.2], [0.5, 0.2, 0.15], [3.0, 2.0, 1.0]],
        type=float
    )
    
    (options, args) = optparser.parse_args()
    input_path = './data/'


    inFile = None
    if type(options.input) is list:
        print(f"\033[36mRunning for mining\033[0m \033[31m{options.input}\033[0m")
        
        for idx, file in enumerate(options.input):
            path = input_path + file
            
            if type(options.minS) is list:
                for minS in options.minS[idx]:
                    runTask(file, minS, path)
            else:
                minS = options.minS
                runTask(file, minS, path)

        
    elif type(options.input) is str:
        file = options.input
        path = input_path + file
        print(f"\033[36mRunning for mining\033[0m \033[31m'{file}'\033[0m")
        
        if type(options.minS) is list:
            for minS in options.minS[0]:
                runTask(file, minS, path)
        else:
            minS = options.minS
            runTask(file, minS, path)
 
    elif options.input is None:
        inFile = sys.stdin
    else:
        print("No dataset filename specified, system with exit\n")
        sys.exit("System will exit")