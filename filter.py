import trainer


# filter best performing solutions by total number of errors
def filter_best_solutions(errors, solutions):

    """

    Filters best solutions based on the total number of errors.

    Parameters
    ----------
    errors : list
        list of total numbers of errors for all results
    solutions : list
        list of solutions

    Returns
    -------
    solution_list : list
        list of solutions

    """

    print("\n\n##############################################")
    print("############FINDING BEST SOLUTIONS############")
    # find best solution ids by total number of errors
    best_results_ids = [i for i, x in enumerate(errors) if x == min(errors)]
    solution_list = list(solutions)
    best_results = [solution_list[i] for i in best_results_ids]  # filter best solutions

    for result in best_results:  # result may contain several solutions for particular number of errors in total
        print("\n##SUM: ", result.errors, "##")  # show total number of errors
        print("FP: ", result.fp, "FN: ", result.fn)  # show number of false positives and false negatives
        print("Number of solutions: ", len(result.solutions_str))  # show number of solutions

        for solution in result.solutions_str:  # iterate over solutions in single ASP result
            print(solution)  # show solutions

    solution_list = []  # create empty solution list

    # create a list of single solutions (each result contains single solution)
    for result in best_results:
        for i in range(0, len(result.solutions_str)):
            # create single solution
            single_solution = trainer.Result(result.solutions_str[i], result.solutions_by_gate[i], result.errors,
                                             result.fp, result.fn, result.size)
            solution_list.append(single_solution)  # add to solution list

    return solution_list


# find shortest solutions (by number of inputs) in list of solutions
def filter_shortest_solutions(solutions):

    """

    Filters solutions based on the size.

    Parameters
    ----------
    solutions : list
        list of solutions

    Returns
    -------
    list
        list of solutions

    """

    # create a list of solution's sizes
    size_list = [solution.size for solution in solutions]

    print("\n\n###################################################")
    print("############FILTERING ACCORDING TO SIZE############")
    # find ids of shortest solutions and filter them
    shortest_solutions_ids = [i for i, x in enumerate(size_list) if x == min(size_list)]
    shortest_solutions = [solutions[i] for i in shortest_solutions_ids]  # filter shortest solutions by id

    for solution in shortest_solutions:  # show shortest solutions
        print("\n##SUM: ", solution.errors, "##")
        print("FP: ", solution.fp, "FN: ", solution.fn)
        print(solution.solutions_str)

    return shortest_solutions


# remove symmetric solutions (that only differ in order of inputs and gates)
def filter_symmetric_solutions(solutions):

    """

    Filters symmetric solutions.

    Parameters
    ----------
    solution_list : list
        list of solutions

    Returns
    -------
    solutions : list
        list of solutions

    """

    solution_list = list(solutions)
    print("\n\n####################################################")
    print("############REMOVING SYMMETRIC SOLUTIONS############\n")
    print("Number of solutions before filtering: ", len(solution_list))
    to_del = []  # list of ids of solutions to delete
    for i in range(0, len(solution_list) - 1):
        for j in range(i + 1, len(solution_list)):
            # check equality of sorted solutions
            # lists of gates and inputs are sorter alphabetically
            if sorted(solution_list[i].solutions_by_gate) == sorted(solution_list[j].solutions_by_gate):
                to_del.append(j)  # add id of solution to delete

    to_del = list(set(to_del))  # remove repeating ids
    to_del.sort(reverse=True)  # sort indices in descending order for removal

    # remove symmetrical solutions
    for id in to_del:
        del solution_list[id]

    print("Number of solutions after filtering: ", len(solution_list))
    for solution in solution_list:  # show unique solutions
        print("\n##SUM: ", solution.errors, "##")
        print("FP: ", solution.fp, "FN: ", solution.fn)
        print(solution.solutions_str)

    return solution_list

