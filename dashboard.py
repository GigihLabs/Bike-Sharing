import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# membuat konfigurasi halaman
st.set_page_config(page_title="WeBike Analysis Dashboard", layout="wide")

# memuat dataset yang telah dibersihkan dan menjawab seluruh pertanyaan EDA
# memuat dataset day.csv yang telah dibersihkan dan dijadikan main_data.csv
df = pd.read_csv("dashboard/main_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])
df['mnth_name'] = df['dteday'].dt.month_name()

# membuat sidebar di kiri
with st.sidebar:
    # memuat gambar logo dan penjelasan singkat tentang aplikasi
    st.image("dashboard/logo.png")
    st.text("Solusi mobilitas perkotaan berbasis teknologi dalam mengatasi kemacetan dan emisi karbon.")

    # membuat filter data
    st.subheader("Filter data berdasarkan rentang waktu:")
    # Widget Input
    min_date = pd.to_datetime(df["dteday"]).min()
    max_date = pd.to_datetime(df["dteday"]).max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    st.header("Konfigurasi Visualisasi")
    
    # membuat filter menggunakan widget input selectbox untuk jenis pengguna
    user_type = st.selectbox("Pilih Jenis Pengguna:", ["Total", "Casual", "Registered"])
    
    # membuat filter menggunakan widget input slider untuk rentang suhu
    min_temp, max_temp = st.slider("Rentang Suhu (Normalized):", 0.0, 1.0, (0.0, 1.0))

# membuat filter menggunakan widget input date sebagai rentang awal dan akhir tanggal
df_filtered = df[(df["dteday"] >= pd.Timestamp(start_date)) & 
                 (df["dteday"] <= pd.Timestamp(end_date))]

# mengisi halaman utama dengan konten
st.title("WeBike Sharing Analysis Dashboard")
st.write(f"Menampilkan data dari {start_date} sampai {end_date}")

# membuat metrik ringkasan sebagai output dari widget input date
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", value=df_filtered['cnt'].sum())
col2.metric("Pengguna Kasual", value=df_filtered['casual'].sum())
col3.metric("Pengguna Terdaftar", value=df_filtered['registered'].sum())

# membuat filter menggunakan logika ukuran suhu atemp
df_filtered = df[(df['atemp'] >= min_temp) & (df['atemp'] <= max_temp)]

# membuat filter menggunakan widget input selectbox untuk menghasilkan barchart
if user_type == "Total":
    target_col = 'cnt'
elif user_type == "Casual":
    target_col = 'casual'
else:
    target_col = 'registered'

# membuat rancangan visualisasi
st.subheader(f"Analisis {user_type} di Rentang Suhu {min_temp} - {max_temp}")
st.bar_chart(df_filtered.groupby('mnth_name')[target_col].sum())

# membuat tab agar dashboard lebih ringkas
tab1, tab2, tab3, tab4 = st.tabs(["Kategori Pengguna dan Cuaca", "Tren Penyewaan Bulanan", "Profil Pengguna", "korelasi Suhu dan Windspeed"])
 
with tab1:
    # membuat 2 kolom barchart
    col1, col2 = st.columns(2)
    
    with col1: # kolom barchart kiri untuk memvisualisasikan Perbandingan Casual vs Registered
        st.markdown("<h5 style='text-align: center;'>Perbandingan Casual vs Registered</h5>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        data_compare = [df['casual'].sum(), df['registered'].sum()]
        ax2.bar(['Casual', 'Registered'], data_compare, color=['#FF9999', '#66B2FF'])
        ax2.grid(True, linestyle='--', axis='y', alpha=0.7)
        ax2.set_title("Total Pengguna Berdasarkan Kategori")
        st.pyplot(fig2)

    with col2: # kolom barchart kanan untuk memvisualisasikan Pengaruh Cuaca terhadap Penyewaan
        st.markdown("<h5 style='text-align: center;'>Pengaruh Cuaca terhadap Penyewaan</h5>", unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, x='weathersit', y='cnt', ax=ax3, palette='viridis')
        ax3.grid(True, linestyle='--', axis='y', alpha=0.7) 
        ax3.set_title("Rata-rata Penyewaan berdasarkan Kondisi Cuaca") 
        ax3.set_xlabel("Kondisi Cuaca (1: Cerah, 2: Mendung, 3: Hujan Ringan)")
        ax3.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig3)

    st.caption("<h6 style='text-align: center;'>Copyright © WeBike - Gigih Dwi Kartika Chandra Wibowo 2026</h6>", unsafe_allow_html=True)

with tab2: # mengisi tab "Tren Penyewaan Bulanan" dengan membuat line chart banyak penyewaan yang terjadi setiap bulan dalam 2 tahun 
    st.subheader("Tren Penyewaan Bulanan Selama Tahun 2011 hingga Tahun 2012")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    monthly_counts = df.groupby(df['dteday'].dt.to_period('M'))['cnt'].sum()
    monthly_counts.plot(kind='line', marker='o', ax=ax1, color='green')
    ax1.set_ylim(bottom=0)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_title("Tren Total Penyewaan Sepeda per Bulan")
    ax1.set_ylabel("Total Pesanan")
    ax1.set_xlabel("Bulan")
    st.pyplot(fig1)

    st.info(
        """
        ### Kesimpulan:
        Pola permintaan cenderung menurun pada akhir tahun 2012 (november - desember) dan diprediksi tidak terjadi lonjakan permintaan yang 
        ekstrem pada awal tahun 2013 (januari - maret). Pada awal tahun 2013 ini, Jadikan kesempatan untuk melakukan pemeliharaan dan perbaikan 
        Armada sepeda guna mempersiapkan lonjakan permintaan yang diprediksi sterjadi pada musim semi akhir maret 2013.""")

    st.caption("<h6 style='text-align: center;'>Copyright © WeBike - Gigih Dwi Kartika Chandra Wibowo 2026</h6>", unsafe_allow_html=True)

with tab3: # mengisi tab "Profil Pengguna" dengan bar chart banyak hari dalam kategori klaster pada setiap bulan selama semester pertama 2012
    st.subheader("Analisis Profil Pengguna (Semester 1, 2012)")

    # menyiapkan data harian dalam bentuk median
    median_cnt = df['cnt'].median()

    # mengkategorikan atau membuat klaster menggunakan logika
    def categorize_day_4(row):
        if row['cnt'] < median_cnt:
            return 'Low_Usage'
        elif row['registered'] > row['casual'] * 2:
            return 'Commuter_Day'
        elif row['casual'] > row['registered']:
            return 'Leisure_Day'
        else:
            return 'Hybrid_Day'

    # mengambil data pada awal semester 1 2012
    h1_2012 = df[(df['dteday'].dt.year == 2012) & (df['dteday'].dt.month <= 6)].copy()
    h1_2012['day_cluster'] = h1_2012.apply(categorize_day_4, axis=1)

    cluster_distribution = h1_2012.groupby([h1_2012['dteday'].dt.month, 'day_cluster']).size().unstack(fill_value=0)

    # menyiapkan kanvas diagram dan memvisualisasikan data
    fig7, ax7 = plt.subplots(figsize=(12, 6))
    cluster_distribution.plot(kind='bar', stacked=True, ax=ax7, colormap='Set2')

    ax7.set_title('Distribusi 4 Profil Pengguna per Bulan (Semester 1, 2012)', fontsize=14)
    ax7.set_xlabel('Bulan', fontsize=12)
    ax7.set_ylabel('Jumlah Hari', fontsize=12)
    ax7.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'], rotation=0)
    ax7.legend(title='Profil Hari', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax7.grid(axis='y', linestyle='--', alpha=0.5)

    # label angka sebagai keterangan jumlah hari di setiap klaster
    for p in ax7.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0:
            ax7.text(x + width/2, y + height/2, int(height), ha='center', va='center', fontsize=9)

    st.pyplot(fig7)

    st.info(
        """
        ### Kesimpulan:
        Pada awal tahun 2012 (januari hingga februari) terjadi aktivitas penyewaan yang sangat rendah, pada rentang waktu tersebut strategi 
        yang perlu dilakukan adalah melarang penempatan sepeda di area terbuka agar tidak rusak akibat cuaca dan perintahkan tim lapangan 
        untuk melakukan perawatan unit-unit sepeda. pada rentang bulan maret hingga juni 2012, lebih banyak pengguna registered mulai beraktivitas. 
        pastikan jumlah ketersediaan unit-unit sepeda cukup untuk menunjang aktivitas para pengguna registered, serta terapkan sistem tukar poin 
        untuk menjaga retensi pengguna registered.""")

    st.caption("<h6 style='text-align: center;'>Copyright © WeBike - Gigih Dwi Kartika Chandra Wibowo 2026</h6>", unsafe_allow_html=True)

with tab4: # mengisi tab "korelasi Suhu dan Windspeed" dengan diagram regresi untuk menghasilkan korelasi
    st.subheader("Analisis Korelasi: Suhu & Kecepatan Angin (Q2 2012)")

    # memuat data per jam menggunakan dataset hour.csv yang sudah dibersihkan
    @st.cache_data
    def load_hourly_data():
        return pd.read_csv("dashboard/hour_cleaned.csv")

    hour_df = load_hourly_data()

    # membuat filter dataset untuk kondisi kuartil kedua tahun 2012, hari kerja, dan jam-jam yang sibuk
    q2_peak_hours = hour_df[
        (hour_df['mnth'].isin([4, 5, 6])) & 
        (hour_df['workingday'] == 1) & 
        (hour_df['hr'].isin([7, 8, 9, 16, 17, 18]))
    ].copy()

    # membuat 2 kolom diagram
    col_cor1, col_cor2 = st.columns(2)

    with col_cor1: # membuat diagram korelasi antara suhu yang dirasakan dengan banyak penyewa
        st.markdown("<h4 style='text-align: center;'>Suhu (atemp) vs Penyewaan</h4>", unsafe_allow_html=True)
        fig_cor1, ax_cor1 = plt.subplots(figsize=(10, 5))
        sns.regplot(data=q2_peak_hours, x='atemp', y='cnt', scatter_kws={'alpha':0.3}, line_kws={'color':'red'}, ax=ax_cor1)
        ax_cor1.set_title('Hubungan Suhu (atemp) vs Penyewaan')
        ax_cor1.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig_cor1)

    with col_cor2: # membuat diagram korelasi antara kecepatan angin dengan banyak penyewa
        st.markdown("<h4 style='text-align: center;'>Kecepatan Angin vs Penyewaan</h4>", unsafe_allow_html=True)
        fig_cor2, ax_cor2 = plt.subplots(figsize=(10, 5))
        sns.regplot(data=q2_peak_hours, x='windspeed', y='cnt', scatter_kws={'alpha':0.3}, line_kws={'color':'blue'}, ax=ax_cor2)
        ax_cor2.set_title('Hubungan Kecepatan Angin vs Penyewaan')
        ax_cor2.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig_cor2)

    # menampilkan tabel korelasi antara 3 objek
    correlation = q2_peak_hours[['atemp', 'windspeed', 'cnt']].corr()
    st.write("Tabel Korelasi:")
    st.dataframe(correlation)

    st.info(
        """
        ### Kesimpulan:
        kondisi cuaca dan musim yang ekstrem seperti kecepatan angin yang tinggi dan suhu udara yang terlalu dingin dapat menurunkan permintaan. 
        strategi yang mungkin dilakukan untuk kondisi cuaca dan musim ini adalah hindari menempatkan sepeda di area terbuka. jika cuaca dan suhu 
        nyaman untuk beraktivitas di luar ruangan, perintahkan tim lapangan untuk mendistribusikan sepeda ke tempat-tempat yang sibuk saat hari 
        kerja di jam 7 pagi hingga jam 6 malam.""")

    st.caption("<h6 style='text-align: center;'>Copyright © WeBike - Gigih Dwi Kartika Chandra Wibowo 2026</h6>", unsafe_allow_html=True)


