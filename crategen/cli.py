import json
import click
from crategen.converter_manager import ConverterManager

@click.command()
@click.option('--input', 'input_file', type=click.Path(exists=True), required=True, help='Path to the input file.')
@click.option('--output', 'output_file', type=click.Path(), required=True, help='Path to the output file.')
@click.option('--conversion-type', 'conversion_type', type=click.Choice(['tes_to_wrroc', 'wes_to_wrroc']), required=True, help='Type of conversion.')
def cli(input_file, output_file, conversion_type):
    with open(input_file, 'r') as f:
        data = json.load(f)

    manager = ConverterManager()

    if conversion_type == 'tes_to_wrroc':
        result = manager.convert_tes_to_wrroc(data)
    elif conversion_type == 'wes_to_wrroc':
        result = manager.convert_wes_to_wrroc(data)

    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__':
    cli()
