import math
def irndcg(query_id, relevant_doc_ids, query_file):
    path = query_file[0:query_file.rfind('\\')]
    relevant_doc_ids = [int(i) for i in relevant_doc_ids]
    relevance_file = path+"\\relevance."+query_id #to fetch relevance values from relavance file4
    relevance = []
    print("relpath:",relevance_file)
    f =  open(relevance_file, "r")
    content = f.read()
    split_content = content.splitlines()
    for i in range(len(split_content)): #searching in relevance file for the relevance of each document
        if i in relevant_doc_ids:
            relevance.append(int(split_content[i]))
            #print(i)
            #print(split_content[i])
    #print(relevance)

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
    try:
        ndcg = dcg/idcg
    except:
        ndcg = 0

    print("NDCG value: " + str(ndcg))

    return ndcg
