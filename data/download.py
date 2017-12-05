import pandas as pd
from sodapy import Socrata
import string

# load indiana metadata spreadsheet
indiana_metadata = pd.read_excel('./Indiana_metaData.xlsx')

# extract uid from metadata
# and add column to metadata
uid = []
for endpoint in indiana_metadata['API Endpoint']:
    uid.append(endpoint.split('.')[-2].split('/')[-1])
indiana_metadata['uids'] = uid

# convert each entry in Column Name column to python list
# and add column to metadata
columns = []
for name in indiana_metadata['Column Name']:
    names = name.split(',')
    names = [name.strip() for name in names]
    columns.append(names)
indiana_metadata['columns'] = columns

# create sodapy client with proper credentials
client = Socrata(
    'hhs-opioid-codeathon.data.socrata.com',
    'r0hTo1hS9c0i2khglj7n1H8sn',
    username='joseph.mckenna@nih.gov',
    password='Abcd#1234')

# # get indiana datasets from socrata
# indiana_datasets = []
# for uid, columns in indiana_metadata[['uid', 'columns']]:
#     indiana_datasets.append(client.get(
#         uid, select=','.join(columns)))  # limits to 1000 rows

# # convert datasets to pandas data frames
# for dataset in indiana_datasets:
#     dataset = pd.DataFrame.from_records(dataset)
