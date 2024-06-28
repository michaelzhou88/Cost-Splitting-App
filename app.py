import streamlit as st
import pandas as pd


# Initialize session state for users and expenses
if 'users' not in st.session_state:
    st.session_state.users = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []


def split_expenses(expenses):
    balances = {user: 0 for user in st.session_state.users}

    for expense in expenses:
        amount_per_user = expense['amount'] / len(expense['shared_by'])
        for user in expense['shared_by']:
            if user != expense['payer']:
                balances[user] -= amount_per_user
            else: 
                balances[expense['payer']] -= amount_per_user 
            balances[expense['payer']] += amount_per_user     

    return balances


# Streamlit UI
st.title("Tabbed")

# User Management
st.header("Users")
new_user = st.text_input("Add a new user")

if st.button("Add User"):
    if new_user and new_user not in st.session_state.users:
        st.session_state.users.append(new_user)
        st.success(f"User '{new_user}' added.")
    elif new_user in st.session_state.users:
        st.warning(f"User '{new_user}' already exists.")
    else:
        st.warning("Please enter a valid user name.")

if st.session_state.users:
    st.write("Current users:")
    st.write(st.session_state.users)

# Expense Management
st.header("Expenses")
expense_description = st.text_input("Expense description")
expense_amount = st.number_input("Expense amount", min_value=0.0, format="%.2f")
payer = st.selectbox("Paid by", st.session_state.users)
shared_by = st.multiselect("Shared by", st.session_state.users, help="help message")

# New Expense - total payment made for the group 
if st.button("Add New Expense"):
    shared_by = st.multiselect("Shared by", st.session_state.users, default=st.session_state.users)
    if expense_description and expense_amount > 0 and payer and shared_by:
        st.session_state.expenses.append({
            'description': expense_description,
            'amount': expense_amount, 
            'payer': payer,
            'shared_by': shared_by
            })
        st.success(f"Expense '{expense_description}' added.")
    else:
        st.warning("Please complete all fields to add an expense")

if st.session_state.expenses:
    st.write("Current expenses:")
    df_expenses = pd.DataFrame(st.session_state.expenses)
    st.write(df_expenses)

# Calculate and Display Balances
if st.session_state.users and st.session_state.expenses:
    st.header("Balances")
    balances = split_expenses(st.session_state.expenses)
    
    st.write("Total amount per user:")
    st.write(balances)

if st.button("Settle Up Payments"):
    st.write("balances")
        