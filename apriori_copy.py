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

# 得到itemset的組合
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


def runApriori(data_iter, minSupport):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)
    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport
    oneCSet= returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
    currentLSet = oneCSet
    k = 2
    info = ''
    while currentLSet != set([]):    
        print(k)
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet= returnItemsWithMinSupport(
            currentLSet, transactionList, minSupport, freqSet
        )
        info += f'{k-1}\t{len(currentLSet)}\t{len(currentCSet)}\n'
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    return toRetItems, info


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


def saveFreq(items, filename, minSupport):
    sort_itemset = sorted(items, key=lambda item: item[1], reverse=True)
    with open(f'./output/step2_task1_dataset{filename}_{minSupport}_result1.txt', 'w') as f:
        for freq in sort_itemset:
            info = str(round(freq[1]*100, 1)) + '\t{' + ",".join(freq[0]) + '}\n'
            f.write(info)

def saveIterInfo(info, filename, minSupport):
    with open(f'./output/step2_task1_dataset{filename}_{minSupport}_result2.txt', 'w') as f:
        f.write(info)


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing csv", default='A.csv'
    )
    optparser.add_option(
        "-s",
        "--minSupport",
        dest="minS",
        help="minimum support value",
        default=0.1,
        type="float",
    )
    
    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print("No dataset filename specified, system with exit\n")
        sys.exit("System will exit")

    minSupport = options.minS / 100
    filename = options.input[-6]

    start_time = time.time()
    items, info = runApriori(inFile, minSupport)
    end_time = time.time()
    
    print("Execute time: {:.5f}".format(end_time - start_time))
    saveFreq(items, filename, options.minS)
    saveIterInfo(info, filename, options.minS)