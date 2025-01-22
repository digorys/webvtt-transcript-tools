import re
import streamlit as st

def shift_transcript(transcript: str) -> str:
    
    # Find all timestamps
    timestamps = re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3})', transcript)

    # Preliminary assertions
    assert len(timestamps) % 2 == 0, \
        'Number of timestamps should be even'

    assert timestamps[2::2] == sorted(timestamps[2::2]), \
        'Timestamps should be in ascending order' 

    # Add a timestamp pair to the end
    shifted_timestamps = timestamps.copy()
    shifted_timestamps.append(str(timestamps[-1]))
    shifted_timestamps.append("00:00:00.000")

    # Remove the first two timestamps
    shifted_timestamps = shifted_timestamps[2:]
    shifted_timestamps[0] = "00:00:00.000"

    assert len(timestamps) == len(shifted_timestamps), \
        'Number of timestamps should remain the same'

    # Shift each timestamp up to the previous one
    shifted_transcript = re.sub(
        r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})',
        lambda m: f"{shifted_timestamps.pop(0)} --> {shifted_timestamps.pop(0)}",
        transcript
    )    

    assert len(transcript) == len(shifted_transcript), \
        'Length of the transcript should remain the same'

    return shifted_transcript

################################# Streamlit UI #################################

st.set_page_config(layout="wide")

st.title("Transcript Shifter \U00002B07\U0000FE0F")

st.write("""Paste your transcript below and click 'Adjust Transcript':
\n - The tool will shift each line to the next set of timestamps.
\n - The first pair of timestamps will be removed.
\n - The **first** and **last** timestamp will be set to 00:00:00.000 so don't forget to change it!
""")

transcript = st.text_area("Input Transcript", height=300)

if st.button("Adjust Transcript"):
    try:
        # Process the transcript
        adjusted_transcript = shift_transcript(transcript)
        
        # Display the adjusted transcript
        st.subheader("Fixed Transcript:")
        st.text_area("Output transcript", adjusted_transcript, height=300)
        
    except Exception as e:
        st.error(f"Error: {e}")