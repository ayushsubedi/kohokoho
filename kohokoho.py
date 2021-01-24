import click
import pandas as pd
from faker import Faker

fake = Faker('en')

class anon(object):
    def __init__(self, df):
        self.df = df

    def anon_name(self, name_column):
        unique_names = self.df[name_column].unique()
        name_dict = {name: fake.name() for name in unique_names}
        self.df[name_column] = self.df[name_column].map(name_dict)

    def anon_df(self):
        return self.df


@click.command()
@click.option(
    '--csv',
    prompt='Enter location of CSV',
    help='Enter a valid filepath or buffer')
def cli(csv):
    df = pd.read_csv(csv)
    koho_df = anon(df)
    click.echo('Column names: '+str(list(df)))
    name_col = click.prompt('Enter column which stores names:', type=str)
    koho_df.anon_name(name_col)
    click.echo(koho_df.anon_df().head())
    
    

if __name__ == '__main__':
    cli()