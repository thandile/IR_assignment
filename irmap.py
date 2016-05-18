def irmap(query_id, relevant_doc_ids, query_file):
    path = query_file[0:query_file.rfind('\\')]
    relevant_doc_ids = [int(i) for i in relevant_doc_ids]
    relevance_file = path+"\\relevance."+query_id #to fetch relevance values from relavance file4
    relevance = []
    f =  open(relevance_file, "r")
    content = f.read()
    split_content = content.splitlines()
    for i in range(len(split_content)): #searching in relevance file for the relevance of each document
        if i in relevant_doc_ids:
            relevance.append(int(split_content[i]))
   # relevance = [1,0, 2]
    precision = []

    relCount = 0
    precisionValue = 0
    for i in range(len(relevance)):
        relCount = relCount + relevance[i]
        print("Total relevance at " + str(i+1) + ": " + str(relCount))
        precisionValue = relCount/(i+1)
        print("Total precision at " + str(i+1) + ": " + str(precisionValue))
        precision.append(precisionValue)
    sum = 0
    for i in precision:
        sum = sum + i

    try:
        map = sum/(len(precision))
    except:
        print("*** Relevance files empty ***")
        map = 0


    print("The MAP value is: " + str(map))

    return map
