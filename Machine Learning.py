import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Membaca data dari file CSV
@st.cache_data
def load_data():
    data = pd.read_csv('Data.csv',delimiter=';')
    return data

# Menampilkan data awal
def show_data(data):
    st.subheader('Data Awal')
    st.write(data)

# Standarisasi data
def standardize_data(data):
    scaler = StandardScaler()
    data_features = data.drop('Country', axis=1)
    scaled_data = scaler.fit_transform(data_features)
    scaled_df = pd.DataFrame(scaled_data, columns=data_features.columns)
    scaled_df['Country'] = data['Country']  # Menambahkan kembali kolom 'Country' ke data yang distandarisasi
    return scaled_df

# Melakukan PCA untuk reduksi dimensi
def apply_pca(data):
    pca = PCA(n_components=1)
    data['PC1'] = pca.fit_transform(data.drop('Country', axis=1))
    return data

# Melakukan klasterisasi dengan K-means
def kmeans_clustering(data, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(data[['GDP per capita', 'PC1']])
    labels = kmeans.labels_

    data['Cluster'] = labels
    return data

# Menampilkan hasil klasterisasi
def show_clusters(data):
    st.subheader('Hasil Klasterisasi')

    fig = px.scatter(data, x='GDP per capita', y='PC1', color='Cluster', hover_data=['Country'], color_continuous_scale='viridis')
    st.plotly_chart(fig)

# Main function
def main():
    st.title('K-means Clustering')

    # Memuat data
    data = load_data()

    # Menampilkan data awal
    show_data(data)

    # Mengatur jumlah klaster
    num_clusters = st.sidebar.slider('Jumlah Klaster', min_value=1, max_value=10, value=5)

    # Standarisasi data
    scaled_data = standardize_data(data)

    # Melakukan PCA
    pca_data = apply_pca(scaled_data)

    # Melakukan klasterisasi
    clustered_data = kmeans_clustering(pca_data, num_clusters)

    # Menampilkan hasil klasterisasi
    show_clusters(clustered_data)

if __name__ == '__main__':
    main()
