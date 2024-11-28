import json
import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch

st.title("Euro 2024 Shot Map")
st.subheader("Filter to a team/player to see all of their shots taken!")

# Load the dataset
df = pd.read_csv('euros_2024_shot_map.csv')  # Corrected filename
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)



def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df

# Team selection
team = st.selectbox('Select a Country', df['team'].sort_values().unique(), index=None)

# Player selection based on the selected team
player = st.selectbox('Select a Player', df[df['team'] == team]['player'].sort_values().unique(), index=None)

# Filter the dataframe based on the selected team and player
filtered_df = filter_data(df, team, player)

# Plot the shot map
pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

def plot_shots(df, ax, pitch):
    for shot in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(shot['location'][0]),
            y=float(shot['location'][1]),
            ax=ax,
            s=100 * shot['shot_statsbomb_xg'],
            color='green' if shot['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if shot['shot_outcome'] == 'Goal' else 0.5,
            zorder=2 if shot['shot_outcome'] == 'Goal' else 1
        )

plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)
