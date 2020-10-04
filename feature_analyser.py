def rank_features_by_frequency(solutions):

    frequency_general = {}  # count occurences in total
    frequency_pos = {}  # count occurences as positive inputs
    frequency_neg = {}  # count occurences as negative inputs

    features_total = 0
    for solution in solutions:  # for all solutions
        for gate in solution.solutions_by_gate:
            for input in gate:
                if input[1] == "positive":
                    if input[0] not in frequency_pos.keys():
                        frequency_pos[input[0]] = 1
                        frequency_general[input[0]] = 1
                    else:
                        frequency_pos[input[0]] = frequency_pos[input[0]] + 1
                        frequency_general[input[0]] = frequency_general[input[0]] + 1
                elif input[1] == "negative":
                    if input[0] not in frequency_neg.keys():
                        frequency_neg[input[0]] = 1
                        frequency_general[input[0]] = 1
                    else:
                        frequency_neg[input[0]] = frequency_neg[input[0]] + 1
                        frequency_general[input[0]] = frequency_general[input[0]] + 1

                features_total += 1

    print("\n###FEATURE FREQUENCY ANALYSIS###")
    print("TOTAL VALUES")
    print("NUMBER OF FEATURES IN ALL SOLUTIONS IN TOTAL: ", features_total)
    print("POSITIVE FEATURES: ")
    for feature in sorted(frequency_pos, key=frequency_pos.get, reverse=True):
        print(feature, ": ", frequency_pos[feature])
    print("NEGATIVE FEATURES: ")
    for feature in sorted(frequency_neg, key=frequency_neg.get, reverse=True):
        print(feature, ": ", frequency_neg[feature])

    print("\nRELATIVE FREQUENCY")
    for feature in sorted(frequency_general, key=frequency_general.get, reverse=True):
        print(feature, ": ", frequency_general[feature]/features_total)
    print("POSITIVE FEATURES: ")
    for feature in sorted(frequency_pos, key=frequency_pos.get, reverse=True):
        print(feature, ": ", frequency_pos[feature]/features_total)
    print("NEGATIVE FEATURES: ")
    for feature in sorted(frequency_neg, key=frequency_neg.get, reverse=True):
        print(feature, ": ", frequency_neg[feature]/features_total)