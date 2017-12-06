import numpy as np
import pandas as pd

# UW County Health Rankings (2010-17)
# Medicaire Part D (2013-15)
# Unemployment rate (2011-2015)
# Accidental drug related deaths (2012-17)

# UW County Health Rankings (2010-17)
dtype = {
    'fips': int,
    'phys_unhealthy_days': float,
    'ment_unhealthy_days': float,
    'teen_birth_rate': float,
    'percent_uninsured': float,
    'primary_care_physician_rate': float,
    'high_school_graduation_rate': float,
    'percent_unemployted': float,
    'percent_children_in_poverty': float,
    'percent_single_parent_household': float,
    'violent_crime_rate': float
}
wisc_2010 = pd.read_excel('./sources/wisc.xlsx', sheet_name='2010', dtype=dtype)
wisc_2010['year'] = 2010

wisc_2011 = pd.read_excel('./sources/wisc.xlsx', sheet_name='2011', dtype=dtype)
wisc_2011['year'] = 2011

wisc_2012 = pd.read_excel('./sources/wisc.xlsx', sheet_name='2012', dtype=dtype)
wisc_2012['year'] = 2012

wisc_2013 = pd.read_excel('./sources/wisc.xlsx', sheet_name='2013', dtype=dtype)
wisc_2013['year'] = 2013

wisc_2014 = pd.read_excel('./sources/wisc.xlsx', sheet_name='2014', dtype=dtype)
wisc_2014['year'] = 2014
wisc_2014['percent_uninsured'] *= 10.
wisc_2014['percent_unemployted'] *= 10.
wisc_2014['percent_children_in_poverty'] *= 10.
wisc_2014['percent_children_in_poverty'] *= 10.

wisc_2015 = pd.read_excel('./sources/wisc.xlsx', sheet_name='2015', dtype=dtype)
wisc_2015['year'] = 2015
wisc_2015['percent_uninsured'] *= 10.
wisc_2015['percent_unemployted'] *= 10.
wisc_2015['percent_children_in_poverty'] *= 10.
wisc_2015['percent_children_in_poverty'] *= 10.

wisc_2016 = pd.read_excel('./sources/wisc.xlsx', sheet_name='2016', dtype=dtype)
wisc_2016['year'] = 2016
wisc_2016['percent_uninsured'] *= 10.
wisc_2016['percent_unemployted'] *= 10.
wisc_2016['percent_children_in_poverty'] *= 10.
wisc_2016['percent_children_in_poverty'] *= 10.

wisc_2017 = pd.read_excel('./sources/wisc.xlsx', sheet_name='2017', dtype=dtype)
wisc_2017['year'] = 2017
wisc_2017['percent_uninsured'] *= 10.
wisc_2017['percent_unemployted'] *= 10.
wisc_2017['percent_children_in_poverty'] *= 10.
wisc_2017['percent_children_in_poverty'] *= 10.

wisc = pd.concat([
    wisc_2010, wisc_2011, wisc_2012, wisc_2013, wisc_2014, wisc_2015,
    wisc_2016, wisc_2017
])

wisc.to_csv('./wisc_sparse.csv', index=False)
wisc.dropna(inplace=True)
wisc.to_csv('./wisc.csv', index=False)

# # Medicaire Part D (2013-15)
# dtype = {
#     'fips': int,
#     'part_d_prescribers': float,
#     'part_d_opioid_prescribers': float,
#     'opioid_claims': float,
#     'extended_release_opioid_claims': float,
#     'overall_claims': float
# }
# mpd_2013 = pd.read_excel(
#     './sources/medicaire_part_d.xlsx', sheet_name='2013', dtype=dtype)
# mpd_2014 = pd.read_excel(
#     './sources/medicaire_part_d.xlsx', sheet_name='2014', dtype=dtype)
# mpd_2015 = pd.read_excel(
#     './sources/medicaire_part_d.xlsx', sheet_name='2015', dtype=dtype)

# mpd_2013['year'] = 2013
# mpd_2014['year'] = 2014
# mpd_2015['year'] = 2015

# mpd = pd.concat([mpd_2013, mpd_2014, mpd_2015])
# mpd.dropna(inplace=True)

# # Unemployment rate (2011-2015)
# dtype = {
#     'state_fips': int,
#     'county_fips': int,
#     'year': object,
#     'unemployment_rate': float
# }
# unemployment = pd.read_excel('./sources/unemployment.xlsx')

# year = []
# for i, date in unemployment['year'].iteritems():
#     year.append(int(date.split(' ')[0].split('/')[-1]))
# unemployment['year'] = year

# fips = []
# for i, (sf, cf) in unemployment[['state_fips', 'county_fips']].iterrows():
#     fips.append(int('%i%03i' % (sf, cf)))
# unemployment = unemployment[['year', 'unemployment_rate']]
# unemployment['fips'] = fips

# left = pd.DataFrame(
#     data=np.random.randint(10, size=(4, 1)), columns=['left_data'])
# right = pd.DataFrame(
#     data=np.random.randint(10, size=(4, 1)), columns=['right_data'])

# left['year'] = [2000, 2001, 2002, 2003]
# right['year'] = [2001, 2002, 2003, 2004]

# left['fips'] = [1, 2, 3, 4]
# right['fips'] = [2, 3, 4, 5]

# print pd.merge(left, right, on['fips', 'year'])
