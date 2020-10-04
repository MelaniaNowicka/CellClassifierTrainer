import argparse
import sys
import trainer
import filter


# command line argument parser
def arg_parser():

    parser = argparse.ArgumentParser(description='ASP-based training of miRNA cell classifiers based on '
                                                 'RnaCancerClassifier (https://github.com/hklarner/RnaCancerClassifier).'
                                                 'Written by Melania Nowicka, FU Berlin, 2019.')

    parser.add_argument('--asp_program', dest='asp_program', type=str,
                        help='ASP program generated with RnaCancerClassifier.')
    parser.add_argument('--test_data', dest='test_data', default=None, type=str, help='Test data set.')
    parser.add_argument('--train_p', dest='train_p', type=int, help='Number of positive samples in training data.')
    parser.add_argument('--train_n', dest='train_n', type=int, help='Number of negative samples in training data.')
    parser.add_argument('--test_p', dest='test_p', type=int, default=None,
                        help='Number of positive samples in test data.')
    parser.add_argument('--test_n', dest='test_n', type=int, default=None,
                        help='Number of negative samples in test data.')
    parser.add_argument('--fp', dest='fp_max', type=int, help='Upper bound on false positives.')
    parser.add_argument('--fn', dest='fn_max', type=int, help='Upper bound of false negatives.')

    params = parser.parse_args()

    return params


# run training of classifiers
def run_trainer():

    params = arg_parser()

    asp_program = params.asp_program  # ASP program
    test_data = params.test_data  # test data set
    fp_max = params.fp_max  # upper bound on false positives allowed in training
    fn_max = params.fn_max  # upper bound on false negatives allowed in training
    train_positives = params.train_p  # number of positive samples in training data
    train_negatives = params.train_n  # number of negative samples in training data
    test_positives = params.test_p  # number of positive samples in test data
    test_negatives = params.test_n  # number of negative samples in test data

    # train classifiers
    errors, found_solutions = trainer.train_classifiers(asp_program, fp_max, fn_max)
    # filter best found solutions by total number of errors
    solution_list = filter.filter_best_solutions(errors, found_solutions)
    # filter shortest classifiers
    shortest_classifiers = filter.filter_shortest_solutions(solution_list)
    # filter symmetric classifiers (that only differ in order of inputs and gates)
    best_results = filter.filter_symmetric_solutions(shortest_classifiers)
    # test classifiers on test data
    if test_data is not None and len(best_results) != 0:
        trainer.test_classifiers(best_results, test_data,
                                 train_positives, train_negatives,
                                 test_positives, test_negatives)


if __name__ == "__main__":

    run_trainer()

