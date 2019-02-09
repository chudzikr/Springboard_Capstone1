
# coding: utf-8

# ### Engineer new features for percentage of KOs Regained > Win
# @todo
# * Create a Result column for Win/Loss
# * Create new columns for 0%, 20%, 40%, 60%, 80%
# * Create "Series Year", i.e., 2017-18, based on Date.  Need to account for tournaments straddling years: i.e., Dec 15 tournament belongs in 2015-16 tournament year. Use time series analysis.

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Show plots inline
#get_ipython().magic('matplotlib inline')

# In[ ]:

#Import Raw (not Diff) Match Data
df = pd.read_csv('../data/output/all_7s_matches.csv')

# In[ ]:
df
#230 rows × 17 columns

# In[ ]:

#From Raghu
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
#df

#Create columns for KO win % bands based on Contestable_Restart_Win_Pct
# Tmp DF to hold values
tmp = pd.DataFrame(columns=['0 - 25', '25 - 50', '50 - 75', '75 - 100'])

#Iterate through rows and create classification for KO Win%
for index, row in df.iterrows():

    #if row['Contestable_Restart_Win_Pct'] == 0:
        #zero = row['0'] = float(0)
        #under25 = row['0 - 25'] = float(0)
        #under50 = row['25 - 50'] = float(0)
        #under75 = row['50 - 75'] = float(0)
        #under100 = row['75 - 100'] = float(0)

    if row['Contestable_Restart_Win_Pct'] >= 0 and row['Contestable_Restart_Win_Pct'] <= 25.0:
        #zero = row['0'] = float(0)
        under25 = row['0 - 25'] = float(0.25*50)
        under50 = row['25 - 50'] = float(0)
        under75 = row['50 - 75'] = float(0)
        under100 = row['75 - 100'] = float(0)

    elif row['Contestable_Restart_Win_Pct'] > 25.0 and row['Contestable_Restart_Win_Pct'] <= 50.0:
        #zero = row['0'] = float(0)
        under25 = row['0 - 25'] = float(0)
        under50 = row['25 - 50'] = float(0.50*50)
        under75 = row['50 - 75'] = float(0)
        under100 = row['75 - 100'] = float(0)

    elif row['Contestable_Restart_Win_Pct'] > 50.0 and row['Contestable_Restart_Win_Pct'] <= 75.0:
        #zero = row['0'] = float(0)
        under25 = row['0 - 25'] = float(0)
        under50 = row['25 - 50'] = float(0)
        under75 = row['50 - 75'] = float(0.75*50)
        under100 = row['75 - 100'] = float(0)

    elif row['Contestable_Restart_Win_Pct'] > 75.0 and row['Contestable_Restart_Win_Pct'] <= 100.0:
        #zero = row['0'] = float(0)
        under25 = row['0 - 25'] = float(0)
        under50 = row['25 - 50'] = float(0)
        under75 = row['50 - 75'] = float(0)
        under100 = row['75 - 100'] = float(1.00*50)

    tmp.loc[index] = (under25, under50, under75, under100)

#df.info()
#type(df.Result[1])
df = pd.concat([df, tmp], axis=1)

df.to_csv("../data/output/matchdata_ko_bands.csv", header=True, index=False)

#print(list(df.columns))
# ['Team', 'Date', 'Tournament', 'Match', 'Possession Time', 'Scores', 'Tries', 'Conversions', 'Passes', 'Contestable_Restart_Win_Pct', 'Pens_Frees Against', 'Ruck_Maul', 'Yellow_Red Cards', 'TurnoversConceded', 'Ruck_retention', 'Lineout_Win_Pct', 'Scrum_Win_Pct', 'Result', '0', '0 - 25', '25 - 50', '50 - 75', '75 - 100']
df

# =============================================================================
# Fit a Random Forest model, examine Feature Importance
# =============================================================================
from sklearn.model_selection import train_test_split

#Drop features that are unneccessary/str or will bias the prediction
rf_data = df.drop((['Team', 'Date', 'Tournament', 'Match', 'Scores', 'Tries', 'Conversions']), axis=1)

#Build model from only KO% values
#rf_data = df[['0','0 - 25','25 - 50','50 - 75', '75 - 100', 'Result']]

#Pull out the variable we're trying to predict: 'Result'
X = rf_data.drop('Result',axis=1)
y = rf_data['Result']
y=y.astype('int')

#Train-Test split (70/30)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

# Fit RF model
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=200, verbose=0)
rfc.fit(X_train, y_train)

# Run predictions
rfc_pred = rfc.predict(X_test)

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score

#Output confusion matrix
print(confusion_matrix(y_test,rfc_pred))

#import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
conf = confusion_matrix(y_test,rfc_pred)
plt.imshow(conf, cmap='binary', interpolation='None')
plt.show()

#import libraries to ignore UndefinedMetricWarning
import warnings
import sklearn.exceptions
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)

#get the model's accuracy score
accuracy_score(y_test, rfc_pred)
print(classification_report(y_test,rfc_pred))

#print accuracy score
rfc.score(X_test, y_test)

# =============================================================================
# Extract feature importance
# =============================================================================

feature_importances = pd.DataFrame(rfc.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance']).sort_values('importance', ascending=False)

print(feature_importances)

#Create a DF of only the most important features
#impt = df[['Poss_Time_Diff','Passes_Diff','Contestable_KO_Win_pct_Diff','PenFK_Against_Diff', 'Ruck_Win_pct_Diff', 'Result']]

#impt = df[['0 - 25', '25 - 50', '50 - 75', '75 - 100', 'Result']]

#Plot relationships of all important features
#sns.pairplot(impt,hue='Result', palette='Set1') #hue='Result'


