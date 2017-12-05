import pandas as pd

indiana_data = pd.read_csv('./indiana.csv', index_col=0)

years = indiana_data.index.unique()
print indiana_data.loc[years[0]].head()
