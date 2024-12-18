# roulette_game

## Overview

This project involves simulating the game of roulette to explore its mathematical foundations and player behavior. Roulette offers a fascinating study of randomness, decision-making, and the psychological dynamics of gambling. The study aims to examine how betting strategies can impact player outcomes and financial sustainability while addressing gambling behaviors.

## Project Goals

- **Simulating three types of players:** one with addictive tendencies (High-risk player), one with rational decision-making (Moderate-risk player), and one with a cautious safety-first strategy (Low-risk player).
- **Analyzing the impact of different betting strategies on player outcomes.**
- **Proposing actionable recommendations tailored to player behavior,** such as cashing out, reducing bet amounts, or skipping rounds to promote sustainable gambling.
- **Introducing a digital twin to enhance analytical depth,** by modeling controlled variations in strategies, game conditions, and player behaviors in a risk-free environment.

## Features

- **Betting Strategies:** Martingale, Fibonacci, D'Alembert, Flat, and All-In.
- **Placement Strategies:** Single Number, Dozens, and Red/Black.
- **Player Profiles:** High-risk, Moderate-risk, and Low-risk players.
- **Digital Twin Simulation:** Simulates a replica player mirroring the betting strategy of the original player.
- **Scenarios:** Predefined scenarios to analyze strategies and outcomes under different conditions.
- **Statistical Reporting:** Generates detailed reports on player performance, house profits, and simulation results.

## File Structure

### Project Root

```
ROULETTE_GAME/
│
├── results/                # Simulation outputs and reports
│   ├── Game_Report_High_Risk_All-In_<date>.txt
│   ├── Game_Report_High_Risk_Martingale_<date>.txt
│   ├── Game_Report_Low_Risk_Dalembert_<date>.txt
│   ├── Game_Report_Low_Risk_Flat-Bet_<date>.txt
│   ├── Game_Report_Moderate_Risk_Fibonacci_<date>.txt
│   ├── Game_Report_Moderate_Risk_Martingale_<date>.txt
│   ├── Game_Report_Plot_<date>.png
│
├── results_examples/       # Organized example reports
│   ├── results_scenario_01/
│   ├── results_scenario_02/
│   ├── results_scenario_03/
│   ├── results_scenario_04/
│   └── results_scenario_05/
│
├── src/                    # Source code
│   ├── betting_strategy.py
│   ├── constants.py
│   ├── main.py
│   ├── placement_strategy.py
│   ├── player.py
│   ├── random_num_gen.py
│   ├── report_generator.py
│   ├── roulette_game.py
│   ├── roulette_simulation_report.py
│   ├── roulette_simulator.py
│   ├── roulette_wheel.py
│   ├── scenario_01.py
│   ├── scenario_02.py
│   ├── scenario_03.py
│   ├── scenario_04.py
│   ├── scenario_05.py
│   └── test_random_num_gen.py
│
└── README.md
```

## Quick Start

1. **Clone the Repository** Download the project and navigate into the main directory:
   ```bash
   git clone <repository_url>
   cd ROULETTE_GAME
   ```

2. **Ensure Dependencies are Installed** This project requires Python 3.8+ and the following libraries:
    - matplotlib
    - numpy
   ```bash
   pip install matplotlib numpy
    ```
3. **Navigate to the Source Code Directory**
   Move into the `src/` folder where the main code resides:
   ```bash
   cd src
   ```

4. **Run the Simulation**
   Execute the `main.py` file to display instructions:
   ```bash
   python3 main.py
   ```

5. **Run a Specific Scenario**
   Replace `<scenario_number>` with the desired scenario (1 to 5):
   ```bash
   python3 main.py 1
   ```

6. **View Results**
   After running a simulation, results are generated in the `results/` directory. 
   Pre-generated results can be found in `results_examples/`.

## Scenarios

### Scenario 1: One Simulation for Each Betting Strategy Analysis (Deterministic)  
A single simulation is performed for each betting strategy. This deterministic approach ensures consistent outcomes for given initial conditions, allowing for an analysis of expected strategy performance.



### Scenario 2: One Simulation for Each Betting Strategy Analysis with Digital Twin (Deterministic)  
Similar to Scenario 1, but incorporates a *digital twin*, a virtual representation of the roulette system that mirrors the physical behavior. The deterministic nature ensures precise and repeatable comparisons between the real system and the digital twin.



### Scenario 3: Simulation Replications for Player Type Analysis (Non-deterministic)  
Focuses on analyzing the behavior of different player types (e.g., conservative, aggressive, random bettors) through multiple simulation replications. Randomness is introduced to simulate real-world variability, capturing stochastic outcomes for diverse strategies.



### Scenario 4: Simulation Replications for Digital Analysis with Digital Twin (Non-deterministic)  
Combines simulation replications with the use of a *digital twin*. Randomness is introduced in the simulations to account for variability, while the digital twin provides a means to validate its accuracy in modeling real-world randomness.



### Scenario 5: Simulation Replications for Digital Analysis with Digital Twin (Deterministic)  
Multiple deterministic replications are performed using a *digital twin*. This setup ensures consistent outcomes for each replication, allowing controlled experimentation to refine the digital twin and evaluate its reliability.

### Scenario 6: Variance Reduction
This scenario focuses on the implementation of Common Random Number variance reduction method. It uses Moderate-risk player and compares Martingale and Fibonacci strategies.

## Scenario 7: Variance Reduction
Antithetic variance reduction method. Implemented for Low-risk and Moderate-risk player.

## Reporting

Reports include:

- Player performance: initial bankroll, final bankroll, profit, rounds played.
- House profit: total profit/loss over simulations.
- Statistical metrics: mean, variance, and confidence intervals.
