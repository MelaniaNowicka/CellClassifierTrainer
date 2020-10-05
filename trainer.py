import classifier
import feature_analyser
import converter
import pyasp
import numpy
import sys


# class for result of ASP computation
class Result:

    def __init__(self, solutions_str, solutions_by_gate, errors, fp, fn, size):
        self.solutions_str = solutions_str  # solutions
        self.solutions_by_gate = solutions_by_gate
        self.errors = errors  # number of errors in total
        self.fp = fp  # number of FPs
        self.fn = fn  # number of FNs
        self.size = size  # size of classifier (in inputs)


# calculate balanced accuracy score
def calculate_balanced_accuracy(tp, tn, p, n):

    try:
        balanced_accuracy = (tp/p + tn/n)/2
    except ZeroDivisionError:
        print("Error: balanced accuracy - division by zero! No negatives or positives in the dataset!")
        sys.exit(0)

    return balanced_accuracy


# training classifiers according to asp_program and max values of false positives and false negatives
def train_classifiers(asp_program, fp_max, fn_max):

    print("############TRAINING CLASSIFIERS############")

    # solver options
    gringo_options = ''
    clasp_options = '--opt-mode=optN --quiet=1'
    solver = pyasp.Gringo4Clasp(gringo_options=gringo_options, clasp_options=clasp_options)  # run clasp

    returned_results = []
    errors = []

    # relax constraints (number of max allowed number of false positives and false negatives)
    for i in range(0, fp_max+1):
        for j in range(0, fn_max+1):
            newfacts = pyasp.TermSet()  # create new TermSet
            newterm_pos = pyasp.Term('upper_bound_falsepos', [i])  # add term "upper bound on false positives"
            newterm_neg = pyasp.Term('upper_bound_falseneg', [j])  # add term "upper bound on false positives"
            newfacts.add(newterm_pos)  # add terms as facts
            newfacts.add(newterm_neg)

            # run solver
            solutions = solver.run([asp_program, newfacts.to_file()], collapseTerms=True, collapseAtoms=False)

            # if solutions were found
            # one result may contain several solutions!
            if len(solutions) != 0:
                new_result = Result(solutions, [], i+j, i, j, 0)
                errors.append(i+j)
                returned_results.append(new_result)

            print("SOLUTIONS FOUND FOR: FP: ", i, " FN: ", j, " SUM:", i+j)

    # if no solutions were found
    if len(returned_results) == 0:
        print("NO SOLUTIONS FOUND")

    returned_results = converter.convert_asp_results(returned_results)


    return errors, returned_results


# test solutions on testing data
def test_classifiers(solution_list, test_data, train_p, train_n, test_p, test_n):

    print("\n\n###########################################")
    print("############TESTING CLASSIFIERS############")

    bacc_train_list = []
    bacc_test_list = []
    tpr_test_list = []
    tnr_test_list = []
    size_list = []

    solution_id = 1
    for solution in solution_list:

        # train data scores
        print("\nSOLUTION ", solution_id)
        solution_id += 1
        print("##SUM: ", solution.errors, "##")
        print("FP: ", solution.fp, "FN: ", solution.fn)
        tp = train_p - solution.fn
        tn = train_n - solution.fp
        train_bacc = calculate_balanced_accuracy(tp, tn, train_p, train_n)  # calculate bacc
        print("TRAIN BACC: ", train_bacc)
        bacc_train_list.append(train_bacc)
        size_list.append(solution.size)
        print(solution.solutions_str)

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

    feature_analyser.rank_features_by_frequency(solution_list)

    # average results for all solutions
    print("\n\n###################################")
    print("############AVG RESULTS############\n")
    print("AVG TRAIN BACC: ", numpy.average(bacc_train_list))
    if len(bacc_test_list) > 1:
        train_std = numpy.std(bacc_train_list, ddof=1)
        print("STD TRAIN BACC: ", train_std)
    else:
        train_std = 0.0
        print("STD TRAIN BACC: ", 0.0)
    print("AVG TEST BACC: ", numpy.average(bacc_test_list))
    if len(bacc_test_list) > 1:
        test_std = numpy.std(bacc_test_list, ddof=1)
        print("STD TEST BACC: ", test_std)
    else:
        test_std = 0.0
        print("STD TEST BACC: ", test_std)
    print("TEST TPR: ", numpy.average(tpr_test_list))
    print("TEST TNR: ", numpy.average(tnr_test_list))
    print("AVG SIZE: ", numpy.average(size_list))
    print("\n")
    print("CSV", ";", numpy.average(bacc_train_list), ";", train_std, ";",
          numpy.average(bacc_test_list), ";", test_std, ";",
          numpy.average(tpr_test_list), ";", numpy.average(tnr_test_list), ";",
          numpy.average(size_list))




