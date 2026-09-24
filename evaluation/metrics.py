def precision_at_k(retrieved, relevant, k):
    return len(set(retrieved[:k]) & set(relevant)) / k if k else 0.0

def recall_at_k(retrieved, relevant, k):
    return len(set(retrieved[:k]) & set(relevant)) / len(set(relevant)) if relevant else 0.0

def hit_rate(retrieved, relevant, k):
    return 1.0 if set(retrieved[:k]) & set(relevant) else 0.0

def mrr(retrieved, relevant):
    relevant=set(relevant)
    for i,item in enumerate(retrieved,1):
        if item in relevant:return 1.0/i
    return 0.0
