# CellClassifierTrainer

CellClassifierTrainer allows to train boolean classifiers based on a feature expression profile. The tool was created to
classify cancerous and control healthy cells based on discretized miRNA differential expression profiles. Although,
CellClassifierTrainer may be applied to other binary classification problems based on discretized features.

CellClassifierTrainer employs [RnaCancerClassifier](https://github.com/hklarner/RnaCancerClassifier)
by [Becker et al.](https://www.frontiersin.org/articles/10.3389/fbioe.2018.00070/full) and automatizes the constraint
relaxation-based optimization as described in Becker et al.

## Input data format

First column (ID) must contain unique sample IDs , second (Annots) - the annotation of samples.
The following columns include discretized miRNA profiles (use ';' as delimiter). Note, ASP does 
not parse characters such as '-', ':', etc. Use only letters and numbers in the header. 

| ID | Annots | miR1 | miR2 |
| -- | ------ | ---- | ---- |
| 1 | 0 | 1 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 1 | 0 | 1 |


## Output

CellClassifierTrainer creates an ASP program (.asp) and prints a log (exemplary log: example.log).

Log sections:

**RNA CANCER CLASSIFIER OUTPUT** - includes output information returned by RnaCancerClassifier

**TRAINING CLASSIFIERS** - shows progress in classifier training

**FINDING BEST SOLUTIONS** - filters best solutions according to the total number of errors

**FILTERING ACCORDING TO SIZE** - filters best solutions according to the size (total number of inputs)

**REMOVING SYMMETRIC SOLUTIONS** - filters symmetric solutions (copies of identical solutions differing only in 
the order of inputs and gates)

**TESTING CLASSIFIERS** - evaluates best classifier's performance on test data set including feature frequency analysis

**AVERAGE RESULTS** - average results for best classifiers

Classifier format:

*gate_input(1,positive,g34) gate_input(1,positive,g4) gate_input(2,negative,g102)**

Each input is described by *gate_input(gate_id,sign,feature_id)*, which translates to (g34 OR g4) AND g102.

## Requirements

CellClassifierTrainer has the following dependencies:

- Python 3.5 (required to run clyngor)
- scikit-learn
- clyngor (https://anaconda.org/conda-forge/clyngor)


## Installation

To download the CellClassifierTrainer from Github, do::

    $ git clone https://github.com/MelaniaNowicka/CellClassifierTrainer


## Running

To use CellClassifierTrainer, run::

    $ python -u run_trainer.py --train_data train_dataset.csv --constr asp_constr.ini --test_data test_dataset.csv 
    --train_p 80 --train_n 80 --test_p 20 --test_n 20 --min_fp 0 --min_fn 0 --max_fp 5 --max_fn 5


Run exemplary training with a command::

    $ python -u run_trainer.py --train_data example_train.csv --constr asp_constr.ini --test_data example_test.csv 
    --train_p 80 --train_n 80 --test_p 20 --test_n 20 --fp 2 --fn 2

Parameters description:

***-- train_data*** - path to training data set (.csv, obligatory)

***-- constr*** - path to ASP program constraints (.csv, explained in the next section, obligatory)

***-- test_data*** - path to test data set (.csv, default None)

***-- train_p*** - number of positive samples in training data set (int, obligatory)

***-- train_n*** - number of negative samples in training data set (int, obligatory)

***-- test_p*** - number of positive samples in test data set (int, default None)

***-- test_n*** - number of negative samples in test data set (int, default None)

***-- min_fp*** - lower bound on allowed false positive errors (int, default 0)

***-- min_fn*** - lower bound on allowed false negative errors (int, default 0)

***-- max_fp*** - upper bound on allowed false positive errors (int, default 0)

***-- max_fn*** - upper bound on allowed false negative errors (int, default 0)

## ASP constraints

ASP constraints are included in constr.csv file. Explanation of particular constraints:
(to know more see [RnaCancerClassifier](https://github.com/hklarner/RnaCancerClassifier)
and [Becker et al.](https://www.frontiersin.org/articles/10.3389/fbioe.2018.00070/full)):

#LowerBoundInputs - lower bound on number of inputs in classifier
#UpperBoundInputs - upper bound on number of inputs in classifier
#LowerBoundGates - lower bound on number of gates in classifier
#UpperBoundGates - upper bound on number of gates in classifier
#BooleanFunctionForm - 0: Conjunctive Normal Form (CNF), 1: Disjunctive Normal Form (DNF)
#UniquenessConstraint - if True inputs should be unique across the classifier, irrespective of whether they are negated or not
[CLASSIFIER CONSTRAINTS]

LowerBoundInputs = 1  
UpperBoundInputs = 10  
LowerBoundGates = 1
UpperBoundGates = 6
BooleanFunctionForm = 0
UniquenessConstraint = False

#Gate type specification 
#Lower and upper bounds on positive and negative inputs in each gate
[GATE SPECIFICATION]
GateType1_LowerBoundPos = 0
GateType1_UpperBoundPos = 3
GateType1_LowerBoundNeg = 0
GateType1_UpperBoundNeg = 0
GateType1_UpperBoundOcc = 2
GateType2_LowerBoundPos = 0
GateType2_UpperBoundPos = 0
GateType2_LowerBoundNeg = 0
GateType2_UpperBoundNeg = 1
GateType2_UpperBoundOcc = 4

#OptimizationStrategy
#0: no optimization
#1: minimize number of inputs then minimize number of gates
#2: minimize number of gates then minimize number of inputs
#3: minimize number of inputs
#4: minimize number of gates
[OPTIMIZATION]
OptimizationStrategy = 1

#EfficiencyConstraint - if True ignore non-relevant features
#BreakSymmetries - if True part of symmetric solutions are removed
#Silent - printing option
[OPTIONAL]
EfficiencyConstraint = False
BreakSymmetries = False
Silent = False

#PerfectClassifier - if True upper bound on false positive and negative errors are 0
#AddBoundsOnErrors - if True add bounds on errors
#UpperBoundFalsePos - upper bound on false positive errors (needed if PerfectClassifier=False)
#UpperBoundFalseNeg - upper bound on false negative errors (needed if PerfectClassifier=False)
[ERROR CONSTRAINTS]
PerfectClassifier = False
AddBoundsOnErrors = False
UpperBoundFalsePos = 0
UpperBoundFalseNeg = 0


