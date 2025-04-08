import pandas as pd
from collections import defaultdict
from itertools import combinations


class TreeNode:
    def __init__(self, item, count=1):
        self.item = item
        self.count = count
        self.children = {}
        self.parent = None

    def increase_count(self, count):
        self.count += count


def build_fp_tree(transactions, min_support):
    root = TreeNode('Root')  
    header_table = defaultdict(int)  

    for transaction in transactions:
        unique_transaction = set(transaction)
        for item in unique_transaction:
            header_table[item] += 1

    header_table = {item: count for item, count in header_table.items() if count >= min_support}

    sorted_items = sorted(header_table.items(), key=lambda x: x[1], reverse=True)
    sorted_items = [item[0] for item in sorted_items] 

    for transaction in transactions:
        unique_transaction = set(transaction)
        filtered_transaction = [item for item in sorted_items if item in unique_transaction]
        if filtered_transaction:
            insert_tree(filtered_transaction, root)

    return root, header_table  
def insert_tree(items, node):
    if items:
        first_item = items[0]
        if first_item in node.children:
            node.children[first_item].increase_count(1)
        else:
            new_node = TreeNode(first_item)
            new_node.parent = node
            node.children[first_item] = new_node

        insert_tree(items[1:], node.children[first_item])


def print_fp_tree(node, level=0):
    if node:
        print(' ' * (level * 4) + f'{node.item}: {node.count}')
        for child in node.children.values():
            print_fp_tree(child, level + 1)


Horizontal_data = pd.read_excel("C:/Users/yahya/Downloads/Horizontal_Format.xlsx")



transactions = Horizontal_data['items'].apply(lambda x: x.split(',')).tolist()

frequency_of_transactions = defaultdict(int)
for transaction in transactions:
    unique_items = set([item.strip() for item in transaction]) 
    for item in unique_items:
        frequency_of_transactions[item] += 1 

min_support = 3
min_confidence = 0.7
frequency_of_transactions = {item: count for item, count in frequency_of_transactions.items() if count >= min_support}
elements = [item for item, count in frequency_of_transactions.items()]

print(elements)
print("\n\n")
print("Frequent set L1 :\n")

print(frequency_of_transactions)

print("\n\n")

fp_tree, header_table = build_fp_tree(transactions, min_support)

print("FP-growth Tree:")
print_fp_tree(fp_tree)
print("\n\n")
# ---------------------------------------------------------------------------------------------------------------------------
rows = []
sorted_items = [item for item, _ in sorted(header_table.items(), key=lambda x: x[1], reverse=True)]
for TiD, items in zip(Horizontal_data['TiD'], Horizontal_data['items']):
    transaction_items = items.split(',')
    transaction_items = [item.strip() for item in transaction_items]
    sorted_transaction = [item for item in sorted_items if item in transaction_items]
    rows.append({'TiD': TiD, 'items': sorted_transaction})

df2 = pd.DataFrame(rows)
df2 = df2.set_index('TiD')

print("\nSorted Transactions DataFrame:")
print(df2)
print("\n\n")
list_of_2 = []
counts_of_2 = defaultdict(int) 

for index, row in df2.iterrows():
    transaction = row['items']
    for ind in elements:
        if ind in transaction:
            unique_pairs = set(tuple(sorted((ind, item))) for item in transaction if item != ind)
            for pair in unique_pairs:
                counts_of_2[pair] += 1 

for pair in counts_of_2:
    counts_of_2[pair] //= 2

frequent_item_set = {pair: count for pair, count in counts_of_2.items() if count >= min_support}
list_of_2 = [(pair, count) for pair, count in frequent_item_set.items()]
      
counts_of_3 = defaultdict(int) 
for index, row in df2.iterrows():
    transaction = row['items'] 
    for triplet in combinations(transaction, 3): 
        sorted_triplet = tuple(sorted(triplet)) 
        counts_of_3[sorted_triplet] += 1  

filtered_triplets = {triplet: count for triplet, count in counts_of_3.items() if count >= min_support}
list_of_3 = [(triplet, count) for triplet, count in filtered_triplets.items()]

list_of_2 = [ (pair, count) for pair, count in frequent_item_set.items()]

counts_of_4 = defaultdict(int) 
for index, row in df2.iterrows():
    transaction = row['items'] 
    for quadruplet in combinations(transaction, 4): 
        sorted_quadruplet = tuple(sorted(quadruplet)) 
        counts_of_4[sorted_quadruplet] += 1  

filtered_quadruplets = {quadruplet: count for quadruplet, count in counts_of_4.items() if count >= min_support}
list_of_4 = [(quadruplet, count) for quadruplet, count in filtered_quadruplets.items()]

counts_of_5 = defaultdict(int)  
for index, row in df2.iterrows():
    transaction = row['items']
    for p5 in combinations(transaction, 5): 
        sorted_pentaplet = tuple(sorted(p5))
        counts_of_5[sorted_pentaplet] += 1

filtered_pentaplets = {pentaplet: count for pentaplet, count in counts_of_5.items() if count >= min_support}
list_of_5 = [(pentaplet, count) for pentaplet, count in filtered_pentaplets.items()]

frequent_item_set_2 = list_of_2 + list_of_3 + list_of_4 + list_of_5
print("Frequent itemset: \n")

print(frequent_item_set_2)

print("\n\n")

