import re
import streamlit as st

def adjust_single_timestamp(timestamp, added_seconds, added_milliseconds):
    hours, minutes, seconds, milliseconds = map(int, re.split(r'[:.]', timestamp))

    # Calculate the new milliseconds and carry over to seconds if necessary
    new_milliseconds = milliseconds + added_milliseconds
    carried_seconds = new_milliseconds // 1000
    new_milliseconds %= 1000

    # Calculate the new seconds and carry over to minutes if necessary
    new_seconds = seconds + added_seconds + carried_seconds
    carried_minutes = new_seconds // 60
    new_seconds %= 60

    # Calculate the new minutes and carry over to hours if necessary
    new_minutes = minutes + carried_minutes
    carried_hours = new_minutes // 60
    new_minutes %= 60

    # Calculate the new hours
    new_hours = hours + carried_hours

    new_timestamp = f"{new_hours:02}:{new_minutes:02}:{new_seconds:02}.{new_milliseconds:03}"

    return new_timestamp

def adjust_transcript(transcript, added_seconds, added_milliseconds):
    # Find all timestamps in the transcript
    timestamps = re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3})', transcript)

    # Initial validation
    assert len(timestamps) % 2 == 0, \
        'Number of timestamps should be even'

    assert timestamps[2::2] == sorted(timestamps[2::2]), \
        'Timestamps should be in ascending order' 
    
    # Adjust the timestamps based on the given values
    adjusted_timestamps = []

    for timestamp in timestamps:
        new_timestamp = adjust_single_timestamp(timestamp, added_seconds, added_milliseconds)
        adjusted_timestamps.append(new_timestamp)

    # Adjust the timestamps in the transcript
    adjusted_transcript = re.sub(
        r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})',
        lambda m: f"{adjusted_timestamps.pop(0)} --> {adjusted_timestamps.pop(0)}",
        transcript
    )    

    # Final Validation
    adjusted_timestamps = re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3})', adjusted_transcript)

    assert len(timestamps) == len(adjusted_timestamps), \
        'Number of timestamps should remain the same'

    assert [old != new for old, new in zip(timestamps, adjusted_timestamps)], \
        'Timestamps should all be different'

    assert "-" not in adjusted_timestamps[0], \
        'Timestamps should not be negative, have you subtracted too many seconds?'
    
    return adjusted_transcript

################################# Streamlit UI #################################

st.set_page_config(layout="wide")

st.title("Transcript Second Adjuster \U000023F0")

st.write("""Paste your transcript below and choose your adjustments:
\n - The tool will adjust every timestamp by the amount specified.
\n - You can also input negative values!""")

transcript = st.text_area("Input Transcript", height=300)

# Get input of seconds and milliseconds from user in two columns
col1, col2 = st.columns(2)
with col1:
    added_seconds = st.number_input("Seconds to add", value=0)
with col2:
    added_milliseconds = st.number_input("Milliseconds to add", value=0)

if st.button("Adjust Transcript"):
    try:
        # Process the transcript
        adjusted_transcript = adjust_transcript(transcript, added_seconds, added_milliseconds)
        
        # Display the adjusted transcript
        st.subheader("Fixed Transcript:")
        st.text_area("Output transcript", adjusted_transcript, height=300)
        
    except Exception as e:
        st.error(f"Error: {e}")
