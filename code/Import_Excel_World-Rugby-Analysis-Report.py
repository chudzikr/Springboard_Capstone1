
# coding: utf-8

# ## Import World Rugby 7s World Series Analysis Reports ##
# Import Analysis Reports (Excel) from each stop on the 2018 7s World Series

# =============================================================================
# TO DO  - 4/25
# Solve "Division by Zero" issue
# Solve Tournament/Match labelling issue (get tournament from file name?)
#  * Tournament name is listed in the file name, as well as the 'Cover Page' tab, rows 12:13       (merged)
#  * Don't think I need match number, but if I needed it, could pull from "match results" tab
# Consolidate column names
# Create Diff calculations
# Add code to read all files in a given directory
# =============================================================================

# In[44]:


# You can use pandas' ExcelFile parse method to read Excel sheets, see io docs:
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

mypath = '/Users/admin/Dropbox/Springboard_DataScience/Capstone1/data/matchdata/2017-18/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Create an empty dataframe with columns to store all appended matches
# BE SURE TO UPDATE WITH NEW COLUMNS
FinalDF = pd.DataFrame()

for i in onlyfiles:
    name = i
    #df = pd.read_excel(mypath + i, sheet_name=0)
    xls = pd.ExcelFile(mypath + i)
    df = xls.parse('Raw Data', skiprows=6, index_col=None, na_values=['NaN'])



    # In[46]:

    df.columns = ['col1', 'Team', 'Opposition', 'Total PointsScored', 'Total PointsConceded', 'Total TriesScored', 'Total TriesConceded', 'Try Scoring Rate(1 every x secs)', 'Try Conceding Rate(1 every x secs)', 'Tries Scored Build-Up(No Ruck/Maul)', 'Tries Conceded Build-Up(No Ruck/Maul)', 'Opp22m Entries', 'Opp22m Entry Rate(1 every  secs)', 'Own22m Entries', 'Own22m Entry Rate(1 every x secs)', 'Tries Scoredper Opp22m Entry', 'Tries Concededper Own22m Entry', 'Possession Time(Own)', 'Possession Time(Opp)', 'Passes', 'Passing Rate(1 every x secs)', 'Rucks Attack', 'Rucking RateAttack (secs)', 'RucksDefence', '% Ruck SuccessOwn', 'Own RucksWon per Match', '% Ruck SuccessOpp', 'Opp RucksWon per Match', 'TurnoversReceived', 'TurnoversConceded', 'TurnoverDifferential', 'OwnContestable Restarts', 'Own ContestableRestarts Regained', 'OppContestable Restarts', 'Opp ContestableRestarts Received', 'Total ScrumsOwn Feed', 'Scrum SuccessOwn Feed', 'Total LineoutsOwn Throw', 'Lineout SuccessOwn Throw', 'Penalty/FKConceded', 'TRM PenaltyConceded', 'Cards']

    # In[47]:
    # drop first column
    df.drop(df.columns[0], axis=1, inplace=True)

    # drop first row
    df.drop([0], inplace=True)

    # Drop unneccessary Average rows
    df = df[df['Team'] != 'Average'] # Remove the 'Average' row
    df = df[df['Team'] != 'Overall Average'] # Remove the 'Average' row


    # In[48]:
    # pseudo: if Team = 'NaN', grab the value from the previous row using .fillna(method='ffill') using forward fill
    # Need to run on only 'Team' column
    df[['Team']] = df[['Team']].fillna(method='ffill')

    # In[51]:
    # Select only matches with the USA playing
    usadf = df.loc[(df['Team'] == 'USA') | (df['Opposition'] == 'USA')]
    # need to combine for for/against or only select USA matches, i.e.,
    # usadf = df.loc[(df['Team'] == 'USA')]
    #usadf

    # ## Calculations/Derivations

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

    # In[ ]:

    # Fill remaining NaNs with 0
    # df[2:31] = df[2:31].fillna(value=0.0)


    # In[52]:

    # ### Column labels ###
    # change col names to match the column names in the PDF import dataframe.

    # =============================================================================
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
    # Try replacing '0 with 'NaN'
    usadf.replace(0, 'NaN', inplace=True)
    usadf = usadf.replace('NaN', np.nan)

    # Calculate conversions
    # used .astype() because values weren't retaining the datatype
    # usadf['Tries'] = usadf['Tries'].astype(int, copy=False)
    #usadf['Tries'] = usadf['Tries'].astype(int, copy=False)
    #usadf['Scores'] = usadf['Scores'].astype(int, copy=False)
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
    usadf['Contestable_Restart_Win_Pct'] =  usadf['Regained'] / usadf['Short']
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

