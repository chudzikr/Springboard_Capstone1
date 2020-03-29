# =============================================================================
# coding: utf-8
# Import World Rugby 7s World Series Analysis Reports ##
# Import 2018-19 Analysis Reports (Excel) from each stop on the 2018 7s World Series
# Create ONLY matchfile data, not Diff data
# =============================================================================
from __future__ import division
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

#mypath = '../../../Capstone1/Stats/2018-19_WR_Summaries/new/'
mypath = '../../../Capstone1/data/matchdata/2018-19/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Create an empty dataframe with columns to store all appended matches
# BE SURE TO UPDATE WITH NEW COLUMNS
FinalDF = pd.DataFrame()

for i in onlyfiles:
    name = i
    #df = pd.read_excel(mypath + i, sheet_name=0)
    #xls = pd.ExcelFile(mypath + i)
    file = mypath + i
    df = pd.read_excel(file, sheet_name=4, skiprows=6, index_col=None, na_values=['NaN'])

    df.columns = ['col1', 'Team', 'Opposition', 'Total PointsScored', 'Total PointsConceded', 'Total TriesScored', 'Total TriesConceded', 'Try Scoring Rate(1 every x secs)', 'Try Conceding Rate(1 every x secs)', 'Tries Scored Build-Up(No Ruck/Maul)', 'Tries Conceded Build-Up(No Ruck/Maul)', 'Opp22m Entries', 'Opp22m Entry Rate(1 every  secs)', 'Own22m Entries', 'Own22m Entry Rate(1 every x secs)', 'Tries Scoredper Opp22m Entry', 'Tries Concededper Own22m Entry', 'Possession Time(Own)', 'Possession Time(Opp)', 'Passes', 'Passing Rate(1 every x secs)', 'Rucks Attack', 'Rucking RateAttack (secs)', 'RucksDefence', '% Ruck SuccessOwn', '% Ruck SuccessOpp', 'TurnoversReceived', 'TurnoversConceded', 'TurnoverDifferential', 'OwnContestable Restarts', 'Own ContestableRestarts Regained', 'OppContestable Restarts', 'Opp ContestableRestarts Received', 'Total ScrumsOwn Feed', 'Scrum SuccessOwn Feed', 'Total LineoutsOwn Throw', 'Lineout SuccessOwn Throw', 'PenaltyFKConceded', 'TRM PenaltyConceded', 'Cards']
    

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
    cols = ['Team', 'Opposition', 'TotalPoints', 'Total PointsScored', 'Total PointsConceded', 'Total TriesScored', 'Total TriesConceded', 'Try Scoring Rate(1 every x secs)', 'Try Conceding Rate(1 every x secs)', 'Tries Scored Build-Up(No Ruck/Maul)', 'Tries Conceded Build-Up(No Ruck/Maul)', 'Opp22m Entries', 'Opp22m Entry Rate(1 every  secs)', 'Own22m Entries', 'Own22m Entry Rate(1 every x secs)', 'Tries Scoredper Opp22m Entry', 'Tries Concededper Own22m Entry', 'Possession Time(Own)', 'Possession Time(Opp)', 'Passes', 'Passing Rate(1 every x secs)', 'Rucks Attack', 'Rucking RateAttack (secs)', 'RucksDefence', '% Ruck SuccessOwn', 'Own RucksWon per Match', '% Ruck SuccessOpp', 'Opp RucksWon per Match', 'TurnoversReceived', 'TurnoversConceded', 'TurnoverDifferential', 'OwnContestable Restarts', 'Own ContestableRestarts Regained', 'OppContestable Restarts', 'Opp ContestableRestarts Received', 'Total ScrumsOwn Feed', 'Scrum SuccessOwn Feed', 'Total LineoutsOwn Throw', 'Lineout SuccessOwn Throw', 'PenaltyFKConceded', 'TRM PenaltyConceded', 'Cards']

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
        'PenaltyFKConceded':'Pens_Frees_Against',
        'TRM PenaltyConceded':'Ruck_Maul',
        'Cards':'Yellow_Red Cards',
        '% Ruck SuccessOwn':'Ruck_retention',
        })
    # =============================================================================
    # Get toournament name
    tournament = name.split()
    usadf['Tournament'] = tournament[0] + '_' + tournament[3] + '_' + tournament[4]
    # Try replacing '0s with 'NaN'
   # usadf.replace(0, 'NaN', inplace=True)
    usadf = usadf.replace('NaN', np.nan)

    # Replace NaN's with zero
    usadf.fillna(value=0, inplace=True)

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
    # usadf['Contestable_Restart_Win_Pct'] =  usadf['Regained'] / usadf['Short']
    # Change method of calculating Restarts Gained, to give them more weight
    usadf['Contestable_Restart_Win_Pct'] = 100 * (usadf['Regained'] / usadf['Short'])
    usadf['Lineout_Win_Pct'] =  usadf['Lineout SuccessOwn Throw'] / usadf['Total LineoutsOwn Throw']
    usadf['Scrum_Win_Pct'] =  usadf['Scrum SuccessOwn Feed'] /  usadf['Total ScrumsOwn Feed']

    # Append each match to FinalDF
    FinalDF = FinalDF.append(usadf, ignore_index=True)

