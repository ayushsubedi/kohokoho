import click
import random
import pandas as pd
from faker import Faker

fake = Faker('en')


class anon(object):
    def __init__(self, df):
        self.original = df.copy()
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

    def anon_email(self, name_col, email_col):
        if name_col == '':
            unique = self.df[email_col].unique()
            map_dict = {_: fake.email() for _ in unique}
            self.df[email_col] = self.df[email_col].map(map_dict)
        else:
            self.df[email_col] = (
                self.df[name_col].str.replace(
                    '\s+', '.') + '@fakeemail.com').str.lower()

    def anon_df(self):
        return self.df

    def _df(self):
        return self.original


@click.command()
@click.option(
    '--csv',
    prompt='Enter location of CSV',
    help='Enter a valid filepath or buffer')
def cli(csv):
    df = pd.read_csv(csv)
    koho_df = anon(df)
    click.echo('Columns info: '+str(df.info()))
    # name
    name_col = click.prompt(
        'Enter column/s which stores names, each column separated by a comma',
        type=str,
        default='')
    if (name_col != ''):
        for col in name_col.split(","):
            koho_df.anon_name(col.strip())
    # id
    id_col = click.prompt(
        'Enter column/s which stores id, each column separated by a comma',
        type=str,
        default='')
    if (id_col != ''):
        for col in id_col.split(","):
            koho_df.anon_id(col.strip())
    # continuous values
    continuous_col = click.prompt(
        'Enter column/s which stores continuous numbers, each column separated by a comma',
        type=str,
        default='')
    if (continuous_col != ''):
        for col in continuous_col.split(","):
            koho_df.anon_continuous_num(col)
    # discrete_col
    discrete_col = click.prompt(
        'Enter column/s which stores discrete numbers, each column separated by a comma',
        type=str,
        default='')
    if (discrete_col != ''):
        for col in discrete_col.split(","):
            koho_df.anon_discrete_num(col)
    # category
    category_col = click.prompt(
        'Enter column/s which stores categorical values, each column separated by a comma',
        type=str,
        default='')
    if (category_col != ''):
        for col in category_col.split(","):
            koho_df.anon_category(col)
    # date
    date_col = click.prompt(
        'Enter column which stores dates, each column separated by a comma',
        type=str,
        default='')
    if (date_col != ''):
        for col in date_col.split(","):
            koho_df.anon_date(date_col)
    # email
    email_col = click.prompt(
        'Enter column which stores email, each column separated by a comma',
        type=str,
        default='')
    if (email_col != ''):
        for col in email_col.split(","):
            koho_df.anon_email(name_col, email_col)
    # original dataset
    click.echo('Original dataset')
    click.echo(koho_df._df().head(10))
    # final dataset
    click.echo('Kohoko dataset')
    click.echo(koho_df.anon_df().head(10))


if __name__ == '__main__':
    cli()
