# =============================================================================
# coding: utf-8
# Import World Rugby 7s World Series Analysis Reports ##
# Import 2017-18 Analysis Reports (Excel) from each stop on the 2018 7s World Series
# *** IMPORTANT!***  Run this file first, and Excel Import file second when processing the data
# =============================================================================

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

#mypath = '../../../Capstone1/data/matchdata/2017-18/new'
mypath = '/Users/admin/Dropbox/Springboard_DataScience/Capstone1/data/2017-18/new/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Create an empty dataframe with columns to store all appended matches
# BE SURE TO UPDATE WITH NEW COLUMNS
FinalDF = pd.DataFrame()

for i in onlyfiles:
    name = i
    #df = pd.read_excel(mypath + i, sheet_name=0)
    xls = pd.ExcelFile(mypath + i)
    df = xls.parse('Raw Data', skiprows=6, index_col=None, na_values=['NaN'])

    df.columns = ['col1', 'Team', 'Opposition', 'Total PointsScored', 'Total PointsConceded', 'Total TriesScored', 'Total TriesConceded', 'Try Scoring Rate(1 every x secs)', 'Try Conceding Rate(1 every x secs)', 'Tries Scored Build-Up(No Ruck/Maul)', 'Tries Conceded Build-Up(No Ruck/Maul)', 'Opp22m Entries', 'Opp22m Entry Rate(1 every  secs)', 'Own22m Entries', 'Own22m Entry Rate(1 every x secs)', 'Tries Scoredper Opp22m Entry', 'Tries Concededper Own22m Entry', 'Possession Time(Own)', 'Possession Time(Opp)', 'Passes', 'Passing Rate(1 every x secs)', 'Rucks Attack', 'Rucking RateAttack (secs)', 'RucksDefence', '% Ruck SuccessOwn', 'Own RucksWon per Match', '% Ruck SuccessOpp', 'Opp RucksWon per Match', 'TurnoversReceived', 'TurnoversConceded', 'TurnoverDifferential', 'OwnContestable Restarts', 'Own ContestableRestarts Regained', 'OppContestable Restarts', 'Opp ContestableRestarts Received', 'Total ScrumsOwn Feed', 'Scrum SuccessOwn Feed', 'Total LineoutsOwn Throw', 'Lineout SuccessOwn Throw', 'Penalty/FKConceded', 'TRM PenaltyConceded', 'Cards']

    # drop first column
    df.drop(df.columns[0], axis=1, inplace=True)

    # drop first row
    df.drop([0], inplace=True)

    # Drop unneccessary Average rows
    df = df[df['Team'] != 'Average'] # Remove the 'Average' row
    df = df[df['Team'] != 'Overall Average'] # Remove the 'Average' row

    # pseudo: if Team = 'NaN', grab the value from the previous row using .fillna(method='ffill') using forward fill
    # Need to run on only 'Team' column
    df[['Team']] = df[['Team']].fillna(method='ffill')

    # Select only matches with the USA playing
    usadf = df.loc[(df['Team'] == 'USA') | (df['Opposition'] == 'USA')]
    # need to combine for for/against or only select USA matches, i.e.,
    # usadf = df.loc[(df['Team'] == 'USA')]

    # Create new column, 'TotalPoints', to use as an aid to identify each match
    usadf['TotalPoints'] = usadf['Total PointsScored'] + usadf['Total PointsConceded']

    #Add 'MatchID column, move 'Totalpoints' to front of dataframe, Reindex
    cols = ['Team', 'Opposition', 'TotalPoints', 'Total PointsScored', 'Total PointsConceded', 'Total TriesScored', 'Total TriesConceded', 'Try Scoring Rate(1 every x secs)', 'Try Conceding Rate(1 every x secs)', 'Tries Scored Build-Up(No Ruck/Maul)', 'Tries Conceded Build-Up(No Ruck/Maul)', 'Opp22m Entries', 'Opp22m Entry Rate(1 every  secs)', 'Own22m Entries', 'Own22m Entry Rate(1 every x secs)', 'Tries Scoredper Opp22m Entry', 'Tries Concededper Own22m Entry', 'Possession Time(Own)', 'Possession Time(Opp)', 'Passes', 'Passing Rate(1 every x secs)', 'Rucks Attack', 'Rucking RateAttack (secs)', 'RucksDefence', '% Ruck SuccessOwn', 'Own RucksWon per Match', '% Ruck SuccessOpp', 'Opp RucksWon per Match', 'TurnoversReceived', 'TurnoversConceded', 'TurnoverDifferential', 'OwnContestable Restarts', 'Own ContestableRestarts Regained', 'OppContestable Restarts', 'Opp ContestableRestarts Received', 'Total ScrumsOwn Feed', 'Scrum SuccessOwn Feed', 'Total LineoutsOwn Throw', 'Lineout SuccessOwn Throw', 'Penalty/FKConceded', 'TRM PenaltyConceded', 'Cards', ]

    usadf = usadf.reindex(columns = cols)

