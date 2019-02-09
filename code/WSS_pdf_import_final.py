# =============================================================================
# Import data from 2016-17 HSBC World Sevens Series Match Data PDFs
# *** IMPORTANT!***   Run this file first, and Excel Import file second when processing the data.
# =============================================================================

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
    possConv = df2['Tries']  # number of possible conversions, converted from str to int
    pts = df2['Scores']  # total points, , converted from str to int
    convPts = (pts - (possConv * 5))
    # if there is a modulus of 1, then there's also a penalty
    df2['Conversions'] = ((convPts / 2) / possConv)  # percentage for conversions taken/made
    df2['Conversions']

    # Combine 'TOs Won' and 'Gen Play TOs'

    #  Drop columns that are not needed
    df2 = df2.drop(['Possessions', 'Avg Possession Time', 'Tries Conceded', 'Points Conceded', 'Lost', 'Tackle Only-Defence', 'Mauls', 'Kicks', 'Restarts', 'Long', 'Errors', 'Set Piece', 'General Play', 'Foul Play'], axis=1)

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

# Change method of calculating Restarts Gained, to give them more weight
FinalDF['Contestable_Restart_Win_Pct'] = 100 * (FinalDF['Regained'] / FinalDF['Short'])

# Drop columns used to create derived columns
FinalDF = FinalDF.drop(['Retained', 'Tackle_Ruck_Mauls','T-Overs Won', 'General Play T/Overs', 'Lineouts Won','Lineouts', 'Short', 'Regained', 'Scrums Won', 'Scrums', 'Lineouts Lost', 'Scrums Lost'], axis=1)

FinalDF = FinalDF[['Team', 'Date','Tournament', 'Match', 'Possession Time', 'Scores', 'Tries', 'Conversions', 'Passes', 'Contestable_Restart_Win_Pct', 'Pens_Frees Against', 'Ruck_Maul', 'Yellow_Red Cards', 'TurnoversConceded', 'Ruck_retention', 'Lineout_Win_Pct','Scrum_Win_Pct']]

# Replace NaN's with zero
FinalDF.fillna(value=0, inplace=True)

# Write the Dataframe to a CSV to keep a file of initial match output
FinalDF.to_csv("../data/output/all_7s_matches.csv", header=True, index=False)

# Get the differnce between the USA and their opposition
# If 'Team'='USA' AND TOURNAMENT and MATCH are ==
#iterate through the rows of the dataframe and get the next row relative to the current row
#if the current row is USA then compute the possesion time of current row (USA) and next row relative to current row
#that is of opponent, find the possesion time relative to USA and put it in a new column called as PossessionTimeRelativeUSA
#In the same manner perform the calculation for other features
# Get 2 rows at a time and perform the calculation hence check if the index is odd or even and perform calculation only on even rows

# Removed 'date' and 'match' for consistency, as they are not available in Excel reports
sub = pd.DataFrame(columns=['Opp', 'Tournament', 'Poss_Time_Diff', 'Score_Diff', 'Conv_Diff', 'Tries_Diff', 'Passes_Diff', 'Contestable_KO_Win_pct_Diff', 'PenFK_Against_Diff', 'RuckMaul_Diff', 'Ruck_Win_pct_Diff', 'Cards_diff', 'Lineout_Win_Pct_Diff','Scrum_Win_Pct_Diff'])

