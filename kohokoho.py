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

    def anon_discrete_num(self, col):
        X_std = (self.df[col] - self.df[col].min()) / (
            self.df[col].max() - self.df[col].min())
        X_scaled = (X_std * (10 - 1) + 1)
        X_scaled_randomized = (X_scaled * random.randint(1, 10)).astype(int)
        self.df[col] = X_scaled_randomized

    def anon_continuous_num(self, col):
        X_std = (self.df[col] - self.df[col].min()) / (
            self.df[col].max() - self.df[col].min())
        X_scaled = (X_std * (10 - 1) + 1)
        X_scaled_randomized = round(X_scaled * random.randint(1, 10), 3)
        self.df[col] = X_scaled_randomized

    def anon_category(self, col):
        unique = self.df[col].unique()
        rand_ = random.randint(0, 1000)
        map_dict = {
            category:  "Category_" + str(rand_) + " " + str(i)
            for i, category in enumerate(unique)
        }
        self.df[col] = self.df[col].map(map_dict)

    def anon_date(self, col):
        self.df[col] = pd.to_datetime(
            self.df[col], infer_datetime_format=True)
        start_date = self.df[col].min()
        end_date = self.df[col].max()
        map_list = [fake.date_between(
            start_date=start_date,
            end_date=end_date) for i in range(self.df.shape[0])]
        self.df[col] = map_list

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
    continuous_col = click.prompt(
        'Enter column which stores continuous numbers', type=str)
    koho_df.anon_continuous_num(continuous_col)
    discrete_col = click.prompt(
        'Enter column which stores discrete numbers', type=str)
    koho_df.anon_discrete_num(discrete_col)
    category_col = click.prompt(
        'Enter column which stores categorical values', type=str)
    koho_df.anon_category(category_col)
    date_col = click.prompt(
        'Enter column which stores dates', type=str)
    koho_df.anon_date(date_col)
    click.echo(koho_df.anon_df().head())


if __name__ == '__main__':
    cli()