# =============================================================================
    # Calculations/Derivations

    def convertSecs(x):
        """Convert possession time from string to seconds"""
        poss = x.split(":")
        min = int(poss[0])
        sec = int(poss[1])
        poss_secs = min * 60 + sec
        return poss_secs

    # convertSecs(df2['Possession Time'][1])
    # total_rows['ColumnID'] = total_rows['ColumnID'].astype(str)
    usadf.loc[:,'Possession Time(Own)'] =  usadf.loc[:,'Possession Time(Own)'].astype(str)
    usadf.loc[:,'Possession Time(Opp)'] =  usadf.loc[:,'Possession Time(Opp)'].astype(str)

    usadf.loc[:,'Possession Time(Own)'] = usadf.loc[:,'Possession Time(Own)'].map(convertSecs)
    usadf.loc[:,'Possession Time(Opp)'] = usadf.loc[:,'Possession Time(Opp)'].map(convertSecs)

    # ### Column labels ###
    # change col names to match the column names in the PDF import dataframe.
    usadf = usadf.rename(columns = {
        'Total PointsScored':'Scores',
        'Possession Time(Own)':'Possession Time',
        'Total TriesScored':'Tries',
        'TurnoversReceived':'T-Overs Won',
        'OwnContestable Restarts':'Short',
        'Own ContestableRestarts Regained':'Regained',
        'Penalty/FKConceded':'Pens_Frees Against',
        'TRM PenaltyConceded':'Ruck_Maul',
        'Cards':'Yellow_Red Cards',
        '% Ruck SuccessOwn':'Ruck_retention',
        })
    # =============================================================================
    # Get toournament name
    tournament = name.split()
    usadf['Tournament'] = tournament[0] + '_' + tournament[3] + '_' + tournament[4]
    # Try replacing '0s with 'NaN'
    usadf.replace(0, 'NaN', inplace=True)
    usadf = usadf.replace('NaN', np.nan)

    # Replace NaN's with zero
    #usadf.fillna(value=0, inplace=True)

    # Calculate conversions
    possConv = usadf['Tries']  # number of possible conversions, converted from str to int
    pts = usadf['Scores']  # total points, , converted from str to int
    convPts = (pts - (possConv * 5))
    # if there is a modulus of 1, then there's also a penalty
    usadf['Conversions'] = ((convPts / 2) / possConv)  # percentage for conversions taken/made
    usadf['Conversions']

    # =============================================================================
    # # Calulated columns -- FIX ISSUE!
    # # Poss > secs, 'Ruck_retention', 'Lineout_Win_Pct', 'Scrum_Win_Pct'
    # #usadf['Possession Time'] =
    #
    # #try:
    # #    usadf['Contestable_Restart_Win_Pct'] = usadf['Regained'] / usadf['Short']
    # #except ZeroDivisionError:
    # #    print(0)
    #     #return 0
    # =============================================================================

    # # check how to handle Div by zero issue in 'Contestable_Restart_Win_Pct', possibly others
    #usadf['Contestable_Restart_Win_Pct'] =  usadf['Regained'] / usadf['Short']
    # Change method of calculating Restarts Gained, to give them more weight
    usadf['Contestable_Restart_Win_Pct'] = 100 * (usadf['Regained'] / usadf['Short'])
    usadf['Lineout_Win_Pct'] =  usadf['Lineout SuccessOwn Throw'] / usadf['Total LineoutsOwn Throw']
    usadf['Scrum_Win_Pct'] =  usadf['Scrum SuccessOwn Feed'] /  usadf['Total ScrumsOwn Feed']

    # Append each match to FinalDF
    FinalDF = FinalDF.append(usadf, ignore_index=True)

