"""
Description     : Simple Python implementation of the Apriori Algorithm
Modified from:  https://github.com/asaini/Apriori
Usage:
    $python apriori_freq.py -f DATASET.csv -s minSupport

    $python apriori_freq.py -f DATASET.csv -s 0.15
"""

import time
from collections import defaultdict
from optparse import OptionParser


class Association_rule:
    def __init__(self, path, minSupport, filename) -> None:
        self.path = path
        self.filename = filename
        self.minSupport = minSupport
    
    def apriori(self):
        itemSet, transactionList = self.get_dataset(self.file_to_dataset())   
        # Global dictionary which stores (key=n-itemSets,value=support)
        # which satisfy minSupport
        freqSet = defaultdict(int)
        largeSet = dict()
        
        # init
        oneCSet= self.pruning(itemSet, transactionList, freqSet)
        F = oneCSet
        k = 2
        
        info = ''
        while F != set([]):
            largeSet[k-1] = F
            L = self.joinSet(F, k)
            F = self.pruning(L, transactionList, freqSet)
            info += f'{k-1}\t{len(L)}\t{len(F)}\n'
            k += 1
            
        def getSupport(itemset):
            return float(freqSet[itemset]) / len(transactionList)
        
        results = []
        for k, F in largeSet.items():
            results.extend([(tuple(itemset), getSupport(itemset)) for itemset in F])

        return results, info
        
    def pruning(self, L, transactionList, freqSet):
        F = set()
        localSet = defaultdict(int)
    
        # support count
        for item in L:
            for transaction in transactionList:
                if item.issubset(transaction):
                    freqSet[item] += 1
                    localSet[item] += 1   
        # support
        for item, count in localSet.items():
            support = float(count) / len(transactionList)
            if support >= self.minSupport:
                F.add(item)
                
        return F
    
    def joinSet(self, itemSet, length):
         return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])
    
    def file_to_dataset(self):
        with open(self.path, 'r') as f:
            for line in f:
                record = frozenset(line.strip().split(" ")[3:])
                yield record
                
    def get_dataset(self, data_iterator):
        transactionList = list()
        itemSet = set()
        for record in data_iterator:
            transaction = frozenset(record)
            transactionList.append(transaction)
            for item in transaction:
                itemSet.add(frozenset([item]))
        return itemSet, transactionList        
    
    def saveFreq(self, items):
        sort_itemset = sorted(items, key=lambda item: item[1], reverse=True)
        with open(f'./output/step2_task1_dataset{self.filename}_{self.minSupport*100}_result1.txt', 'w') as f:
            for freq in sort_itemset:
                info = str(round(freq[1]*100, 1)) + '\t{' + ",".join(freq[0]) + '}\n'
                f.write(info)
    
    def saveIterInfo(self, info):
        with open(f'./output/step2_task1_dataset{self.filename}_{self.minSupport*100}_result2.txt', 'w') as f:
            f.write(info)


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
    model = Association_rule(options.input, options.minS/100, options.input[-5])

    start_time = time.time()
    freq_itemsets, info = model.apriori()
    end_time = time.time()
    
    model.saveFreq(freq_itemsets)
    model.saveIterInfo(info)
    print("Execute time: {:.5f}".format(end_time - start_time))