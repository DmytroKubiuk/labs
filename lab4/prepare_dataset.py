import pandas as pd
import numpy as np

red_df = pd.read_csv('wine+quality/winequality-red.csv', sep=';')
white_df = pd.read_csv('wine+quality/winequality-white.csv', sep=';')

red_df['type'] = 'red'
white_df['type'] = 'white'

combined_df = pd.concat([red_df, white_df], ignore_index=True)

columns = ['chlorides', 'sulphates', 'free sulfur dioxide']
for column in columns:
    combined_df.loc[combined_df.sample(frac=0.1).index, column] = np.nan

print(combined_df.isnull().sum())

combined_df.to_csv('wine+quality/winequality.csv', index=False)
