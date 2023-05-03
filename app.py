# IMP : if user_defined_datapoints.csv already exists, delete it before running this script 

import streamlit as st
import pandas as pd
import numpy as np

# Load the predicted outputs file
df = pd.read_csv('predicted_outputs.csv')

# Define the number of rows to display at a time
ROWS_PER_PAGE = 20

# Create a list of emotions to choose from
emotions = ['negative', 'neutral', 'positive']

# Create a new column for the user-selected emotions
df['Selected Emotion'] = df['predicted_emotion']

# Define a function to update the selected emotion for a given row
def update_selected_emotion(row_idx, selected_emotion, updated_rows):
    if df.at[row_idx, 'Selected Emotion'] != selected_emotion:
        df.at[row_idx, 'Selected Emotion'] = selected_emotion
        updated_rows.append(row_idx)

# Define a function to display a page of rows with drop-downs for selecting new emotions
def display_page(page_idx, updated_rows):
    start_idx = page_idx * ROWS_PER_PAGE
    end_idx = start_idx + ROWS_PER_PAGE

    page_df = df.iloc[start_idx:end_idx]

    for i, row in page_df.iterrows():
        selected_emotion = st.selectbox(f"{row['text']}\nPredicted Emotion: {row['predicted_emotion']}", emotions, index=emotions.index(row['Selected Emotion']), key=i)
        update_selected_emotion(i, selected_emotion, updated_rows)

    return page_df

# Define the initial page index
page_idx = st.session_state.get('page_idx', 0)

# Create a list to store the indices of the updated rows
updated_rows = []

# Display the current page of rows
page_df = display_page(page_idx, updated_rows)

# Display pagination controls
if len(df) > ROWS_PER_PAGE:
    num_pages = int(np.ceil(len(df) / ROWS_PER_PAGE))
    if page_idx > 0:
        if st.button('Previous Page'):
            page_idx -= 1
            st.session_state['page_idx'] = page_idx
            updated_rows.clear()
            page_df = display_page(page_idx, updated_rows)
            st.experimental_rerun()
    if page_idx < num_pages - 1:
        if st.button('Next Page'):
            page_idx += 1
            st.session_state['page_idx'] = page_idx
            updated_rows.clear()
            page_df = display_page(page_idx, updated_rows)
            st.experimental_rerun()
    st.write(f'Page {page_idx + 1}/{num_pages}')

# Add a button to confirm the changes
if st.button('Confirm Changes'):
    if updated_rows:
        updated_df = df.iloc[updated_rows]
        updated_df.to_csv('user_defined_datapoints.csv', mode='a', header=False, index=False)
        st.write(f'{len(updated_rows)} rows saved.')
    else:
        st.write('No changes to save.')
