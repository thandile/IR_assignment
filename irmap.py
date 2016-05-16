def irmap():
    relevance = [1,0, 2]
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
    map = sum/(len(precision))
    print("The MAP value is: " + str(map))
irmap()