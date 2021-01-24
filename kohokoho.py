import click
import random
import pandas as pd
from faker import Faker

fake = Faker('en')

class anon(object):
    def __init__(self, df):
        self.df = df

    def anon_name(self, col):
        unique = self.df[col].unique()
        map_dict = {_: fake.name() for _ in unique}
        self.df[col] = self.df[col].map(map_dict)

    def anon_id(self, col):
        unique = self.df[col].unique()
        map_dict = {_: fake.uuid4() for _ in unique}
        self.df[col] = self.df[col].map(map_dict)

    def anon_whole_num(self, col):
        X_std = (self.df[col] - self.df[col].min()) / (self.df[col].max() - self.df[col].min())
        X_scaled = (X_std * (10 - 1) + 1) 
        X_scaled_whole_randomized = (X_scaled * random.randint(1, 10)).astype(int)
        self.df[col] = X_scaled_whole_randomized


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
    click.echo('Columns info: '+str(df.info()))
    name_col = click.prompt('Enter column which stores names', type=str)
    koho_df.anon_name(name_col)
    
    id_col = click.prompt('Enter column which stores id', type=str)
    koho_df.anon_id(id_col)

    whole_col = click.prompt('Enter column which stores whole numbers', type=str)
    koho_df.anon_whole_num(whole_col)

    click.echo(koho_df.anon_df().head())
    

if __name__ == '__main__':
    cli()