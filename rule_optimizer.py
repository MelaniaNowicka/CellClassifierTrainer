import time
import sys
from clyngor import solve
import ASP_prog_generator
import argparse
import trainer
import converter
import filter


def optimize_rules(instance, program, fp_max, fn_max):

    """

    Optimizes rules according to ASP constraints.

    Parameters
    ----------
    instance : str
        instance
    program : str
        program
    fp_max : int
        upper bound on false positives
    fn_max : int
        upper bound on false negatives

    """

    print("##TRAINING RULES##")
    start = time.time()

    constraints = \
        "\n".join(["upper_bound_falsepos(" + str(fp_max) + ").", "upper_bound_falseneg(" + str(fn_max) + ")."])
    asp_program = instance + constraints + program  # add constraints to the instance and the program

    opt = '--opt-mode=optN'  # add clasp option - return all optimal models
    answers = solve(inline=asp_program, options=opt)  # solve program

    #  '--quiet=1' option does not work with clyngor
    #  answers.with_optimality returns information about optimality of answers
    solutions = []
    for answer in answers.with_optimality:
        if answer[2] is True:  # if solution is optimal
            solutions.append(list(answer)[0])  # ad solutions to solution list

    returned_results = []
    errors = []

    if len(solutions) != 0:  # if solutions were found
        new_result = trainer.Result(solutions, [], fp_max + fn_max, fp_max, fn_max, 0)  # create new result
        errors.append(fp_max + fn_max)
        returned_results.append(new_result)  # note, one result may contain several solutions!

    # convert asp results to string and lists
    returned_results = converter.convert_asp_results(returned_results)
    solution_list = filter.filter_best_solutions(errors, returned_results)
    solutions = filter.filter_symmetric_solutions(solution_list)

    solution_counter = 0

    print("\n")
    print("RULE LIST\n")
    header = ["ID", "size", "feature1", "sign1", "feature2", "sign2", "gate"]
    print(";".join(header))

    if len(solutions) != 0:

        for solution in solutions:

            solution_counter += 1
            row = [str(solution_counter), str(len(solution.solutions_by_gate))]

            for gate in solution.solutions_by_gate:
                for input in gate:
                    row.append(input[0])
                    row.append(input[1])
                if len(gate) == 2 and gate[0][1] == 'positive' and gate[1][1] == 'positive':
                    row.append('0')
                else:
                    row.append('1')

            print(";".join(row))
    else:
        print("NO SOLUTIONS FOUND")

    print("\n")
    end = time.time()
    print("time: ", end - start)


# command line argument parser
def arg_parser():

    """

    Function to parse command line arguments.

    Returns
    ----------
    namespace
        parsed arguments

    """

    parser = argparse.ArgumentParser(description='ASP-based rule optimizer using'
                                                 'RnaCancerClassifier(https://github.com/hklarner/RnaCancerClassifier).'
                                                 'Written by Melania Nowicka, FU Berlin, 2019.')

    parser.add_argument('--train_data', dest='train_data', type=str, default=None,
                        help='Training data set file.')
    parser.add_argument('--constr', dest='constr', type=str, default=None,
                        help='Constraints for ASP program.')
    parser.add_argument('--max_fp', dest='fp_max', type=int, default=0, help='Upper bound on false positives.')
    parser.add_argument('--max_fn', dest='fn_max', type=int, default=0, help='Upper bound on false negatives.')

    params = parser.parse_args()

    return params


def run_rule_optimizer():

    """

    Runs the training of classifiers.

    """

    start_train = time.time()

    params = arg_parser()  # parse arguments

    if params.train_data is None:  # if no train data is given
        print("ERROR: Train data set file not given.")
        sys.exit(0)
    else:
        if params.constr is None:
            print("ERROR: ASP constraints file not given.")
            sys.exit(0)
        else:
            instance, program = \
                ASP_prog_generator.create_asp_prog(params.train_data, params.constr)  # generate ASP program
        fp_max = params.fp_max  # upper bound on false positives allowed in training
        fn_max = params.fn_max  # upper bound on false negatives allowed in training

    optimize_rules(instance, program, fp_max, fn_max)

    end_train = time.time()
    training_time = end_train - start_train
    print("TRAINING TIME: ", end_train - start_train)


if __name__ == "__main__":

    run_rule_optimizer()
