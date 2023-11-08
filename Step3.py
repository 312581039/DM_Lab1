# ECLAT

import time

def Vertical_data(x):
    Vertical_dict = {}
    for index, items in enumerate(x):
        for item in items:
            Vertical_dict[item] = Vertical_dict.get(item, []) + [index]
    return Vertical_dict

def main(data, support_per):
    Vertical_dict = Vertical_data(data)
    Vertical_dict = {k:v for k,v in Vertical_dict.items() if len(v)>support_per}
    a = Vertical_dict
    while True:
        a_len = len(a)
        a_list = list(a)
        a = {}
        for i in range(a_len-1):
            for j in range(i+1, a_len):
                key_i = a_list[i]
                key_j = a_list[j]
                inter = sorted(set(Vertical_dict[key_i]) & set(Vertical_dict[key_j]))
                if len(inter) > support_per:
                    key_list = sorted(set(key_i.split() + key_j.split()))
                    key_str = " ".join(key_list)
                    a[key_str] = inter
        Vertical_dict = {**Vertical_dict, **a}
        if len(a) <= 1:
            FreqSet = {}
            for itemset, index in Vertical_dict.items():
                support = float(len(index)) / len(data)
                itemset = '{' + ",".join(itemset.split(" ")) + '}'
                FreqSet[itemset] = support*100 
            break
    return FreqSet

if __name__ == '__main__':

    root = './data/'
    files = ['A.data', 'B.data', 'C.data']
    minSupport = [[1.0, 0.5, 0.2], [0.5, 0.2, 0.15], [3.0, 2.0, 1.0]]
    print(f"\033[36mRunning for mining\033[0m \033[31m{files}\033[0m")
    for idx, file in enumerate(files):
        data = []
        path = root + file
        with open(path, 'r') as f:
            for line in f:
                data.append(line.strip().split(" ")[3:])
        for minS in minSupport[idx]:      
            support = len(data) * (minS/100)
            print(f"-> Mining \033[31m{file}\033[0m with minS \033[32m{minS} ({minS/100}%)\033[0m")
            print("-> Start mining Frequent Itemset (Task 1)...")
            start = time.time()
            FreqSet = main(data, support_per=support)
            end = time.time()
            print("Execute time - Task 1: \033[31m{:.5f}\033[0m".format(end - start))
            sort_itemset = sorted(FreqSet.items(), key=lambda item: item[1], reverse=True)
            with open(f'./output/step3_task1_dataset{file[-6]}_{minS}_result1.txt', 'w') as f:
                for freq in sort_itemset:
                    info = str(round(freq[1], 1)) + '\t' + freq[0] + '\n'
                    f.write(info) 
    