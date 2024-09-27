import csv
import itertools
import json
from typing import Any, Dict, List

from loguru import logger


def load_json_config(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as f:
        return json.load(f)


def generate_value_combinations(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = []
    for key, value in params.items():
        if isinstance(value, dict):
            sub_combinations = generate_value_combinations(value)
            items.append([(key, comb) for comb in sub_combinations])
        elif isinstance(value, list):
            items.append([(key, item) for item in value])
        else:
            items.append([(key, value)])

    return [dict(combination) for combination in itertools.product(*items)]


def generate_permutation_table(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    arch_params = config['parameters']['architecture']
    context_params = config['parameters']['context']

    arch_combinations = generate_value_combinations(arch_params)
    context_combinations = generate_value_combinations(context_params)

    permutations = []
    for arch_comb in arch_combinations:
        for context_comb in context_combinations:
            permutations.append(
                {
                    "architecture": json.dumps(arch_comb),
                    "context": json.dumps(context_comb),
                }
            )

    return permutations


def export_to_csv(data: List[Dict[str, Any]], output_file: str):
    if not data:
        return

    fieldnames = ['index'] + list(data[0].keys())

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        for index, row in enumerate(data, start=1):
            row_with_index = {'index': index, **row}
            writer.writerow(row_with_index)


def export_permutation_table(config_file: str, output_csv: str):
    config = load_json_config(config_file)

    permutation_table = generate_permutation_table(config)
    export_to_csv(permutation_table, output_csv)
