import argparse
import sys
from datetime import datetime
import time

import ASP_prog_generator
import trainer
import filter


# command line argument parser
def arg_parser():

    """ Function to parse command line arguments.

    Returns
    ----------
    namespace
        parsed arguments

    """

    parser = argparse.ArgumentParser(description='ASP-based training of miRNA cell classifiers using'
                                                 'RnaCancerClassifier(https://github.com/hklarner/RnaCancerClassifier).'
                                                 'Written by Melania Nowicka, FU Berlin, 2019.')

    parser.add_argument('--train_data', dest='train_data', type=str, default=None,
                        help='Training data set file.')
    parser.add_argument('--constr', dest='constr', type=str, default=None,
                        help='Constraints for ASP program.')
    parser.add_argument('--test_data', dest='test_data', default=None, type=str, help='Test data set file.')
    parser.add_argument('--train_p', dest='train_p', type=int, help='Number of positive samples in training data.')
    parser.add_argument('--train_n', dest='train_n', type=int, help='Number of negative samples in training data.')
    parser.add_argument('--test_p', dest='test_p', type=int, default=None,
                        help='Number of positive samples in test data.')
    parser.add_argument('--test_n', dest='test_n', type=int, default=None,
                        help='Number of negative samples in test data.')
    parser.add_argument('--min_fp', dest='fp_min', type=int, default=0, help='Lower bound on false positives.')
    parser.add_argument('--min_fn', dest='fn_min', type=int, default=0, help='Lower bound on false negatives.')
    parser.add_argument('--max_fp', dest='fp_max', type=int, default=0, help='Upper bound on false positives.')
    parser.add_argument('--max_fn', dest='fn_max', type=int, default=0, help='Upper bound on false negatives.')

    params = parser.parse_args()

    return params


# run training of classifiers
def run_trainer():

    """

    Runs the training of classifiers.

    """

    print("Log date: ", datetime.now().isoformat(), "\n")

    start_train = time.time()

    params = arg_parser()  # parse arguments

    if params.train_data is None:  # if no train data is given
        print("ERROR: Train data set file not given.")
        sys.exit(0)
    else:
        if params.constr is None:
            print("ERROR: ASP constraint file not given.")
            sys.exit(0)
        else:
            instance, program = \
                ASP_prog_generator.create_asp_prog(params.train_data, params.constr)  # generate ASP program
        test_data = params.test_data  # test data set
        fp_min = params.fp_min  # lower bound on false positives allowed in training
        fn_min = params.fn_min  # lower bound on false negatives allowed in training
        fp_max = params.fp_max  # upper bound on false positives allowed in training
        fn_max = params.fn_max  # upper bound on false negatives allowed in training
        train_positives = params.train_p  # number of positive samples in training data
        train_negatives = params.train_n  # number of negative samples in training data
        test_positives = params.test_p  # number of positive samples in test data
        test_negatives = params.test_n  # number of negative samples in test data

        print("\nDATA INFO")
        print("Train data set: ", params.train_data)
        print("Number of TP in train data: ", params.train_p)
        print("Number of TN in train data: ", params.train_n)
        print("Test data set: ", params.test_data)
        print("Number of TP in test data: ", params.test_p)
        print("Number of TN in test data: ", params.test_n)

        print("\nTRAINING PARAMETERS")
        print("Min FP: ", params.fp_min)
        print("Min FN: ", params.fn_min)
        print("Max FP: ", params.fp_max)
        print("Max FN: ", params.fn_max)

        # train classifiers
        errors, found_solutions = trainer.train_classifiers(instance, program, fp_min, fn_min, fp_max, fn_max)
        # filter best found solutions by total number of errors
        solution_list = filter.filter_best_solutions(errors, found_solutions)
        # filter shortest classifiers
        shortest_classifiers = filter.filter_shortest_solutions(solution_list)
        # filter symmetric classifiers (that only differ in order of inputs and gates)
        best_results = filter.filter_symmetric_solutions(shortest_classifiers)
        # test classifiers on test data
        if test_data is not None and len(list(best_results)) != 0:
            trainer.test_classifiers(best_results, test_data,
                                     train_positives, train_negatives,
                                     test_positives, test_negatives)

    end_train = time.time()
    training_time = end_train - start_train
    print("TRAINING TIME: ", end_train - start_train)


if __name__ == "__main__":

    run_trainer()
