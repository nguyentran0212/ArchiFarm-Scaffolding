import json
import os
from enum import Enum, auto
from io import open
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.theme import Theme

console = Console(theme=Theme({"prompt": "cyan", "input": "green"}))


class FIELD_TYPE(Enum):
    STRING = auto()
    INTEGER = auto()
    PATH = auto()
    BOOLEAN = auto()
    KEY_VALUE = auto()
    PREDEFINED_KEY_VALUE = auto()
    LIST = auto()
    NESTED_KEY_VALUE = auto()
    SELECT = auto()
    JSON_FILE = auto()  # New field type for JSON file input
    DYNAMIC_LIST = auto()


def print_section(title: str):
    """Print a section title with a decorative border."""
    console.print(
        Panel(f"[bold cyan]{title}[/bold cyan]", expand=False, border_style="blue")
    )


def get_string_input(prompt: str, default: Optional[str] = None) -> str | None:
    """Get a single line string input from the user with enhanced formatting."""
    return Prompt.ask(f"{prompt}", default=default, console=console)


def get_selection(
    prompt: str, options: List[Any], default: Optional[int] = None
) -> Any:
    """Get a selection from a list of options with enhanced formatting."""
    table = Table(show_header=False, box=None)
    for i, option in enumerate(options, start=1):
        table.add_row(f"[cyan]{i}.[/cyan]", str(option))
    console.print(table)

    if default is not None:
        prompt += f" [dim](default: {default})[/dim]"

    while True:
        choice = Prompt.ask(
            f"{prompt}", default=str(default) if default else None, console=console
        )
        try:
            choice = int(choice) if choice is not None else 0
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except ValueError:
            pass
        console.print("[red]Invalid selection. Please try again.[/red]")


def get_boolean_input(prompt: str, default: Optional[bool] = None) -> bool:
    """Get a yes/no answer from the user with enhanced formatting."""
    return Confirm.ask(f"{prompt}", default=default, console=console) or False


def get_path_input(
    prompt: str,
    default: Optional[str] = None,
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
) -> str | None:
    """Get a file or directory path input from the user with enhanced formatting."""
    while True:
        path = Prompt.ask(f"{prompt}", default=default, console=console)
        if path is None:
            return None
        path_obj = Path(path)
        if exists and not path_obj.exists():
            console.print("[red]Path does not exist. Please try again.[/red]")
            continue
        if not file_okay and path_obj.is_file():
            console.print(
                "[red]Files are not allowed. Please enter a directory path.[/red]"
            )
            continue
        if not dir_okay and path_obj.is_dir():
            console.print(
                "[red]Directories are not allowed. Please enter a file path.[/red]"
            )
            continue
        if writable and not os.access(path, os.W_OK):
            console.print("[red]Path is not writable. Please try again.[/red]")
            continue
        if readable and not os.access(path, os.R_OK):
            console.print("[red]Path is not readable. Please try again.[/red]")
            continue
        return path


