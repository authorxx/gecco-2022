# GECCO2022: Evolutionary-based Automated Testing for GraphQL APIs

In this package, we provide necessary information for replicating the experiment in the paper. We provide:

## Black-Box experiments

- jar: runnable jar for EvoMaster.

- exp.py: a python script to build tools and all the case studies

- results: contains compressed generated data

- : contains all the automatically generated files including logs, reports, scripts and tests. 

- analyze.R: an R script to analyze results and generate table and figures in the paper.

- EvoMaster: the tool used in the paper.

- EMB: contains the APIs used for white-box experiments in the paper

### Quick build and run:

Step 1. In this repo, we provide a python script.

Go to the root, run

`python exp.py no 1000 gql 1 30 100000 1 4`

Step 2. After the execution is done, you will see a folder named gql. Go to gql and run:

`./runall.sh`

Step 3. After the execution is done, you will see repositories named:

- logs: containing all the generated logs,

- reports: containing all the generated statistics,

- scripts: containing all the generated scripts,

- tests: containing the automatically generated tests for the APIS presented in the paper.
