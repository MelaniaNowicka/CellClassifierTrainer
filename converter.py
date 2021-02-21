# convert asp solution to list of gates
def convert_solution_to_list(inputs):

    """

    Converts a solution to a list of lists.

    Parameters
    ----------
    inputs : list
        list of classifier's inputs

    Returns
    ----------
    list
        solution as a list of lists

    """

    new_gate = []
    new_solution = []
    input_list = list(inputs)
    gate_id = input_list[0][0]  # assign the first gate id

    for i in range(0, len(input_list)):  # iterate over inputs in solution

        if input_list[i][0] == gate_id:  # if the current input's gate id is still same
            new_gate.append((input_list[i][2], input_list[i][1]))  # add next input to the gate (feature id, sign)

            if i == len(input_list) - 1:  # if this is the last input in the classifier
                new_solution.append(sorted(new_gate))  # add last gate to solution

        else:  # if the current input's gate id is different
            new_solution.append(sorted(new_gate))  # add current gate to solution
            new_gate = []  # create new gate
            gate_id = input_list[i][0]  # assign new current gate id
            new_gate.append((input_list[i][2], input_list[i][1]))  # add next input to the gate (feature id, sign)

            if i == len(input_list) - 1:  # if this is the last input
                new_solution.append(sorted(new_gate))  # add last gate to solution

    return new_solution


# convert ASP results to strings and lists of gates
def convert_asp_results(results):

    """

    Converts ASP answers to a lists of lists and string.

    Format:

    - list of lists of lists: [[feature_id_1, sign_1], [feature_id_2, sign_2]],
    e.g., [[[miR_1, positive], [miR_2, positive]], [[miR_3, negative]]
    - string: gate_input(gate_id, feature_id, sign) gate_input(gate_id, feature_id, sign), \
    e.g., gate_input(1, miR_1, positive) gate_input(1, miR_2, positive) gate_input(2, miR_2, negative)

    Parameters
    ----------
    results : list
        list containing results in a solver-returned format

    Returns
    ----------
    list
        formatted results

    """

    size = 0

    print("\nPRINTING RESULTS:")
    # iterate over found results
    for result in results:
        print("\n##SUM: ", result.errors, "##")  # total number of errors for solutions in result
        print("FP: ", result.fp, "FN: ", result.fn)  # number of false positives and negatives
        print("Number of solutions: ", len(result.solutions_str))  # number of solutions in result

        solutions_by_str = []
        solutions_by_gate = []

        # iterate over solutions in result
        for solution in result.solutions_str:

            # iterate over atoms in solution (contains: gate id, sign and feature id)
            input_list = []
            for atom in solution:  # atom[1][0] - gate id, atom[1][1] - sign and atom[1][2]] - feature id
                input_list.append([str(atom[1][0]), atom[1][1], atom[1][2]])

            # sort inputs by gate id and then alphabetically
            input_list.sort(key=lambda inputs: (inputs[0], inputs))

            inputs_str = []  # keep inputs as strings
            for i in input_list:
                input_str = ",".join(i)
                inputs_str.append("".join(['gate_input', '(', input_str, ') ']))

            size = len(input_list)  # check the current size of classifier

            new_solution = convert_solution_to_list(input_list)  # convert solution to list of gates

            print("".join(inputs_str))  # show solution
            solutions_by_str.append("".join(inputs_str))  # add solution as string
            solutions_by_gate.append(sorted(new_solution))  # add solution as list of gates

        result.solutions_str = solutions_by_str  # replace all solutions as strings in result
        result.solutions_by_gate = solutions_by_gate  # add all solutions as lists of gates in result
        result.size = size  # add size of solutions in single result

    return results
