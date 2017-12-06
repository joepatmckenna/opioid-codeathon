import pandas as pd
from sodapy import Socrata


# convert comma-separated list to python list
def string_list_to_list(string_list):
    l = string_list
    l = l.split(',')
    l = [li.strip() for li in l]
    return l


# load state metadata spreadsheet
state_metadata = pd.read_excel('./metadata.xlsx', sheetname='state')

# extract uids from API endpoints
uid = []
for endpoint in state_metadata['endpoints']:
    uid.append(endpoint.split('.')[-2].split('/')[-1])
state_metadata['uid'] = uid

# convert each entry in 'columns' and 'variables' column to list
# and create list of dicts that map column names to variable names
col_to_var = []
for i, (columns, variables) in state_metadata[['columns',
                                               'variables']].iterrows():
    columns = string_list_to_list(columns)
    variables = string_list_to_list(variables)
    state_metadata['columns'].iloc[i] = columns
    state_metadata['variables'].iloc[i] = variables
    col_to_var.append(dict(zip(columns, variables)))

# create sodapy client with proper credentials
client = Socrata(
    'hhs-opioid-codeathon.data.socrata.com',
    'r0hTo1hS9c0i2khglj7n1H8sn',
    username='joseph.mckenna@nih.gov',
    password='Abcd#1234')

# get datasets from socrata
state_datasets = []
for i, (uid, columns, nrows) in state_metadata[['uid', 'columns',
                                                'nrows']].iterrows():
    dataset = client.get(uid, select=','.join(columns), limit=nrows)
    state_datasets.append(dataset)

# convert datasets to pandas data frames
state_datasets = [pd.DataFrame.from_records(ds) for ds in state_datasets]

# relabel dataset columns to variable names
for i, ds in enumerate(state_datasets):
    state_datasets[i].columns = [col_to_var[i][c] for c in ds.columns]

#
# Local Unemployment dataset
#
state_fips, state = [], []
for i, (sf, s) in state_datasets[0][['state_fips', 'state']].iterrows():
    state_fips.append(sf)
    state.append(s)
state_datasets[0] = state_datasets[0][[
    'state_fips', 'year', 'unemployment_rate'
]]

# create state_fips lookup dict
state_fips_to_state = dict(zip(state_fips, state))
state_to_state_fips = dict(zip(state, state_fips))
state_fips_to_state['78'] = 'VI'
state_to_state_fips['VI'] = '78'
state_fips_to_state['60'] = 'AS'
state_to_state_fips['AS'] = '60'
state_fips_to_state['00'] = 'AE'
state_to_state_fips['AE'] = '00'
state_fips_to_state['69'] = 'MP'
state_to_state_fips['MP'] = '69'
state_fips_to_state['66'] = 'GU'
state_to_state_fips['GU'] = '66'
state_fips_to_state['99'] = 'ZZ'
state_to_state_fips['ZZ'] = '99'
state_fips_to_state['98'] = 'AA'
state_to_state_fips['AA'] = '98'

# extract year from year string
for i, year in state_datasets[0]['year'].iteritems():
    state_datasets[0]['year'].iloc[i] = year[:4]

#
# CDC Wonder Underlying Cause
#
state_datasets[1] = state_datasets[1][[
    'fips', 'year', 'primary_cause', 'deaths', 'population'
]]
for i, fips in state_datasets[1]['fips'].iteritems():
    state_datasets[1]['fips'].iloc[i] = fips[:2]

#
# Medicaire Part D Opioid Prescriber
#
fips = []
for _, state in state_datasets[2]['state'].iteritems():
    fips.append(state_to_state_fips[state])
state_datasets[2] = state_datasets[2][[
    'medicaire_opioid_claims', 'medicaire_claims'
]]
state_datasets[2]['year'] = 2013
state_datasets[2]['fips'] = fips
