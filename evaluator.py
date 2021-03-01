import numpy
import os
import sys
import classifier
import feature_analyser


# calculate balanced accuracy score
def calculate_balanced_accuracy(tp, tn, p, n):

    """

    Calculates balanced accuracy (bacc = (tp/p + tn/n)/2).

    Parameters
    ----------
    tp : int
        number of true positives
    tn : int
        number of true negatives
    p : int
        number of positives
    n : int
        number of negatives

    Returns
    -------
    float
        balanced accuracy

    """

    try:
        balanced_accuracy = (tp/p + tn/n)/2
    except ZeroDivisionError:
        print("Error: balanced accuracy - division by zero! No negatives or positives in the dataset!")
        sys.exit(0)

    return balanced_accuracy


# test solutions on testing data
def test_classifiers(solutions, test_data, train_p, train_n, test_p, test_n):

    """

    Tests classifiers on test data set.

    Parameters
    ----------
    solutions : list
        list of found solutions
    test_data : str
        test data set
    train_p : int
        number of positives in train data
    train_n : int
        number of negatives in train data
    test_p : int
        number of positives in test data
    test_n : int
        number of negatives in test data

    """

    print("\n\n###########################################")
    print("############TESTING CLASSIFIERS############")
    print("###########################################\n")

    bacc_train_list = []
    bacc_test_list = []
    tpr_test_list = []
    tnr_test_list = []
    size_list = []

    solution_id = 1
    for solution in solutions:  # iterate over solutions

        # train data scores
        print("\nSOLUTION ", solution_id)  # show solution id
        solution_id += 1
        print("##SUM: ", solution.errors, "##")  # show number of errors
        print("FP: ", solution.fp, "FN: ", solution.fn)  # show number of false positives and negatives
        tp = train_p - solution.fn  # calculate number of true positives
        tn = train_n - solution.fp  # calculate number of true negatives
        train_bacc = calculate_balanced_accuracy(tp, tn, train_p, train_n)  # calculate train bacc
        print("TRAIN BACC: ", train_bacc)
        bacc_train_list.append(train_bacc)
        size_list.append(solution.size)  # size of classifier in number of inputs
        print(solution.solutions_str)  # show solution

        if test_data is not None:
            # test data scores
            # calculate false positives and negatives
            fn, fp = classifier.check_classifier(test_data, solution.solutions_str)
            print("FP: ", fp, " FN: ", fn)
            tp = test_p - fn  # calculate true positives
            tpr_test_list.append(tp/test_p)  # calculate true positive rate and add to list
            tn = test_n - fp  # calculate true negatives
            tnr_test_list.append(tn/test_n)  # calculate true negative rate and add to list
            bacc = calculate_balanced_accuracy(tp, tn, test_p, test_n)  # calculate bacc
            print("TEST BACC: ", bacc)
            bacc_test_list.append(bacc)

    path_train = test_data
    head_tail = os.path.split(path_train)
    path = head_tail[0]
    file_name = head_tail[1]

    # feature_analyser.rank_features_by_frequency(solutions, path, file_name)  # analyse features

    # average results for all solutions
    print("\n\n###################################")
    print("############AVERAGE RESULTS############")
    print("###################################\n")
    print("AVG TRAIN BACC: ", numpy.average(bacc_train_list))  # calculate average train bacc
    if len(bacc_train_list) > 1:  # if more than one solution was found
        train_std = numpy.std(bacc_train_list, ddof=1)
        print("STD TRAIN BACC: ", train_std)
    else:
        train_std = 0.0
        print("STD TRAIN BACC: ", 0.0)

    if test_data is not None:
        print("AVG TEST BACC: ", numpy.average(bacc_test_list))  # calculate average test bacc
        if len(bacc_test_list) > 1:  # if more than one solution was found
            test_std = numpy.std(bacc_test_list, ddof=1)
            print("STD TEST BACC: ", test_std)
        else:
            test_std = 0.0
            print("STD TEST BACC: ", test_std)
        print("TEST TPR: ", numpy.average(tpr_test_list))  # calculate average tpr
        print("TEST TNR: ", numpy.average(tnr_test_list))  # calculate average tnr
    print("AVG SIZE: ", numpy.average(size_list))  # calculate average size
    print("\n")

    if test_data is not None:
        print("CSV", ";", numpy.average(bacc_train_list), ";", train_std, ";",
              numpy.average(bacc_test_list), ";", test_std, ";",
              numpy.average(tpr_test_list), ";", numpy.average(tnr_test_list), ";",
              numpy.average(size_list))
    else:
        print("CSV", ";", numpy.average(bacc_train_list), ";", train_std, ";",
              numpy.average(bacc_test_list), ";", 0.0, ";",
              0.0, ";", 0.0, ";",
              numpy.average(size_list))
