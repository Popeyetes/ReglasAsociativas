from itertools import combinations

def apriori(transactions, min_support, min_confidence):
    items = set(item for t in transactions for item in t)
    n = len(transactions)
    logs = []

    def support_count(itemset):
        return sum(1 for t in transactions if set(itemset).issubset(set(t)))

    min_count_required = min_support * n

    freq = {}
    k1 = {frozenset([i]): support_count([i]) for i in items}
    k1_filtered = {k: v for k, v in k1.items() if v >= min_count_required}
    freq.update(k1_filtered)
    
    logs.append({
        "action": "K=1",
        "candidates": [{"itemset": sorted(list(k)), "count": v, "passed": v >= min_count_required} for k, v in k1.items()],
        "min_required": min_count_required
    })

    current = list(k1_filtered.keys())
    k = 2
    while current:
        candidates = set()
        for a, b in combinations(current, 2):
            union = a | b
            if len(union) == k:
                candidates.add(union)
        candidates_counts = {}
        for c in candidates:
            candidates_counts[c] = support_count(list(c))
            
        new = {c: v for c, v in candidates_counts.items() if v >= min_count_required}
        freq.update(new)
        
        if candidates_counts:
            logs.append({
                "action": f"K={k}",
                "candidates": [{"itemset": sorted(list(c)), "count": v, "passed": v >= min_count_required} for c, v in candidates_counts.items()],
                "min_required": min_count_required
            })
            
        current = list(new.keys())
        k += 1

    rules = []
    for itemset in freq:
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for ant in combinations(itemset, size):
                ant = frozenset(ant)
                cons = itemset - ant
                sup = freq[itemset] / n
                conf = freq[itemset] / freq[ant]
                sup_cons = freq[cons] / n if cons in freq else support_count(list(cons)) / n
                lift = conf / sup_cons if sup_cons > 0 else 0
                if conf >= min_confidence:
                    rules.append({
                        "antecedent": sorted(ant),
                        "consequent": sorted(cons),
                        "support": round(sup, 4),
                        "confidence": round(conf, 4),
                        "lift": round(lift, 4),
                        "count": freq[itemset],
                        "ant_count": freq[ant],
                        "cons_count": freq[cons] if cons in freq else support_count(list(cons)),
                        "total_transactions": n
                    })
    return sorted(rules, key=lambda x: -x["confidence"]), logs
