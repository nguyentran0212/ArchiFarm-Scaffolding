# Experiment Management CLI

This component is responsible for interacting with user to help them write experiment matrix. It prompt users for list of context parameters and architecture parameters and use those information to construct experiment matrix CSV file (refer to workflow engine README.md or the paper for more details about experiment matrix CSV file). Based on the given matrix, the CLI tool use full factorial to create experiment matrix CSV file.

In the future, other strategy for generating CSV files from given parameters could be implemented by extending this tool.

## Implementation strategy

The CLI tool can accept a `config.toml` that list the types of parameters (e.g., in-cluster and cross-cluster bandwidth and latency, DLT platform type, DLT platform architecture). Based on the configuration, the tool can prompt user accordingly and generate experiment matrix (e.g., "what are in-cluster bandwidths to experiments (Array)?").


---


# How to install and run the cli tool

1. Install all the dependencies

```bash
pip install -r requirements.txt
```

2. Build the project

```bash
pyinstaller --onefile --noconsole --nocolor --name=experiment-cli src/main.py
```

3. Run the project

```bash
./dist/experiment-cli --config form_config.yml
```

4. For more information, run the project with the help flag

```bash
./dist/experiment-cli --help
```

---

# Form Configuration Guide

This README explains how to create a form for input using the `form_config.toml` file.

## Overview

The `form_config.toml` file defines the structure and properties of form fields. Each field is represented by a TOML key with nested properties.

## Field Types

- `STRING`: Text input
- `INTEGER`: Numeric input with optional min/max
- `ENUM`: Dropdown selection
- `PATH`: File or directory path input
- `BOOLEAN`: Yes/No checkbox
- `LIST`: Comma-separated list input
- `NESTED_KEY_VALUE`: Hierarchical key-value structure (default if not specified)

## Common Properties

- `type`: Specifies the field type (optional, defaults to NESTED_KEY_VALUE)
- `prompt`: User-facing question or instruction
- `description`: Detailed explanation of the field
- `default`: Default value (if applicable)
- `example`: Example input to guide users

## Example Usage

1. Define fields in `form_config.toml`
2. Parse the TOML file in your application
3. Generate form elements based on field types and properties
4. Validate user input against defined constraints
5. Process the collected data for your experiment or configuration

## Tips

- Use clear and concise prompts and descriptions
- Provide sensible defaults and examples where possible
- Utilize nested structures for complex data
- Remember that unspecified types default to NESTED_KEY_VALUE

For detailed implementation, refer to the `form_config.toml` file and your application's form generation logic.