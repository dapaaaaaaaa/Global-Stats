import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as colors

judul = "GLOBAL STATS"
sub = "Tugas Besar Mata Kuliah: Perancangan Aplikasi Sains Data"

st.set_page_config(page_title=judul,
                   page_icon=":bird:",
                   layout="wide")

st.title(judul)
st.caption(sub)

df = pd.read_csv('Data1.csv')

# Ambil data GDP per capita, life expectancy, dan negara dari DataFrame
gdp_per_capita = df[[' Country ', ' gdppercap ']]
life_expectancy = df[[' Country ', ' lifeexpectatbirth ']]

# Urutkan data GDP per capita secara menurun
gdp_per_capita = gdp_per_capita.sort_values(' gdppercap ')
life_expectancy = life_expectancy.sort_values(' lifeexpectatbirth ')

# Tambahkan slider untuk menentukan jumlah negara yang ingin ditampilkan
with st.sidebar:
    num_countries = st.slider("Jumlah Negara yang Ditampilkan", min_value=1, max_value=50,
                              value=1)

# Ambil n negara terkaya dan terendah sesuai dengan input slider
top_n_richest = gdp_per_capita.tail(num_countries).reset_index(drop=True)
top_n_poorest = gdp_per_capita.head(num_countries).reset_index(drop=True)

# Definisikan skala warna gradasi
bar_colorscale = colors.diverging.RdYlBu

# Plot Top n Negara Terkaya
fig_richest = go.Figure(data=go.Bar(
    x=top_n_richest[' gdppercap '],
    y=top_n_richest[' Country '],
    orientation='h',
    marker=dict(
        color=top_n_richest[' gdppercap '],  # Warna berdasarkan GDP per Capita
        colorscale=bar_colorscale,  # Skala warna gradasi
        colorbar=dict(title='GDP per Capita'),  # Tambahkan colorbar
        cmax=top_n_richest[' gdppercap '].max(),  # Nilai maksimum untuk skala warna
        cmin=top_n_richest[' gdppercap '].min()  # Nilai minimum untuk skala warna
    ),
    hovertemplate='Negara: %{y}<br>GDP per Capita: %{x}<extra></extra>'
))

fig_richest.update_layout(
    title={
        'text': f"Top {num_countries} Negara Terkaya",
        'font': {'size': 24}
    },
    xaxis_title="GDP per Capita",
    yaxis_title="Negara"
)

# Plot Top n Negara Termiskin
fig_poorest = go.Figure(data=go.Bar(
    x=top_n_poorest[' gdppercap '],
    y=top_n_poorest[' Country '],
    orientation='h',
    marker=dict(
        color=top_n_poorest[' gdppercap '],  # Warna berdasarkan GDP per Capita
        colorscale=bar_colorscale,  # Skala warna gradasi
        colorbar=dict(title='GDP per Capita'),  # Tambahkan colorbar
        cmax=top_n_poorest[' gdppercap '].max(),  # Nilai maksimum untuk skala warna
        cmin=top_n_poorest[' gdppercap '].min()  # Nilai minimum untuk skala warna
    ),
    hovertemplate='Negara: %{y}<br>GDP per Capita: %{x}<extra></extra>'
))

fig_poorest.update_layout(
    title={
        'text': f"Top {num_countries} Negara Termiskin",
        'font': {'size': 24}
    },
    xaxis_title="GDP per Capita",
    yaxis_title="Negara"
)

# Bubble Chart GDP per Capita dan Life Expectancy
fig_bubble = go.Figure(data=go.Scatter(
    x=df[' gdppercap '],
    y=df[' lifeexpectatbirth '],
    mode='markers',
    marker=dict(
        color=df[' gdppercap '],  # Warna berdasarkan GDP per Capita
        colorscale='Viridis',  # Skala warna estetik
        size=df[' gdppercap '],  # Ukuran berdasarkan GDP per Capita
        sizemode='area',
        sizeref=2.0 * max(df[' gdppercap ']) / (30 ** 2),  # Skala ukuran bubble
        sizemin=4
    ),
    hovertemplate='Negara: %{text}<br>GDP per Capita: %{x}<br>Life Expectancy: %{y}<extra></extra>',
    text=df[' Country ']
))

fig_bubble.update_layout(
    title={
        'text': "GDP per Capita vs Life Expectancy",
        'font': {'size': 24}
    },
    xaxis_title="GDP per Capita",
    yaxis_title="Life Expectancy",
    showlegend=False
)

# Menampilkan plot menggunakan Streamlit
st.plotly_chart(fig_richest)
st.plotly_chart(fig_poorest)

st.header("Nilai GDP per Capita Negara")
st.table(gdp_per_capita.head(num_countries).reset_index(drop=True))

st.header("Nilai Life Expectancy Negara")
st.table(life_expectancy.head(num_countries).reset_index(drop=True))

st.plotly_chart(fig_bubble)
