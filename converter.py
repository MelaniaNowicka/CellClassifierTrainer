# convert asp solution to list of gates
def convert_solution_to_list(inputs):

    new_gate = []
    new_solution = []
    gate_id = inputs[0][0]  # assign the first gate id

    for i in range(0, len(inputs)):  # iterate over inputs in solution

        if inputs[i][0] == gate_id:  # if the current input's id is still same
            new_gate.append((inputs[i][2], inputs[i][1]))  # add next input to the gate (feature id, sign)

            if i == len(inputs) - 1:  # if this is the last input
                new_solution.append(sorted(new_gate))  # add last gate to solution

        else:  # if the current input's id is different
            new_solution.append(sorted(new_gate))  # add current gate to solution
            new_gate = []  # create new gate
            gate_id = inputs[i][0]  # assign new current gate id
            new_gate.append((inputs[i][2], inputs[i][1]))  # add next input to the gate (feature id, sign)

            if i == len(inputs) - 1:  # if this is the last input
                new_solution.append(sorted(new_gate))  # add last gate to solution

    return new_solution


# convert ASP results to strings and lists of gates
def convert_asp_results(results):

    size = 0

    # iterate over found results
    for result in results:
        print("\n##SUM: ", result.errors, "##")  # total number of errors for solutions in result
        print("FP: ", result.fp, "FN: ", result.fn)  # number of false positives and negatives
        print("Number of solutions: ", len(result.solutions_str))  # number of solutions in result

        solutions_by_str = []
        solutions_by_gate = []

        # iterate over solutions in result
        for solution in result.solutions_str:

            # iterate over atoms in solution (contains gate id, sign and feature id)
            input_list = []
            for atom in solution:
                input_list.append(atom.args())

            # sort inputs by gate id and alphabetically
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

