import streamlit as st
import requests
import numpy as np
import plotly.express as px
import pandas as pd

st.title('Pokemon explorer!')

pokemon_number = st.slider('Choose a pokemon number!', 1, 151)

url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number}/"
response = requests.get(url).json()

pokemon_name = response['name']
pokemon_height = response['height']
pokemon_weight = response['weight']
pokemon_cry = response['cries']['latest']
pokemon_pic = response['sprites']['front_default']
moves = [move['move']['name'] for move in response['moves']]
move_list = ",\n".join(moves).replace('-',' ').title()
move_count = len(response['moves'])
pokemon_types = [each['type']['name'] for each in response['types']]

col1, col2, col3 = st.columns([3, 3, 2])

with col1:
    st.header(pokemon_name.title(), divider="red")
    s = ', '.join(str(x) for x in pokemon_types)
    st.write(f"**Types:** {s}")
with col3:
    st.image(pokemon_pic)

#cries
st.subheader(':violet[Listen to this pokemon!]', divider = 'violet')
st.audio(pokemon_cry)

#size
st.subheader(':blue[Size information!]', divider = 'blue')
st.write(f'**Height:** {pokemon_height}m')
st.write(f'**Weight:** {pokemon_weight}kg')

#compare heights & weights
other_pokemon = [np.random.randint(1,151),np.random.randint(1,151),np.random.randint(1,151),np.random.randint(1,151)]
st.button(":rainbow[Click to compare against different pokemon!]")
all_names = [pokemon_name.title()]
all_heights = [pokemon_height]
all_weights = [pokemon_weight]

for x in other_pokemon:
    other_responses = requests.get(f"https://pokeapi.co/api/v2/pokemon/{x}/").json()
    all_names.append(other_responses['name'].title())
    all_heights.append(other_responses['height'])
    all_weights.append(other_responses['weight'])


height_dict = dict(zip(all_names,all_heights))
weight_dict = dict(zip(all_names,all_weights))


col1, col2 = st.columns([2, 2])
with col1:
    st.bar_chart(height_dict, x_label = 'Pokemon name', y_label = 'Pokemon height')
with col2:
    st.bar_chart(weight_dict, x_label = 'Pokemon name', y_label = 'Pokemon weight')

#moves
st.subheader(':orange[Moves!]', divider = 'orange')
st.write(f"This pokemon can learn {move_count} moves:")
st.write(move_list)

#base stats
base_stats_keys = [stat['stat']['name'] for stat in response['stats']]
base_stats_values = [stat['base_stat'] for stat in response['stats']]
base_stats = dict(zip(base_stats_keys, base_stats_values))

st.subheader(':green[Base stats!]', divider = 'green')

tab1, tab2 = st.tabs(["Bar chart","Radar plot"])
with tab1:
    st.bar_chart(base_stats, 
             x_label = 'Base stat level', 
             y_label = 'Stat name', 
             horizontal=True)
with tab2:
    df = pd.DataFrame(dict(base_stats), index = [1])
    radplot = px.line_polar(df, r = base_stats_values, theta = base_stats_keys, line_close = True)
    st.plotly_chart(radplot)