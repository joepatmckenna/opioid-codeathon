import pandas as pd
from sodapy import Socrata


# convert comma-separated list to python list
def string_list_to_list(string_list):
    l = string_list
    l = l.split(',')
    l = [li.strip() for li in l]
    return l


# load indiana metadata spreadsheet
indiana_metadata = pd.read_excel('./metadata.xlsx', sheetname='Indiana')

# extract uids from API endpoints
uid = []
for endpoint in indiana_metadata['endpoints']:
    uid.append(endpoint.split('.')[-2].split('/')[-1])
indiana_metadata['uid'] = uid

# convert each entry in 'columns' and 'variables' column to list
# and create list of dicts that map column names to variable names
col_to_var = []
for i, (columns, variables) in indiana_metadata[['columns',
                                                 'variables']].iterrows():
    columns = string_list_to_list(columns)
    variables = string_list_to_list(variables)
    indiana_metadata['columns'].iloc[i] = columns
    indiana_metadata['variables'].iloc[i] = variables
    col_to_var.append(dict(zip(columns, variables)))

# create sodapy client with proper credentials
client = Socrata(
    'hhs-opioid-codeathon.data.socrata.com',
    'r0hTo1hS9c0i2khglj7n1H8sn',
    username='joseph.mckenna@nih.gov',
    password='Abcd#1234')

# store indiana fips/counties
uid = indiana_metadata['uid'].iloc[0]
dataset = client.get(uid, select='GEOG_ID, GEOG_NAME')
dataset = pd.DataFrame.from_records(dataset)
indiana_fips = dataset['GEOG_ID'].values
indiana_counties = dataset['GEOG_NAME'].values
indiana_fips_to_county = dict(zip(indiana_fips, indiana_counties))

# get indiana datasets from socrata
indiana_datasets = []
for i, (uid, columns) in indiana_metadata[['uid', 'columns']].iterrows():
    dataset = client.get(uid, select=','.join(columns))
    indiana_datasets.append(dataset)

# convert datasets to pandas data frames
indiana_datasets = [pd.DataFrame.from_records(ds) for ds in indiana_datasets]

# relabel dataset columns to variable names
for i, ds in enumerate(indiana_datasets):
    indiana_datasets[i].columns = [col_to_var[i][c] for c in ds.columns]

# aggregate entries to count naloxone providers
naloxone_providers = indiana_datasets[-1]['fips'].value_counts(
    sort=False).sort_index()
data = np.stack(
    (naloxone_providers.index.values, naloxone_providers.values), axis=1)
indiana_datasets[-1] = pd.DataFrame(
    data=data, columns=['fips', 'naloxone_providers'])
indiana_datasets[-1]['year'] = 2017

# concatenate datasets
indiana_data = pd.concat(indiana_datasets)

# convert data type
indiana_data = indiana_data.apply(pd.to_numeric)
indiana_data['year'] = indiana_data['year'].astype('string')
indiana_data['fips'] = indiana_data['fips'].astype('string')

# group datasets then flatten
indiana_data = indiana_data.groupby(['year', 'fips']).sum()
indiana_data.reset_index(inplace=True)

county = []
for i, fips in indiana_data['fips'].iteritems():
    county.append(indiana_fips_to_county[fips])
indiana_data['county'] = county

indiana_data.set_index('year', inplace=True)

# write to file
indiana_data.to_csv('./indiana.csv')
