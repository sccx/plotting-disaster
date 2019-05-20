#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 15:41:50 2019

@author: sccx
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def percentage_calculator(df):
    percentages = pd.DataFrame()
    total_counties = 3142
    for i in df['year'].unique():
        count = df.loc[drc['year'] == i].count()
        percent = (count / total_counties) * 100
        percentages[i] = percent
    return percentages



xls_file = pd.ExcelFile("DataVizDisasterSummariesFV12.19.2016.xlsx")
df = pd.read_excel(xls_file, sheet_name='FEMA Declarations')

years = df['Unnamed: 1']
states = df['Unnamed: 4']
counties = df['Unnamed: 6']
disaster_type = df['Unnamed: 8']
incidents = df['Unnamed: 9']

disasters = pd.concat([years, states, counties, disaster_type, incidents], axis=1)
disasters.drop(disasters.index[:2], inplace=True)
disasters.rename(columns={"Unnamed: 1":"year", "Unnamed: 4":"state","Unnamed: 6":"county", "Unnamed: 8":"declaration", "Unnamed: 9":"incident"}, inplace=True)
disasters.to_csv('FEMA_disasters.csv')

dec = disasters.loc[disasters['declaration'] == 'DR']

dr = dec.copy()
drc = dr[dr.county != 'Statewide']

new = percentage_calculator(drc)
new.drop(['state', 'county', 'declaration', 'incident'], inplace=True)
new.rename({'year':'percent'}, inplace = True)

declared_counties = new.T
declared_counties = declared_counties.sort_index()
declared_counties.reset_index(level=0, inplace=True)
declared_counties.rename(index=str, columns={'index':'year'}, inplace = True)


fema = declared_counties[16:]
fema.reset_index(drop=True)

x=fema["year"]
y=fema["percent"]
plt.fill_between(x, y)
plt.show()


fema.plot(kind='bar',x='year',y='percent',color='b',width=0.8)
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
line = slope * x + intercept

#%%

plt.plot(x,y,'o', x, line)



