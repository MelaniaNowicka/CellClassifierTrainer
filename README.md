# CellClassifierTrainer

CellClassifierTrainer allows to train boolean classifiers based on a feature expression profile. The tool was created to
classify cancerous and control healthy cells based on discretized miRNA differential expression profiles. Although,
CellClassifierTrainer may be applied to other binary classification problems based on discretized features.

CellClassifierTrainer employs [RnaCancerClassifier](https://github.com/hklarner/RnaCancerClassifier)
by [Becker et al.](https://www.frontiersin.org/articles/10.3389/fbioe.2018.00070/full) and automatizes the constraint
relaxation-based optimization as described in Becker et al.

## Input data format

First column (ID) must contain unique sample IDs , second (Annots) - the annotation of samples.
The following columns include discretized miRNA profiles (use ';' as delimiter).

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


## Requirements

CellClassifierTrainer has the following dependencies:

- Python 3.5
- scikit-learn
- clyngor (https://anaconda.org/conda-forge/clyngor)


## Installation

To download the CellClassifierTrainer from Github, do::

    $ git clone https://github.com/MelaniaNowicka/CellClassifierTrainer


## Running

To use CellClassifierTrainer, run::

    $ python -u run_trainer.py --train_data train_dataset.csv --constr asp_constr.csv --test_data test_dataset.csv --train_p 80 --train_n 80 --test_p 20 --test_n 20 --fp 5 --fn 5


Run exemplary training with a command::

    $ python -u run_trainer.py --train_data example_train.csv --constr asp_constr.csv --test_data example_test.csv --train_p 80 --train_n 80 --test_p 20 --test_n 20 --fp 2 --fn 2

Parameters description:

**- - train_data** - path to training data set (.csv, obligatory)

**- - constr** - path to ASP program constraints (.csv, explained in the next section, obligatory)

**- - test_data** - path to test data set (.csv, default None)

**- - train_p** - number of positive samples in training data set (int, obligatory)

**- - train_n** - number of negative samples in training data set (int, obligatory)

**- - test_p** - number of positive samples in test data set (int, default None)

**- - test_n** - number of negative samples in test data set (int, default None)

**- - min_fp** - lower bound on allowed false positive errors (int, default 0)

**- - min_fn** - lower bound on allowed false negative errors (int, default 0)

**- - max_fp** - upper bound on allowed false positive errors (int, default 0)

**- - max_fn** - upper bound on allowed false negative errors (int, default 0)

## ASP constraints

ASP constraints are included in constr.csv file. Explanation of particular constraints:
(to know more see [RnaCancerClassifier](https://github.com/hklarner/RnaCancerClassifier)
and [Becker et al.](https://www.frontiersin.org/articles/10.3389/fbioe.2018.00070/full)):

**LowerBoundInputs** - lower bound on number of inputs in classifier (int)

**UpperBoundInputs** - upper bound on number of inputs in classifier (int)

**LowerBoundGates** - lower bound on number of gates in classifier (int)

**UpperBoundGates** - upper bound on number of gates in classifier (int)

**EfficiencyConstraint** - if 1 ignore non-relevant features, otherwise 0

**BreakSymmetries** - if 1 part of symmetric solutions are removed, otherwise 0

**Silent** - if 1 print all information, otherwise 0

**UniquenessConstraint** - if 1 inputs should be unique across the classifier, irrespective of whether they are negated or not, otherwise 0

**OptimizationStrategy**
* 0 - no optimization
* 1 - minimize number of inputs then minimize number of gates
* 2 - minimize number of gates then minimize number of inputs
* 3 - minimize number of inputs
* 4 - minimize number of gates

**PerfectClassifier** - if 1 look for perfect classifiers (no errors allowed), otherwise 0

**AddBoundsOnErrors** - if 1 add bounds on errors, otherwise 0

**UpperBoundFalsePos** - upper bound on false positive errors (needed if PerfectClassifier=0 and AddBoundsOnErrors=0)

**UpperBoundFalseNeg** - upper bound on false negative errors (needed if PerfectClassifier=0 and AddBoundsOnErrors=0)

**GateTypeX_LowerBoundPos** - lower bound on positive inputs in gate type X (X - number of gate type (1, 2, 3...))

**GateTypeX_UpperBoundPos** - upper bound on positive input in gate type X

**GateTypeX_LowerBoundNeg** - lower bound on negative inputs in gate type X

**GateTypeX_UpperBoundNeg** - upper bound on negative input in gate type X

**GateTypeX_UpperBoundOcc** - upper bound on number of occurrences of gate type X

