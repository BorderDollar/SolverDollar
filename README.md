# BorderDollar Fund Allocation Solver - SolverDollar

## Overview

The Fund Allocation Solver is a Python script designed to optimize the allocation of funds across multiple campaigns. Each campaign has a target funding amount and an interest rate. The solver ensures that funders are allocated to campaigns in a way that meets the campaign targets with minimal excess capital. Additionally, it tracks the history of funder allocations, including the duration each funder spends in a campaign before being reallocated.

## Features

- Add multiple campaigns with specific target amounts and interest rates.
- Add funders with unique IDs and contribution amounts.
- Optimize fund allocation across campaigns to minimize excess capital.
- Track and update funder allocations dynamically.
- Log the history of funder allocations, including the transition between campaigns and the duration of each allocation.

## Requirements

- Python 3.x
- Pandas library

You can install the required library using pip:

```sh
pip install pandas
