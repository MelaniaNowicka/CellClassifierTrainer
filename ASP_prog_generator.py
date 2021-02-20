import csv
import classifier


def create_asp_prog(input, constraints):

    """
    Function to create ASP program.

    Parameters
    ----------
    input : str
        name of input train data file
    constraints : str
        name of inputs constraints file

    Returns
    -------
    instance : str
        ASP instance
    program : str
        ASP program

    """

    FnameCSV = input
    FnameASP = input.replace(".csv", ".asp")

    ConReader = csv.reader(open(constraints), delimiter=';')

    Constraints = dict((rows[0], rows[1]) for rows in ConReader)

    GateTypes = []

    GateType1 = {
        "LowerBoundPos": int(Constraints.get("GateType1_LowerBoundPos")),
        "LowerBoundNeg": int(Constraints.get("GateType1_LowerBoundNeg")),
        "UpperBoundPos": int(Constraints.get("GateType1_UpperBoundPos")),
        "UpperBoundNeg": int(Constraints.get("GateType1_UpperBoundNeg")),
        "UpperBoundOcc": int(Constraints.get("GateType1_UpperBoundOcc"))
    }

    GateType2 = {
        "LowerBoundPos": int(Constraints.get("GateType2_LowerBoundPos")),
        "LowerBoundNeg": int(Constraints.get("GateType2_LowerBoundNeg")),
        "UpperBoundPos": int(Constraints.get("GateType2_UpperBoundPos")),
        "UpperBoundNeg": int(Constraints.get("GateType2_UpperBoundNeg")),
        "UpperBoundOcc": int(Constraints.get("GateType2_UpperBoundOcc"))
    }

    GateTypes = [GateType1, GateType2]

    Constraints.get("PerfectClassifier")

    instance, program = classifier.csv2asp(FnameCSV,
                                           FnameASP,
                                           int(Constraints.get("LowerBoundInputs")),
                                           int(Constraints.get("UpperBoundInputs")),
                                           int(Constraints.get("LowerBoundGates")),
                                           int(Constraints.get("UpperBoundGates")),
                                           GateTypes,
                                           int(Constraints.get("EfficiencyConstraint")),
                                           int(Constraints.get("OptimizationStrategy")),
                                           int(Constraints.get("BreakSymmetries")),
                                           int(Constraints.get("Silent")),
                                           int(Constraints.get("UniquenessConstraint")),
                                           int(Constraints.get("BooleanFunctionForm")),
                                           int(Constraints.get("PerfectClassifier")),
                                           int(Constraints.get("AddBoundsOnErrors")),
                                           int(Constraints.get("UpperBoundFalsePos")),
                                           int(Constraints.get("UpperBoundFalseNeg")))

    instance = "\n".join(instance)
    program = "\n".join(program)

    return instance, program

