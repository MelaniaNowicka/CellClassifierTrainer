# -*- coding: utf-8 -*-
import csv
import subprocess
from scipy.io import loadmat
import numpy as np


def csv2rows(FnameCSV):

    """

    Converts a csv file to a list of dictionaries.

    Parameters
    ----------
    FnameCSV : str
        name of input file

    Returns
    -------
    miRNAs : list
        names of features
    rows : list
        data

    """

    with open(FnameCSV, 'r') as f:
        reader = csv.reader(f, delimiter=";")
        for x in reader:
            if not x: continue
            header = x
            header = [x.strip() for x in header]
            break

        miRNAs = [x for x in header if not x in ["ID", "Annots"]]

        IDs = set([])
        rows = []
        for x in reader:
            if not x: continue
            if not x[0].strip(): continue
            newrow = dict(zip(header,[y.strip() for y in x]))
            if newrow["ID"] in IDs:
                print("\n***ERROR: row IDs must be unique, found duplicate (%s)."%newrow["ID"])
                raise Exception
            IDs.add(newrow["ID"])
            rows.append(newrow)

    return miRNAs, rows


def csv2asp(fname_csv,
            fname_asp,
            lower_bound_inputs,
            upper_bound_inputs,
            lower_bound_gates,
            upper_bound_gates,
            gate_types,
            efficiency_constraint,
            optimization_strategy,
            break_symmetries,
            silent,
            uniqueness_constraint,
            perfect_classifier,
            add_bounds_on_errors,
            upper_bound_false_pos,
            upper_bound_false_neg
            ):

    """

    Converts data and constraints to an ASP program.

    Parameters
    ----------
    fname_csv : str
        name of input file
    fname_asp : str
        name of output file
    lower_bound_inputs : int
        lower bound on number of inputs in classifier
    upper_bound_inputs : int
        upper bound on number of inputs in classifier
    lower_bound_gates : int
        lower bound on number of gates in classifier
    upper_bound_gates : int
        upper bound on number of gates in classifier
    gate_types : list
        description of allowed gates
    efficiency_constraint : bool
        if True ignore non-relevant features
    optimization_strategy : int
        - 0: no optimization
        - 1: minimize number of inputs then minimize number of gates
        - 2: minimize number of gates then minimize number of inputs
        - 3: minimize number of inputs
        - 4: minimize number of gates
    break_symmetries : bool
        if True part of symmetric solutions are removed
    silent : bool
        printing option
    uniqueness_constraint bool
        if True inputs should be unique across the classifier, irrespective of whether they are negated or not
    perfect_classifier : bool
        if True upper bound on false positive and negative errors are 0
    add_bounds_on_errors : bool
        if True add bounds on errors
    upper_bound_false_pos : int
        upper bound on false positive errors (needed if PerfectClassifier=False)
    upper_bound_false_neg : int
        upper bound on false negative errors (needed if PerfectClassifier=False)

    Returns
    -------
    miRNAs : list
        names of features
    rows : list
        data

    """

    optimization_strategy_mapping = {0: "no optimization",
                                     1: "minimize number of inputs then minimize number of gates",
                                     2: "minimize number of gates then minimize number of inputs",
                                     3: "minimize number of inputs",
                                     4: "minimize number of gates"}

    if not silent:
        print("####RNA CANCER CLASSIFIER OUTPUT####\n")
        print("Input file:", fname_csv)
        print("Upper bound on inputs:", upper_bound_inputs)
        print("Upper bound on gates:", upper_bound_gates)
        print("Gate types:")
        for i in range(0, len(gate_types)):
            print("Type ", i+1)
            [print(key, ": ", gate_types[i][key]) for key in gate_types[i].keys()]
        print("Efficiency constraints:", efficiency_constraint)
        print("Optimization strategy:", optimization_strategy, "(%s)"
              % optimization_strategy_mapping[optimization_strategy])

    assert(lower_bound_gates > 0)
    assert(lower_bound_inputs > 0)

    miRNAs, rows = csv2rows(fname_csv)

    if not silent:
        print("miRNAs: ", len(miRNAs))
        print("samples:", len(rows))

    instance = ['']
    instance += ['% ASP constraints for computing a miRNA cancer classifier']
    instance += ['% that agrees with given tissue data and satisfies given structural constraints.']
    instance += ['% note: A classifier is a Boolean expression in conjunctive form.']
    instance += ['% the homepage of the project is https://github.com/hklarner/RnaCancerClassifier.']
    instance += ['% written by K. Becker and H. Klarner, March 2016, FU Berlin.']
    instance += ['']
    instance += ['%% InputFile = %s' % fname_csv]
    instance += ['%% Efficiency constraints: %s' % str(efficiency_constraint)]
    instance += ['%% Optimization strategy: %i  (%s)'
                 % (optimization_strategy, optimization_strategy_mapping[optimization_strategy])]
    instance += ['']
    instance += ['']

    instance += ['%%% The tissue data']
    dummy = []
    for x in rows:
        y = "healthy" if x["Annots"] == "0" else "cancer"
        dummy.append("tissue(%s,%s)." % (x["ID"], y))
        if sum(map(len, dummy)) > 100:
            instance += [" ".join(dummy)]
            dummy = []

    instance += [" ".join(dummy)]
    instance += [""]
    instance += ['%%% The miRNA data']
    dummy = []
    for x in rows:
        for miRNA in miRNAs:
            y = "high" if x[miRNA] == "1" else "low"
            dummy.append("data(%s,%s,%s)." % (x["ID"], miRNA, y))
            if sum(map(len, dummy)) > 100:
                instance += [" ".join(dummy)]
                dummy = []

    instance += [' '.join(dummy)]
    instance += ['']
    instance += ['']

    instance += ["%%% User Input"]
    instance += ['lower_bound_inputs(%i).' % lower_bound_inputs]
    instance += ['upper_bound_inputs(%i).' % upper_bound_inputs]
    instance += ['lower_bound_gates(%i).' % lower_bound_gates]
    instance += ['upper_bound_gates(%i).' % upper_bound_gates]
    instance += ['']

    for x, gate_type in enumerate(gate_types):
        instance += ["%% gate type %i."%(x+1)]
        instance += ["is_gate_type(%i)."%(x+1)]
        instance += ["upper_bound_pos_inputs(%i, %i)." % (x+1, gate_type["UpperBoundPos"])]
        instance += ["upper_bound_neg_inputs(%i, %i)." % (x+1, gate_type["UpperBoundNeg"])]
        instance += ["lower_bound_pos_inputs(%i, %i)." % (x+1, gate_type["LowerBoundPos"])]
        instance += ["lower_bound_neg_inputs(%i, %i)." % (x+1, gate_type["LowerBoundNeg"])]
        instance += ["upper_bound_gate_occurence(%i, %i)." % (x+1, gate_type["UpperBoundOcc"])]
        instance += ['']

    program = ['']
    program += ['% binding of variables']
    program += ["is_tissue_id(X) :- tissue(X,Y)."]
    program += ["is_mirna(Y) :- data(X,Y,Z)."]
    program += ['is_sign(positive). is_sign(negative).']
    program += ['']
    program += ['']

    program += ['%%% Constraints']
    program += ['% number of gates']
    program += ['1 {number_of_gates(X..Y)} 1 :- lower_bound_gates(X), upper_bound_gates(Y).']
    program += ['is_gate_id(1..X) :- number_of_gates(X).']
    program += ['']

    program += ['% assignment of gate types']
    program += ['1 {gate_type(GateID, X): is_gate_type(X)} 1 :- is_gate_id(GateID).']
    program += ['']

    if efficiency_constraint:
        program += ['% inputs for gates (EfficiencyConstraint=True)']
        program += ['feasible_pos_miRNA(MiRNA) :- data(TissueID, MiRNA, high), tissue(TissueID,cancer).']
        program += ['feasible_neg_miRNA(MiRNA) :- data(TissueID, MiRNA, low),  tissue(TissueID,cancer).']
        program += ['feasible_pos_miRNA(MiRNA) :- gate_input(GateID, positive, MiRNA).']
        program += ['feasible_neg_miRNA(MiRNA) :- gate_input(GateID, negative, MiRNA).']
        program += ['']
        program += ['X {gate_input(GateID, positive, MiRNA): feasible_pos_miRNA(MiRNA)} Y '
                    ':- gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), '
                    'upper_bound_pos_inputs(GateType, Y).']
        program += ['X {gate_input(GateID, negative, MiRNA): feasible_neg_miRNA(MiRNA)} Y '
                    ':- gate_type(GateID, GateType), lower_bound_neg_inputs(GateType, X), '
                    'upper_bound_neg_inputs(GateType, Y).']
        program += ['']

    else:
        program += ['% inputs for gates (EfficiencyConstraint=False)']
        program += ['X {gate_input(GateID, positive, MiRNA): is_mirna(MiRNA)} Y '
                    ':- gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), '
                    'upper_bound_pos_inputs(GateType, Y).']
        program += ['X {gate_input(GateID, negative, MiRNA): is_mirna(MiRNA)} Y '
                    ':- gate_type(GateID, GateType), lower_bound_neg_inputs(GateType, X), '
                    'upper_bound_neg_inputs(GateType, Y).']
        program += ['']

    program += ['% at least one input for each gate']
    program += ['1 {gate_input(GateID,Sign,MiRNA): is_sign(Sign), is_mirna(MiRNA)} :- is_gate_id(GateID).']
    program += ['']

    program += ['% inputs must be unique for gates']
    program += ["{gate_input(GateID,Sign,MiRNA): is_sign(Sign)} 1 :- is_mirna(MiRNA), is_gate_id(GateID)."]
    program += ['']

    if uniqueness_constraint:
        program += ['% inputs must be unique for classifier']
        program += ["{gate_input(GateID,Sign,MiRNA): is_sign(Sign), is_gate_id(GateID)} 1 :- is_mirna(MiRNA)."]
        program += ['']

    program += ['% number of inputs is bounded']
    program += ['X {gate_input(GateID,Sign,MiRNA): is_gate_id(GateID), is_sign(Sign), is_mirna(MiRNA)} Y '
                ':- lower_bound_inputs(X), upper_bound_inputs(Y).']
    program += ['']

    program += ['% occurences of gate types is bounded']
    program += ['{gate_type(GateID,GateType): is_gate_id(GateID)} X :- upper_bound_gate_occurence(GateType,X).']
    program += ['']

    program += ['% gates fire condition']
    program += ["gate_fires(GateID,TissueID) :- gate_input(GateID,positive,MiRNA), data(TissueID,MiRNA,high)."]
    program += ["gate_fires(GateID,TissueID) :- gate_input(GateID,negative,MiRNA), data(TissueID,MiRNA,low)."]
    program += ['']

    program += ['% prediction of classifier']
    program += ["classifier(TissueID,healthy) "
               ":- not gate_fires(GateID, TissueID), is_gate_id(GateID), is_tissue_id(TissueID)."]
    program += ["classifier(TissueID,cancer) :- not classifier(TissueID, healthy), is_tissue_id(TissueID)."]
    program += ['']

    if perfect_classifier:
        program += ['% consistency of classifier and data (PerfectClassifier=True)']
        program += [':- tissue(TissueID,healthy), classifier(TissueID,cancer).']
        program += [':- tissue(TissueID,cancer),  classifier(TissueID,healthy).']
        program += ['']
    else:
        program += ['% consistency of classifier and data (PerfectClassifier=False)']
        if add_bounds_on_errors is True:
            program += ['upper_bound_falsepos(%i).' % upper_bound_false_pos]
            program += ['upper_bound_falseneg(%i).' % upper_bound_false_neg]
        program += [':- X+1 {tissue(TissueID,healthy) : classifier(TissueID,cancer)}, upper_bound_falsepos(X).']
        program += [':- X+1 {tissue(TissueID,cancer) : classifier(TissueID,healthy)}, upper_bound_falseneg(X).']
        program += ['']

    if break_symmetries:
        program += ['']
        program += ['%%% Breaking symmDuetries']
        program += ['% gate id symmetries']
        program += ['GateType1 <= GateType2 '
                    ':- gate_type(GateID1, GateType1), gate_type(GateID2, GateType2), GateID1 <= GateID2.']
        program += ['']
        program += ['']

    if optimization_strategy == 1:
        program += ['% optimization setup 1: first number of inputs then number of gates.']
        program += ['#minimize{ 1@1,(GateID,MiRNA): gate_input(GateID,Sign,MiRNA) }.']
        program += ['#minimize{ 1@2,GateID:gate_input(GateID,Sign,MiRNA) }.']

    elif optimization_strategy == 2:
        program += ['% optimization setup 2: first number of gates then number of inputs.']
        program += ['#minimize{ 1@1,GateID:gate_input(GateID,Sign,MiRNA) }.']
        program += ['#minimize{ 1@2,(GateID,MiRNA): gate_input(GateID,Sign,MiRNA) }.']

    elif optimization_strategy == 3:
        program += ['% optimization setup 3: only number of inputs.']
        program += ['#minimize{ 1,(GateID,MiRNA):gate_input(GateID,Sign,MiRNA) }.']

    elif optimization_strategy == 4:
        program += ['% optimization setup 4: only number of gates.']
        program += ['#minimize{ 1,GateID:gate_input(GateID,Sign,MiRNA) }.']

    elif optimization_strategy == 0:
        program += ['% no optimization selected']

    program += ['']
    program += ["#show gate_input/3."]

    datafile = instance + program

    if fname_asp is None:
        return "\n".join(datafile)
    else:
        with open(fname_asp, 'w') as f:
            f.writelines("\n".join(datafile))

    if not silent:
        print("\ncreated:", fname_asp)
        if optimization_strategy > 0:
            print("now run: gringo %s | clasp --opt-mode=optN --quiet=1" % fname_asp)
        else:
            print("now run: gringo %s | clasp -n0" % fname_asp)

    return instance, program


