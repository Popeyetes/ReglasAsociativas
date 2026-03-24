from collections import defaultdict
from itertools import combinations

def eclat(transactions, min_support, min_confidence):
    n = len(transactions)
    min_count = max(1, int(min_support * n))
    logs = []

    tid_sets = defaultdict(set)
    for tid, t in enumerate(transactions):
        for item in t:
            tid_sets[frozenset([item])].add(tid)

    freq_itemsets = {k: v for k, v in tid_sets.items() if len(v) >= min_count}
    logs.append({"action": "K=1", "frequent": len(freq_itemsets)})

    def eclat_recurse(prefix_items, level=2):
        items = list(prefix_items.keys())
        for i in range(len(items)):
            new_prefix = {}
            for j in range(i + 1, len(items)):
                inter = prefix_items[items[i]] & prefix_items[items[j]]
                if len(inter) >= min_count:
                    new_key = items[i] | items[j]
                    new_prefix[new_key] = inter
                    freq_itemsets[new_key] = inter
            if new_prefix:
                logs.append({"action": f"Intersect K={level}", "frequent_found": len(new_prefix)})
                eclat_recurse(new_prefix, level + 1)

    eclat_recurse({k: v for k, v in freq_itemsets.items()})

    rules = []
    for itemset, tids in freq_itemsets.items():
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for ant in combinations(itemset, size):
                ant = frozenset(ant)
                cons = itemset - ant
                sup = len(tids) / n
                ant_tids = freq_itemsets.get(ant)
                if ant_tids is None:
                    ant_tids = {tid for tid, t in enumerate(transactions) if ant.issubset(set(t))}
                ant_cnt = len(ant_tids) if ant_tids else 0
                
                cons_tids = freq_itemsets.get(cons)
                if cons_tids is None:
                    cons_tids = {tid for tid, t in enumerate(transactions) if cons.issubset(set(t))}
                cons_cnt = len(cons_tids) if cons_tids else 0
                
                conf = len(tids) / ant_cnt if ant_cnt else 0
                sup_cons = cons_cnt / n
                lift = conf / sup_cons if sup_cons > 0 else 0
                
                if conf >= min_confidence:
                    rules.append({
                        "antecedent": sorted(ant),
                        "consequent": sorted(cons),
                        "support": round(sup, 4),
                        "confidence": round(conf, 4),
                        "lift": round(lift, 4),
                        "count": len(tids),
                        "ant_count": ant_cnt,
                        "cons_count": cons_cnt,
                        "total_transactions": n
                    })
    return sorted(rules, key=lambda x: -x["confidence"]), logs
