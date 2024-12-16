# Main - Setup and Run Simulation
import sys

from scenario_01 import scenario_01
from scenario_02 import scenario_02
from scenario_03 import scenario_03
from scenario_04 import scenario_04
from scenario_05 import scenario_05
from scenario_06 import scenario_06
from scenario_07 import scenario_07

def how_to_run_simulation():
    print("---------------------------------------------")
    print("Scenarios: ")
    print("---------------------------------------------")
    print("  Scenario 1: One Simulation for Each Betting Strategy Analysis (Deterministic)")
    print("  Scenario 2: One Simulation for Each Betting Strategy Analysis with Digital Twin (Deterministic)")
    print("  Scenario 3: Simulation Replications for Player Type Analysis (Non-deterministic)")
    print("  Scenario 4: Simulation Replications for Digital Analysis with Digital Twin (Non-deterministic)")
    print("  Scenario 5: Simulation Replications for Digital Analysis with Digital Twin (Deterministic)")
    print("---------------------------------------------")
    print("Run the simulation with 2 arguments like so:")
    print("$ python3 main.py <scenario_number>")
    print("---------------------------------------------")

def main():
    # Get system arguments
    args = sys.argv

    # Check number of arguments
    if len(args) == 1:
        how_to_run_simulation()
        return

    # Check arguments
    scenario_num = int(args[1])

    # Run simulation
    if scenario_num == 1:
        scenario_01()
    elif scenario_num == 2:
        scenario_02()
    elif scenario_num == 3:
        scenario_03()
    elif scenario_num == 4:
        scenario_04()
    elif scenario_num == 5:
        scenario_05()
    elif scenario_num == 6:
        scenario_06()
    elif scenario_num == 7:
        scenario_07()
    else:
        print("Not Abailable scenario")

if __name__ == "__main__":
    main()
    