import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil import parser

# Load data from CSV
read_file = pd.read_excel("wontime.xlsx")


# Write the dataframe object 
# into csv file 
read_file.to_csv("/var/app/wubbyontimepercentage.csv",  
                index = None, 
                header=True) 
    
df = pd.DataFrame(pd.read_csv("wubbyontimepercentage.csv")) 
# Custom function to parse dates
def custom_date_parser(date_str):
    try:
        return parser.parse(date_str)
    except (TypeError, ValueError):
        return pd.NaT

# Apply custom date parser to the 'd' column
df['d'] = df['d'].apply(custom_date_parser)

# Drop rows with NaT values in the 'd' column
df = df.dropna(subset=['d'])

# Set up the Streamlit app
st.set_page_config(page_title="Wubby Stream Statistics")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overall Statistics","Pick a Stream"])

#maybe home page after wrapped
#if page == "Home":
    #st.title("Latest Stream Statistics")
    #last_row = df.iloc[-1]

    #st.write("### Expected (ET):")
    #expected_time = last_row['et']
    #st.write(f'<p style="font-size:30px;">{expected_time}</p>', unsafe_allow_html=True)

    #st.write("### Actual (AT):")
    #actual_time = last_row['at']
    #st.write(f'<p style="font-size:30px;">{actual_time}</p>', unsafe_allow_html=True)
    #st.write("### Time Late (TL):")
    #time_late = last_row['tl']
    #tl_color = 'green' if time_late == '0:00' else ('yellow' if '0:01' <= time_late <= '0:05' else 'red')
    #st.write(f'<p style="font-size:30px; color:{tl_color};">{time_late}</p>', unsafe_allow_html=True)

    # Notes section
    #st.write("### Notes:")
    #notes_text = last_row['Notes']
    #st.write(f'<p style="font-size:20px;">{notes_text}</p>', unsafe_allow_html=True)


# Main content
if page == "Pick a Stream":
    st.title("Pick a Stream")
    st.header("idk pick one")

    # Get unique dates from the DataFrame
    unique_dates = sorted(df['d'].dt.date.unique())
    selected_date = st.selectbox("Pick a date", unique_dates, index=len(unique_dates) - 1, key="pick_stream_date")

    # Display stream time, actual time, and tl for the selected date
    selected_row = df[df['d'].dt.date == selected_date].iloc[0]

    if pd.isna(selected_row['C']):  # Check if 'C' is not populated
        st.write(f"## Stream Time (ET): {selected_row['et']}")
        st.write(f"## Actual Time (AT): {selected_row['at']}")
        st.write(f"## Time Late (TL): {selected_row['tl']} minutes")
    else:
        st.write("## Stream was canceled.")
    
    # Notes section
    notes_text = selected_row['Notes']
    if pd.isna(selected_row['Notes']):
        st.write("### No notes recorded.")
    else:
        st.write(f"\n #### Notes: {notes_text}")

elif page == "Overall Statistics":
    st.title("Wubby Time Card Wrapped™")
    st.write("*Tracking started on march 11, 2023*")
    
    # Stats

    st.write("# Numbers")
    canceled_streams = int(round(df['C'].sum(), 0))
    st.write(f"### Number of streams cancelled: {canceled_streams}")

    # Count late streams (exclude non-numeric values)
    late_streams = df[df['tl'] >'00:00:00'].shape[0]
    st.write(f"### Number of streams late: {late_streams}")

    early_streams = df[df['TE'] > '00:00:00'].shape[0]
    st.write(f"### Number of streams early: {early_streams}")

    al_being_called_bitch = int(round(df['AB'].sum(), 0))
    st.write(f"### Number of times Allux got called a bitch (on stream): {al_being_called_bitch}")
    

    mic_airborne = int(round(df['MA'].sum(),0))
    st.write(f"### Number of times the mic has fallen: {mic_airborne}")

    total_streams = len(df['d'].dt.date.unique())
    st.write(f"### Total number of tracked streams: {total_streams}")

    st.write("# Graphs")

    #lateness graph
    st.write("### Lateness over time:")   
    filtered_df = df[['d', 'tl']].dropna()
    filtered_df['tl'] = filtered_df['tl']
    st.line_chart(filtered_df.set_index('d'))
    
    #mic graph
    st.write("### Mic Airborne over time:")
    scatter_df = df[['d', 'MA']].fillna(0)
    st.line_chart(scatter_df.set_index('d'))

    #allux bitch graph
    st.write("### Allux being called a bitch over time:")
    filtered_df = df[['d', 'AB']].fillna(0)
    st.line_chart(filtered_df.set_index('d'))

    #allux 
    
    
    st.write("Note: There are more collumns in the dataset that were ommitted for various reasons")
    st.write("*The NG (No Gold) collumn was ommitted because cases just stopped being opened on a daily baises*")
    st.write("*The ST (Stunlocked) collumn was ommitted because it became a every stream occurance (just a stream counter, lol)*")
    st.write("*RD (reddit mention) collumn was omitted because i just stopped tracking it for some reason")
