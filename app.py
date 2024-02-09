import streamlit as st
import pandas as pd

def process_raw_data(raw_data_file):
    df = pd.read_excel(raw_data_file)

    # Convert 'date' and 'time' columns to datetime format
    df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))

    # Extract date from datetime column
    df['date'] = df['datetime'].dt.date

    # Calculate total duration for each inside and outside
    df['Inside Duration'] = df[df['position'].str.lower() == 'inside']['datetime'].diff().dt.total_seconds().fillna(0)
    df['Outside Duration'] = df[df['position'].str.lower() != 'inside']['datetime'].diff().dt.total_seconds().fillna(0)

    # Calculate the number of picking and placing activities done
    df['Number of Picked'] = (df['activity'] == 'picked').astype(int)
    df['Number of Placed'] = (df['activity'] == 'placed').astype(int)

    # Group by date and aggregate values
    output_df = df.groupby('date').agg({
        'Inside Duration': 'sum',
        'Outside Duration': 'sum',
        'Number of Picked': 'sum',
        'Number of Placed': 'sum'
    }).reset_index()

    return output_df

# Streamlit UI
st.title('Raw Data Processing')

# File uploader
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        output_df = process_raw_data(uploaded_file)
        st.write(output_df)
    except Exception as e:
        st.error(f"An error occurred: {e}")
