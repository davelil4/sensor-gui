import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

df.to_csv('gapminder_unfiltered.csv', index=False)