def get_integer_input(
    prompt: str,
    default: Optional[int] = None,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    """Get an integer input from the user with enhanced formatting."""
    while True:
        try:
            value = int(
                Prompt.ask(
                    f"{prompt}",
                    default=str(default) if default is not None else None,
                    console=console,
                )
                or 0
            )
            if (min_value is None or value >= min_value) and (
                max_value is None or value <= max_value
            ):
                return value
            console.print(
                f"[red]Value must be between {min_value} and {max_value}. Please try again.[/red]"
            )
        except ValueError:
            console.print("[red]Invalid input. Please enter an integer.[/red]")


def get_key_value_list(
    prompt: str,
) -> Dict[str, str]:
    """Get a list of key-value pairs from the user."""
    console.print(f"[cyan]{prompt}[/cyan]")
    key_value_dict = {}
    while True:
        key = get_string_input("Enter key")
        value = get_string_input("Enter value")
        key_value_dict[key] = value

        if not get_boolean_input(
            "Do you want to add another key-value pair?", default=False
        ):
            break

    return key_value_dict


def get_predefined_key_values(
    keys: List[str], prompts: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    """Get values for a predefined set of keys from the user."""
    key_value_dict = {}
    for key in keys:
        prompt = prompts.get(key, key) if prompts else key
        value = get_string_input(prompt)
        key_value_dict[key] = value

    return key_value_dict


def get_list_input(
    prompt: str,
    default: Optional[List[Any]] = None,
    example: str = "item1,item2,item3",
    select_from: Optional[List[str]] = None,
) -> List[str]:
    """
    Get a list of strings from the user, either by selection or comma-separated input.

    If select_from is provided, user selects from the given options.
    Otherwise, user inputs a comma-separated list.
    """
    if select_from:
        selected_items = []
        while True:
            item = get_selection(f"{prompt} (select one item at a time)", select_from)
            selected_items.append(item)
            if not get_boolean_input("Do you want to add another item?", default=False):
                break
        return selected_items
    else:
        default_str = ",".join(map(str, default)) if default else None
        hint = f"(e.g., {example})"
        full_prompt = f"{prompt} {hint}"

        while True:
            user_input = typer.prompt(full_prompt, default=default_str, type=str)

            # Validate the input
            if not user_input.strip():
                typer.echo("Input cannot be empty. Please try again.")
                continue

            if ',' not in user_input:
                typer.echo("Input must be a comma-separated list. Please try again.")
                continue

            items = [item.strip() for item in user_input.split(",")]
            if any(not item for item in items):
                typer.echo("Each item in the list must not be empty. Please try again.")
                continue

            return items


def get_json_file_input(prompt: str, default: Optional[str] = None) -> Dict[str, Any]:
    """Get JSON data from a local file."""
    while True:
        file_path = get_path_input(
            prompt,
            default=default,
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        )
        if file_path is None:
            return {}
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            return data
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON file. Please try again.[/red]")
        except IOError:
            console.print("[red]Error reading the file. Please try again.[/red]")


def get_dynamic_list_input(
    prompt: str, item_prompt: str, example: str = "4"
) -> List[str]:
    """Get a dynamic list of strings from the user."""
    while True:
        try:
            count = int(Prompt.ask(f"{prompt} (e.g., {example})", console=console))
            if count <= 0:
                console.print("[red]Please enter a positive number.[/red]")
                continue
            break
        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")

    items = []
    for i in range(count):
        item = Prompt.ask(item_prompt.format(index=i), console=console)
        items.append(item)

    return items


def get_dynamic_list_dict_input(
    prompt: str, item_config: Dict[str, Any], example: str = "3"
) -> List[Dict[str, Any]]:
    """Get a dynamic list of dictionaries from the user."""
    while True:
        try:
            count = int(Prompt.ask(f"{prompt} (e.g., {example})", console=console))
            if count <= 0:
                console.print("[red]Please enter a positive number.[/red]")
                continue
            break
        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")

    items = []
    for i in range(count):
        console.print(f"\n[cyan]Entering details for item {i + 1}:[/cyan]")
        item = {}
        for key, field_config in item_config.items():
            # logger.info(f"Getting nested key-value input for {key}, {field_config}")
            field_type = field_config.get('type', 'STRING').upper()
            field_prompt = field_config.get('prompt', f"Enter {key}")
            field_description = field_config.get('description', '')
            if field_description:
                console.print(f"[blue italic]{field_description}[/blue italic]")

            if field_type == 'STRING':
                item[key] = get_string_input(
                    field_prompt, default=field_config.get('default')
                )
            elif field_type == 'INTEGER':
                item[key] = get_integer_input(
                    field_prompt, default=field_config.get('default')
                )
            elif field_type == 'BOOLEAN':
                item[key] = get_boolean_input(
                    field_prompt, default=field_config.get('default')
                )
            elif field_type == 'DYNAMIC_LIST':
                item[key] = get_dynamic_list_input(
                    field_prompt,
                    field_config.get('item_prompt', 'Enter item[{index}]'),
                    example=field_config.get('example', ''),
                )
            elif field_type == 'KEY_VALUE':
                item[key] = get_key_value_list(field_prompt)

            elif field_type == 'DYNAMIC_LIST[DICT]':
                item[key] = get_dynamic_list_dict_input(
                    field_prompt,
                    field_config.get('items', {}),
                    example=field_config.get('example', ''),
                )
            else:
                console.print(
                    f"[red]Unsupported field type: {field_type} in DYNAMIC_LIST[DICT] [/red]"
                )

        items.append(item)

    return items


def get_nested_key_value_input(
    field_config: Dict[str, Any], is_top_level: bool
) -> Dict[str, Any]:
    """Get nested key-value input from the user with enhanced formatting."""
    result = {}
    for key, nested_field_config in field_config.items():
        # logger.info(f"Getting nested key-value input for {key}, {nested_field_config}")
        if key not in ['type', 'prompt', 'description']:
            if isinstance(nested_field_config, str):
                value = process_field(
                    {key: nested_field_config}, result, is_top_level=False
                )
            else:
                value = process_field(nested_field_config, result, is_top_level=False)
            if value is not None:
                result[key] = value
    return result


def process_field(
    field_config: Dict[str, Any], result: Dict[str, Any], is_top_level: bool = True
) -> Any:
    """Process a single field based on its configuration with enhanced formatting."""
    if len(field_config) == 1:
        if 'description' in field_config:
            console.print("*" * 80)  # Separator between fields
            console.print(
                f"[blue italic]{field_config['description']}[/blue italic]",
                style="bold",
            )
            console.print("*" * 80)  # Separator between fields
            return None

    description = field_config.get('description', '')
    field_type = field_config.get('type', 'NESTED_KEY_VALUE').upper()
    if field_type == 'NESTED_KEY_VALUE':
        field_type = 'NESTED_KEY_VALUE'
    prompt = field_config.get('prompt', '')

    console.print()

    if description:
        if is_top_level and field_type == 'NESTED_KEY_VALUE':
            print_section(description)
        else:
            console.print(f"[blue italic]{description}[/blue italic]")

    if field_type == 'STRING':
        return get_string_input(prompt, default=field_config.get('default'))
    elif field_type == 'INTEGER':
        return get_integer_input(
            prompt,
            default=field_config.get('default'),
            min_value=field_config.get('min'),
            max_value=field_config.get('max'),
        )
    elif field_type == 'BOOLEAN':
        return get_boolean_input(prompt, default=field_config.get('default'))
    elif field_type == 'LIST':
        return get_list_input(
            prompt,
            default=field_config.get('default'),
            example=field_config.get('example', ''),
        )
    elif field_type == 'DYNAMIC_LIST':
        return get_dynamic_list_input(
            prompt,
            field_config.get('item_prompt', 'Enter item[{index}]'),
            example=field_config.get('example', ''),
        )
    elif field_type == 'DYNAMIC_LIST[DICT]':
        return get_dynamic_list_dict_input(
            prompt,
            field_config.get('items', {}),
            example=field_config.get('example', ''),
        )
    elif field_type == 'NESTED_KEY_VALUE':
        return get_nested_key_value_input(field_config, is_top_level)
    else:
        console.print(f"[red]Unsupported field type: {field_type}[/red]")
        return None
