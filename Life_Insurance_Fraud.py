import csv
from datetime import datetime
from collections import defaultdict

def fraud_summary(file_path):
    claims = []

    # Read and parse the CSV file
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert string dates to datetime objects
            row['policy_start'] = datetime.strptime(row['policy_start'], '%Y-%m-%d')
            row['claim_date'] = datetime.strptime(row['claim_date'], '%Y-%m-%d')
            # Convert claim amount to float
            row['claim_amount'] = float(row['claim_amount'])
            claims.append(row)

    # Flag claims filed within 30 days of policy start
    flagged_early = [c for c in claims if (c['claim_date'] - c['policy_start']).days < 30]

    # Flag claims with amount above $100,000
    flagged_large = [c for c in claims if c['claim_amount'] > 100000]

    # Group claims by policy number to check multiple claims within 90 days
    claims_by_policy = defaultdict(list)
    for c in claims:
        claims_by_policy[c['policy_number']].append(c)

    flagged_multiple = []
    for policy, clist in claims_by_policy.items():
        # Sort claims by date for each policy
        clist_sorted = sorted(clist, key=lambda x: x['claim_date'])
        for i in range(len(clist_sorted) - 1):
            delta = (clist_sorted[i+1]['claim_date'] - clist_sorted[i]['claim_date']).days
            if delta <= 90:
                flagged_multiple.append(policy)
                break

    # Print summary report
    print("Fraud Summary Report:")
    print(f"Claims filed within 30 days of policy start: {len(flagged_early)}")
    print(f"Claims with amount above $100,000: {len(flagged_large)}")
    print(f"Policies with multiple claims within 90 days: {len(flagged_multiple)}")

if __name__ == "__main__":
    # Replace 'claims_sample.csv' with your actual CSV file path
    fraud_summary('claims_sample.csv')
