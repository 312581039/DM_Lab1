Data format: [TID] [TID] [NITEMS] [ITEMSET]
ex. [1] [1] [4] [67 78 139 366]
- TID is a transaction identifier
- NITEMS is the number of items in that transaction
- ITEMSET is the set of items making up that transaction.
All ITEMSETS are sorted lexicographically. Note that TID is repeated for consistency with the sequence generator.

-
[fname].data -- the actual data file
[fname].conf -- configuration info
[fname].pat -- the embedded patterns