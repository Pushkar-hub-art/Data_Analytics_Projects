# IPL 2025 - BOWLERS DATA ANALYSIS
# Uses: pandas, numpy, matplotlib
"""
Columns/ Heading :

Player Name","Team","Matches","Inn","Overs","Runs",
"WKT","BBI","AVG","ECO","SR","4W","5W"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


try:
    bowler = pd.read_csv("IPL2025Bowlers.csv")
except FileNotFoundError:
    raise SystemExit(
        "ERROR: 'IPL2025Bowlers.csv' not found. "
        "Keep the CSV in the same folder as this script."
    )



#////////////////////// INDIVIDUAL BOWLER ANALYSIS/////////////


def best_bowler():
    """
    Returns the bowler with the best single-innings bowling figures (BBI),
    e.g. "4/18" is better than "3/10".

    BBI format is "wickets/runs" (e.g. "3/24" = 3 wickets for 24 runs).
    """
    split_cols = bowler['BBI'].str.split('/', expand=True)
    bowler['Wickets_BBI'] = split_cols[0].astype(int)
    bowler['Runs_BBI'] = split_cols[1].astype(int)

    # More wickets is better; if tied on wickets, fewer runs conceded is better
    sorted_bowlers = bowler.sort_values(
        by=['Wickets_BBI', 'Runs_BBI'],
        ascending=[False, True]
    )

    return sorted_bowlers.iloc[0]


def most_wicket():
    """Returns the bowler with the most wickets (Purple Cap contender)."""
    most_wkt_player = bowler.loc[bowler["WKT"].idxmax()]
    return most_wkt_player


def best_economical_player():
    """Returns the bowler with the best (lowest) economy rate."""
    BEP = bowler.sort_values(by="ECO", ascending=True)
    return BEP.iloc[0]


def worst_economical_player():
   
    WEP = bowler.sort_values(by="ECO", ascending=False)
    return WEP.iloc[0]


def best_strick_rate_player():
    """Returns the bowler with the best (lowest) bowling strike rate."""
    BSRP = bowler["SR"].idxmin()  # FIX: lower SR is better for bowlers, so idxmin, not idxmax
    return bowler.loc[BSRP]


def most_4_wkt():
    """Returns the bowler with the most 4-wicket hauls."""
    M4W = bowler["4W"].idxmax()
    return bowler.loc[M4W]


def most_5_wkt():
    """Returns the bowler with the most 5-wicket hauls."""
    M5W = bowler["5W"].idxmax()
    return bowler.loc[M5W]


def bowler_award():
    
    print("\n1. Purple cap (most wickets)")
    print("2. Best economy")
    print("3. Most 4-wicket hauls")
    print("4. Most 5-wicket hauls")
    print("5. Best strike rate")
    print("6. Best bowling figures (BBI)")

    try:
        num = int(input("\nCHOOSE THE INDEX OF THE AWARD: "))
    except ValueError:
        print("\nPLEASE ENTER A VALID NUMBER")
        return None

    if num == 1:
        return most_wicket()
    elif num == 2:
        return best_economical_player()
    elif num == 3:
        return most_4_wkt()
    elif num == 4:
        return most_5_wkt()
    elif num == 5:
        return best_strick_rate_player()
    elif num == 6:
        return best_bowler()
    else:
        print("\nPLEASE ENTER A VALID INDEX (1-6)")
        return None


def particular_player():
    """
    Accepts a bowler name and displays that player's row.
   
    """
    player_name = input("\nENTER PLAYER NAME: ").strip()
    player_data = bowler[bowler['Player Name'].str.lower() == player_name.lower()]

    if player_data.empty:
        print("\nPLAYER NOT FOUND. Check spelling and try again.")
        return None

    return player_data


def compare_2_bowlers():
    """
    Compares two bowlers head-to-head across key stats and
    prints a per-stat winner. 
    """
    p1 = input("\nENTER NAME OF PLAYER 1: ").strip()
    p2 = input("\nENTER NAME OF PLAYER 2: ").strip()

    player1 = bowler[bowler["Player Name"].str.lower() == p1.lower()]
    player2 = bowler[bowler["Player Name"].str.lower() == p2.lower()]

    if player1.empty or player2.empty:
        missing = p1 if player1.empty else p2
        print(f"\nPLAYER '{missing}' NOT FOUND. Check spelling and try again.")
        return

    # stat: True if HIGHER is better, False if LOWER is better
    stats = {
        "WKT": True,
        "ECO": False,
        "SR": False,
        "AVG": False,
        "4W": True,
        "5W": True,
    }

    print(f"\nStat        {p1:<15}{p2:<15}")
    for stat in stats:
        print(f"{stat:<12}{player1.iloc[0][stat]:<15}{player2.iloc[0][stat]:<15}")

    print("\n---WINNER PER STAT---\n")
    for stat, higher_is_better in stats.items():
        v1, v2 = player1.iloc[0][stat], player2.iloc[0][stat]
        if v1 == v2:
            print(f"{stat}: TIE")
        elif (v1 > v2) == higher_is_better:
            print(f"{stat}: winner -> {p1}")
        else:
            print(f"{stat}: winner -> {p2}")


def top_n_wicket_takers():
    """
    Shows top N wicket takers, both as a bar chart and a dataframe.
    """
    n = int(input("\nEnter number of players you want to check for: "))

    top_bowlers = bowler.sort_values(by="WKT", ascending=False)
    n_player = top_bowlers.head(n)

    plt.figure(figsize=(10, 5))
    plt.bar(x=n_player["Player Name"], height=n_player["WKT"], label="Wickets per player", color="crimson")
    plt.xlabel("Player Name")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Total Wickets")
    plt.title(f"Top {n} Wicket Takers - IPL 2025")
    plt.legend()
    plt.tight_layout()# is used to automatically adjust your plot's subplots and margins so that labels, titles, and axes do not overlap.
    plt.show()

    return top_bowlers[["Player Name", "WKT"]].head(n)



# /////////////////////TEAM ANALYSIS////////////////


def highest_team_bowler():
    """
    Accepts a team name and returns the best bowler (by wickets)
    in that team.
    """
    team_name = input("Enter team: ").upper()
    team_player = bowler[bowler["Team"] == team_name]

    if team_player.empty:
        print("\nTEAM NOT FOUND.")
        return None

    return team_player.loc[team_player['WKT'].idxmax()]


def team_worst_bowler():
    """
    Accepts a team name and returns the worst bowler (highest economy)
    in that team.
    """
    team_name = input("Enter team: ").upper()
    team_player = bowler[bowler["Team"] == team_name]

    if team_player.empty:
        print("\nTEAM NOT FOUND.")
        return None

    return team_player.loc[team_player['ECO'].idxmax()]


def particular_team():
    """
    Accepts a team name and displays every bowler from that team.
    """
    team_name = input("\nENTER TEAM NAME: ").upper()
    team_data = bowler[bowler['Team'] == team_name]

    if team_data.empty:
        print("\nTEAM NOT FOUND.")
        return None

    return team_data


def team_total_wickets():
    """
    Shows total wickets taken by each team (sum across all their
    bowlers)
    """
    team_wkts = (
        bowler.groupby("Team")["WKT"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 5))
    plt.bar(team_wkts.index, team_wkts.values, color="darkred")
    plt.xlabel("Team")
    plt.ylabel("Total Wickets (all bowlers combined)")
    plt.title("Total Wickets Taken Per Team - IPL 2025")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    return team_wkts



# //////////////RANGE OF PLAYERS////////////////




def bowler_above_wickets():
    """ Lists bowlers with wickets at or above a given value/threshould."""
    w = int(input("\nENTER WICKETS ABOVE WHICH YOU WANT TO CHECK: "))
    bowler_above_w = bowler[bowler["WKT"] >= w]
    return bowler_above_w[["Player Name", "Team", "WKT"]]


def top_n_economy():
    """Top N most economical bowlers (lowest ECO)."""
    n = int(input("\nENTER N: "))
    return bowler.sort_values(by="ECO", ascending=True)[
        ["Player Name", "Team", "ECO", "WKT", "SR"]
    ].head(n)


def top_n_sr():
    """Top N bowlers by best (lowest) strike rate."""
    n = int(input("\nENTER N: "))
    return bowler.sort_values(by="SR", ascending=True)[
        ["Player Name", "Team", "SR", "WKT", "ECO"]
    ].head(n)


def top_n_4w():
    """Top N bowlers by most 4-wicket hauls."""
    n = int(input("\nENTER N: "))
    return bowler.sort_values(by="4W", ascending=False)[
        ["Player Name", "Team", "4W", "WKT"]
    ].head(n)


def top_n_5w():
    """Top N bowlers by most 5-wicket hauls."""
    n = int(input("\nENTER N: "))
    return bowler.sort_values(by="5W", ascending=False)[
        ["Player Name", "Team", "5W", "WKT"]
    ].head(n)



# //////////// VISUAL ANALYSIS//////////////

def wickets_distribution():
    """
    Histogram showing how wickets are distributed across ALL
    bowlers in the tournament
    """
    plt.figure(figsize=(9, 5))
    plt.hist(bowler["WKT"], bins=20, color="steelblue", edgecolor="black")
    plt.xlabel("Wickets Taken")
    plt.ylabel("Number of Bowlers")
    plt.title("Distribution of Wickets Across All Bowlers - IPL 2025")
    plt.tight_layout()
    plt.show()




def bowling_impact_score():
    """
    A simple composite score combining wickets taken, economy, and
    strike rate (all normalized 0-1, with ECO/SR inverted since lower

    """
    n = int(input("\nENTER N: "))

    temp = bowler.copy()
    temp["WKT_norm"] = temp["WKT"] / temp["WKT"].max()
    temp["ECO_norm"] = 1 - (temp["ECO"] / temp["ECO"].max())
    temp["SR_norm"] = 1 - (temp["SR"] / temp["SR"].max())
    temp["Impact_Score"] = (
        (temp["WKT_norm"] + temp["ECO_norm"] + temp["SR_norm"]) / 3 * 100
    ).round(1)

    return temp.sort_values(by="Impact_Score", ascending=False)[
        ["Player Name", "Team", "WKT", "ECO", "SR", "Impact_Score"]
    ].head(n)


