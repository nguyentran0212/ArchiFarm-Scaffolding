"""
CLI tool code in here
"""

import json
import os
from datetime import datetime

import requests
import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Confirm
from rich.theme import Theme

from src.exports import export_permutation_table
from src.form_processor import generate_input_form

load_dotenv()

app = typer.Typer()

N8N_PROTOCOL = os.getenv("N8N_PROTOCOL")
N8N_SERVER = os.getenv("N8N_SERVER")
N8N_PORT = os.getenv("N8N_PORT")
N8N_HOOK_PATH = os.getenv("N8N_HOOK_PATH")
N8N_API_KEY = os.getenv("N8N_API_KEY")
N8N_EXPERIMENT_LOGS_ABSOLUTE_DIR = os.getenv("N8N_EXPERIMENT_LOGS_ABSOLUTE_DIR")

workflow_webhook_url = f"{N8N_PROTOCOL}://{N8N_SERVER}:{N8N_PORT}/{N8N_HOOK_PATH}"

console = Console(theme=Theme({"prompt": "cyan", "input": "green"}))


@app.command(name="create")
def create(
    config_path: str = typer.Option(
        "form_config.toml",
        "--config",
        "-c",
        help="Path to the configuration file",
        prompt=True,
    ),
):
    """Create experiment requests using a dynamic form"""
    form_results = generate_input_form(config_path)

    console.print("Experiment configuration:")
    for key, value in form_results.items():
        console.print(f"[cyan]{key}:[/cyan] {value}")

    confirm = Confirm.ask(
        "[bold]Do you want to create this experiment?[/bold]", console=console
    )
    if not confirm:
        console.print("[red]Operation cancelled.[/red]")
        return

    # Here you would implement the logic to create the experiment using form_results
    console.print("[green]Creating experiment...[/green]")
    # Generate JSON output file
    metadata = form_results.get('metadata', {})
    title = metadata.get('title', 'Dynamic_Input_Form').replace(' ', '_')
    version = metadata.get('version', '1.0')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{title}_{version}_{timestamp}.json"

    output_dir = "outputs"  # Ensure this directory exists
    os.makedirs(output_dir, exist_ok=True)
    json_output_file = os.path.join(output_dir, filename)
    with open(json_output_file, 'w') as f:
        json.dump(form_results, f, indent=2)

    permutation_table_file = f"{title}_permutation_table_{version}_{timestamp}.csv"
    permutation_table_output_file = os.path.join(output_dir, permutation_table_file)
    export_permutation_table(json_output_file, permutation_table_output_file)
    console.print(f"[green]Output saved to {filename}[/green]")
    console.print(f"[green]Permutation table saved to {permutation_table_file}[/green]")


@app.command(name="export-csv")
def export_csv(
    json_file: str = typer.Option(
        ...,
        "--json-file",
        "-j",
        help="Path to the existing JSON configuration file",
        prompt=True,
    ),
    output_file: str = typer.Option(
        ...,
        "--output-file",
        "-o",
        help="Path to save the permutation table CSV file",
        prompt=True,
    ),
):
    """Export permutation table from an existing JSON configuration file"""
    if not os.path.exists(json_file):
        console.print(f"[red]Error: JSON file '{json_file}' does not exist.[/red]")
        return

    try:
        export_permutation_table(json_file, output_file)
        console.print(f"[green]Permutation table exported to {output_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error exporting permutation table: {str(e)}[/red]")


@app.command(name="submit")
def submit(
    csv_file: str = typer.Option(
        None,
        "--csv-file",
        "-c",
        help="Path to the CSV file to submit",
        prompt=False,
    ),
    webhook_url: str = typer.Option(
        workflow_webhook_url,
        "--webhook-url",
        "-w",
        help="URL of the n8n local service webhook",
        prompt=True,
    ),
):
    """Submit the CSV file to an n8n local service webhook"""
    if csv_file is None or not os.path.exists(csv_file):
        output_dir = "outputs"  # Ensure this directory exists
        csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
        if csv_files:
            console.print(
                f"[yellow]CSV file not found. Read csv from {output_dir}, Select from the following list or enter a custom path:[/yellow]"
            )
            for i, file in enumerate(csv_files):
                console.print(f"[yellow]{i+1}. {file}[/yellow]")
            console.print(f"[yellow]{len(csv_files)+1}. Not in this list[/yellow]")

            selection = (
                int(
                    input(
                        "Enter the number of the CSV file to submit or select the last option for a custom path: "
                    )
                )
                - 1
            )
            if 0 <= selection < len(csv_files):
                csv_file = os.path.join(output_dir, csv_files[selection])
            elif selection == len(csv_files):
                csv_file = input("Enter the path of the CSV file to submit: ")
            else:
                console.print(f"[red]Invalid selection. Please try again.[/red]")
                return
        else:
            console.print(
                f"[red]Error: No CSV files found in the output directory.[/red]"
            )
            return

    try:
        with open(csv_file, 'r') as file:
            data = file.read()
        response = requests.post(
            webhook_url,
            data=data,
            headers={'Content-Type': 'text/plain; charset=utf-8'},
        )
        if response.status_code == 200:
            console.print(f"[green]CSV file submitted to {webhook_url}[/green]")
        else:
            console.print(f"[red]Error submitting CSV file: {response.text}[/red]")
    except Exception as e:
        console.print(f"[red]Error submitting CSV file: {str(e)}[/red]")
