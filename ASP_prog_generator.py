import csv
import configparser
import classifier


def create_asp_prog(input_file, config_file_name):

    """
    Function to create ASP program.

    Parameters
    ----------
    input_file : str
        name of input train data file
    config_file_name : str
        name of constraint file

    Returns
    -------
    instance : str
        ASP instance
    program : str
        ASP program

    """

    config_file = configparser.ConfigParser()
    config_file.read(config_file_name)

    FnameCSV = input_file
    FnameASP = input_file.replace(".csv", ".asp")

    GateTypes = []

    GateType1 = {
        "LowerBoundPos": int(config_file['GATE SPECIFICATION']['GateType1_LowerBoundPos']),
        "LowerBoundNeg": int(config_file['GATE SPECIFICATION']['GateType1_LowerBoundNeg']),
        "UpperBoundPos": int(config_file['GATE SPECIFICATION']['GateType1_UpperBoundPos']),
        "UpperBoundNeg": int(config_file['GATE SPECIFICATION']['GateType1_UpperBoundNeg']),
        "UpperBoundOcc": int(config_file['GATE SPECIFICATION']['GateType1_UpperBoundOcc']),
    }

    GateType2 = {
        "LowerBoundPos": int(config_file['GATE SPECIFICATION']['GateType2_LowerBoundPos']),
        "LowerBoundNeg": int(config_file['GATE SPECIFICATION']['GateType2_LowerBoundNeg']),
        "UpperBoundPos": int(config_file['GATE SPECIFICATION']['GateType2_UpperBoundPos']),
        "UpperBoundNeg": int(config_file['GATE SPECIFICATION']['GateType2_UpperBoundNeg']),
        "UpperBoundOcc": int(config_file['GATE SPECIFICATION']['GateType2_UpperBoundOcc']),
    }

    GateTypes = [GateType1, GateType2]

    instance, program = \
        classifier.csv2asp(fname_csv=FnameCSV,
                           fname_asp=FnameASP,
                           lower_bound_inputs=int(config_file['CLASSIFIER CONSTRAINTS']['LowerBoundInputs']),
                           upper_bound_inputs=int(config_file['CLASSIFIER CONSTRAINTS']['UpperBoundInputs']),
                           lower_bound_gates=int(config_file['CLASSIFIER CONSTRAINTS']['LowerBoundGates']),
                           upper_bound_gates=int(config_file['CLASSIFIER CONSTRAINTS']['UpperBoundGates']),
                           gate_types=GateTypes,
                           efficiency_constraint=config_file.getboolean('OPTIONAL', 'EfficiencyConstraint'),
                           optimization_strategy=int(config_file['OPTIMIZATION']['OptimizationStrategy']),
                           break_symmetries=config_file.getboolean('OPTIONAL', 'BreakSymmetries'),
                           silent=config_file.getboolean('OPTIONAL', 'Silent'),
                           uniqueness_constraint=config_file.getboolean('CLASSIFIER CONSTRAINTS', 'UniquenessConstraint'),
                           boolean_function_form=int(config_file['CLASSIFIER CONSTRAINTS']['BooleanFunctionForm']),
                           perfect_classifier=config_file.getboolean('ERROR CONSTRAINTS', 'PerfectClassifier'),
                           add_bounds_on_errors=config_file.getboolean('ERROR CONSTRAINTS', 'AddBoundsOnErrors'),
                           upper_bound_false_pos=int(config_file['ERROR CONSTRAINTS']['UpperBoundFalsePos']),
                           upper_bound_false_neg=int(config_file['ERROR CONSTRAINTS']['UpperBoundFalseNeg']))

    instance = "\n".join(instance)
    program = "\n".join(program)

    return instance, program

