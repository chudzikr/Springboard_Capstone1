
# Import data from 2016-17 HSBC World Sevens Series Match Data PDFs
import pandas as pd
from os import listdir
from os.path import isfile, join

mypath = '/Users/admin/Dropbox/Springboard_DataScience/Capstone1/data/matchdata/2015-2017/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Create an empty dataframe with columns to store all appended matches
FinalDF = pd.DataFrame()
#FinalDF = pd.DataFrame(columns = ['Tournament', 'Match', 'Team', 'Date', 'Possession Time', 'Possessions', 'Avg Possession Time', 'Scores', 'Tries', 'Conversions', 'Tries Conceded', 'Points Conceded', 'Passes', 'Tackle_Ruck_Mauls', 'Retained', 'Lost', 'T-Overs Won', 'Tackle Only-Defence', 'Mauls', 'Kicks', 'General Play T/Overs', 'Lineouts', 'Own Won', 'Own Lost', 'Scrums', 'Own Won', 'Own Lost', 'Restarts', 'Long', 'Short', 'Regained', 'Errors', 'Pens_Frees Against', 'Ruck_Maul', 'Set Piece', 'General Play', 'Foul Play', 'Yellow_Red Cards'])


# iterate through all files in directory, get filename for later use - match#, etc.
for i in onlyfiles:
    name = i
    df = pd.read_excel(mypath + i, sheet_name=0)

    # read each file
    #df.head()

    # Get name for Team 1 (str)
    team1 = df.iloc[0,2]
    # Get name for Team 2
    team2 = df.iloc[0,5]

    # trim scores and whitespace from name
    team1 = str.strip(team1[:-6])
    team2 = str.strip(team2[:-6])

    # check output
    #print(team2 + " vs " + team1)

    # Get date string from 'Printed...', convert to datetime
    matchdate = df.iloc[37][0]
    tourdate = pd.to_datetime(matchdate.split()[2])
    type(tourdate)

    # Drop all unnceccessary rows, from 'Printed ...' row [37] onwards
    df2 = df.iloc[0:37, :]
    #df2

    # create df2, a transformed dataframe
    df2 = df2.T
    df2

    # create new columns with cleaned names
    newcols = ['col1','col2','Possession Time',
     'Possessions',
     'Avg Possession Time',
     'Scores',
     'Tries',
     'Conversions',
     'Goals',
     'Tries Conceded',
     'Points Conceded',
     'Passes',
     'Tackle_Ruck_Mauls',
     'Retained',
     'Lost',
     'T-Overs Won',
     'Tackle Only-Defence',
     'Mauls',
     'Kicks',
     'General Play T/Overs',
     'Lineouts',
     'Lineouts Won',
     'Lineouts Lost',
     'Scrums',
     'Scrums Won',
     'Scrums Lost',
     'Restarts',
     'Long',
     'Short',
     'Regained',
     'Errors',
     'Pens_Frees Against',
     'Ruck_Maul',
     'Set Piece',
     'General Play',
     'Foul Play',
     'Yellow_Red Cards']

    df2.columns = newcols
    df2

    # Keep only 'Total' rows, so effectively H1, H2 Rows are dropped
    df2 = df2[df2.loc[:,'col2'] == 'Total']
    df2

    # create new column for teams, date
    df2['Team'] = [team1, team2]
    df2['Date'] = tourdate # need to create an empty column fist??
    # Don't worry - it's a warning, not an error
    #df2

    # drop unncessary columns - no idea what 'Goals' is
    df2 = df2.drop(['col1', 'col2', 'Goals'], axis=1)


    # Fill NAs with '0'
    # df2 = df2.fillna(0)
    # df2

    # reset index
    # df2.index
    df2.reset_index(drop=True, inplace=True)
    #df2 = df2.drop(['index'], axis=1)
    #df2

    # create column for match name
    # i.e., '2016_Cape_Town_7s_Match_16_South_Africa_vs_USA'
    matchName = name.split('.')
    matchno = matchName[0]
    tournament = matchno.split('_7s_')[0]
    match = matchno.split('_7s_')[1]

    df2['Tournament'] = tournament
    df2['Match'] = match

    # ## Calculations/Derivations

    def convertSecs(x):
        """Convert possession time from string to seconds"""
        poss = x.split(":")
        min = int(poss[0])
        sec = int(poss[1])
        poss_secs = min * 60 + sec
        return poss_secs

    # convertSecs(df2['Possession Time'][1])
    df2['Possession Time'] = df2['Possession Time'].map(convertSecs)

    # Calculate Avg. Possession
    df2['Possessions'] = df2['Possessions'].astype(int, copy=False)
    df2['Avg Possession Time'] = df2['Possession Time'] / df2['Possessions']

    # Calculate conversions
    # used .astype() because values weren't retaining the datatype
    #df2['Tries'] = df2['Tries'].astype(int, copy=False)
    #df2['Scores'] = df2['Scores'].astype(int, copy=False)
    possConv = df2['Tries']  # number of possible conversions, converted from str to int
    pts = df2['Scores']  # total points, , converted from str to int
    convPts = (pts - (possConv * 5))
    # if there is a modulus of 1, then there's also a penalty
    df2['Conversions'] = ((convPts / 2) / possConv)  # percentage for conversions taken/made
    df2['Conversions']

    # Combine 'TOs Won' and 'Gen Play TOs'



    # In[744]:

    #  Drop columns that are not needed
    df2 = df2.drop(['Possessions', 'Avg Possession Time', 'Tries Conceded', 'Points Conceded', 'Lost', 'Tackle Only-Defence', 'Mauls', 'Kicks', 'Restarts', 'Long', 'Errors', 'Set Piece', 'General Play', 'Foul Play'], axis=1)

    # In[745]:

    # Append each match to FinalDF
    FinalDF = FinalDF.append(df2, ignore_index=True)

