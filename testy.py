def settle_debts(balance_dict):
    creditors = []
    debtors = []

    # Separate creditors and debtors
    for person, balance in balance_dict.items():
        if balance > 0:
            creditors.append((person, balance))
        elif balance < 0:
            debtors.append((person, -balance))  # store as positive for easier calculation

    # Results to store who owes whom
    settlements = []

    i, j = 0, 0

    while i < len(creditors) and j < len(debtors):
        creditor, credit = creditors[i]
        debtor, debt = debtors[j]

        # Determine the amount to be settled in this transaction
        settle_amount = min(credit, debt)

        # Record the settlement
        settlements.append((debtor, creditor, settle_amount))

        # Adjust the remaining balances
        creditors[i] = (creditor, credit - settle_amount)
        debtors[j] = (debtor, debt - settle_amount)

        # Move to the next creditor or debtor if their balance is settled
        if creditors[i][1] == 0:
            i += 1
        if debtors[j][1] == 0:
            j += 1

    return settlements

# Example usage
balance_dict = {
    "geo": -15,
    "jakub": 0,
    "mike": 15
}

settlements = settle_debts(balance_dict)

for debtor, creditor, amount in settlements:
    print(f"{debtor} owes {creditor} ${amount}")
