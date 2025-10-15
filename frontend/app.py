import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# ---------------------
# Session state
# ---------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page_reload" not in st.session_state:
    st.session_state.page_reload = False

# ---------------------
# Handle page reload
# ---------------------
if st.session_state.page_reload:
    st.session_state.page_reload = False
    st.experimental_rerun = lambda: None  # Dummy for backward compatibility

# ---------------------
# LOGIN / REGISTER
# ---------------------
if not st.session_state.user:
    st.title("🔐 Login or Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username.strip() == "" or password.strip() == "":
                st.error("Please enter username and password.")
            else:
                try:
                    res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
                    res.raise_for_status()
                    st.session_state.user = res.json()
                    st.success(f"Welcome {st.session_state.user['username']}!")
                    st.session_state.page_reload = True
                    st.stop()  # Stop and rerun
                except Exception as e:
                    st.error(f"Login failed: {e}")

    with tab2:
        username = st.text_input("New Username", key="reg_user")
        password = st.text_input("New Password", type="password", key="reg_pass")
        role = st.selectbox("Role", ["student", "admin"])
        if st.button("Register"):
            if username.strip() == "" or password.strip() == "":
                st.error("Please enter username and password.")
            else:
                try:
                    res = requests.post(
                        f"{API_URL}/register",
                        json={"username": username, "password": password, "role": role},
                    )
                    res.raise_for_status()
                    st.success("Registration successful! You can now login.")
                except Exception as e:
                    st.error(f"Registration failed: {e}")

    st.stop()

# ---------------------
# DASHBOARD AFTER LOGIN
# ---------------------
user = st.session_state.user
st.sidebar.title(f"Welcome, {user['username']} 👋 ({user['role']})")

# Admin sees all records, student sees own
if user["role"] == "student":
    section = st.sidebar.radio("Navigation", ["Add Record", "View Records", "Logout"])
else:
    section = st.sidebar.radio("Navigation", ["View Records", "Logout"])

if section == "Logout":
    st.session_state.user = None
    st.session_state.page_reload = True
    st.stop()

# ---------------------
# ADD RECORD (Students Only)
# ---------------------
if section == "Add Record":
    st.header("🧮 Add Student Performance Record")

    name = st.text_input("Student Name")
    hours = st.number_input("Hours Studied", min_value=0.0, max_value=24.0, step=0.5)
    attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0)
    sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, step=0.5)

    if st.button("Add Record"):
        if name.strip() == "":
            st.error("Student name cannot be empty.")
        else:
            data = {
                "name": name,
                "hours_studied": hours,
                "attendance": attendance,
                "sleep_hours": sleep,
                "prediction": None,  # Backend computes prediction
                "created_by": user["username"],
            }
            try:
                res = requests.post(f"{API_URL}/students", json=data)
                res.raise_for_status()
                result = res.json()
                st.success("✅ Record added successfully!")
                st.info(f"Predicted Performance: {result['data']['prediction']}")
                st.session_state.page_reload = True
                st.stop()  # Stop and rerun to clear inputs
            except Exception as e:
                st.error(f"Failed to add record: {e}")

# ---------------------
# VIEW RECORDS
# ---------------------
if section in ["View Records"]:
    st.header("📊 Student Records")

    try:
        res = requests.get(
            f"{API_URL}/students", params={"username": user["username"], "role": user["role"]}
        )
        res.raise_for_status()
        records = res.json()

        if not records:
            st.info("No records available.")
        else:
            df = pd.DataFrame(records)
            cols = ["name", "hours_studied", "attendance", "sleep_hours", "prediction", "created_by"]
            df = df[cols] if all(c in df.columns for c in cols) else df

            # Admin: filter by prediction
            if user["role"] == "admin":
                prediction_filter = st.multiselect(
                    "Filter by Prediction",
                    options=df["prediction"].unique(),
                    default=df["prediction"].unique(),
                )
                df = df[df["prediction"].isin(prediction_filter)]

            st.dataframe(df, use_container_width=True)

            # Chart for prediction distribution
            st.subheader("📊 Prediction Distribution")
            chart_data = df["prediction"].value_counts().reset_index()
            chart_data.columns = ["Prediction", "Count"]
            st.bar_chart(chart_data.set_index("Prediction"))

    except Exception as e:
        st.error(f"Error fetching records: {e}")