def gateinputs2function(gate_inputs):

    """
    Converts gate_inputs to a function.

    Parameters
    ----------
    gate_inputs : str
        number of true positives

    Returns
    -------
    function
        gate_inputs as a function

    """

    example = "Example for GateInputs:" \
              "gate_input(1,positive,g189) gate_input(1,positive,g224) gate_input(2,positive,g89) " \
              "gate_input(2,positive,g108) gate_input(2,positive,g154) gate_input(3,negative,g31)"

    if "." in gate_inputs:
        print('removing dots (".") from GateInputs')
        gate_inputs = gate_inputs.replace(".", "")
    if ", " in gate_inputs or " ," in gate_inputs:
        print("remove spaces inside of gate_input predecates.")
        print(example)
        raise Exception

    gate_inputs = gate_inputs.strip()
    gate_inputs = gate_inputs.split()
    #print(" found %i input(s) for function generation:"%len(GateInputs),GateInputs)
    gate_inputs = [x[x.find("(") + 1:-1].split(",") for x in gate_inputs]

    seen = set([])
    Gates = {}
    for id, sign, rna in gate_inputs:
        #if rna in seen:
            #print("miRNA %s appears several times in GateInputs!"%rna)
        if not id in Gates:
            Gates[id] = set([])

        Gates[id].add((rna,sign))
        seen.add(rna)

    def function(SampleDict):
        false_pos = False
        false_neg = False
        malfunction = []
        classifier_fires = True

        for gateid, inputs in Gates.items():
            gate_fires = False
            rnas = set([])
            for rna, sign in inputs:
                rnas.add(rna)
                if sign=="positive" and SampleDict[rna]=="1":
                    gate_fires = True
                elif sign=="negative" and SampleDict[rna]=="0":
                    gate_fires = True

            if SampleDict["Annots"] == "1" and not gate_fires:
                false_neg = True
                malfunction+= [{"tissue":"cancer",
                                "tissue_id":SampleDict["ID"],
                                "gate_id":gateid,
                                "gate_inputs":inputs,
                                "miRNA_expressions":","
                                    .join(["%s=%s"%item for item in SampleDict.items() if item[0] in rnas])}]

            if SampleDict["Annots"] == "0" and gate_fires:
                malfunction+= [{"tissue":"healthy",
                                "tissue_id":SampleDict["ID"],
                                "gate_id":gateid,
                                "gate_inputs":inputs,
                                "miRNA_expressions":","
                                    .join(["%s=%s"%item for item in SampleDict.items() if item[0] in rnas])}]

            classifier_fires = classifier_fires and gate_fires

        if SampleDict["Annots"] == "0" and not classifier_fires:
            malfunction = []

        if SampleDict["Annots"] == "0" and classifier_fires:
            false_pos = True

        return false_pos, false_neg, malfunction

    return function