# =============================================================================
# TEST REMOVING 'DROPCOLS' to get full data set 
#
# dropcols = ['Total PointsConceded', 'Total TriesConceded','Try Scoring Rate(1 every x secs)',
# 'Try Conceding Rate(1 every x secs)', 'Tries Scored Build-Up(No Ruck/Maul)',
# 'Tries Conceded Build-Up(No Ruck/Maul)', 'Opp22m Entries', 'Opp22m Entry Rate(1 every  secs)', 'Own22m Entries', 'Own22m Entry Rate(1 every x secs)', 'Tries Scoredper Opp22m Entry',
# 'Tries Concededper Own22m Entry', 'Possession Time(Opp)', 'Passing Rate(1 every x secs)', 'Rucking RateAttack (secs)', 'RucksDefence', 'Own RucksWon per Match', '% Ruck SuccessOpp',
# 'Opp RucksWon per Match', 'TurnoversConceded', 'TurnoverDifferential', 'OppContestable Restarts', 'Opp ContestableRestarts Received', 'Regained', 'Short', 'Lineout SuccessOwn Throw', 'Total LineoutsOwn Throw', 'Scrum SuccessOwn Feed', 'Total ScrumsOwn Feed']
# FinalDF.drop(dropcols, axis=1, inplace=True)
# =============================================================================

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

# TEST REMOVING
#
#FinalDF = FinalDF[['Team', 'Opposition', 'MatchID', 'TotalPoints', 'Tournament', 'Conversions', 'Contestable_Restart_Win_Pct', 'Lineout_Win_Pct', 'Scrum_Win_Pct', 'Scores', 'Tries', 'Possession Time', 'Passes', 'Rucks Attack', 'Ruck_retention', 'T-Overs Won', 'Pens_Frees_Against', 'Ruck_Maul', 'Yellow_Red Cards']]

# Convert all team /opp names to Upper case for consistency
FinalDF['Opposition'] = FinalDF['Opposition'].str.upper()
FinalDF['Team'] = FinalDF['Team'].str.upper()

FinalDF = FinalDF[['Team', 'Opposition', 'MatchID', 'Tournament', 'TotalPoints', 'Scores', 'Total PointsConceded', 'Tries', 'Conversions', 'Total TriesConceded', 'Try Scoring Rate(1 every x secs)', 'Try Conceding Rate(1 every x secs)', 'Tries Scored Build-Up(No Ruck/Maul)', 'Tries Conceded Build-Up(No Ruck/Maul)', 'Opp22m Entries', 'Opp22m Entry Rate(1 every  secs)', 'Own22m Entries', 'Own22m Entry Rate(1 every x secs)', 'Tries Scoredper Opp22m Entry', 'Tries Concededper Own22m Entry', 'Possession Time', 'Possession Time(Opp)', 'Passes', 'Passing Rate(1 every x secs)', 'Rucks Attack', 'Rucking RateAttack (secs)', 'RucksDefence', 'Ruck_retention', 'Own RucksWon per Match', '% Ruck SuccessOpp', 'Opp RucksWon per Match', 'T-Overs Won', 'TurnoversConceded', 'TurnoverDifferential', 'Short', 'Regained', 'OppContestable Restarts', 'Opp ContestableRestarts Received', 'Total ScrumsOwn Feed', 'Scrum SuccessOwn Feed', 'Total LineoutsOwn Throw', 'Lineout SuccessOwn Throw', 'Pens_Frees_Against', 'Ruck_Maul', 'Yellow_Red Cards', 'Contestable_Restart_Win_Pct', 'Lineout_Win_Pct', 'Scrum_Win_Pct']]

# Replace NaN's with zero
FinalDF.fillna(value=0, inplace=True)

# Write the Dataframe to a CSV to keep a file of initial match output
# FinalDF.to_csv("../data/output/all_Excel_FinalDF_matches.csv", mode='a', header=False, index=False)
FinalDF.to_csv("../data/output/all_Excel_FinalDF_matches_2018-19_matchdata_032920.csv", header=True, index=False)