dropcols = ['Total PointsConceded', 'Total TriesConceded','Try Scoring Rate(1 every x secs)',
'Try Conceding Rate(1 every x secs)', 'Tries Scored Build-Up(No Ruck/Maul)',
'Tries Conceded Build-Up(No Ruck/Maul)', 'Opp22m Entries', 'Opp22m Entry Rate(1 every  secs)', 'Own22m Entries', 'Own22m Entry Rate(1 every x secs)', 'Tries Scoredper Opp22m Entry',
'Tries Concededper Own22m Entry', 'Possession Time(Opp)', 'Passing Rate(1 every x secs)', 'Rucking RateAttack (secs)', 'RucksDefence', 'Own RucksWon per Match', '% Ruck SuccessOpp',
'Opp RucksWon per Match', 'TurnoversConceded', 'TurnoverDifferential', 'OppContestable Restarts', 'Opp ContestableRestarts Received', 'Regained', 'Short', 'Lineout SuccessOwn Throw', 'Total LineoutsOwn Throw', 'Scrum SuccessOwn Feed', 'Total ScrumsOwn Feed']
FinalDF.drop(dropcols, axis=1, inplace=True)

tempusa = FinalDF.groupby('Team')
tempusa = tempusa.get_group('USA')
tempopp = FinalDF.groupby('Opposition')
tempopp = tempopp.get_group('USA')

tempusa = tempusa.sort_values(by=['Opposition', 'Tournament', 'TotalPoints'])
tempopp = tempopp.sort_values(by=['Team', 'Tournament', 'TotalPoints'])

#Assign a MatchID to tempusa
tempusa.reset_index(drop=True, inplace=True)
tempusa['MatchID'] = tempusa.index + 1

#Assign a MatchID to tempopp
tempopp.reset_index(drop=True, inplace=True)
tempopp['MatchID'] = tempopp.index + 1

# Now that the USA and Opp matches all have the same MatchIDs, based on Team, Opp, Tournament,
# and TotalPoints, concat them both and order rows by MatchID, pairing each team in a match together
FinalDF = pd.concat([tempusa, tempopp])
FinalDF = FinalDF.sort_values(by=['MatchID'])

FinalDF = FinalDF[['Team', 'Opposition', 'MatchID', 'TotalPoints', 'Tournament', 'Conversions', 'Contestable_Restart_Win_Pct', 'Lineout_Win_Pct', 'Scrum_Win_Pct', 'Scores', 'Tries', 'Possession Time', 'Passes', 'Rucks Attack', 'Ruck_retention', 'T-Overs Won', 'Pens_Frees Against', 'Ruck_Maul', 'Yellow_Red Cards']]

# Replace NaN's with zero
FinalDF.fillna(value=0, inplace=True)

# Write the Dataframe to a CSV to keep a file of initial match output
FinalDF.to_csv("../data/output/all_Excel_FinalDF_matches.csv", mode='a', header=False, index=False)

# =============================================================================
# CONDUCT 'DIFF' OPERATIONS, CREATE NEW DATAFRAME
# Create new dataframe to hold diff values
#
# =============================================================================
# removed 'Date' and 'Match',
sub = pd.DataFrame(columns=['MatchID','Opp', 'Tournament', 'Poss_Time_Diff', 'Score_Diff', 'Conv_Diff', 'Tries_Diff', 'Passes_Diff', 'Contestable_KO_Win_pct_Diff', 'PenFK_Against_Diff', 'RuckMaul_Diff', 'Ruck_Win_pct_Diff', 'Cards_diff', 'Lineout_Win_Pct_Diff','Scrum_Win_Pct_Diff'])

#Reset index
FinalDF.reset_index(inplace=True)

for index, row in FinalDF.iterrows():
      if index % 2 == 0:
         new_row = FinalDF.iloc[index+1]
         if row['Team'] == "USA":
             # Get match, date, etc., values
             opp = new_row['Team']
             #date = new_row['Date']
             tourn = new_row['Tournament']
             match = new_row['MatchID']
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

             # Ruck-Maul - # Ruck-Maul- don't need to coerce to a float
             TotRM = row['Ruck_Maul'] + new_row['Ruck_Maul']
             RMUSA = row['Ruck_Maul']*100/TotRM
             RMOpp = new_row['Ruck_Maul']*100/TotRM
             RM_diff = RMUSA - RMOpp

             # OLD Method for 'Cards'