def check_classifier(fname_csv, gate_inputs):

    """
    Calculates the number of false positive and negative errors of a classifier for a given data set.

    Parameters
    ----------
    fname_csv : int
        number of true positives
    gate_inputs : int
        number of true negatives

    Returns
    -------
    false_neg : int
        number of false negative errors
    false_pos : int
        number of false positive errors

    """

    #Example for GateInputs: gate_input(1,positive,g189) gate_input(1,positive,g224) gate_input(2,positive,g89)
    #gate_input(2,positive,g108) gate_input(2,positive,g154) gate_input(3,negative,g31)

    #print("\n--- check_classifier")

    miRNAs, rows = csv2rows(fname_csv)

    #print(" miRNAs: ", len(miRNAs))
    #print(" samples:", len(rows))

    false_neg = 0
    false_pos = 0

    function = gateinputs2function(gate_inputs)
    #print(" testing each sample against the function..")
    hits = set([])
    for x in rows:
        fp, fn, malfunction = function(x)
        if fp:
            false_pos += 1
        if fn:
            false_neg += 1

        #if malfunction:
            #hits.add(x["ID"])
            #for location in malfunction:
                #print(" ** found malfunction:")
                #for item in sorted(location.items()):
                    #print("    %s = %s"%item)

    #print(" classifier =",GateInputs)
    #print(" data =",FnameCSV)
    #if hits:
        #print(" result = %i inconsistencies"%(len(hits)), hits)
        #print(" false positives:", false_pos)
        #print(" false negatives:", false_neg)
    #else:
        #print(" result = classifier and data are consistent")

    return false_neg, false_pos


def check_csv(fname_csv):

    """
    Counts how many features are constant across all samples, and checks if there are inconsistencies in the data
    (identical feature profile but different annotation)

    Parameters
    ----------
    fname_csv : str
        name of input data file

    """

    print("\n--- check_csv")

    miRNAs, rows = csv2rows(fname_csv)
    print(" miRNAs: ", len(miRNAs))
    print(" samples:", len(rows))

    healthy = sum([1 for x in rows if x["Annots"]=="0"])
    print("  healthy: %i"%healthy)
    print("  cancer: %i"%(len(rows)-healthy))

    inconsistencies = []
    seen = []
    for x in rows:
        for y in seen:
            if all(x[rna]==y[rna] for rna in miRNAs):
                if x["Annots"]!=y["Annots"]:
                    inconsistencies.append(x["ID"])
        seen.append(x)

    constants = []
    for rna in miRNAs:
        value = rows[0][rna]
        if all(x[rna]==value for x in rows):
            constants.append(rna)

    print(" inconsistencies (%i): %s"%(len(inconsistencies),",".join(inconsistencies) or "-"))
    print(" constants (%i): %s"%(len(constants),",".join(constants) or "-"))


if __name__=="__main__":
    print("nothing to do")

