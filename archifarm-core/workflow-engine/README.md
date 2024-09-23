# Workflow Engine

This component is responsible for performing a set of architecture farming experiment. It takes an **Experiment Matrix** in form of a CSV file with n rows and m columns as input. Each row provides the specification of one experiment. Each column provides the value of one parameter. The workflow engine carries out experiments according to the experiment matrix to retrieve the experiment results necessary for carrying out data analysis. 

The workflow engine is implemented using [n8n](https://n8n.io). This repository contains a docker compose to start n8n and a workflow template.

## General experiment workflow

For each experiment in an experiment matrix

1. Verify that infrastructure is operational
2. Confirm and Reset context parameters if necessary
3. Set context parameters according to the experiment specification
4. Set architecture parameters
5. Start the experiment
6. Review, gather, and store results
7. Reset context parameters
