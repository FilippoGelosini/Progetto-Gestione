import math

def calculate_dcg(scores):
    dcg = scores[0]
    for i in range(1, len(scores)):
        dcg += scores[i] / math.log2(i + 1)
    return dcg

def calculate_idcg(scores):
    scores_sorted = sorted(scores, reverse=True)
    return calculate_dcg(scores_sorted)

def calculate_ndcg(scores):
    dcg = calculate_dcg(scores)
    idcg = calculate_idcg(scores)
    if idcg == 0:
        return 0
    return dcg / idcg

scores = [3,3,1,0,3,3,3,0,3,2]

dcg_score = calculate_dcg(scores)
print("DCG Score:", dcg_score)

idcg_score = calculate_idcg(scores)
print("IDCG Score:", idcg_score)

ndcg_score = calculate_ndcg(scores)
print("nDCG Score:", ndcg_score)
