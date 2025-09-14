import streamlit as st
import pandas as pd
import os
import datetime
import pywhatkit as kit

# =====================
# Page Config & Styling
# =====================
st.set_page_config(page_title="AI Workshop Registration - Social Eagle", layout="centered")

st.markdown(
    """
    <style>
        body {
            background-color: #0e0e0e;
            color: #e0e0ff;
        }
        .stApp {
            background-color: #0e0e0e;
            color: #e0e0ff;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #a64ca6;
        }
        .stButton button {
            background-color: #a64ca6;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
        }
        .stTextInput, .stSlider, .stTextArea {
            color: #e0e0ff;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================
# File Setup
# =====================
filename = "registrations.csv"
if not os.path.exists(filename):
    df = pd.DataFrame(columns=["Name", "Age", "Phone"])
    df.to_csv(filename, index=False)

# =====================
# Registration Form
# =====================
st.title("🤖 Social Eagle AI Workshop Registration")

with st.form("registration_form"):
    name = st.text_input("Full Name")
    age = st.slider("Age", 10, 100, 25)
    phone = st.text_input("WhatsApp Number (with country code, e.g. 91xxxxxxxxxx)")

    submitted = st.form_submit_button("Register")

    if submitted:
        if name.strip() and phone.strip():
            df = pd.read_csv(filename, dtype=str)
            new_entry = pd.DataFrame([[name, age, phone]], columns=["Name", "Age", "Phone"])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(filename, index=False)
            st.success(f"✅ Thank you {name}, you are registered for the AI Workshop!")
        else:
            st.error("⚠️ Please fill in all fields before submitting.")

# =====================
# Admin Section
# =====================
st.subheader("🔑 Admin Tools")

if os.path.exists(filename):
    df = pd.read_csv(filename, dtype=str)  # keep all as strings

    # Clean phone numbers
    df["Phone"] = (
        df["Phone"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    # Download CSV button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Registration List (CSV)",
        data=csv,
        file_name="registrations.csv",
        mime="text/csv",
    )

    # WhatsApp Messaging
    st.write("📲 Send WhatsApp Message to Registered Participants")

    message = st.text_area("Enter the message to send:")

    if st.button("Send WhatsApp Messages"):
        if not message.strip():
            st.error("⚠️ Please enter a message before sending.")
        else:
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute + 2  # start sending after 2 minutes

            for phone in df["Phone"]:
                if phone.lower() == "nan" or phone == "":
                    continue  # skip invalid numbers
                try:
                    kit.sendwhatmsg(phone, message, hour, minute, wait_time=10, tab_close=True)
                    st.success(f"✅ WhatsApp message scheduled for {phone}")
                    minute += 1  # space messages 1 minute apart
                except Exception as e:
                    st.error(f"❌ Failed to send message to {phone}: {e}")
