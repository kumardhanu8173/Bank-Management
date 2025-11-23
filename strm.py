import streamlit as st
import json
from pathlib import Path
import random
import string

###########============python -m streamlit run strm.py================###################
# ===================== CONFIG =====================
st.set_page_config(page_title="MyBank", page_icon="🏦", layout="centered")
st.title("🏦 MyBank - Simple Banking System")

DATABASE = "database.json"

# ===================== DATA HANDLING =====================


def load_data():
    """Load data safely. If file is empty or corrupted, return empty list."""
    if Path(DATABASE).exists():
        try:
            with open(DATABASE, 'r') as f:
                content = f.read().strip()
                if content == "":
                    return []
                return json.loads(content)
        except:
            return []
    return []


def save_data(data):
    with open(DATABASE, 'w') as f:
        json.dump(data, f, indent=4)


def generate_account_no():
    alpha = random.choices(string.ascii_uppercase, k=5)
    digits = random.choices(string.digits, k=4)
    chars = alpha + digits
    random.shuffle(chars)
    return "".join(chars)


# Load data
if "bank_data" not in st.session_state:
    st.session_state.bank_data = load_data()

data = st.session_state.bank_data

# ===================== HELPER FUNCTION =====================


def find_user(acc_no, pin):
    for user in data:
        if user.get("Account No.") == acc_no and user.get("pin") == pin:
            return user
    return None


# ===================== SIDEBAR MENU =====================
st.sidebar.title("Menu")
choice = st.sidebar.selectbox("Choose Action", [
    "Create Account",
    "Deposit Money",
    "Withdraw Money",
    "View Details",
    "Update Details",
    "Delete Account"
])

# ===================== CREATE ACCOUNT =====================
if choice == "Create Account":
    st.header("🆕 Create New Account")
    with st.form("create_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number (10 digits)")
        pin = st.text_input("Set 4-digit PIN", type="password", max_chars=4)

        submitted = st.form_submit_button("Create Account")
        if submitted:
            if not all([name, email, phone, pin]):
                st.error("All fields are required!")
            elif len(phone) != 10 or not phone.isdigit():
                st.error("Phone must be exactly 10 digits")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("PIN must be exactly 4 digits")
            else:
                acc_no = generate_account_no()
                new_user = {
                    "name": name,
                    "email": email,
                    "phone No.": int(phone),
                    "pin": int(pin),
                    "Account No.": acc_no,
                    "balance": 0
                }
                data.append(new_user)
                save_data(data)
                st.success(f"Account Created Successfully!")
                st.info(f"Your Account Number: {acc_no}\nSave it safely!")
                st.balloons()

# ===================== DEPOSIT MONEY =====================
elif choice == "Deposit Money":
    st.header("💰 Deposit Money")
    with st.form("deposit_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input(
            "Amount to Deposit (₹)", min_value=1, max_value=10000)

        submitted = st.form_submit_button("Deposit")
        if submitted:
            user = find_user(acc_no, int(pin)) if pin.isdigit() else None
            if not user:
                st.error("Invalid Account Number or PIN")
            else:
                user["balance"] += amount
                save_data(data)
                st.success(f"₹{amount} deposited successfully!")
                st.write(f"New Balance: ₹{user['balance']}")

# ===================== WITHDRAW MONEY =====================
elif choice == "Withdraw Money":
    st.header("💸 Withdraw Money")
    with st.form("withdraw_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input(
            "Amount to Withdraw (₹)", min_value=1, max_value=10000)

        submitted = st.form_submit_button("Withdraw")
        if submitted:
            user = find_user(acc_no, int(pin)) if pin.isdigit() else None
            if not user:
                st.error("Invalid Account Number or PIN")
            elif amount > user["balance"]:
                st.error(
                    f"Insufficient balance! Available: ₹{user['balance']}")
            else:
                user["balance"] -= amount
                save_data(data)
                st.success(f"₹{amount} withdrawn successfully!")
                st.write(f"Remaining Balance: ₹{user['balance']}")

# ===================== VIEW DETAILS =====================
elif choice == "View Details":
    st.header("👀 View Account Details")
    with st.form("details_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)

        submitted = st.form_submit_button("Show Details")
        if submitted:
            user = find_user(acc_no, int(pin)) if pin.isdigit() else None
            if not user:
                st.error("Invalid Account Number or PIN")
            else:
                st.success("Account Found!")
                st.json(user)

# ===================== UPDATE DETAILS =====================
elif choice == "Update Details":
    st.header("✏ Update Account Details")
    with st.form("update_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("Current PIN", type="password", max_chars=4)

        new_name = st.text_input("New Name")
        new_email = st.text_input("New Email")
        new_phone = st.text_input("New Phone (10 digits)")
        new_pin = st.text_input("New PIN (4 digits)",
                                type="password", max_chars=4)

        submitted = st.form_submit_button("Update Details")
        if submitted:
            user = find_user(acc_no, int(pin)) if pin.isdigit() else None
            if not user:
                st.error("Invalid Account Number or PIN")
            else:
                if new_name:
                    user["name"] = new_name
                if new_email:
                    user["email"] = new_email
                if new_phone.isdigit() and len(new_phone) == 10:
                    user["phone No."] = int(new_phone)
                if new_pin.isdigit() and len(new_pin) == 4:
                    user["pin"] = int(new_pin)

                save_data(data)
                st.success("Details updated successfully!")

# ===================== DELETE ACCOUNT =====================
elif choice == "Delete Account":
    st.header("🗑 Delete Account")
    with st.form("delete_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        confirm = st.checkbox("I understand this cannot be undone")

        submitted = st.form_submit_button("Delete Account")
        if submitted:
            if not confirm:
                st.error("Please confirm deletion")
            else:
                user = find_user(acc_no, int(pin)) if pin.isdigit() else None
                if not user:
                    st.error("Invalid Account Number or PIN")
                else:
                    data.remove(user)
                    save_data(data)
                    st.error("Account deleted permanently!")

# ===================== FOOTER =====================
st.sidebar.markdown("---")
st.sidebar.info(f"Total Accounts: {len(data)}")
st.caption("Simple Banking System • Built with ❤ using Streamlit")