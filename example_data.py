import trainer


# creates solutions with different total error number
def create_example_best_solutions_instance():

    solution_1_str = "gate_input(1,positive,hsamiR135b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,positive,hsamiR1395p) gate_input(2,positive,hsamiR141)"

    solution_1_by_gate = [[("hsamiR135b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "positive"), ("hsamiR141", "positive")]]

    solution_1 = trainer.Result(solution_1_str, solution_1_by_gate, 3, 1, 2, 4)

    solution_2_str = "gate_input(1,positive,hsamiR135b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,positive,hsamiR1395p) gate_input(2,positive,hsamiR141) "

    solution_2_by_gate = [[("hsamiR135b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "positive"), ("hsamiR141", "positive")]]

    solution_2 = trainer.Result(solution_2_str, solution_2_by_gate, 3, 1, 2, 4)

    solution_3_str = "gate_input(1,positive,hsamiR12b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,positive,hsamiR1395p)"

    solution_3_by_gate = [[("hsamiR12b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "negative")]]

    solution_3 = trainer.Result(solution_3_str, solution_3_by_gate, 0, 0, 0, 3)

    solution_4_str = "gate_input(1,positive,hsamiR12b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,positive,hsamiR1395p)"

    solution_4_by_gate = [[("hsamiR12b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "negative")]]

    solution_4 = trainer.Result(solution_4_str, solution_4_by_gate, 0, 0, 0, 3)

    result_1 = trainer.Result([solution_1_str, solution_2_str], [solution_1_by_gate, solution_2_by_gate], 3, 1, 2, 4)
    result_2 = trainer.Result([solution_3_str, solution_4_str], [solution_3_by_gate, solution_4_by_gate], 0, 0, 0, 3)

    results = [result_1, result_2]

    correct_output = [solution_3.solutions_by_gate, solution_4.solutions_by_gate]

    return results, correct_output


# creates set of solutions of different size
def create_example_size_instance():

    solution_1_str = "gate_input(1,positive,hsamiR135b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,positive,hsamiR1395p) gate_input(2,positive,hsamiR141) "

    solution_1_by_gate = [[("hsamiR135b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "positive"), ("hsamiR141", "positive")]]

    solution_1 = trainer.Result(solution_1_str, solution_1_by_gate, 4, 2, 2, 4)

    solution_2_str = "gate_input(1,positive,hsamiR135b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,positive,hsamiR1395p) gate_input(2,positive,hsamiR141)"

    solution_2_by_gate = [[("hsamiR135b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "positive"), ("hsamiR141", "positive")]]

    solution_2 = trainer.Result(solution_2_str, solution_2_by_gate, 4, 2, 2, 4)

    solution_3_str = "gate_input(1,positive,hsamiR12b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,positive,hsamiR1395p)"

    solution_3_by_gate = [[("hsamiR12b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "negative")]]

    solution_3 = trainer.Result(solution_3_str, solution_3_by_gate, 3, 1, 2, 3)

    solution_4_str = "gate_input(1,positive,hsamiR12b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,positive,hsamiR1395p)"

    solution_4_by_gate = [[("hsamiR12b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "negative")]]

    solution_4 = trainer.Result(solution_4_str, solution_4_by_gate, 3, 1, 2, 3)

    solution_list = [solution_1, solution_2, solution_3, solution_4]

    correct_output = [solution_3, solution_4]

    return solution_list, correct_output


def create_example_symmetry_instance():

    solution_1_str = "gate_input(1,positive,hsamiR135b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,positive,hsamiR1395p) gate_input(2,positive,hsamiR141) " \
                     "gate_input(2,positive,hsamiR144) "

    solution_1_by_gate = [[("hsamiR135b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "positive"), ("hsamiR141", "positive"), ("hsamiR144", "positive")]]

    solution_1 = trainer.Result(solution_1_str, solution_1_by_gate, 5, 2, 3, 5)

    solution_2_str = "gate_input(1,positive,hsamiR1395p) gate_input(1,positive,hsamiR141) " \
                     "gate_input(1,positive,hsamiR144) " \
                     "gate_input(2,positive,hsamiR135b) gate_input(2,positive,hsamiR345x9y1) "

    solution_2_by_gate = [[("hsamiR1395p", "positive"), ("hsamiR141", "positive"), ("hsamiR144", "positive")],
                          [("hsamiR135b", "positive"), ("hsamiR345x9y1", "positive")]]

    solution_2 = trainer.Result(solution_2_str, solution_2_by_gate, 5, 2, 3, 5)

    solution_3_str = "gate_input(1,positive,hsamiR12b) gate_input(1,positive,hsamiR345x9y1) " \
                     "gate_input(2,negative,hsamiR1395p) gate_input(3,negtive,hsamiR141) "

    solution_3_by_gate = [[("hsamiR12b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "negative")], [("hsamiR141", "negative")]]

    solution_3 = trainer.Result(solution_3_str, solution_3_by_gate, 5, 2, 3, 4)

    solution_4_str = "gate_input(1,positive,hsamiR141) " \
                     "gate_input(2,positive,hsamiR12b) gate_input(2,positive,hsamiR345x9y1) " \
                     "gate_input(3,positive,hsamiR1395p) "

    solution_4_by_gate = [[("hsamiR141", "negative")], [("hsamiR12b", "positive"), ("hsamiR345x9y1", "positive")],
                          [("hsamiR1395p", "negative")]]

    solution_4 = trainer.Result(solution_4_str, solution_4_by_gate, 5, 2, 3, 4)

    solution_list = [solution_1, solution_2, solution_3, solution_4]

    correct_output = [solution_1, solution_3]

    return solution_list, correct_output