for index, row in FinalDF.iterrows():
    if index % 2 == 0:
       new_row = FinalDF.iloc[index+1]
       if row['Team'] == "USA":
           # Get match, date, etc., values
           # Removed 'date' and 'match' for consistency - not available in Excel reports
           opp = new_row['Team']
           #date = new_row['Date']
           tourn = new_row['Tournament']
           #match = new_row['Match']

           #Possession Time
           TotPossTime = float(row['Possession Time']) + float(new_row['Possession Time'])
           PossessionUSA = float(row['Possession Time']*100)/TotPossTime
           PossessionOpp = float(new_row['Possession Time']*100)/TotPossTime
           posess_time_diff = PossessionUSA - PossessionOpp

           # Scores
           TotScores = float(row['Scores']) + float(new_row['Scores'])
           ScoresUSA = float(row['Scores']*100)/TotScores
           ScoresOpp = float(new_row['Scores']*100)/TotScores
           scores_diff = ScoresUSA - ScoresOpp

           # Tries
           TotTries = float(row['Tries']) + float(new_row['Tries'])
           TriesUSA = float(row['Tries']*100)/TotTries
           TriesOpp = float(new_row['Tries']*100)/TotTries
           tries_diff = TriesUSA - TriesOpp

           # Conversions - already a float/pct
           conv_diff = row['Conversions'] - new_row['Conversions']

           # Passes
           TotPasses = float(row['Passes']) + float(new_row['Passes'])
           PassesUSA = float(row['Passes']*100)/TotPasses
           PassesOpp = float(new_row['Passes']*100)/TotPasses
           passes_diff = PassesUSA - PassesOpp

           # Contestable_KO_Regained_pct - already a float
           kopct_diff = row['Contestable_Restart_Win_Pct'] -  new_row['Contestable_Restart_Win_Pct']

           # Pen-FK
           TotPenFk = float(row['Pens_Frees Against']) + float(new_row['Pens_Frees Against'])
           PenFkUSA = float(row['Pens_Frees Against']*100)/TotPenFk
           PenFkOpp = float(new_row['Pens_Frees Against']*100)/TotPenFk
           PenFk_diff = PenFkUSA - PenFkOpp

           # Ruck-Maul
           TotRM = float(row['Ruck_Maul']) + float(new_row['Ruck_Maul'])
           RMUSA = float(row['Ruck_Maul']*100)/TotRM
           RMOpp = float(new_row['Ruck_Maul']*100)/TotRM
           RM_diff = RMUSA - RMOpp

            # Cards with a factor of -50 applied
           CardsUSA = row['Yellow_Red Cards']
           CardsOpp = new_row['Yellow_Red Cards']
           CardsUSA_fac = CardsUSA * -50
           CardsOpp_fac = CardsOpp * -50
           Cards_diff = CardsUSA_fac - CardsOpp_fac

           # LO Win
           LOWin_diff = row['Lineout_Win_Pct'] - new_row['Lineout_Win_Pct']

           # Ruck REtention - already a float/pct
           RuckWin_diff  = row['Ruck_retention'] - new_row['Ruck_retention']

           # Scrum Win Scrum_Win_Pct
           ScrumWin_diff = row['Scrum_Win_Pct'] - new_row['Scrum_Win_Pct']

           # Create a new now with the difference values
           # Add 'Cards_diff' back in later
           sub.loc[index] = (opp, tourn, posess_time_diff, scores_diff, tries_diff, conv_diff, passes_diff, kopct_diff, PenFk_diff, RM_diff, RuckWin_diff, Cards_diff, LOWin_diff, ScrumWin_diff)

       if new_row['Team'] == "USA":
           # Get match, date, etc., values
           # Removed 'date' and 'match' for consistency, as they are not available in Excel reports
           opp = row['Team']
           #date = row['Date']
           tourn = row['Tournament']
           #match = row['Match']

           #Possession Time
           TotPossTime = float(row['Possession Time']) + float(new_row['Possession Time'])
           PossessionUSA = float(new_row['Possession Time']*100)/TotPossTime
           PossessionOpp = float(row['Possession Time']*100)/TotPossTime
           posess_time_diff = PossessionUSA - PossessionOpp

           # Scores
           TotScores = float(row['Scores']) + float(new_row['Scores'])
           ScoresUSA = float(new_row['Scores']*100)/TotScores
           ScoresOpp = float(row['Scores']*100)/TotScores
           scores_diff = ScoresUSA - ScoresOpp

           # Tries
           TotTries = float(row['Tries']) + float(new_row['Tries'])
           TriesUSA = float(new_row['Tries']*100)/TotTries
           TriesOpp = float(row['Tries']*100)/TotTries
           tries_diff = TriesUSA - TriesOpp

           # Conversions - already a float/pct
           conv_diff = new_row['Conversions'] - row['Conversions']

           # Passes
           TotPasses = float(row['Passes']) + float(new_row['Passes'])
           PassesUSA = float(new_row['Passes']*100)/TotPasses
           PassesOpp = float(row['Passes']*100)/TotPasses
           passes_diff = PassesUSA - PassesOpp

           # Contestable_KO_Regained_pct - already a float
           kopct_diff = row['Contestable_Restart_Win_Pct'] - new_row['Contestable_Restart_Win_Pct']

           # Pen-FK
           TotPenFk = float(row['Pens_Frees Against']) + float(new_row['Pens_Frees Against'])
           PenFkUSA = float(new_row['Pens_Frees Against']*100)/TotPenFk
           PenFkOpp = float(row['Pens_Frees Against']*100)/TotPenFk
           PenFk_diff = PenFkUSA - PenFkOpp

           # Ruck-Maul
           TotRM = float(row['Ruck_Maul']) + float(new_row['Ruck_Maul'])
           RMUSA = float(new_row['Ruck_Maul']*100)/TotRM
           RMOpp = float(row['Ruck_Maul']*100)/TotRM
           RM_diff = RMUSA - RMOpp

# Cards with a factor of -50 applied
           CardsUSA = new_row['Yellow_Red Cards']
           CardsOpp = row['Yellow_Red Cards']
           CardsUSA_fac = CardsUSA * -50
           CardsOpp_fac = CardsOpp * -50
           Cards_diff = CardsUSA_fac - CardsOpp_fac

           # LO Win
           LOWin_diff = new_row['Lineout_Win_Pct'] - row['Lineout_Win_Pct']

           # Ruck REtention - already a float/pct
           RuckWin_diff = new_row['Ruck_retention'] - row['Ruck_retention']

           # Scrum Win Scrum_Win_Pct
           ScrumWin_diff = new_row['Scrum_Win_Pct'] - row['Scrum_Win_Pct']

           # Create a new now with the difference values
           # Add 'Cards_diff' back in later
           sub.loc[index] = (opp, tourn, posess_time_diff, scores_diff, tries_diff, conv_diff, passes_diff, kopct_diff, PenFk_diff, RM_diff, RuckWin_diff, Cards_diff, LOWin_diff, ScrumWin_diff)

sub.to_csv("../data/output/final_diffs_all.csv", header=True, index=False)