
# IPL 2025 - BATTERS DATA ANALYSIS
# Uses: pandas, numpy, matplotlib

"""
Columns in CSV :
"Player Name","Team","Matches","Inn","No","Runs","HS",
"AVG","BF","SR","100s","50s","4s","6s"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


try:
    batter = pd.read_csv("IPL2025Batters.csv")
except FileNotFoundError:
    raise SystemExit(
        "ERROR: 'IPL2025Batters.csv' not found. "
        "Keep the CSV in the same folder as this script."
    )





# ///////////////////////INDIVIDUAL BATTER ANALYSIS


def best_batter():
    
    best = batter.loc[batter["AVG"].idxmax()]
    return best


def worst_player():
    """
    Returns the batter with the LOWEST batting average.
    """
    worst = batter.loc[batter["AVG"].idxmin()]
    return worst


def batter_award():
    
    print("\n1. Orange cap")
    print("2. Best strike rate")
    print("3. Most 4s")
    print("4. Most 6s")
    print("5. Boundary king")
    print("6. Highest individual score")
    print("7. 50s king")
    print("8. Century king")

    try:
        num = int(input("\nCHOOSE THE INDEX OF THE AWARD: "))
    except ValueError:
        print("\nPLEASE ENTER A VALID NUMBER")
        return None

    if num == 1:
        return batter.loc[batter['Runs'].idxmax()]
    elif num == 2:
        batter['BST'] = (batter["Runs"] / batter["BF"]) * 100
        return batter.loc[batter['BST'].idxmax()]
    elif num == 3:
        return batter.loc[batter['4s'].idxmax()]
    elif num == 4:
        return batter.loc[batter['6s'].idxmax()]
    elif num == 5:
        batter["Boundaries"] = batter['4s'] + batter["6s"]
        return batter.loc[batter["Boundaries"].idxmax()]
    elif num == 6:
        return batter.loc[batter['HS'].idxmax()]
    elif num == 7:
        return batter.loc[batter["50s"].idxmax()]
    elif num == 8:
        return batter.loc[batter["100s"].idxmax()]
    else:
        print("\nPLEASE ENTER A VALID INDEX (1-8)")
        return None


def particular_player():
    """
    Accepts a player name and displays that player's row.
    """
    player_name = input("\nENTER PLAYER NAME: ").strip()
    player_data = batter[batter['Player Name'].str.lower() == player_name.lower()]

    if player_data.empty:
        print("\nPLAYER NOT FOUND. Check spelling and try again.")
        return None

    return player_data


def top_n_batter():
    """
    Shows top N run scorers, both as a bar chart and a dataframe.
    """
    n = int(input("\nEnter number of players you want to check for: "))

    top_players = batter.sort_values(by="Runs", ascending=False)
    n_player = top_players.head(n)

    plt.figure(figsize=(10, 5))
    plt.bar(x=n_player["Player Name"], height=n_player["Runs"], label="Runs per player")
    plt.xlabel("Player Name")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Total Runs")
    plt.title(f"Top {n} Run Scorers - IPL 2025")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return top_players[["Player Name", "Runs"]].head(n)


def compare_2_players():
    """
    Compares two players head-to-head across key stats and
    prints a per-stat winner.

    < and > — you've got these right:

    {value:<n} → left-align, pad with spaces on the right (so left edge stays fixed)
    {value:>n} → right-align, pad with spaces on the left (so right edge stays fixed)

    Center is ^, not =:

    {value:^n} → center-align, padding split roughly evenly on both sides
    """
    p1 = input("\nENTER NAME OF PLAYER 1: ").strip()
    p2 = input("\nENTER NAME OF PLAYER 2: ").strip()

    player1 = batter[batter["Player Name"].str.lower() == p1.lower()]
    player2 = batter[batter["Player Name"].str.lower() == p2.lower()]

    if player1.empty or player2.empty:
        missing = p1 if player1.empty else p2
        print(f"\nPLAYER '{missing}' NOT FOUND. Check spelling and try again.")
        return

    stats = ["Runs", "AVG", "SR", "100s", "50s", "4s", "6s"]

    print(f"\nStat        {p1:<15}{p2:<15}")
    for stat in stats:
        print(f"{stat:<12}{player1.iloc[0][stat]:<15}{player2.iloc[0][stat]:<15}")

    print("\n---WINNER PER STAT---\n")
    for stat in stats:
        v1, v2 = player1.iloc[0][stat], player2.iloc[0][stat]
        if v1 == v2:
            print(f"{stat}: TIE")
        elif v1 > v2:
            print(f"{stat}: winner -> {p1}")
        else:
            print(f"{stat}: winner -> {p2}")



# ///////////////////TEAM ANALYSIS/////////////////////////////


def highest_team_batter():
    """
    Accepts a team name and returns the best batter (by AVG) in that team.
    """
    team_name = input("Enter team: ").upper()
    team_player = batter[batter["Team"] == team_name]

    if team_player.empty:
        print("\nTEAM NOT FOUND.")
        return None

    return team_player.loc[team_player['AVG'].idxmax()]


def team_worst_batter():
    """
    Accepts a team name and returns the worst batter (by AVG) in that team.
    """
    team_name = input("Enter team: ").upper()
    team_player = batter[batter["Team"] == team_name]

    if team_player.empty:
        print("\nTEAM NOT FOUND.")
        return None

    return team_player.loc[team_player['AVG'].idxmin()]


def particular_team():
    """
    Accepts a team name and displays every batter from that team.
    """
    team_name = input("\nENTER TEAM NAME: ").upper()
    team_data = batter[batter['Team'] == team_name]

    if team_data.empty:
        print("\nTEAM NOT FOUND.")
        return None

    return team_data


def team_total_runs():
    """
    Shows total runs scored by each team (sum across all their batters)
    """
    team_runs = (
        batter.groupby("Team")["Runs"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 5))
    plt.bar(team_runs.index, team_runs.values, color="teal")
    plt.xlabel("Team")
    plt.ylabel("Total Runs (all batters combined)")
    plt.title("Total Runs Scored Per Team - IPL 2025")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    return team_runs



# /////////////////RANGE OF PLAYERS///////////////////


def player_above_runs():
    r = int(input("\nENTER RUNS ABOVE WHICH YOU WANT TO CHECK: "))
    player_above_r = batter[batter["Runs"] >= r]
    return player_above_r[["Player Name", "Team", "Runs"]]


def top_n_average():
    """Display top N batters based on batting average."""
    n = int(input("\nENTER N: "))
    return batter.sort_values(by="AVG", ascending=False)[
        ["Player Name", "Team", "AVG", "Runs", "SR"]
    ].head(n)


def top_n_sr():
    """Display top N batters based on Strike Rate."""
    n = int(input("\nENTER N: "))
    return batter.sort_values(by="SR", ascending=False)[
        ["Player Name", "Team", "SR", "Runs", "AVG"]
    ].head(n)


def top_n_fours():
    """Display top N batters having most fours."""
    n = int(input("\nENTER N: "))
    return batter.sort_values(by="4s", ascending=False)[
        ["Player Name", "Team", "4s", "Runs", "AVG"]
    ].head(n)


def top_n_sixes():
    """Display top N batters having most sixes."""
    n = int(input("\nENTER N: "))
    return batter.sort_values(by="6s", ascending=False)[
        ["Player Name", "Team", "6s", "Runs", "AVG"]
    ].head(n)





# ///////////////////VISUAL ANALYSIS//////////////////////


def boundary_percentage():
    """
    What % of a player's total runs came from boundaries (4s and 6s)?
    """
    n = int(input("\nENTER N: "))

    temp = batter.copy()
    temp["Boundary_Runs"] = temp["4s"] * 4 + temp["6s"] * 6
    temp["Boundary_%"] = (temp["Boundary_Runs"] / temp["Runs"]) * 100
    temp = temp.replace(np.inf, np.nan).dropna(subset=["Boundary_%"])
    """
    in the upper line of code we made use of 2 functions 
    .replace (old , new )--> replace / swap values ... 
        - here old values means +ve or -ve infinity values as runs might be 0 and lead to inifinity values
        - a set of old values can be matches using [ a,b,c] , either of a b c can be replaced with new value
    .dropna() --> drops the row / value which holds nan(not a number) values 
        -subset=[] --> helps to only check specific column instead of all columns 
    """

    result = temp.sort_values(by="Boundary_%", ascending=False)[
        ["Player Name", "Team", "Runs", "Boundary_Runs", "Boundary_%"]
    ].head(n)

    result["Boundary_%"] = result["Boundary_%"].round(1)#rounding off to 1 number after decimal point
    return result


def runs_distribution():
    """
    Histogram showing how runs are distributed across ALL batters
    in the tournament
    """
    plt.figure(figsize=(9, 5))
    plt.hist(batter["Runs"], bins=20, color="orange", edgecolor="black")
    plt.xlabel("Runs Scored")
    plt.ylabel("Number of Players")
    plt.title("Distribution of Runs Across All Batters - IPL 2025")
    plt.tight_layout()
    plt.show()




def consistency_score():
    """
    A simple composite 'impact score' combining AVG and SR
    """
    n = int(input("\nENTER N: "))

    temp = batter.copy()
    temp["AVG_norm"] = temp["AVG"] / temp["AVG"].max()
    temp["SR_norm"] = temp["SR"] / temp["SR"].max()
    temp["Impact_Score"] = ((temp["AVG_norm"] + temp["SR_norm"]) / 2 * 100).round(1)

    return temp.sort_values(by="Impact_Score", ascending=False)[
        ["Player Name", "Team", "AVG", "SR", "Impact_Score"]
    ].head(n)


