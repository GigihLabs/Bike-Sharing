# WeBike Analysis Dashboard

Submission untuk Proyek Analisis Data - Dicoding "Belajar Dasar Analisis Data". Dashboard ini memberikan wawasan mendalam mengenai tren penyewaan sepeda berdasarkan data historis, pengaruh cuaca, dan profil perilaku pengguna.

## Ringkasan Proyek
Proyek ini menganalisis dataset "Bike Sharing" untuk menjawab beberapa pertanyaan kunci:
1. **Prediksi Kebutuhan Armada:** Bagaimana tren pertumbuhan volume penyewaan bulanan dan prediksi untuk kuartal mendatang?
2. **Analisis Perilaku (Clustering):** Bagaimana karakteristik pengguna dapat diklasifikasikan ke dalam kategori *Low, Commuter, Leisure,* dan *Hybrid*?
3. **Pengaruh Cuaca:** Bagaimana faktor eksternal seperti suhu dan kecepatan angin memengaruhi minat penyewaan?

## Fitur Dashboard
- **Filter Rentang Waktu:** Menyesuaikan data berdasarkan tanggal yang dipilih.
- **Filter Jenis Pengguna:** Memisahkan data antara pengguna kasual dan terdaftar (*registered*).
- **Analisis Lanjutan:** Fitur manual grouping/clustering untuk profil pengguna.
- **Visualisasi Interaktif:** Grafik tren dan korelasi yang informatif.

## Setup Environment (Lokal)

Jika Anda ingin menjalankan proyek ini di komputer lokal, ikuti langkah-langkah berikut:

1. **Clone Repositori**
   ```bash
   git clone [https://github.com/GigihLabs/Bike-Sharing.git](https://github.com/GigihLabs/Bike-Sharing.git)
   cd Bike-Sharing

2. **Buat Virtual Environment**
   python -m venv venv
   source venv/bin/activate
   
4. **Install Dependensi**
   pip install -r requirements.txt
  
5. **Jalankan Aplikasi Streamlit**
   streamlit run dashboard/dashboard.py
