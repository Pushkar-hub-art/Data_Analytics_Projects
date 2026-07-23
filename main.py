"""
PROJECT IPL 2025 
This file is the single entry point for the project. It imports the
batting and bowling analysis functions from their own files and drives
everything through one menu.

REQUIRED FILES :
- batter_code.py  ->  batting analysis functions
- bowler_code.py  ->  bowling analysis functions
- IPL2025Batters.csv, IPL2025Bowlers.csv 

"""

import pandas as pd

import batter_code as batter_code
import bowler_code as bowler_code



#////////////////////////BATTING FUNCTION/////////////////////////////////


def batting():
    options = {
        1: ("Best batter", batter_code.best_batter),
        2: ("Worst batter", batter_code.worst_player),
        3: ("Best batter in a team", batter_code.highest_team_batter),
        4: ("Worst batter in a team", batter_code.team_worst_batter),
        5: ("Particular player", batter_code.particular_player),
        6: ("Batting awards", batter_code.batter_award),
        7: ("Particular team", batter_code.particular_team),
        8: ("Top N batters (+ chart)", batter_code.top_n_batter),
        9: ("Compare 2 players", batter_code.compare_2_players),
        10: ("Total runs per team (+ chart)", batter_code.team_total_runs),
        11: ("Players above a run threshold", batter_code.player_above_runs),
        12: ("Top N by average", batter_code.top_n_average),
        13: ("Top N by strike rate", batter_code.top_n_sr),
        14: ("Top N by fours", batter_code.top_n_fours),
        15: ("Top N by sixes", batter_code.top_n_sixes),
        16: ("Boundary percentage leaders", batter_code.boundary_percentage),
        17: ("Runs distribution histogram", batter_code.runs_distribution),
        18: ("Impact score ranking", batter_code.consistency_score),
    }

    print("\n---MAKE A CHOICE IN BATTERS---")
    for key, (label, _) in options.items():
        print(f"{key}. {label}")#printing the index and title of function

    batter_choice = int(input("\nEnter a Choice :"))
    if batter_choice not in options:
        print("\nINVALID CHOICE")
        return

    label, func = options[batter_choice]
    output = func()
    if output is not None:
        print(output)




# //////////////////////////////BOWLING FUNCTIONS//////////////

def balling():
    options = {
        1: ("Best bowling figures (BBI)", bowler_code.best_bowler),
        2: ("Most wickets", bowler_code.most_wicket),
        3: ("Best strike rate bowler", bowler_code.best_strick_rate_player),
        4: ("Best economical bowler", bowler_code.best_economical_player),
        5: ("Worst economical (most expensive) bowler", bowler_code.worst_economical_player),
        6: ("Most 4-wicket hauls", bowler_code.most_4_wkt),
        7: ("Most 5-wicket hauls", bowler_code.most_5_wkt),
        8: ("Bowling awards", bowler_code.bowler_award),
        9: ("Particular player", bowler_code.particular_player),
        10: ("Compare 2 bowlers", bowler_code.compare_2_bowlers),
        11: ("Top N wicket takers (+ chart)", bowler_code.top_n_wicket_takers),
        12: ("Best bowler in a team", bowler_code.highest_team_bowler),
        13: ("Worst bowler in a team", bowler_code.team_worst_bowler),
        14: ("Particular team", bowler_code.particular_team),
        15: ("Total wickets per team (+ chart)", bowler_code.team_total_wickets),
        16: ("Bowlers above a wicket threshold", bowler_code.bowler_above_wickets),
        17: ("Top N by economy", bowler_code.top_n_economy),
        18: ("Top N by strike rate", bowler_code.top_n_sr),
        19: ("Top N by 4-wicket hauls", bowler_code.top_n_4w),
        20: ("Top N by 5-wicket hauls", bowler_code.top_n_5w),
        21: ("Wickets distribution histogram", bowler_code.wickets_distribution),
        22: ("Bowling impact score ranking", bowler_code.bowling_impact_score),
    }

    print("\n---MAKE A CHOICE IN BOWLERS---")
    for key, (label, _) in options.items():
        print(f"{key}. {label}")

    choice = int(input("\nEnter a Choice: "))
    if choice not in options:
        print("\nINVALID CHOICE")
        return

    label, func = options[choice]
    output = func()
    if output is not None:
        print(output)


# ///////////////// ALL-ROUNDER ANALYSIS (combines both datasets)///////////////////


def best_all_rounder():
    """
    Builds a composite score from:
      - batting: Runs, AVG, SR (higher is better)
      - bowling: WKT, ECO, SR  (WKT higher is better, ECO/SR lower is better)

    """
    n = int(input("\nEnter number of all-rounders to show: "))
    if n is None:
        return

    bat_df = batter_code.batter[["Player Name", "Team", "Runs", "AVG", "SR"]].copy()
    bowl_df = bowler_code.bowler[["Player Name", "WKT", "ECO", "SR"]].copy()

    bat_df = bat_df.rename(columns={"SR": "Bat_SR"})
    bowl_df = bowl_df.rename(columns={"SR": "Bowl_SR"})

    merged = pd.merge(bat_df, bowl_df, on="Player Name", how="inner")
    #merging on basis of player name and using inner join 

    if merged.empty:
        print("\nNo players found in both batting and bowling datasets.")
        return

    merged["Runs_norm"] = merged["Runs"] / (merged["Runs"].max())
    merged["AVG_norm"] = merged["AVG"] / (merged["AVG"].max())
    merged["BatSR_norm"] = merged["Bat_SR"] / (merged["Bat_SR"].max())
    merged["WKT_norm"] = merged["WKT"] / (merged["WKT"].max())
    merged["ECO_norm"] = 1 - (merged["ECO"] / (merged["ECO"].max()))
    merged["BowlSR_norm"] = 1 - (merged["Bowl_SR"] / (merged["Bowl_SR"].max()))
    #subtracting from 1 as the least the better ..

    merged["All_Rounder_Score"] = (
        merged["Runs_norm"] + merged["AVG_norm"] + merged["BatSR_norm"]
        + merged["WKT_norm"] + merged["ECO_norm"] + merged["BowlSR_norm"]
    ) / 6 * 100
    merged["All_Rounder_Score"] = merged["All_Rounder_Score"].round(1)

    result = merged.sort_values(by="All_Rounder_Score", ascending=False)[
        ["Player Name", "Team", "Runs", "WKT", "All_Rounder_Score"]
    ].head(n)

    print(result)


def team_dashboard():
    """
    Quick side-by-side view - best batting team (most total runs)
    and best bowling team (most total wickets) 
    """
    print("\n--- TOTAL RUNS PER TEAM ---")
    runs = batter_code.team_total_runs()
    print(runs)

    print("\n--- TOTAL WICKETS PER TEAM ---")
    wkts = bowler_code.team_total_wickets()
    print(wkts)



# /////////////////////////MAIN MENU////////////////////////////


def main():
    while True:
        print("\n----MAKE A CHOICE----")
        print("1. Batting")
        print("2. Bowling")
        print("3. Best all-rounder")
        print("4. Team dashboard (best batting team + best bowling team)")
        print("5. Exit")

        choice = int(input("\nEnter a Choice : "))

        if choice == 1:
            batting()
        elif choice == 2:
            balling()
        elif choice == 3:
            best_all_rounder()
        elif choice == 4:
            team_dashboard()
        elif choice == 5:
            print("Exiting......")
            break
        else:
            print("\nINVALID CHOICE, TRY AGAIN")


if __name__ == "__main__":
    main()