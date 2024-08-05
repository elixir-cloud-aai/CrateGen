import click
import json
from crategen.converter_manager import ConverterManager

@click.command()
@click.option('--input', prompt='Input file', help='Path to the input JSON file.')
@click.option('--output', prompt='Output file', help='Path to the output JSON file.')
@click.option('--conversion-type', prompt='Conversion type', type=click.Choice(['tes-to-wrroc', 'wes-to-wrroc', 'wrroc-to-tes', 'wrroc-to-wes']), help='Type of conversion to perform.')
def cli(input, output, conversion_type):
    """
    Command Line Interface for converting TES/WES to WRROC and vice versa.
    """
    manager = ConverterManager()

    # Load input data from JSON file
    with open(input, 'r') as input_file:
        data = json.load(input_file)

    # Perform the conversion based on the specified type
    if conversion_type == 'tes-to-wrroc':
        result = manager.convert_tes_to_wrroc(data)
    elif conversion_type == 'wes-to-wrroc':
        result = manager.convert_wes_to_wrroc(data)
    elif conversion_type == 'wrroc-to-tes':
        result = manager.convert_wrroc_to_tes(data)
    elif conversion_type == 'wrroc-to-wes':
        result = manager.convert_wrroc_to_wes(data)
    
    # Save the result to the output JSON file
    with open(output, 'w') as output_file:
        json.dump(result, output_file, indent=4)

if __name__ == '__main__':
    cli()
