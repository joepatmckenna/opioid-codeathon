import numpy as np
import pandas as pd

adrd = pd.read_excel('./Accidental_Drug_Related_Deaths__2012-June_2017.xlsx')

adrd = adrd[[
    'Date', 'Death County', 'Heroin', 'Fentanyl', 'Benzodiazepine',
    'Oxycodone', 'Oxymorphone', 'Hydrocodone', 'Tramad',
    'Morphine (not heroin)', 'Any Opioid'
]]

print 'number reports with year and county info:', (adrd[[
    'Date', 'Death County'
]].isnull().sum(axis=1) == 0).sum()