strong_list_of_2 = []
for (i1,i2),k in list_of_2:
    for j in range(2):
        if j==0:
            conf=k/frequency_of_transactions[i1]
            if conf>=min_confidence:
                strong_list_of_2.append(([i1,i2],k,conf) )
        else:
            conf=k/frequency_of_transactions[i2]
            if conf>=min_confidence:
                strong_list_of_2.append(([i2,i1],k,conf) )


pair_dict = {tuple(sorted(pair)): count for pair, count in list_of_2}
triplet_dict = {tuple(sorted(triplet)): count for triplet, count in list_of_3} 
strong_list_of_3 = []

for (i1, i2, i3), k in list_of_3:
    for j in range(6):
        if j == 0:
            conf = k / pair_dict.get((i1, i2), 1)  
            if conf >= min_confidence:
                strong_list_of_3.append(([[i1, i2], i3], k, conf))
        elif j == 1:
            conf = k / pair_dict.get((i2, i3), 1)
            if conf >= min_confidence:
                strong_list_of_3.append(([[i2, i3], i1], k, conf))
        elif j == 2:
            conf = k / pair_dict.get((i1, i3), 1)
            if conf >= min_confidence:
                strong_list_of_3.append(([[i1, i3], i2], k, conf))
        elif j == 3:
            conf = k / frequency_of_transactions[i1]
            if conf >= min_confidence:
                strong_list_of_3.append(([i1, [i3, i2]], k, conf))
        elif j == 4:
            conf = k / frequency_of_transactions[i2]
            if conf >= min_confidence:
                strong_list_of_3.append(([i2, [i3, i1]], k, conf))
        elif j == 5:
            conf = k / frequency_of_transactions[i3]
            if conf >= min_confidence:
                strong_list_of_3.append(([i3, [i2, i1]], k, conf))

strong_list_of_4 = []

for (i1, i2, i3, i4), k in list_of_4:
    for j in range(14):
        if j == 0:
            conf = k / pair_dict.get((i1, i2), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i1, i2], i3, i4], k, conf))
        elif j == 1:
            conf = k / pair_dict.get((i1, i3), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i1, i3], i2, i4], k, conf))
        elif j == 2:
            conf = k / pair_dict.get((i1, i4), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i1, i4], i2, i3], k, conf))
        elif j == 3:
            conf = k / pair_dict.get((i2, i3), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i2, i3], i1, i4], k, conf))
        elif j == 4:
            conf = k / pair_dict.get((i2, i4), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i2, i4], i1, i3], k, conf))
        elif j == 5:
            conf = k / pair_dict.get((i3, i4), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i3, i4], i1, i2], k, conf))

        elif j == 6:
            conf = k / triplet_dict.get((i1, i2, i3), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i1, i2, i3], i4], k, conf))
        elif j == 7:
            conf = k / triplet_dict.get((i1, i2, i4), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i1, i2, i4], i3], k, conf))
        elif j == 8:
            conf = k / triplet_dict.get((i1, i3, i4), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i1, i3, i4], i2], k, conf))
        elif j == 9:
            conf = k / triplet_dict.get((i2, i3, i4), 1)
            if conf >= min_confidence:
                strong_list_of_4.append(([[i2, i3, i4], i1], k, conf))

        elif j == 10:
            conf = k / frequency_of_transactions[i1]
            if conf >= min_confidence:
                strong_list_of_4.append(([i1, [i2, i3, i4]], k, conf))
        elif j == 11:
            conf = k / frequency_of_transactions[i2]
            if conf >= min_confidence:
                strong_list_of_4.append(([i2, [i1, i3, i4]], k, conf))
        elif j == 12:
            conf = k / frequency_of_transactions[i3]
            if conf >= min_confidence:
                strong_list_of_4.append(([i3, [i1, i2, i4]], k, conf))
        elif j == 13:
            conf = k / frequency_of_transactions[i4]
            if conf >= min_confidence:
                strong_list_of_4.append(([i4, [i1, i2, i3]], k, conf))
                
                
strong_list = strong_list_of_2 + strong_list_of_3
print("Strong Rules :\n")
print(strong_list)
print("\n\n")

lift_list_of_2=[]
for (i1,i2),k in list_of_2:
   lift=(k/5)/((frequency_of_transactions[i1]/5)* (frequency_of_transactions[i2]/5))
   lift_list_of_2.append([[i1,i2],k,lift])
   
lift_list_of_3=[]
for (i1,i2,i3),k in list_of_3:
   lift=(k/5)/((frequency_of_transactions[i1]/5)* (frequency_of_transactions[i2]/5)*(frequency_of_transactions[i3]/5))
   lift_list_of_3.append([[i1,i2,i3],k,lift])

lift_list_of_4 = []
for (i1, i2, i3, i4), k in list_of_4:
    lift = (k / 5) / ((frequency_of_transactions[i1] / 5) * (frequency_of_transactions[i2] / 5) * (frequency_of_transactions[i3] / 5) * (frequency_of_transactions[i4] / 5))
    lift_list_of_4.append([[i1, i2, i3, i4], k, lift])
    
lift_list_of_5 = []
for (i1, i2, i3, i4, i5), k in list_of_5:
    lift = (k / 5) / ((frequency_of_transactions[i1] / 5) * (frequency_of_transactions[i2] / 5) * (frequency_of_transactions[i3] / 5) * (frequency_of_transactions[i4] / 5) * (frequency_of_transactions[i5] / 5))
    lift_list_of_5.append([[i1, i2, i3, i4, i5], k, lift])

lift_list = lift_list_of_2 + lift_list_of_3 + lift_list_of_4 + lift_list_of_5
print("Lift List :\n")
print(lift_list)
