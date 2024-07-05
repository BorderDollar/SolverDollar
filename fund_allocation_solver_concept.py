import itertools
import pandas as pd
from datetime import datetime

# define Campaign class that contains information about the campaign
class Campaign:
    def __init__(self, campaign_id, target_amount, interest_rate):
        self.campaign_id = campaign_id
        self.target_amount = target_amount
        self.interest_rate = interest_rate
        self.current_allocation = []
        self.excess_capital = float('inf')

    def optimize_allocation(self, funders):
        best_combination, best_excess = self.find_best_funding_combination(funders)
        self.current_allocation = best_combination
        self.excess_capital = best_excess

    def find_best_funding_combination(self, funders):
        best_combination = []
        best_excess = float('inf')

        for r in range(1, len(funders) + 1):
            for combo in itertools.combinations(funders, r):
                total_funding = sum(funder['amount'] for funder in combo)
                if total_funding >= self.target_amount:
                    excess = total_funding - self.target_amount
                    if excess < best_excess:
                        best_excess = excess
                        best_combination = combo
                    if best_excess == 0:
                        return best_combination, best_excess

        return best_combination, best_excess

# we define the fund solver as a separate Class
class FundSolver:
    def __init__(self):
        # initialize an array of campaigns and funders
        self.campaigns = []
        self.funders = []
        self.funder_allocation_history = []

    def add_campaign(self, campaign_id, target_amount, interest_rate):
        campaign = Campaign(campaign_id, target_amount, interest_rate)
        self.campaigns.append(campaign)

    def add_funder(self, amount):
        funder = {'amount': amount, 'start_time': datetime.now(), 'campaign_id': None}
        self.funders.append(funder)
        self.optimize_all_campaigns()

    def remove_funder(self, amount):
        funder = next((f for f in self.funders if f['amount'] == amount), None)
        if funder:
            self.funders.remove(funder)
            self.optimize_all_campaigns()
        else:
            print(f"Funder with amount {amount} not found.")

    def optimize_all_campaigns(self):
        for campaign in self.campaigns:
            campaign.optimize_allocation(self.funders)
            for funder in self.funders:
                if funder in campaign.current_allocation:
                    if funder['campaign_id'] != campaign.campaign_id:
                        self.update_funder_allocation(funder, campaign.campaign_id)

    def update_funder_allocation(self, funder, new_campaign_id):
        if funder['campaign_id'] is not None:
            duration = (datetime.now() - funder['start_time']).total_seconds()
            self.funder_allocation_history.append({
                'amount': funder['amount'],
                'from_campaign_id': funder['campaign_id'],
                'to_campaign_id': new_campaign_id,
                'start_time': funder['start_time'],
                'end_time': datetime.now(),
                'duration': duration
            })
        funder['campaign_id'] = new_campaign_id
        funder['start_time'] = datetime.now()

    def get_campaign_allocations(self):
        allocations = []
        for campaign in self.campaigns:
            allocations.append({
                "campaign_id": campaign.campaign_id,
                "target_amount": campaign.target_amount,
                "interest_rate": campaign.interest_rate,
                "current_allocation": [funder['amount'] for funder in campaign.current_allocation],
                "excess_capital": campaign.excess_capital
            })
        return allocations

    def get_funder_allocation_history(self):
        return self.funder_allocation_history

# Example usage
solver = FundSolver()

# Add campaigns
solver.add_campaign(campaign_id=1, target_amount=800, interest_rate=5.0)
solver.add_campaign(campaign_id=2, target_amount=1200, interest_rate=7.5)
solver.add_campaign(campaign_id=3, target_amount=1000, interest_rate=15)

# Add funders
solver.add_funder(100)
solver.add_funder(200)
solver.add_funder(300)
solver.add_funder(400)
solver.add_funder(500)
solver.add_funder(300)

# Get current allocations
allocations = solver.get_campaign_allocations()
df_allocations = pd.DataFrame(allocations)
print("Campaign Allocations")
print(df_allocations)

# Remove a funder
solver.remove_funder(300)

# Get current allocations after removal
allocations_after_removal = solver.get_campaign_allocations()
df_allocations_after_removal = pd.DataFrame(allocations_after_removal)
print("Campaign Allocations After Removal")
print(df_allocations_after_removal)

# Get funder allocation history
history = solver.get_funder_allocation_history()
df_history = pd.DataFrame(history)
print("Funder Allocation History")
print(df_history)
