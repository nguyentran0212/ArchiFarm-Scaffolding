from typing import Any, Dict

import tomli
from rich.console import Console
from rich.panel import Panel

from src.inputs import (
    process_field,  # Add this import
)

console = Console()


def generate_input_form(config_path: str) -> Dict[str, Any]:
    """Generate a dynamic input form with enhanced formatting."""
    with open(config_path, 'rb') as file:
        config = tomli.load(file)

    metadata = config.get('metadata', {})
    form_config = config.get('parameters', {})

    console.print(
        Panel(
            f"[bold green]{metadata.get('title', 'Dynamic Input Form')}[/bold green]",
            expand=False,
        )
    )
    if 'description' in metadata:
        console.print(f"[italic]{metadata['description']}[/italic]")
    if 'version' in metadata:
        console.print(f"Version: {metadata['version']}")
    if 'timestamp' in metadata:
        console.print(f"Last updated: {metadata['timestamp']}")
    for key, value in metadata.items():
        if key not in ['title', 'description', 'version', 'timestamp']:
            console.print(f"{key}: {value}")
    console.print("─" * 40)  # Separator

    result = {'metadata': metadata, 'parameters': {}}
    for key, field_config in form_config.items():
        if isinstance(field_config, str):
            value = process_field(
                {key: field_config}, result['parameters'], is_top_level=True
            )
        else:
            value = process_field(field_config, result['parameters'], is_top_level=True)
        if value is not None:
            result['parameters'][key] = value
        console.print("─" * 40)  # Separator between fields

    console.print(Panel("[bold green]Form Completed[/bold green]", expand=False))

    return result
