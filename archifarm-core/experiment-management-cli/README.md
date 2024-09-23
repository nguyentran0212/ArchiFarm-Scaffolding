# Experiment Management CLI

This component is responsible for interacting with user to help them write experiment matrix. It prompt users for list of context parameters and architecture parameters and use those information to construct experiment matrix CSV file (refer to workflow engine README.md or the paper for more details about experiment matrix CSV file). Based on the given matrix, the CLI tool use full factorial to create experiment matrix CSV file. 

In the future, other strategy for generating CSV files from given parameters could be implemented by extending this tool. 

## Implementation strategy

The CLI tool can accept a `config.toml` that list the types of parameters (e.g., in-cluster and cross-cluster bandwidth and latency, DLT platform type, DLT platform architecture). Based on the configuration, the tool can prompt user accordingly and generate experiment matrix (e.g., "what are in-cluster bandwidths to experiments (Array)?").
