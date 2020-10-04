def optimize_rules(asp_program, fp_max, fn_max):

    print("##TRAINING RULES##")
    start = time.time()

    gringo_options = ''
    clasp_options = '--opt-mode=optN --quiet=1'
    solver = Gringo4Clasp(gringo_options=gringo_options, clasp_options=clasp_options)  # run clasp

    newfacts = TermSet()
    newterm_pos = Term('upper_bound_falsepos', [fp_max])
    newterm_neg = Term('upper_bound_falseneg', [fn_max])
    newfacts.add(newterm_pos)
    newfacts.add(newterm_neg)

    solutions = solver.run([asp_program, newfacts.to_file()], collapseTerms=True, collapseAtoms=False)

    for solution in solutions:

        gates = []
        for atom in solution:
            gates.append(atom.args())

        gates.sort(key=lambda gates: gates[0])

        inputs_str = []
        for gate in gates:
            input = ",".join(gate)
            inputs_str.append("".join(['gate_input', '(', input, ') ']))

        print("".join(inputs_str))

    rules = []
    rows = []
    solution_counter = 0

    header = ["ID", "size", "miRNA1", "sign1", "miRNA2", "sign2"]
    print(";".join(header))

    if len(solutions) != 0:
        for solution in solutions:
            solution_counter += 1
            gates = []

            for atom in solution:
                gates.append(atom.args())

            gates.sort(key=lambda gates: gates[0])

            inputs_str = []
            row = []
            row.append(str(solution_counter))
            row.append(str(len(gates)))
            for atom in gates:
                input = ",".join(atom)
                inputs_str.append("".join(['gate_input', '(', input, ') ']))

                row.append(atom[2])
                if(atom[1] == "negative"):
                    row.append("0")
                if(atom[1] == "positive"):
                    row.append("1")

            #print("".join(inputs_str))
            print(";".join(row))

    end = time.time()
    print("time: ", end - start)
