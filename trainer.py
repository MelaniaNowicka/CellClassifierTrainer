import converter
from clyngor import solve
import time


# class for result of ASP computation
class Result:

    """

    Class representing an ASP Result.

    Attributes
    ----------
    solutions_str : list
        list of all solutions belonging to the Result (formatted as strings)
    solutions_by_gate : list
        list of all solutions belonging to the Result (formatted as lists)
    errors : int
        list of total errors received for the Result
    fp : int
        number of false positives received for the Result
    fn : int
        number of false negatives received for the Result
    size : int
        size of solutions in the Result

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


# training classifiers according to asp_program and max values of false positives and false negatives
def train_classifiers(instance, program, fp_min, fn_min, fp_max, fn_max, max_time, start_train):

    """
    Trains classifiers according to constraints relaxation described in Becker et al. [1]_
    using RnaCancerClassifier [2]_ and Clyngor [3]_.

    Parameters
    ----------
    instance : str
        instance, i.e., data and constant constraints
    program : str
        ASP program, i.e., logic rules
    fp_min : int
        number of min allowed false positive errors
    fn_min : int
        number of min allowed false negative errors
    fp_max : int
        number of max allowed false positive errors
    fn_max : int
        number of max allowed false negative errors

    Returns
    -------
    errors : list
        list of number of errors
    returned_results : list
        list of returned results

    References
    ----------
    .. [1] `Becker K, Klarner H, Nowicka M and Siebert H (2018) Designing miRNA-Based Synthetic Cell Classifier \
    Circuits Using Answer Set Programming. Front. Bioeng. Biotechnol. 6:70. <10.3389/fbioe.2018.00070>`_
    .. [2] `RnaCancerClassifier <https://github.com/MelaniaNowicka/RnaCancerClassifier>`_, RnaCancerClassifier \
    source code.
    .. [3] `Clyngor <https://github.com/Aluriak/clyngor>`_, Clyngor source code.

    """

    print("\n############################################")
    print("############TRAINING CLASSIFIERS############")
    print("############################################\n")

    returned_results = []
    errors = []

    print("\nProgress...")
    # relax constraints (number of max allowed number of false positives and false negatives)
    for i in range(fp_min, fp_max+1):  # relax number of false positives
        for j in range(fn_min, fn_max+1):  # relax number of false negatives

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
                print("\nSolutions found for: FP: ", i, " FN: ", j, " SUM:", i + j)
                new_result = Result(solutions, [], i+j, i, j, 0)  # create new result
                # convert asp results to string and lists
                new_result_readable = converter.convert_asp_results([new_result])[0]
                for solution in new_result_readable.solutions_str:
                    print(solution)
                returned_results.append(new_result_readable)  # note, one result may contain several solutions!
                errors.append(i+j)  # add total number of errors to list of errors

            # check current time
            current_time = time.time()
            elapsed_time = current_time - start_train
            if elapsed_time >= max_time:
                print("\nTIME WARNING: Time of computation exceeded ", max_time, " seconds.")
                break
        else:
            continue
        break

    print("\nCollecting answers finished.")

    # if no solutions were found
    if len(returned_results) == 0:
        print("NO SOLUTIONS FOUND")

    # convert asp results to string and lists
    # returned_results = converter.convert_asp_results(returned_results)

    return errors, returned_results
