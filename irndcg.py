import sys
import math
def irndcg():
    relevance = [5, 2, 3, 0, 1]
    dcg = 0
    j = 1
    #dcg value
    for i in range(len(relevance)):
        dcg = dcg + (relevance[i]/(math.log(j+1)/math.log(2)))
        j = j + 1
    print("DCG value: " + str(dcg))
    #idcg value  .... sort to ideal order.
    relevance.sort()
    relevance.reverse()
    print("Idea; order" + str(relevance))

    idcg = 0
    k = 1
    for i in range(len(relevance)):
        idcg = idcg + (relevance[i]/(math.log(k+1)/math.log(2)))

        k = k +1
    print("IDCG value: "+ str(idcg))

    #NDCG value
    ndcg = dcg/idcg
    print("NDCG value: " + str(ndcg))
irndcg()