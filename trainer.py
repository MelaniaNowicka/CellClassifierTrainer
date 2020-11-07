import classifier
import feature_analyser
import converter
from clyngor import solve
import numpy
import sys


# class for result of ASP computation
class Result:

    """

    Class representing an ASP Result.

    Parameters
    ----------
    solutions_str : list
        the list of all solutions belonging to the Result formatted as strings
    solutions_by_gate : list
        the list of all solutions belonging to the Result formatted as lists
    errors : int
        the list of total errors received for the Result
    fp : int
        the number of false positives received for the Result
    fn : int
        the number of false negatives received for the Result
    size : int
        the size of solutions in the Result

    Methods
    -------
    """

    def __init__(self, solutions_str, solutions_by_gate, errors, fp, fn, size):
        self.solutions_str = solutions_str  # solutions as str
        self.solutions_by_gate = solutions_by_gate  # solutions as lists
        self.errors = errors  # number of errors in total
        self.fp = fp  # number of FPs
        self.fn = fn  # number of FNs
        self.size = size  # size of classifier (in inputs)


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


# training classifiers according to asp_program and max values of false positives and false negatives
def train_classifiers(instance, program, fp_max, fn_max):

    """
    Trains classifiers according to constraints relaxation described in Becker et al. [1]_
    using RnaCancerClassifier [2]_ and Clyngor [3]_.

    Parameters
    ----------
    instance : str
        instance
    program : str
        ASP program
    fp_max : int
        number of max allowed false positive errors
    fn_max : int
        number of max allowed false negative errors

    Returns
    -------
    float
        balanced accuracy

    References
    ----------
    .. [1] `Becker K, Klarner H, Nowicka M and Siebert H (2018) Designing miRNA-Based Synthetic Cell Classifier \
    Circuits Using Answer Set Programming. Front. Bioeng. Biotechnol. 6:70. <10.3389/fbioe.2018.00070>`_
    .. [2] `RnaCancerClassifier <https://github.com/MelaniaNowicka/RnaCancerClassifier>`_, RnaCancerClassifier \
    source code.
    .. [3] `Clyngor <https://github.com/Aluriak/clyngor>`_, Clyngor source code.

    """

    print("\n############TRAINING CLASSIFIERS############")

    returned_results = []
    errors = []

    print("\nProgress...")
    # relax constraints (number of max allowed number of false positives and false negatives)
    for i in range(0, fp_max+1):  # relax number of false positives
        for j in range(0, fn_max+1):  # relax number of false negatives

            print("Trying: FP: ", i, " FN: ", j, " SUM:", i + j)
            # create new constraints
            constraints = "\n".join(["upper_bound_falsepos(" + str(i) + ").", "upper_bound_falseneg(" + str(j) + ")."])
            asp_program = instance+constraints+program  # add constraints to the instance and the program
            opt = '--opt-mode=optN'  # add clasp option - return all optimal models
            answers = solve(inline=asp_program, options=opt)  # solve program

            #  '--quiet=1' option does not work with clyngor
            #  answers.with_optimality returns information about optimality of answers
            solutions = []
            for answer in answers.with_optimality:
                if answer[2] is True:  # if solution is optimal
                    solutions.append(list(answer)[0])  # ad solutions to solution list

            if len(solutions) != 0:  # if solutions were found
                new_result = Result(solutions, [], i+j, i, j, 0)  # create new result
                errors.append(i+j)  # add total number of errors to list of errors
                returned_results.append(new_result)  # note, one result may contain several solutions!
                print("Solutions found for: FP: ", i, " FN: ", j, " SUM:", i + j)



    print("\nCollecting answers finished.")

    # if no solutions were found
    if len(returned_results) == 0:
        print("NO SOLUTIONS FOUND")

    # convert asp results to string and lists
    returned_results = converter.convert_asp_results(returned_results)

    return errors, returned_results


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

    bacc_train_list = []
    bacc_test_list = []
    tpr_test_list = []
    tnr_test_list = []
    size_list = []

    solution_id = 1
    for solution in solutions:  # iterate over solutions

        # train data scores
        print("\nSOLUTION ", solution_id)
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

    feature_analyser.rank_features_by_frequency(solutions)  # analyse features

    # average results for all solutions
    print("\n\n###################################")
    print("############AVG RESULTS############\n")
    print("AVG TRAIN BACC: ", numpy.average(bacc_train_list))  # calculate average train bacc
    if len(bacc_test_list) > 1:  # if more than one solution was found
        train_std = numpy.std(bacc_train_list, ddof=1)
        print("STD TRAIN BACC: ", train_std)
    else:
        train_std = 0.0
        print("STD TRAIN BACC: ", 0.0)
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
    print("CSV", ";", numpy.average(bacc_train_list), ";", train_std, ";",
          numpy.average(bacc_test_list), ";", test_std, ";",
          numpy.average(tpr_test_list), ";", numpy.average(tnr_test_list), ";",
          numpy.average(size_list))