#             TotCards = float(row['Yellow_Red Cards']) + float(new_row['Yellow_Red Cards'])
#             CardsUSA = float(row['Yellow_Red Cards']*100)/TotCards
#             CardsOpp = float(new_row['Yellow_Red Cards']*100)/TotCards
#             Cards_diff = CardsUSA - CardsOpp

             # Cards with a factor of -50 applied
             CardsUSA = row['Yellow_Red Cards']
             CardsOpp = new_row['Yellow_Red Cards']
             CardsUSA_fac = CardsUSA * -50
             CardsOpp_fac = CardsOpp * -50
             Cards_diff = CardsUSA_fac - CardsOpp_fac

             # Ruck REtention - already a float/pct
             LOWin_diff = row['Lineout_Win_Pct'] - new_row['Lineout_Win_Pct']

             # LO Win
             RuckWin_diff = row['Ruck_retention'] - new_row['Ruck_retention']

             # Scrum Win Scrum_Win_Pct
             ScrumWin_diff = row['Scrum_Win_Pct'] - new_row['Scrum_Win_Pct']

             # Create a new row with the difference values
             # Add 'Cards_diff' back in later
             sub.loc[index] = (match, opp, tourn, posess_time_diff, scores_diff, tries_diff, conv_diff, passes_diff, kopct_diff, PenFk_diff, RM_diff, RuckWin_diff, Cards_diff, LOWin_diff, ScrumWin_diff)


         #if new_row['Team'] == "USA":
         #if new_row['Opposition'] == "USA":
         else:
             # Get match, date, etc., values
             opp = row['Team']
             #date = row['Date']
             tourn = row['Tournament']
             match = row['MatchID']
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

             # Ruck-Maul- don't need to coerce to a float
             TotRM = row['Ruck_Maul'] + new_row['Ruck_Maul']
             RMUSA = new_row['Ruck_Maul']*100/TotRM
             RMOpp = row['Ruck_Maul']*100/TotRM
             RM_diff = RMUSA - RMOpp

             # OLD Method for 'Cards'
             #TotCards = float(row['Yellow_Red Cards']) + float(new_row['Yellow_Red Cards'])
             #CardsUSA = float(new_row['Yellow_Red Cards']*100)/TotCards
             #CardsOpp = float(row['Yellow_Red Cards']*100)/TotCards
             #Cards_diff = CardsUSA - CardsOpp

             # Cards with a factor of -50 applied
             CardsOpp = row['Yellow_Red Cards']
             CardsUSA = new_row['Yellow_Red Cards']
             CardsUSA_fac = CardsUSA * -50
             CardsOpp_fac = CardsOpp * -50
             Cards_diff = CardsUSA_fac - CardsOpp_fac

             # Ruck REtention - already a float/pct
             LOWin_diff = new_row['Lineout_Win_Pct'] - row['Lineout_Win_Pct']

             # LO Win
             RuckWin_diff = new_row['Ruck_retention'] - row['Ruck_retention']

             # Scrum Win Scrum_Win_Pct
             ScrumWin_diff = new_row['Scrum_Win_Pct'] - row['Scrum_Win_Pct']

             # Create a new now with the difference values
             # Add 'Cards_diff' back in later
             sub.loc[index] = (match, opp, tourn, posess_time_diff, scores_diff, tries_diff, conv_diff, passes_diff, kopct_diff, PenFk_diff, RM_diff, RuckWin_diff, Cards_diff, LOWin_diff, ScrumWin_diff)

# =============================================================================
#FINAL CLEANUP
#Drop the MatchID column before outputting CSV
sub.drop(['MatchID'], axis=1, inplace=True)

# Replace NaN's with zero
sub.fillna(value=0, inplace=True)

# write/append dataframe to CSV file
# Use the 'to_csv' write mode of 'a' to append a new DF to an existing CSV
# You can append to a csv by opening the file in append mode, t
sub.to_csv('../data/output/final_diffs_validate.csv', mode='a', header=False, index=False)