# columns to drop
# Lineouts - 'Own Lost', Scrums - 'Own Lost', 'Ruck_Maul'

# columns to calculate
# Tackle_Ruck_Mauls/Retained = Ruck Retention, Lineouts/Own Won = Own_Lineout_Win,
# Scrums/Own Won = Own_Scrum_Win, short/regained = own_contestable restarts won

# 'TurnoversConceded' is 'General Play T/Overs'
FinalDF['TurnoversConceded'] = FinalDF['General Play T/Overs']

# Calculate derived columns
FinalDF['Ruck_retention'] = FinalDF['Retained'] / FinalDF['Tackle_Ruck_Mauls']
FinalDF['Lineout_Win_Pct'] = FinalDF['Lineouts Won'] / FinalDF['Lineouts']
FinalDF['Scrum_Win_Pct'] = FinalDF['Scrums Won'] / FinalDF['Scrums']
FinalDF['Contestable_KO_Regained_pct'] = FinalDF['Regained'] / FinalDF['Short']

# Drop columns used to create derived columns
FinalDF = FinalDF.drop(['Retained', 'Tackle_Ruck_Mauls','T-Overs Won', 'General Play T/Overs', 'Lineouts Won','Lineouts', 'Short', 'Regained', 'Scrums Won', 'Scrums', 'Lineouts Lost', 'Scrums Lost'], axis=1)

FinalDF = FinalDF[['Team', 'Match', 'Tournament', 'Scores', 'Tries', 'Conversions', 'Possession Time', 'Passes', 'Ruck_Maul', 'Ruck_retention', 'Lineout_Win_Pct', 'Scrum_Win_Pct', 'Contestable_KO_Regained_pct', 'Pens_Frees Against', 'TurnoversConceded', 'Yellow_Red Cards']]

# Write the Dataframe to a CSV to keep a file of initial match output
#FinalDF.to_csv("../data/output/all_7s_matches.csv", mode='a', header=False, index=False)
FinalDF.to_csv("../data/output/all_matches.csv", mode='a', header=False, index=False)