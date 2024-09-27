# ArchiFarm: Exploring Architectural Design Space with Data Farming

## Overview

ArchiFarm is a comprehensive framework designed to aid software architects in exploring and evaluating the architectural design space using the technique of Data Farming (DF). It leverages rapid prototyping, high-performance computing, and statistical analysis to generate the necessary data that informs architectural decision-making processes.

## Key Concepts

### Architectural Design Space
ArchiFarm conceptualizes the design process of software architecture as a navigation through a multi-dimensional vector space. Each dimension represents a design decision, and each value along a dimension signifies a design option. Architects aim to find optimal paths through this space that push the architecture toward desirable Quality Attributes (QAs) reflecting project requirements.

### Data Farming
Data Farming is an interdisciplinary approach that uses deliberate data generation via simulation models and prototypes. By running numerous experiments across a parameter space, DF helps study the impact of design decisions and contextual factors on a system's architecture.

## Main Components

### Architecture Farming Process
An iterative and collaborative process that maps phases of architecture design decision-making onto the DF loop-of-loops model:
1. **Rapid Scenario Prototyping**: Expands vague QA requirements into testable QA scenarios.
2. **Model Development**: Constructs prototypes reflecting design decisions to be evaluated.
3. **Experiment Design**: Defines parameter values and prunes the parameter space to keep experiments computationally feasible.
4. **Experiment Execution**: Runs experiments using the defined matrix and gathers data.
5. **Data Analysis and Visualization**: Applies statistical analysis and visualization to derive insights.

### Distillations
These are simulation models or prototypes containing tunable parameters and measurement tools. Distillations enable the evaluation of various architecture decision options and contextual factors.

### ArchiFarm Instances
Software suite responsible for conducting experiments, interfacing with testbed infrastructures, managing workflows, and logging experiment data.

## Contributions

1. Conceptualization of leveraging DF for software architecture design exploration and evaluation.
2. Definition of a collaborative and iterative architecture farming process.
3. Development of a model for creating distillations of architectural design decisions.
4. Provision of a reference architecture for implementing an ArchiFarm instance.
5. Case study demonstrating the feasibility of ArchiFarm in supporting design decisions.

## Use Cases

ArchiFarm is particularly useful in:
- Technology selection decisions.
- System configuration decisions.
- Evaluating and comparing design options under varying contextual factors.

# How to run the whole stack

1. Run `start.sh` to start all the services in docker
2. Go to `archifarm-core/experiment-management-cli` and follow the instructions in the README.md to run the experiment management cli
3. Run `stop.sh` to stop all the services in docker

# Services
All services are dockerized and run in docker compose. You can find the docker compose file inside each service folder.

# Docker Services
Docker Containers and Port Mappings
grafana                               3333->3000/tcp  3333->3000/tcp
prometheus                            9090->9090/tcp  9090->9090/tcp
cadvisor                              8080->8080/tcp  8080->8080/tcp
workflow-engine-n8n-1                 5678->5678/tcp  5678->5678/tcp
workflow-engine-postgres-1            5432/tcp
archifarm-prototyping-tools-api-1     8002->8002/tcp  8002->8002/tcp
archifarm-context-controllers-api-1   8001->8001/tcp  8001->8001/tcp
mongo                                 27017->27017/tcp  27017->27017/tcp