#    # Append each match to FinalDF
#    FinalDF = FinalDF.append(usadf, ignore_index=True)

    # =============================================================================
    # CONDUCT 'DIFF' OPERATIONS, CREATE NEW DATAFRAME
    #
    # Create new dataframe to hold diff values
    #
    # =============================================================================
    # removed 'Date' and 'Match',
    sub = pd.DataFrame(columns=['Opp', 'Tournament', 'Poss_Time_Diff', 'Score_Diff', 'Conv_Diff', 'Tries_Diff', 'Passes_Diff', 'Contestable_KO_Win_pct_Diff', 'PenFK_Against_Diff', 'RuckMaul_Diff', 'Ruck_Win_pct_Diff', 'Cards_diff', 'Lineout_Win_Pct_Diff','Scrum_Win_Pct_Diff'])


    for index, row in FinalDF.iterrows():
         if index % 2 == 0:
            new_row = FinalDF.iloc[index+1]
            if row['Team'] == "USA":
                # Get match, date, etc., values
                opp = new_row['Team']
                #date = new_row['Date']
                tourn = new_row['Tournament']
                # match = new_row['Match']
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

                # Cards
                TotCards = float(row['Yellow_Red Cards']) + float(new_row['Yellow_Red Cards'])
                CardsUSA = float(row['Yellow_Red Cards']*100)/TotCards
                CardsOpp = float(new_row['Yellow_Red Cards']*100)/TotCards
                Cards_diff = CardsUSA - CardsOpp

                # Ruck REtention - already a float/pct
                RuckWin_diff = row['Lineout_Win_Pct'] - new_row['Lineout_Win_Pct']

                # LO Win
                LOWin_diff = row['Ruck_retention'] - new_row['Ruck_retention']

                # Scrum Win Scrum_Win_Pct
                ScrumWin_diff = row['Scrum_Win_Pct'] - new_row['Scrum_Win_Pct']

                # Create a new now with the difference values
                # Add 'Cards_diff' back in later
                sub.loc[index] = (opp, tourn, posess_time_diff, scores_diff, tries_diff, conv_diff, passes_diff, kopct_diff, PenFk_diff, RM_diff, RuckWin_diff, Cards_diff, LOWin_diff, ScrumWin_diff)

            if new_row['Team'] == 'USA':
                # Get match, date, etc., values
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

                # Cards
                TotCards = float(row['Yellow_Red Cards']) + float(new_row['Yellow_Red Cards'])
                CardsUSA = float(new_row['Yellow_Red Cards']*100)/TotCards
                CardsOpp = float(row['Yellow_Red Cards']*100)/TotCards
                Cards_diff = CardsUSA - CardsOpp

                # Ruck REtention - already a float/pct
                RuckWin_diff = new_row['Lineout_Win_Pct'] - row['Lineout_Win_Pct']

                # LO Win
                LOWin_diff = new_row['Ruck_retention'] - row['Ruck_retention']

                # Scrum Win Scrum_Win_Pct
                ScrumWin_diff = new_row['Scrum_Win_Pct'] - row['Scrum_Win_Pct']

                # Create a new now with the difference values
                # Add 'Cards_diff' back in later
                sub.loc[index] = (opp, tourn, posess_time_diff, scores_diff, tries_diff, conv_diff, passes_diff, kopct_diff, PenFk_diff, RM_diff, RuckWin_diff, Cards_diff, LOWin_diff, ScrumWin_diff)


    # Write the Dataframe to a CSV
    #FinalDF.to_csv("../data/output/all_7s_matches.csv", header=True, index=False)

    sub.to_csv("../data/output/final_excel_sub_df.csv", header=True, index=False)

    # Append each match to FinalDF
    #FinalDF = FinalDF.append(usadf, ignore_index=True)
# =============================================================================

# In[54]:

# write dataframe to CSV file
# USe the write mode of 'a' to append
# https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file (see helper function in this page)
# You can append to a csv by opening the file in append mode, then appending a new DF to it
#FinalDF.to_csv(path_or_buf='../data/output/worldrugby_game_analysis_all.csv')
