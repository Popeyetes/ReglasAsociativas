from collections import defaultdict
from itertools import combinations

class FPNode:
    def __init__(self, item, count=0, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None
        
    def to_dict(self):
        return {
            "name": str(self.item) if self.item is not None else "Root",
            "count": self.count,
            "children": [child.to_dict() for child in self.children.values()]
        }

class FPTree:
    def __init__(self, transactions, min_count):
        self.header = {}
        self.root = FPNode(None)
        freq = defaultdict(int)
        for t in transactions:
            for item in t:
                freq[item] += 1
        self.freq = {k: v for k, v in freq.items() if v >= min_count}
        for t in transactions:
            sorted_t = sorted([i for i in t if i in self.freq],
                               key=lambda x: -self.freq[x])
            if sorted_t:
                self._insert(sorted_t, self.root)

    def _insert(self, items, node):
        if not items:
            return
        item = items[0]
        if item in node.children:
            node.children[item].count += 1
        else:
            child = FPNode(item, 1, node)
            node.children[item] = child
            if item not in self.header:
                self.header[item] = child
            else:
                cur = self.header[item]
                while cur.link:
                    cur = cur.link
                cur.link = child
        self._insert(items[1:], node.children[item])

def fp_growth(transactions, min_support, min_confidence):
    n = len(transactions)
    min_count = max(1, int(min_support * n))
    logs = []

    def mine(tree, prefix, freq_itemsets):
        for item in tree.header:
            new_prefix = prefix | {item}
            support = tree.freq.get(item, 0)
            freq_itemsets[frozenset(new_prefix)] = support
            
            cond_patterns = []
            cpb_counts = defaultdict(int)
            candidate_items_counts = defaultdict(int)
            
            node = tree.header[item]
            while node:
                path = []
                parent = node.parent
                while parent and parent.item is not None:
                    path.append(parent.item)
                    parent = parent.parent
                if path:
                    path.reverse() # Root to leaf order
                    cpb_counts[tuple(path)] += node.count
                    cond_patterns.extend([path] * node.count)
                node = node.link
            
            cpb_formatted = [{"path": list(p), "count": c} for p, c in cpb_counts.items()]
            for p, c in cpb_counts.items():
                for p_item in p:
                    candidate_items_counts[p_item] += c
                    
            cond_tree_items = {}

            if cond_patterns:
                cond_tree = FPTree(cond_patterns, min_count)
                if cond_tree.header:
                    cond_tree_items = {k: v for k, v in cond_tree.freq.items()}
                    mine(cond_tree, new_prefix, freq_itemsets)
            
            if len(prefix) == 0:
                logs.append({
                    "action": "mine_table_row",
                    "item": item,
                    "prefix": list(prefix),
                    "cpb": cpb_formatted,
                    "candidates": dict(candidate_items_counts),
                    "frequent": cond_tree_items
                })

    tree = FPTree(transactions, min_count)
    freq_itemsets = {}
    
    sorted_freq = sorted(tree.freq.items(), key=lambda x: -x[1])
    logs.append({
        "action": "frequent_items_sorted",
        "items": sorted_freq
    })
    
    logs.append({
        "action": "initial_tree",
        "tree": tree.root.to_dict()
    })

    mine(tree, frozenset(), freq_itemsets)

    freq1 = defaultdict(int)
    for t in transactions:
        for item in t:
            freq1[frozenset([item])] += 1
    for k, v in freq1.items():
        if v >= min_count:
            freq_itemsets[k] = v

    rules = []
    for itemset, cnt in freq_itemsets.items():
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for ant in combinations(itemset, size):
                ant = frozenset(ant)
                cons = itemset - ant
                sup = cnt / n
                ant_cnt = freq_itemsets.get(ant, sum(1 for t in transactions if ant.issubset(set(t))))
                conf = cnt / ant_cnt if ant_cnt else 0
                cons_cnt = freq_itemsets.get(cons, sum(1 for t in transactions if cons.issubset(set(t))))
                sup_cons = cons_cnt / n
                lift = conf / sup_cons if sup_cons > 0 else 0
                if conf >= min_confidence and sup >= min_support:
                    rules.append({
                        "antecedent": sorted(ant),
                        "consequent": sorted(cons),
                        "support": round(sup, 4),
                        "confidence": round(conf, 4),
                        "lift": round(lift, 4),
                        "count": cnt,
                        "ant_count": ant_cnt,
                        "cons_count": cons_cnt,
                        "total_transactions": n
                    })
    return sorted(rules, key=lambda x: -x["confidence"]), logs
