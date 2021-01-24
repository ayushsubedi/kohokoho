import click
import pandas as pd


@click.command()
@click.option(
    '--csv',
    prompt='Enter location of CSV',
    help='Enter a valid filepath or buffer')
def cli(csv):
    try:
        df = pd.read_csv(csv)
    except Exception as e:
        click.echo('Error parsing csv file' + str(e))
    else:
        click.echo(df.head())


if __name__ == '__main__':
    cli()