import click
from .converter_manager import ConverterManager

manager = ConverterManager()

@click.command()
@click.option('--input', required=True, help='Input data file')
@click.option('--output', required=True, help='Output data file')
@click.option('--type', required=True, type=click.Choice(['tes-to-wrroc', 'wes-to-wrroc', 'wrroc-to-tes', 'wrroc-to-wes']), help='Conversion type')
def cli(input, output, type):
    with open(input, 'r') as infile:
        data = infile.read()

    if type == 'tes-to-wrroc':
        result = manager.convert_tes_to_wrroc(data)
    elif type == 'wes-to-wrroc':
        result = manager.convert_wes_to_wrroc(data)
    elif type == 'wrroc-to-tes':
        result = manager.convert_wrroc_to_tes(data)
    elif type == 'wrroc-to-wes':
        result = manager.convert_wrroc_to_wes(data)

    with open(output, 'w') as outfile:
        outfile.write(result)

if __name__ == '__main__':
    cli()
