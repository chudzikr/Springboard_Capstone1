
# coding: utf-8

# ### Engineer new features for percentage of KOs Regained > Win
# @todo
# * Create a Result column for Win/Loss
# * Create new columns for 0%, 20%, 40%, 60%, 80%
# * Create "Series Year", i.e., 2017-18, based on Date.  Need to account for tournaments straddling years: i.e., Dec 15 tournament belongs in 2015-16 tournament year. Use time series analysis.

# In[ ]:


import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns

# Show plots inline
#get_ipython().magic('matplotlib inline')


# In[ ]:


#Import Raw (not Diff) Match Data
df = pd.read_csv('../data/output/all_7s_matches.csv')


# In[ ]:
df
#230 rows × 17 columns


# In[ ]:


#20% regains  40% regains    60% regains
#0                             0.6*50


# In[ ]:


#Create a Result column for Win/Loss. Do in pre-processing code?

#Temp DF to hold 'Result'
sub = pd.DataFrame(columns=['Result'])

#Iterate through rows and create 'Result' for Win/Loss (Win=1, Win=0)
for index, row in df.iterrows():
    if index%2 == 0:
        new_row = df.iloc[index+1]
        if row['Match'] == new_row['Match']:
            if row['Scores'] > new_row['Scores']:
                result1 = row['Result'] = 1
                result2 = new_row['Result'] = 0
            elif row['Scores'] < new_row['Scores']:
                result1 = row['Result'] = 0
                result2 = new_row['Result'] = 1
            else:
                result1 = row['Result'] = 2
                result2 = new_row['Result'] = 2

            sub.loc[index] = (result1)
            sub.loc[index+1]  = (result2)


# In[ ]:

df = pd.concat([df, sub], axis=1)
df


# In[ ]:

#Create columns for KO win % bands based on Contestable_Restart_Win_Pct
# Tmp DF to hold values
tmp = pd.DataFrame(columns=['0', '0 - 25', '25 - 50', '50 - 75', '75 - 100'])

#Iterate through rows and create classification for KO Win%
for index, row in df.iterrows():
    if row['Contestable_Restart_Win_Pct'] == 0:
        zero = row['0'] = float(0)
        under25 = row['0 - 25'] = float(0)
        under50 = row['25 - 50'] = float(0)
        under75 = row['50 - 75'] = float(0)
        under100 = row['75 - 100'] = float(0)

    elif row['Contestable_Restart_Win_Pct'] > 0 and row['Contestable_Restart_Win_Pct'] <= 25.0:
        zero = row['0'] = float(0)
        under25 = row['0 - 25'] = float(0.25*50)
        under50 = row['25 - 50'] = float(0)
        under75 = row['50 - 75'] = float(0)
        under100 = row['75 - 100'] = float(0)

    elif row['Contestable_Restart_Win_Pct'] > 25.0 and row['Contestable_Restart_Win_Pct'] <= 50.0:
        zero = row['0'] = float(0)
        under25 = row['0 - 25'] = float(0)
        under50 = row['25 - 50'] = float(0.50*50)
        under75 = row['50 - 75'] = float(0)
        under100 = row['75 - 100'] = float(0)

    elif row['Contestable_Restart_Win_Pct'] > 50.0 and row['Contestable_Restart_Win_Pct'] <= 75.0:
        zero = row['0'] = float(0)
        under25 = row['0 - 25'] = float(0)
        under50 = row['25 - 50'] = float(0)
        under75 = row['50 - 75'] = float(0.75*50)
        under100 = row['75 - 100'] = float(0)

    elif row['Contestable_Restart_Win_Pct'] > 75.0 and row['Contestable_Restart_Win_Pct'] <= 100.0:
        zero = row['0'] = float(0)
        under25 = row['0 - 25'] = float(0)
        under50 = row['25 - 50'] = float(0)
        under75 = row['50 - 75'] = float(0)
        under100 = row['75 - 100'] = float(1.00*50)

    tmp.loc[index] = (zero, under25, under50, under75, under100)


# In[ ]:

df.info()


# In[ ]:

df = pd.concat([df, tmp], axis=1)

df.to_csv("../data/output/matchdata_ko_bands.csv", header=True, index=False)

