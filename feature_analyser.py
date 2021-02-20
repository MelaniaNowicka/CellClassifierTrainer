import seaborn
import pandas
from matplotlib import pyplot


def rank_features_by_frequency(solutions, path, file_name):

    """

    Ranks the features in classifiers by frequency.

    Parameters
    ----------
    solutions : list
        list of solutions
    path : str
        path for output files
    file_name : str
        input file name

    """

    frequency_general = {}  # count occurrences in total
    frequency_pos = {}  # count occurrences as positive inputs
    frequency_neg = {}  # count occurrences as negative inputs

    features_total = 0
    for solution in solutions:  # for all solutions
        for gate in solution.solutions_by_gate:  # for all gates
            for inp in gate:  # for each input in gate
                if inp[1] == "positive":  # count positive inputs
                    if inp[0] not in frequency_pos.keys():  # check whether the input key is already in the dict
                        frequency_pos[inp[0]] = 1  # add key
                        frequency_general[inp[0]] = 1
                    else:
                        frequency_pos[inp[0]] += 1  # add occurrence
                        frequency_general[inp[0]] += 1
                elif inp[1] == "negative":  # count negative inputs
                    if inp[0] not in frequency_neg.keys():
                        frequency_neg[inp[0]] = 1
                        frequency_general[inp[0]] = 1
                    else:
                        frequency_neg[inp[0]] += 1
                        frequency_general[inp[0]] += 1

                features_total += 1

    header = {'feature': [], 'level': [], 'relative_frequency': []}
    frequency_data = pandas.DataFrame(data=header)

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
        row = [feature, "high", frequency_pos[feature] / features_total]
        frequency_data.loc[len(frequency_data)] = row
    print("NEGATIVE FEATURES: ")
    for feature in sorted(frequency_neg, key=frequency_neg.get, reverse=True):
        print(feature, ": ", frequency_neg[feature]/features_total)
        row = [feature, "low", frequency_neg[feature]/features_total]
        frequency_data.loc[len(frequency_data)] = row

    # plot relative frequencies
    colors = ["#14645aff", "#bfcd53ff"]
    seaborn.set_palette(seaborn.color_palette(colors))
    seaborn.color_palette("pastel")
    ax = seaborn.barplot(x=frequency_data.index, y="relative_frequency", hue="level", data=frequency_data, dodge=False)
    ax.set_xticklabels(frequency_data["feature"])
    pyplot.xticks(rotation=90)
    pyplot.tight_layout()
    pyplot.xlabel("")
    pyplot.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    pyplot.savefig("/".join([path, "_".join([file_name.replace(".csv", ""), "frequency_plot.png"])]),
                   bbox_inches="tight")
