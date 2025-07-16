# Laporan Proyek Machine Learning - Risna Dwi Indriani

## Project Overview

  Pemilihan jurusan perguruan tinggi merupakan salah satu keputusan penting bagi siswa yang baru lulus sekolah menengah atas. Terutama pada bidang sosial dan humaniora (soshum), banyak siswa yang masih bingung menentukan jurusan yang sesuai dengan minat dan kemampuan mereka. Kesalahan dalam memilih jurusan dapat berdampak negatif pada motivasi belajar dan prestasi akademik.
  
  Seiring dengan perkembangan teknologi dan tersedianya data yang beragam, sistem rekomendasi menjadi solusi efektif untuk membantu siswa dalam pengambilan keputusan pemilihan jurusan. Pada proyek ini, digunakan tiga dataset utama, yaitu data universitas (universities), data jurusan (majors), dan skor UTBK bidang sosial dan humaniora (score humanities). Ketiga dataset tersebut menjadi dasar dalam mengembangkan sistem rekomendasi yang lebih personal dan relevan bagi setiap siswa.
  
  Sistem rekomendasi ini menggabungkan dua pendekatan utama, yaitu Content-Based Filtering yang merekomendasikan jurusan berdasarkan kesamaan fitur jurusan yang diminati pengguna, dan Collaborative Filtering yang memanfaatkan pola preferensi pengguna lain dengan minat serupa. Dengan penggabungan kedua teknik tersebut, diharapkan sistem dapat memberikan rekomendasi jurusan soshum yang sesuai dengan potensi dan preferensi calon mahasiswa, sehingga meningkatkan peluang keberhasilan akademik di masa depan.

## Business Understanding

### Problem Statements

1. Bagaimana memanfaatkan data universitas, jurusan, dan skor UTBK bidang sosial dan humaniora untuk membantu siswa memilih jurusan yang tepat?

2. Bagaimana membuat rekomendasi jurusan yang sesuai dengan minat dan kemampuan siswa berdasarkan data yang tersedia?

3. Bagaimana menggabungkan informasi dari preferensi siswa dan pola pengguna lain untuk meningkatkan akurasi rekomendasi?

### Goals

1. Mengembangkan sistem rekomendasi jurusan sosial dan humaniora yang menggunakan data universitas, jurusan, dan skor UTBK sebagai dasar analisis.

2. Menerapkan metode Content-Based Filtering dan Collaborative Filtering untuk memberikan rekomendasi yang personal dan akurat.

3. Membantu siswa dalam pengambilan keputusan jurusan yang tepat, berdasarkan potensi akademik dan preferensi mereka, guna meningkatkan keberhasilan studi di masa depan.

### Solution statements

  Untuk mencapai tujuan pengembangan sistem rekomendasi jurusan soshum, dua pendekatan utama akan digunakan:
  
  1. Content-Based Filtering
  Pendekatan ini merekomendasikan jurusan berdasarkan kemiripan karakteristik jurusan yang pernah diminati atau dipilih oleh pengguna. Sistem akan menganalisis fitur-fitur dari jurusan dan mencocokkannya dengan preferensi pengguna, sehingga menghasilkan rekomendasi yang relevan secara personal.
  
  2. Collaborative Filtering
  Pendekatan ini menggunakan pola preferensi pengguna lain yang memiliki minat atau perilaku serupa untuk memberikan rekomendasi. Dengan cara ini, sistem dapat mengenali jurusan yang mungkin diminati oleh pengguna berdasarkan rekomendasi dari pengguna lain yang memiliki profil dan skor ujian serupa.

## Data Understanding

### Data Loading

  Dataset yang digunakan dalam proyek ini berasal dari platform Kaggle dengan judul Indonesia College Entrance Examination - UTBK 2019. Menurut informasi dari sumber data, dataset tersebut dikumpulkan oleh Eko J. Salim melalui situs pemeringkatan tempat para peserta ujian berasal. Dataset ini berisi sekitar 147 ribu sampel dari total 1,1 juta skor yang tersedia. Namun, data tersebut tidak mewakili keseluruhan 1,1 juta karena berasal dari sumber pihak ketiga, sehingga ada kemungkinan terdapat data yang kurang valid. Terdapat empat dataset secara keseluruhan, namun hanya tiga yang digunakan dalam pengembangan model sistem rekomendasi kali ini, yaitu dataset jurusan (major), skor soshum (score_humanities), dan universitas (universities).

[Dataset UTBK 2019 - Kaggle](https://www.kaggle.com/datasets/ekojsalim/indonesia-college-entrance-examination-utbk-2019)

### Read Dataset

**Universities Dataset**

  Dataset ini berisi informasi mengenai universitas yang menjadi tujuan peserta ujian. Setiap baris merepresentasikan satu universitas beserta detail identitasnya.

- Jumlah data: 85 baris, masing-masing merepresentasikan satu entri universitas.
- Jumlah kolom: 3 kolom, yaitu:
    - Unnamed: Kolom tanpa nama yang kemungkinan merupakan indeks otomatis dari sistem. Kolom ini dapat diabaikan apabila tidak mengandung informasi penting.
    - id_university: Merupakan ID unik yang digunakan untuk mengidentifikasi setiap universitas.
    - university_name: Nama lengkap dari masing-masing universitas.

  Untuk memahami kondisi awal data sebelum dilakukan proses pembersihan, dilakukan pengecekan missing value menggunakan fungsi .isnull().sum(). Berikut hasilnya:
  
  | Kolom            | Jumlah Missing Value |
  | ---------------- | -------------------- |
  | Unnamed: 0       | 0                    |
  | id\_university   | 0                    |
  | university\_name | 0                    |
  
  Berdasarkan hasil di atas, tidak terdapat nilai yang hilang (missing values) di dalam dataset Universities. Dengan demikian, data ini dalam kondisi lengkap dan siap digunakan untuk proses selanjutnya.

**Majors Dataset**
  
Dataset Majors memuat informasi terkait program studi atau jurusan yang tersedia di berbagai universitas. Dataset ini penting untuk memahami struktur program studi serta untuk analisis lebih lanjut yang mengaitkan jurusan dengan universitas dan kapasitas penerimaan mahasiswa.

*Jumlah Baris dan Kolom:*

Dataset ini memiliki 3167 baris dan 6 kolom (tidak termasuk kolom Unnamed: 0 yang merupakan hasil ekspor dan dapat diabaikan).

*Deskripsi Kolom:*

- Unnamed: 0 : Kolom indeks otomatis dari hasil ekspor data, tidak mengandung informasi penting dan dapat diabaikan.

- id_major : ID unik untuk setiap jurusan.

- id_university : ID dari universitas tempat jurusan tersebut berada. Dapat digunakan untuk relasi dengan dataset Universities.

- type : Jenis atau kategori jurusan, misalnya science, humanities, dan lainnya.

- major_name : Nama jurusan, contohnya Teknik Sipil, Kedokteran, Manajemen, dll.

- capacity : Kapasitas daya tampung jurusan, menunjukkan jumlah maksimum mahasiswa yang dapat diterima.

  Untuk memahami kondisi awal data sebelum dilakukan proses pembersihan, dilakukan pengecekan missing value menggunakan fungsi .isnull().sum(). Berikut hasilnya:
  
  | Kolom          | Jumlah Missing Value |
  | -------------- | -------------------- |
  | Unnamed: 0     | 0                    |
  | id\_major      | 0                    |
  | id\_university | 0                    |
  | type           | 0                    |
  | major\_name    | 0                    |
  | capacity       | 0                    |
  
  Hasil di atas menunjukkan bahwa tidak terdapat nilai yang hilang (missing values) dalam dataset major. Seluruh kolom memiliki data yang lengkap, sehingga data ini siap untuk digunakan dalam proses analisis atau penggabungan (merging) dengan dataset lain.

**Score Humanities (Score_Soshum) Dataset**

  Dataset ini berisi data skor peserta ujian UTBK pada bidang sosial dan humaniora. Skor mencakup hasil subtes seperti Ekonomi, Geografi, Sejarah, Sosiologi, dan mata pelajaran terkait lainnya.
  
  * Jumlah data: Terdapat 61.202 baris (rows), yang masing-masing mewakili satu data pendaftaran atau pilihan jurusan dari seorang peserta ujian (calon mahasiswa).
  * Jumlah fitur: Dataset terdiri dari 15 kolom (columns) dengan rincian sebagai berikut:
  
  - Unnamed: 0 : Kolom tanpa nama yang kemungkinan merupakan indeks otomatis dari sistem atau hasil ekspor file, yang biasanya tidak mengandung informasi penting.
  - id_first_major : ID jurusan pilihan pertama yang dipilih oleh peserta.
  - id_first_university : ID universitas dari jurusan pilihan pertama.
  - id_second_major : ID jurusan pilihan kedua.
  - id_second_university : ID universitas dari jurusan pilihan kedua.
  - id_user : ID unik yang merepresentasikan peserta ujian.
  - score_eko : Skor peserta pada mata pelajaran Ekonomi.
  - score_geo : Skor peserta pada mata pelajaran Geografi.
  - score_kmb : Skor Kemampuan Berpikir Matematis dan Berlogika.
  - score_kpu : Skor Kemampuan Penalaran Umum.
  - score_kua : Skor Kemampuan Verbal (Bahasa Indonesia dan Bahasa Inggris).
  - score_mat : Skor peserta pada mata pelajaran Matematika.
  - score_ppu : Skor Pengetahuan dan Pemahaman Umum.
  - score_sej : Skor peserta pada mata pelajaran Sejarah.
  - score_sos : Skor rata-rata untuk kelompok mata pelajaran sosial.
 
  Untuk memahami kondisi awal data sebelum dilakukan proses pembersihan, dilakukan pengecekan missing value menggunakan fungsi .isnull().sum(). Berikut hasilnya:
  
  | Kolom                  | Jumlah Missing Value |
  | ---------------------- | -------------------- |
  | Unnamed: 0             | 0                    |
  | id\_first\_major       | 0                    |
  | id\_first\_university  | 0                    |
  | id\_second\_major      | 0                    |
  | id\_second\_university | 0                    |
  | id\_user               | 0                    |
  | score\_eko             | 0                    |
  | score\_geo             | 0                    |
  | score\_kmb             | 0                    |
  | score\_kpu             | 0                    |
  | score\_kua             | 0                    |
  | score\_mat             | 0                    |
  | score\_ppu             | 0                    |
  | score\_sej             | 0                    |
  | score\_sos             | 0                    |
  
  Seluruh kolom pada dataset score_humanities tidak memiliki missing value, yang berarti data lengkap dan dapat langsung digunakan untuk proses analisis lebih lanjut seperti pemodelan prediktif, visualisasi skor, atau analisis pemilihan jurusan.

# Exploratory Data Analysis (EDA) | Univariate

## EDA | Dataset Universitas

1. Cek Karakteristik Dataset

  Tahap ini meliputi analisis sifat-sifat dasar dari dataset, seperti jumlah baris, tipe data setiap kolom, serta statistik deskriptif seperti rata-rata, median, kuartil, nilai maksimum, minimum, dan standar deviasi. Pemahaman terhadap karakteristik dataset ini penting untuk memastikan kesiapan data dalam proses analisis dan mendeteksi potensi masalah. Pada dataset universitas, hasil pemeriksaan menunjukkan tidak adanya masalah signifikan, sehingga dapat disimpulkan bahwa dataset ini cukup valid dan siap digunakan.

2. Menghitung Nilai Unik

  Tahap ini meliputi penghitungan jumlah nilai unik pada suatu kolom atau variabel dalam dataset. Proses ini bertujuan untuk memahami variasi dan distribusi data di dalam kolom tersebut. Dengan mengetahui jumlah nilai unik, kita dapat menilai tingkat keberagaman atau keseragaman data. Pada kolom-kolom dalam dataset universitas, ditemukan bahwa variabel id universitas dan nama universitas masing-masing memiliki 85 nilai unik.

## EDA | Dataset Major

1. Cek Karakteristik Dataset

  Tahap ini meliputi analisis sifat-sifat dasar dari dataset, seperti jumlah baris, tipe data setiap kolom, serta statistik deskriptif seperti rata-rata, median, kuartil, nilai maksimum, minimum, dan standar deviasi. Pemahaman terhadap karakteristik dataset ini penting untuk memastikan kesiapan data dalam proses analisis dan mendeteksi potensi masalah. Pada dataset universitas, hasil pemeriksaan menunjukkan tidak adanya masalah signifikan, sehingga dapat disimpulkan bahwa dataset ini cukup valid dan siap digunakan.

2. Menghitung Nilai Unik

  Tahap ini melibatkan penghitungan jumlah nilai unik pada beberapa kolom dalam dataset untuk memahami variasi dan distribusi data di masing-masing kolom tersebut. Dengan mengetahui jumlah nilai unik, kita dapat mengevaluasi tingkat keberagaman data. Pada hasil analisis, didapatkan bahwa kolom id universitas memiliki 85 nilai unik, kolom id major memiliki 3167 nilai unik, dan kolom kapasitas memiliki 143 nilai unik.

## EDA | Dataset Score_Humanities

1. Menghitung Nilai Unik

Dalam dataset yang berisi 61.202 entri, terdapat lima kolom yang berkaitan dengan identitas pengguna serta pilihan program studi dan universitas, yaitu id_first_major, id_first_university, id_second_major, id_second_university, dan id_user. Berikut ini merupakan hasil analisis nilai unik dari masing-masing kolom tersebut:

### id_first_major (Jumlah unik: 1290)

- Kolom ini merepresentasikan pilihan program studi pertama yang dipilih oleh pengguna.

- Terdapat 1.290 jenis program studi berbeda yang dipilih sebagai pilihan pertama.

- Nilai ini menunjukkan variasi yang cukup tinggi dalam minat studi awal dari pengguna.

### id_first_university (Jumlah unik: 87)

- Kolom ini mencatat universitas pertama yang menjadi pilihan pengguna.

- Terdapat 87 universitas berbeda yang tercatat sebagai pilihan pertama.

- Ini menunjukkan bahwa pengguna memiliki beragam preferensi universitas dalam pilihan pertamanya.

### id_second_major (Jumlah unik: 1353)

- Kolom ini menunjukkan program studi kedua yang dipilih oleh pengguna (jika ada).

- Terdapat 1.353 jenis program studi berbeda sebagai pilihan kedua, bahkan lebih banyak dari pilihan pertama, yang dapat mengindikasikan bahwa pengguna mengeksplorasi lebih banyak opsi pada pilihan kedua.

### id_second_university (Jumlah unik: 86)

- Kolom ini menyimpan data universitas pilihan kedua pengguna.

- Terdapat 86 universitas berbeda yang dipilih pada pilihan kedua, sedikit lebih sedikit dibanding pilihan pertama.

### id_user (Jumlah unik: 61.202)

- Kolom ini merupakan identitas unik setiap pengguna dalam dataset.

- Jumlah nilai uniknya sama dengan jumlah total entri (61.202), yang menandakan bahwa tidak ada duplikasi pengguna, dan setiap baris dalam dataset merepresentasikan satu pengguna yang unik.

2. Cek Karakteristik Dataset

  Tahap ini meliputi analisis sifat-sifat dasar dari dataset, seperti jumlah baris, tipe data setiap kolom, serta statistik deskriptif seperti rata-rata, median, kuartil, nilai maksimum, minimum, dan standar deviasi. Pemahaman terhadap karakteristik dataset ini penting untuk memastikan kesiapan data dalam proses analisis dan mendeteksi potensi masalah. Pada dataset universitas, hasil pemeriksaan menunjukkan tidak adanya masalah signifikan, sehingga dapat disimpulkan bahwa dataset ini cukup valid dan siap digunakan.

# Data Preparation

## Data Preparation Umum

  Bagian ini menjelaskan berbagai langkah persiapan data yang dilakukan sebelum tahap pemodelan. Teknik-teknik ini meliputi pembersihan data, transformasi fitur, dan penggabungan dataset untuk memastikan data yang digunakan dalam model bersih, konsisten, dan sesuai kebutuhan analisis.

1. Penghapusan Kolom
   
  a. Kolom Unnamed: 0 pada Dataset Universitas, Major, dan Score_Humanities
  
  Kolom Unnamed: 0 muncul akibat proses ekspor file CSV yang secara otomatis menambahkan indeks baris sebagai kolom baru. Kolom ini tidak memiliki informasi penting atau relevansi terhadap proses analisis dan pemodelan. Oleh karena itu, kolom Unnamed: 0 dihapus dari ketiga dataset (universitas, major, dan score_humanities) untuk menyederhanakan struktur data dan menghindari kebingungan.
  
  
  b. Kolom id_second_major dan id_second_university pada Dataset Score_Humanities
  
  Dalam dataset score_humanities, setiap pengguna memiliki dua pilihan jurusan dan universitas: pilihan pertama (id_first_major, id_first_university) dan pilihan kedua (id_second_major, id_second_university). Namun, untuk keperluan sistem rekomendasi ini, hanya data dari pilihan pertama yang digunakan agar fokus dan konsistensi data tetap terjaga. Oleh karena itu, kolom id_second_major dan id_second_university dihapus karena tidak digunakan dalam proses analisis maupun pemodelan.

2. Penggantian Nama Kolom pada Dataset Score_Humanities

  Pada tahap ini, dilakukan proses penggantian nama kolom (rename) pada dataset score_humanities dengan tujuan untuk menyelaraskan penamaan kolom agar konsisten dengan dataset lain yang akan digabungkan. Secara spesifik, kolom id_first_major diubah namanya menjadi id_major, dan kolom id_first_university diubah menjadi id_university. Langkah ini penting agar saat proses penggabungan (merge) antar dataset, nama kolom yang menjadi kunci penggabungan memiliki kesamaan format dan memudahkan dalam analisis data selanjutnya. Setelah proses penggantian nama kolom, dilakukan pemeriksaan awal terhadap lima baris pertama dataset menggunakan fungsi head(5) untuk memastikan perubahan telah diterapkan dengan benar.
      
3. Pembuatan Fitur Rata-rata Nilai
   
  Tahap ini merupakan proses penghitungan rata-rata nilai ujian berdasarkan beberapa subtes yang menjadi syarat kualifikasi nilai ujian. Sebuah kolom baru bernama rata_rata_nilai dibuat dengan menghitung rata-rata dari beberapa nilai subtes, yaitu Ekonomi, Geografi, Kemampuan Membaca dan Menulis (KMB), Kemampuan Penalaran Umum (KPU), Kemampuan Kuantitatif (KUA), Matematika, Pengetahuan dan Pemahaman Umum (PPU), Sejarah, dan Sosial. 

4. Menggabungkan Tiga Dataset
   
Tahap ini dilakukan dengan menggabungkan tiga dataset, yaitu score_humanities, major, dan universitas. Penggabungan ini bertujuan untuk menyatukan informasi penting dari ketiga dataset agar analisis dapat dilakukan secara menyeluruh dan terpadu. Pada dataframe hasil gabungan, terdapat kolom-kolom utama seperti id_user, id_major, dan id_university yang tergabung dalam satu tabel lengkap dengan nama jurusan, kapasitas, serta nama universitas terkait. Data hasil penggabungan memiliki total 61.202 baris dan 8 kolom, dimana seluruh variabel dan baris telah sesuai serta konsisten. Selanjutnya, dilakukan pengecekan ulang untuk memastikan kualitas data sebelum digunakan dalam tahap analisis berikutnya.

5. Data Filtering

Pada tahap ini, dilakukan proses penyaringan data untuk memastikan hanya entri yang relevan dengan fokus analisis yang dipertahankan. Karena analisis difokuskan pada jurusan-jurusan dalam bidang sosial dan humaniora (humanities), maka entri dengan kategori science dianggap tidak relevan dan perlu dihapus dari dataset.

Proses filtering dilakukan dengan menghapus semua baris yang memiliki nilai 'science' pada kolom type. Langkah ini dilakukan menggunakan kode berikut:
merged_data_clean = merged_data[merged_data['type'] != 'science']

Dengan perintah ini, semua entri jurusan yang bertipe 'science' dihilangkan dari data gabungan (merged_data). Dataset hasil filtering disimpan dalam merged_data_clean dan menjadi dasar untuk analisis berikutnya.

Setelah proses ini, dilakukan verifikasi terhadap kolom type untuk memastikan bahwa nilai 'science' telah sepenuhnya dihapus. Hasil verifikasi menunjukkan bahwa dataset sudah hanya memuat jurusan dengan kategori selain 'science', sehingga sesuai dengan kebutuhan analisis pada bidang sosial dan humaniora.

6. Penanganan Missing Value

Setelah melakukan penggabungan beberapa dataset, ditemukan banyak baris yang memiliki nilai kosong (missing value). Hal ini terjadi karena adanya perbedaan jumlah baris antar dataset yang menyebabkan beberapa data tidak terpasangkan dengan sempurna. Variabel yang terdeteksi memiliki missing value antara lain type, major_name, capacity, id_university, dan university_name. Sementara itu, variabel id_major, id_user, dan rata_rata_nilai tidak mengalami missing value sama sekali. Selanjutnya, missing value pada variabel-variabel tersebut berhasil diatasi dengan metode penghapusan baris (dropping). Dengan demikian, kondisi data saat ini sudah bersih dari missing value sehingga siap digunakan untuk pelatihan model agar hasilnya optimal.

7. Penanganan Kolom Duplikat
   
Setelah dilakukan pengurutan data, tahap berikutnya adalah memeriksa adanya duplikasi pada kolom id_major, yang akan digunakan dalam proses pelatihan model. Ditemukan bahwa kolom tersebut memiliki sebanyak 61.202 data duplikat. Jika tidak diatasi, keberadaan duplikasi ini dapat memengaruhi kualitas hasil pelatihan model. Oleh karena itu, seluruh duplikasi pada kolom id_major dihapus. Setelah proses pembersihan ini, jumlah data yang tersisa, khususnya pada kolom id_major, menjadi 1.286 baris unik, yang akan digunakan sebagai data final dalam pelatihan model.

## Data Preparation - Content Based Filtering

1. Konversi Data Series Menjadi List

Dalam tahap ini, dilakukan proses konversi data dari tipe pandas.Series ke dalam format list. Tujuan dari langkah ini adalah untuk mempermudah manipulasi dan penggunaan data pada tahap-tahap analisis lanjutan, khususnya dalam implementasi sistem rekomendasi atau model machine learning yang umumnya menerima input dalam format list.

Kolom yang dikonversi antara lain:

- id_major → merepresentasikan ID jurusan,

- university_name → nama universitas tempat jurusan berada,

- major_name → nama jurusan atau program studi.

Proses konversi dilakukan menggunakan fungsi .tolist() dari pustaka pandas, yang menghasilkan tiga buah list:

id_major = p['id_major'].tolist()
nama_Univ = p['university_name'].tolist()
nama_Prodi = p['major_name'].tolist()

Setelah konversi, dilakukan verifikasi terhadap panjang masing-masing list untuk memastikan tidak terjadi kehilangan atau ketidaksesuaian data. Hasil verifikasi menunjukkan bahwa ketiganya memiliki panjang yang sama, yaitu sebanyak 1.286 entri, sehingga dapat disimpulkan bahwa proses konversi berhasil dilakukan dengan benar dan data dalam list sudah siap digunakan untuk proses selanjutnya.

Langkah ini penting karena list merupakan struktur data yang lebih fleksibel untuk digunakan dalam iterasi, pemetaan, serta integrasi ke dalam berbagai algoritma analisis dan pemodelan.

2. Membuat Dictionary
   
Pada tahap ini, dilakukan pembuatan struktur data dictionary dalam bentuk DataFrame untuk memetakan hubungan antara ID jurusan (id_major), nama universitas (university_name), dan nama jurusan (major_name). Tujuan pembuatan dictionary ini adalah untuk memudahkan proses pencarian dan pengelolaan data dengan menggunakan pasangan key-value, sehingga data numerik yang digunakan oleh model atau sistem rekomendasi dapat dihubungkan kembali dengan informasi yang mudah dipahami oleh pengguna.

Penggunaan dictionary sangat penting dalam konteks sistem rekomendasi, di mana model biasanya bekerja dengan data berbasis ID atau angka agar proses komputasi menjadi lebih efisien. Namun, hasil akhir yang disajikan kepada pengguna harus tetap menggunakan nama jurusan dan universitas agar informatif dan mudah dimengerti.

Implementasi pembuatan dictionary dilakukan dengan menggabungkan list yang sudah dikonversi sebelumnya (id_major, nama_Univ, dan nama_Prodi) ke dalam sebuah DataFrame id_new, seperti pada kode berikut:

id_new = pd.DataFrame({
    'id_major': id_major,
    'university_name': nama_Univ,
    'major_name': nama_Prodi
})

DataFrame hasil penggabungan ini berisi 1.286 baris data, di mana setiap baris merepresentasikan satu jurusan beserta universitas terkait. Contoh isi beberapa baris data dapat dilihat pada sampel berikut:

| id\_major | university\_name           | major\_name                         |
| --------- | -------------------------- | ----------------------------------- |
| 3322014   | INSTITUT TEKNOLOGI BANDUNG | FAKULTAS SENIRUPA DAN DESAIN (FSRD) |
| 3212057   | UNIVERSITAS INDONESIA      | ILMU KOMUNIKASI                     |
| 3722057   | UNIVERSITAS BRAWIJAYA      | MANAJEMEN                           |
| 3212081   | UNIVERSITAS INDONESIA      | KRIMINOLOGI                         |
| 3812106   | UNIVERSITAS AIRLANGGA      | AKUNTANSI                           |

Selanjutnya, data ini dicek kembali dengan menampilkan beberapa sampel secara acak untuk memastikan integritas data tetap terjaga setelah proses penggabungan:

data = id_new
data.sample(5)

Pembuatan dictionary ini menjadi dasar penting dalam proses transformasi dan interpretasi data, terutama ketika data numerik hasil pemodelan perlu dikaitkan kembali dengan nama jurusan dan universitas dalam sistem rekomendasi agar hasil analisis dapat disajikan secara informatif dan user-friendly.

3. TF-IDF Vectorizer
   
Pada tahap ini, digunakan metode TF-IDF (Term Frequency-Inverse Document Frequency) untuk mengukur tingkat kepentingan setiap kata dalam nama jurusan (major_name) terhadap keseluruhan data jurusan yang ada. TF-IDF adalah teknik yang mengombinasikan dua konsep utama:

- Term Frequency (TF): Menghitung frekuensi kemunculan kata dalam satu dokumen (dalam hal ini, nama jurusan).

- Inverse Document Frequency (IDF): Menilai seberapa umum kata tersebut muncul di seluruh kumpulan dokumen, sehingga kata-kata yang sangat sering muncul di banyak dokumen akan memiliki bobot lebih rendah.

Penggunaan TF-IDF membantu dalam menyeimbangkan bobot kata sehingga kata-kata yang sering muncul di hampir semua jurusan tidak terlalu dominan, dan kata-kata unik atau penting lebih diberi bobot yang lebih besar. Hal ini membuat analisis menjadi lebih akurat dibandingkan hanya mengandalkan frekuensi kata biasa.

Proses ini dilakukan dengan memanfaatkan fungsi TfidfVectorizer() dari pustaka scikit-learn. Variabel major_name digunakan sebagai input, di mana setiap nama jurusan diolah untuk menghasilkan matriks fitur TF-IDF. Fungsi ini secara otomatis melakukan pemetaan dari indeks fitur numerik ke nama kata dan mengubah data menjadi bentuk matriks sparse.

Contoh kata-kata yang dihasilkan sebagai fitur dari proses ini antara lain:

['adm', 'admin', 'administrasi', 'agama', 'akuntansi', 'bahasa', 'ekonomi', 'filsafat', 'hukum', 'komunikasi', 'kriminologi', 'manajemen', 'musik', 'pendidikan', 'politik', 'psikologi', 'sastra', 'sejarah', 'seni', 'teknik', 'teknologi', ...]

Matriks TF-IDF yang dihasilkan memiliki ukuran 1286 x 230, di mana:

- 1286 adalah jumlah jurusan (baris),

- 230 adalah jumlah kata unik (kolom) yang menjadi fitur.

Matriks ini kemudian dikonversi ke dalam bentuk dense matrix dengan fungsi .todense() sebagai persiapan untuk proses perhitungan kemiripan antar jurusan menggunakan metode Cosine Similarity pada tahap berikutnya.

Berikut contoh representasi matriks TF-IDF dalam bentuk DataFrame dengan kolom mewakili kata-kata fitur dan baris mewakili jurusan berdasarkan id_major:

| id\_major | adm | administrasi | agama | akuntansi | ... | seni | teknik | teknologi |
| --------- | --- | ------------ | ----- | --------- | --- | ---- | ------ | --------- |
| 3652225   | 0.0 | 0.0          | 0.0   | 0.0       | ... | 0.0  | 0.0    | 0.0       |
| 3552093   | 0.0 | 0.0          | 0.0   | 0.0       | ... | 0.0  | 0.0    | 0.0       |
| 3232023   | 0.0 | 0.0          | 0.0   | 0.0       | ... | 0.0  | 0.0    | 0.0       |
| ...       | ... | ...          | ...   | ...       | ... | ...  | ...    | ...       |

Kelebihan TF-IDF:
- Menangkap Kepentingan Kata: Mampu menurunkan bobot kata-kata umum sehingga fokus pada kata-kata yang lebih relevan.

- Sederhana dan Efektif: Mudah diimplementasikan dan efisien untuk pengolahan teks dan sistem rekomendasi.

- Tidak Memerlukan Label: Dapat diterapkan pada data teks tanpa perlu anotasi khusus.

Kekurangan TF-IDF:
- Tidak Memperhitungkan Konteks: Mengabaikan urutan kata dan konteks kalimat sehingga makna bisa kurang tepat.

- Rentan pada Sinonim dan Ambiguitas: Tidak membedakan kata dengan makna berbeda tetapi bentuk sama, maupun sinonim.

- Dimensi Matriks Besar: Pada data besar, matriks bisa sangat besar dan sparse sehingga memerlukan kapasitas memori dan komputasi yang tinggi.

## Data Preparation - Collaborative Filtering

1. Encode Dataset

Pada tahap awal persiapan data untuk metode Collaborative Filtering, diperlukan proses encoding pada variabel kategorikal agar dapat diproses oleh model pembelajaran mesin yang umumnya hanya menerima input dalam bentuk numerik.

Variabel yang di-encode pada tahap ini adalah:

- id_user — ID unik dari pengguna (user)

- id_major — ID unik dari jurusan (major)

Proses yang dilakukan:
  1. Mendapatkan nilai unik dari id_user dan id_major menggunakan fungsi .unique().
  Ini bertujuan untuk mengeliminasi duplikasi sehingga setiap nilai hanya muncul sekali.
  
  2. Mengubah array unik tersebut menjadi list dengan fungsi .tolist().
  List ini memudahkan proses encoding selanjutnya.
  
  3. Melakukan encoding dengan memetakan setiap nilai unik ke indeks integer menggunakan fungsi dictionary comprehension.
  Contoh: User dengan id_user tertentu di-mapping ke angka 0, user berikutnya ke 1, dan seterusnya. Hal yang sama dilakukan untuk id_major.
  
  4. Membuat mapping balik dari indeks integer ke nilai asli untuk memudahkan interpretasi hasil setelah pemodelan.

Proses encoding ini sangat penting agar data yang awalnya berupa string atau ID kategorikal dapat diproses oleh algoritma collaborative filtering yang menggunakan representasi numerik.

2. Mapping Features

Setelah melakukan encoding pada variabel id_user dan id_major menjadi indeks numerik unik, langkah selanjutnya adalah melakukan pemetaan hasil encoding tersebut ke dalam dataframe utama. Pada tahap ini, nilai-nilai id_user dan id_major diubah menjadi representasi numerik yang kemudian disimpan ke dalam kolom baru bernama user dan prodi. Proses pemetaan ini sangat penting karena algoritma machine learning, termasuk metode Collaborative Filtering, memerlukan input dalam bentuk angka agar dapat memproses data dengan lebih efisien. Dengan melakukan mapping ini, setiap pengguna dan program studi memiliki identitas numerik yang unik dan konsisten untuk keperluan analisis dan pemodelan.

Setelah proses mapping, dilakukan analisis statistik deskriptif untuk memahami karakteristik data secara keseluruhan. Dari hasil analisis, diketahui bahwa terdapat 1.286 pengguna unik dan 346 program studi berbeda dalam dataset ini. Selain itu, nilai rata-rata tes mahasiswa yang terekam memiliki rentang yang cukup luas, dengan nilai minimum sebesar 346,33 dan nilai maksimum mencapai 691,67. Informasi ini memberikan gambaran awal tentang jumlah entitas yang terlibat serta variasi nilai yang akan diproses dalam tahap pemodelan berikutnya. Dengan demikian, tahap mapping dan analisis statistik ini menjadi fondasi penting dalam memastikan data siap untuk diolah lebih lanjut menggunakan metode Collaborative Filtering.

3. Split Data Menjadi Train dan Validasi

Pada tahap ini, dilakukan proses pra-pemrosesan data dengan tujuan menyiapkan dataset agar siap digunakan dalam pelatihan model. Pertama-tama, seluruh data dalam dataframe df diacak menggunakan fungsi .sample() dengan parameter frac=1, yang berarti seluruh baris data diacak, dan random_state=42 agar pengacakan bersifat konsisten dan dapat direproduksi di lain waktu. Pengacakan ini penting untuk memastikan bahwa distribusi data pada tahap pelatihan dan validasi tidak bias dan mewakili kondisi data secara keseluruhan.

Setelah data diacak, kolom user dan prodi yang sudah berisi nilai numerik hasil encoding dipisahkan sebagai fitur input (x). Sementara itu, kolom target rata_rata_nilai dinormalisasi menggunakan teknik Min-Max Scaling agar nilainya berada dalam rentang 0 hingga 1. Normalisasi ini bertujuan agar perbedaan skala antar fitur tidak mempengaruhi proses pembelajaran model dan mempercepat konvergensi saat pelatihan.

Selanjutnya, dataset dibagi menjadi dua bagian, yaitu 80% data untuk pelatihan (train) dan 20% sisanya untuk validasi (validation). Pembagian ini dilakukan secara langsung dengan mengambil potongan data setelah pengacakan, sehingga model dapat dilatih dengan sebagian besar data dan diuji kinerjanya pada data yang belum pernah dilihat sebelumnya. Pendekatan ini dikenal dengan istilah train-test split, yang merupakan teknik umum dalam machine learning untuk memastikan evaluasi model yang lebih objektif dan menghindari overfitting.

Dengan demikian, pada akhir proses ini diperoleh variabel x_train dan y_train sebagai data fitur dan target untuk pelatihan, serta x_val dan y_val sebagai data untuk validasi model. Data yang sudah terpisah dan ternormalisasi ini siap digunakan dalam tahap pelatihan model Collaborative Filtering selanjutnya.

# Modeling | Content Based Filtering

## Content Based Filtering

  Tahap berikutnya adalah proses pemodelan, yaitu pembuatan model machine learning yang akan digunakan sebagai sistem rekomendasi untuk memberikan rekomendasi buku terbaik kepada pengguna dengan menggunakan beberapa algoritma tertentu.
  
  Sistem rekomendasi berbasis Content-Based Filtering (CB) bekerja dengan memberikan rekomendasi berdasarkan deskripsi atau karakteristik dari item itu sendiri. Model ini mempelajari preferensi pengguna dengan mencocokkan item yang memiliki kemiripan dengan item yang sebelumnya disukai atau sedang dikaji oleh pengguna. Semakin banyak informasi yang tersedia mengenai pengguna, maka tingkat akurasi rekomendasi yang dihasilkan juga akan semakin meningkat.

  **Kelebihan Content-Based Filtering:**
  
  - Transparansi: Rekomendasi yang dihasilkan dapat dijelaskan melalui analisis fitur atau konten dari item yang diminati oleh pengguna.
    
  - Tidak Bergantung pada Data Pengguna Lain: Sistem hanya menggunakan preferensi dan riwayat pengguna secara individual, sehingga tidak memerlukan data dari pengguna lain.
    
  - Mampu Mengakomodasi Item Baru: Dapat memberikan rekomendasi untuk item baru yang belum pernah dinilai oleh pengguna lain, selama item tersebut memiliki karakteristik yang serupa dengan item favorit pengguna.
  
  **Kekurangan Content-Based Filtering:**
  
  - Keterbatasan dalam Analisis Konten: Rekomendasi dapat kurang akurat apabila analisis terhadap fitur atau konten item tidak mendalam, terutama untuk item dengan fitur yang kompleks.
    
  - Sulit Menyesuaikan dengan Perubahan Preferensi: Sistem cenderung memberikan rekomendasi yang serupa dengan item yang pernah disukai pengguna, sehingga kurang responsif terhadap perubahan selera pengguna.
    
  - Terbatas dalam Keanekaragaman Rekomendasi: Rekomendasi yang dihasilkan cenderung homogen dan kurang beragam karena berfokus pada kemiripan dengan item yang telah dipilih sebelumnya.

## Cosine Similarity

Tahap perhitungan Cosine Similarity bertujuan untuk mengukur tingkat kemiripan antara dua item dalam ruang vektor, yang dalam konteks ini diaplikasikan pada program studi (prodi) berdasarkan representasi vektor hasil transformasi TF-IDF. Cosine similarity bekerja dengan menghitung sudut kosinus antara dua vektor; semakin kecil sudutnya, semakin besar nilai kemiripan yang dihasilkan, dengan nilai berkisar antara 0 hingga 1. Teknik ini sangat berguna dalam pendekatan content-based filtering, karena memungkinkan sistem untuk menemukan item yang mirip satu sama lain berdasarkan konten atau atributnya.

Dalam implementasinya, proses ini diawali dengan menghitung matriks kemiripan dari tfidf_matrix menggunakan fungsi cosine_similarity() dari pustaka sklearn. Hasilnya adalah sebuah array dua dimensi (cosine_sim) yang menunjukkan nilai kemiripan antara setiap pasangan program studi. Nilai diagonal dari matriks ini adalah 1 karena setiap item memiliki kemiripan maksimum dengan dirinya sendiri. Nilai-nilai lainnya merepresentasikan tingkat kemiripan antar program studi yang berbeda, dengan sebagian besar nilai mendekati nol karena sifat data TF-IDF yang cenderung spars (jarang).

Selanjutnya, hasil dari perhitungan cosine similarity disimpan dalam bentuk DataFrame baru (cosine_sim_df), dengan indeks dan kolom berupa nilai id_major, sehingga memudahkan pencarian kemiripan antar prodi secara langsung berdasarkan ID-nya. Struktur dari cosine_sim_df berbentuk matriks simetris berukuran 1286x1286, yang berarti seluruh kombinasi kemiripan antar 1.286 program studi telah dihitung.

  **Kelebihan Cosine Similarity:**
  
  - Mengabaikan Skala: Cosine similarity hanya mempertimbangkan arah vektor, sehingga tidak terpengaruh oleh panjang atau besar nilai fitur. Ini cocok untuk data teks atau fitur berbasis frekuensi seperti TF-IDF.
  
  - Efisien untuk Data Sparsity: Cocok untuk data berdimensi tinggi dan spars (jarang), seperti representasi dokumen atau user-item matrix.
  
  - Mudah Diimplementasikan: Fungsi cosine similarity sudah tersedia dalam banyak pustaka Python (seperti sklearn), sehingga mudah digunakan dalam proyek.
  
  - Hasil Interpretatif: Nilai hasil cosine similarity berada di antara 0 dan 1 (atau -1 jika tidak dibatasi), yang mudah dipahami dalam konteks kemiripan.
  
  **Kekurangan Cosine Similarity:**
  
  - Tidak Memperhatikan Magnitudo: Karena hanya memperhatikan arah, informasi tentang seberapa besar vektor diabaikan. Ini bisa menjadi kelemahan jika besar nilai sebenarnya penting.
  
  - Kurang Akurat untuk Data Non-Teks: Metode ini sangat cocok untuk data berbasis teks, tetapi kurang optimal untuk jenis data lain jika tidak diolah terlebih dahulu dengan baik.
  
  - Skalabilitas: Pada dataset yang sangat besar, menghitung kesamaan kosinus antara banyak item bisa memerlukan waktu dan memori yang besar.
  
  - Tidak Menangani Konteks: Cosine similarity hanya melihat kemiripan statis antar fitur, tanpa mempertimbangkan konteks historis atau perilaku pengguna.

## Top-N Recommendation | Content-Based Filtering

  Pada tahap ini, dibuat sebuah fungsi yang bertujuan menghasilkan rekomendasi jurusan. Fungsi ini memiliki beberapa parameter, dengan satu parameter wajib yaitu id_major (ID jurusan yang ingin dicari rekomendasinya), serta beberapa parameter opsional seperti similarity_data (matriks hasil perhitungan kesamaan kosinus antar jurusan), items (DataFrame yang berisi detail setiap jurusan seperti ID, nama universitas, dan nama jurusan), dan k (jumlah rekomendasi yang diinginkan, dengan nilai default sebanyak 5).
  
  Fungsi ini bekerja dengan memanfaatkan argpartition() untuk melakukan partisi elemen-elemen secara tidak langsung berdasarkan nilai kesamaan, kemudian data diubah menjadi array NumPy dan dilakukan proses pengurutan untuk menentukan indeks dengan tingkat kesamaan tertinggi. Selanjutnya, ID jurusan yang menjadi input akan dihapus dari daftar hasil agar sistem tidak merekomendasikan jurusan yang sama dengan pilihan awal pengguna, menggunakan fungsi drop().

  Sebagai output, fungsi ini akan mengembalikan sebuah DataFrame yang berisi k jurusan dengan tingkat kemiripan tertinggi berdasarkan jurusan input. Berikut ini merupakan tampilan input dari pengguna dan hasil rekomendasi jurusan yang diberikan oleh sistem:
  
  **Jurusan Target (ID: 7112114)**
    
  | id\_major | university\_name       | major\_name                 |
  | --------- | ---------------------- | --------------------------- |
  | 7112114   | UNIVERSITAS HASANUDDIN | ILMU HUBUNGAN INTERNASIONAL |
  
  **5 Rekomendasi Teratas Berdasarkan Jurusan Target**
      
  | id\_major | university\_name                  | major\_name                 |
  | --------- | --------------------------------- | --------------------------- |
  | 1332094   | UNIVERSITAS MARITIM RAJA ALI HAJI | ILMU HUBUNGAN INTERNASIONAL |
  | 5412075   | UNIVERSITAS MULAWARMAN            | ILMU HUBUNGAN INTERNASIONAL |
  | 1712183   | UNIVERSITAS SRIWIJAYA             | ILMU HUBUNGAN INTERNASIONAL |
  | 1412141   | UNIVERSITAS ANDALAS               | ILMU HUBUNGAN INTERNASIONAL |
  | 3212177   | UNIVERSITAS INDONESIA             | ILMU HUBUNGAN INTERNASIONAL |

  Berdasarkan hasil pada Tabel 2, jurusan dengan ID 7112114 yaitu Ilmu Hubungan Internasional direkomendasikan 5 jurusan serupa yang memiliki kesamaan pada kata kunci “Ilmu Hubungan Internasional”.

## Model Development | Collaborative Filtering
  Collaborative Filtering merupakan salah satu metode yang digunakan dalam sistem rekomendasi dengan prinsip memberikan rekomendasi berdasarkan preferensi pengguna lain yang memiliki pola minat serupa. Dalam konteks proyek sistem rekomendasi jurusan ini, Collaborative Filtering berfungsi untuk menyarankan jurusan kepada pengguna berdasarkan kesamaan pilihan atau interaksi pengguna lain dalam dataset.
  
  Secara teknis, metode ini memanfaatkan matriks interaksi antara pengguna dan jurusan, di mana setiap baris merepresentasikan pengguna dan setiap kolom merepresentasikan jurusan. Collaborative Filtering kemudian mengidentifikasi pengguna lain yang memiliki preferensi atau perilaku serupa, dan merekomendasikan jurusan yang disukai oleh pengguna serupa tersebut. Contohnya, apabila dua pengguna memiliki ketertarikan pada jurusan yang sama, maka jurusan lain yang diminati oleh salah satu pengguna dapat direkomendasikan kepada pengguna lainnya.

**Kelebihan Collaborative Filtering:**

  - Tidak memerlukan informasi detail tentang konten jurusan: Metode ini tidak bergantung pada karakteristik atau deskripsi jurusan, sehingga tidak membutuhkan analisis fitur secara eksplisit.
    
  - Mampu menangkap preferensi pengguna yang kompleks: Dengan memanfaatkan pola interaksi pengguna, metode ini dapat memberikan rekomendasi yang sesuai dengan minat unik dan kompleks pengguna.
    
  - Adaptif terhadap preferensi pengguna: Seiring bertambahnya data interaksi, sistem mampu meningkatkan akurasi rekomendasi yang diberikan secara personal.

**Kekurangan Collaborative Filtering:**

  - Permasalahan Cold Start: Sistem kesulitan memberikan rekomendasi untuk pengguna baru maupun jurusan baru yang belum memiliki data interaksi.
  
  - Sparsity atau Keterbatasan Data: Jika data interaksi pengguna dan jurusan sangat sedikit atau jarang, performa rekomendasi dapat menurun karena sulit menemukan pola kemiripan.
  
  - Masalah Skalabilitas: Pada dataset besar dengan banyak pengguna dan jurusan, perhitungan kesamaan menjadi lebih kompleks dan membutuhkan sumber daya komputasi yang tinggi.

## Generate Class RecommenderNet

  Pada tahap ini, kelas RecommenderNet didefinisikan sebagai model jaringan saraf tiruan untuk sistem rekomendasi. Model ini memanfaatkan embedding layers untuk merepresentasikan pengguna (mahasiswa) dan produk (program studi) dalam ruang fitur berdimensi rendah (embedding space). Setiap pengguna dan produk diwakili oleh vektor embedding dengan ukuran yang ditentukan oleh parameter embedding_size. Embedding layers berfungsi untuk mengekstraksi representasi vektor dari pengguna dan produk, sedangkan embedding bias layers digunakan untuk menangani bias yang melekat pada setiap pengguna dan produk. Selanjutnya, dalam metode call, vektor embedding pengguna dan produk diambil berdasarkan input yang diberikan, kemudian dilakukan operasi dot product antara kedua vektor tersebut. Hasil dari operasi ini kemudian dijumlahkan dengan bias pengguna dan bias produk, lalu dilewatkan melalui fungsi aktivasi sigmoid. Output akhir dari model berupa probabilitas yang merepresentasikan kemungkinan pengguna (mahasiswa) menyukai produk (program studi) yang direkomendasikan.

## Compile Model

  Pada tahap ini, model RecommenderNet yang telah dirancang sebelumnya akan dilakukan proses kompilasi. Proses dimulai dengan menginisialisasi model menggunakan parameter jumlah pengguna (num_user), jumlah produk (num_prodi), dan ukuran embedding (embedding_size) yang ditetapkan sebesar 50 dan diberikan sebagai argumen saat pembuatan objek model. Selanjutnya, model dikompilasi dengan menentukan fungsi kerugian (loss function), optimizer, dan metrik evaluasi yang akan digunakan selama proses pelatihan. Fungsi kerugian yang dipilih adalah Binary Crossentropy karena permasalahan ini merupakan klasifikasi biner, yaitu memprediksi apakah pengguna menyukai suatu produk atau tidak. Optimizer yang digunakan adalah Adam (Adaptive Moment Estimation), yang bertugas mengoptimalkan proses pelatihan dengan memperbarui bobot model secara efisien. Sedangkan metrik evaluasi yang dipakai adalah Root Mean Squared Error (RMSE) untuk mengukur performa model selama pelatihan. Setelah tahap kompilasi selesai, model siap untuk dilatih menggunakan data yang tersedia.

## Implementasi Fungsi Callback

  Dalam rangka meningkatkan efektivitas dan efisiensi proses pelatihan model, digunakan dua fungsi callback yakni ReduceLROnPlateau() dan EarlyStopping(). Fungsi-fungsi callback ini memungkinkan model secara dinamis menyesuaikan laju pembelajaran (learning rate) selama pelatihan sehingga memudahkan model untuk mencapai titik konvergensi yang optimal dalam melakukan generalisasi terhadap data. Pada tahap ini, dua callback didefinisikan untuk diaplikasikan selama pelatihan model jaringan saraf.
  
  Pertama, ReduceLROnPlateau berfungsi untuk menurunkan laju pembelajaran apabila tidak terdapat peningkatan pada nilai loss dari data validasi (val_loss) setelah sejumlah epoch tertentu (parameter patience). Penurunan laju pembelajaran dilakukan dengan faktor pengurangan yang ditentukan oleh parameter factor, sementara parameter min_lr menetapkan batas bawah laju pembelajaran yang dapat dicapai.
  
  Kedua, EarlyStopping bertugas untuk menghentikan proses pelatihan secara otomatis jika nilai loss pada data validasi tidak mengalami penurunan setelah sejumlah epoch tertentu. Hal ini berguna untuk mencegah overfitting sekaligus menghemat waktu pelatihan. Parameter restore_best_weights=True memastikan bahwa bobot model akan dikembalikan ke kondisi terbaik yang tercapai selama pelatihan saat proses dihentikan.
  
## Training Model

  Pada tahap ini, model jaringan saraf dilatih menggunakan metode fit() pada objek model yang telah dikompilasi sebelumnya. Proses pelatihan dilakukan dengan menggunakan data latih (x_train dan y_train) dengan ukuran batch sebesar 64 dan dijalankan selama 100 epoch. Data validasi (x_val dan y_val) digunakan untuk memonitor performa model sepanjang pelatihan. Selama proses pelatihan, dua callback yaitu reduce_lr dan early_stop diterapkan untuk mengoptimalkan proses. Fungsi reduce_lr secara otomatis menurunkan laju pembelajaran apabila tidak terjadi perbaikan pada nilai loss data validasi (val_loss) dalam beberapa epoch, sedangkan early_stop menghentikan pelatihan lebih awal jika tidak ada penurunan nilai loss pada data validasi setelah sejumlah epoch tertentu. Semua hasil dari proses pelatihan tersebut disimpan dalam variabel history yang nantinya dapat digunakan untuk keperluan analisis atau visualisasi performa model.

## Top-N Recommendation

  Tahap ini melibatkan beberapa proses utama. Pertama, dilakukan pengambilan sampel data secara acak dari dataframe df untuk mengekstraksi seluruh program studi (prodi) yang telah dipilih oleh pengguna tertentu. Selanjutnya, program studi yang belum dipilih oleh pengguna tersebut diidentifikasi dan difilter agar hanya program studi yang terdapat dalam kamus encoding prodi yang menjadi objek pertimbangan.
  
  Setelah itu, dibuat sebuah array yang berisi ID pengguna yang diulang sebanyak jumlah prodi yang tidak dipilih, serta ID dari prodi-prodi yang belum dipilih tersebut. Array ini digunakan untuk memprediksi skor atau rating bagi setiap pasangan pengguna-prodi menggunakan model yang telah dilatih. Berdasarkan prediksi tersebut, 10 program studi dengan skor tertinggi kemudian dipilih sebagai rekomendasi. Rekomendasi ini kemudian disajikan bersamaan dengan program studi yang sebelumnya telah dipilih oleh pengguna, untuk memberikan konteks yang lebih jelas terkait preferensi pengguna.

  Selanjutnya, model collaborative filtering yang telah dilatih sebelumnya digunakan untuk memprediksi skor untuk setiap pasangan pengguna-prodi yang belum dipilih. Sepuluh program studi dengan skor tertinggi dipilih sebagai rekomendasi, kemudian ID program studi tersebut dikonversi kembali menjadi nama program studi. Selain itu, daftar program studi yang telah dipilih oleh pengguna beserta nama universitasnya juga ditampilkan sebagai pembanding terhadap rekomendasi yang diberikan. Akhirnya, daftar 10 program studi rekomendasi bersama dengan nama universitasnya ditampilkan guna membantu pengguna dalam pengambilan keputusan. Proses ini bertujuan untuk memberikan gambaran yang komprehensif mengenai pilihan program studi yang relevan dengan preferensi pengguna, sekaligus menawarkan alternatif yang sesuai berdasarkan model collaborative filtering yang sudah dikembangkan.
  
  Tabel 3. Input untuk user dengan id 258842 dan jurusan 'MANAJEMEN' :
| index | id\_major | id\_user | rata\_rata\_nilai | type       | major\_name | capacity | id\_university | university\_name           | user | prodi |
| ----- | --------- | -------- | ----------------- | ---------- | ----------- | -------- | -------------- | -------------------------- | ---- | ----- |
| 44681 | 7412013   | 258842   | 445.888889        | humanities | MANAJEMEN   | 120.0    | 741.0          | UNIVERSITAS SULAWESI BARAT | 1205 | 1205  |

  Tabel 4. Hasil rekomendasi untuk user dengan id 258842 dan jurusan 'MANAJEMEN' :
| index | id\_major | id\_user | rata\_rata\_nilai | type       | major\_name               | capacity | id\_university | university\_name                    | user | prodi |
| ----- | --------- | -------- | ----------------- | ---------- | ------------------------- | -------- | -------------- | ----------------------------------- | ---- | ----- |
| 19280 | 9112025   | 129964   | 584.111111        | humanities | ILMU ADMINISTRASI NEGARA  | 18.0     | 911.0          | UNIVERSITAS CENDERAWASIH            | 1007 | 1007  |
| 15603 | 9112041   | 107461   | 552.333333        | humanities | ILMU HUKUM                | 65.0     | 911.0          | UNIVERSITAS CENDERAWASIH            | 966  | 966   |
| 462   | 3552015   | 4204     | 555.777778        | humanities | SASTRA INDONESIA          | 60.0     | 355.0          | UNIVERSITAS DIPONEGORO              | 286  | 286   |
| 416   | 3312035   | 3872     | 556.444444        | humanities | AKUNTANSI                 | 111.0    | 331.0          | UNIVERSITAS SINGAPERBANGSA KARAWANG | 266  | 266   |
| 517   | 3732245   | 4605     | 588.000000        | humanities | BAHASA DAN SASTRA INGGRIS | 30.0     | 373.0          | UNIVERSITAS NEGERI MALANG           | 319  | 319   |
| 84    | 3532162   | 769      | 571.777778        | humanities | PENDIDIKAN SEJARAH        | 40.0     | 353.0          | UNIVERSITAS SEBELAS MARET           | 82   | 82    |
| 111   | 1422062   | 1037     | 569.444444        | humanities | PSIKOLOGI                 | 120.0    | 142.0          | UNIVERSITAS NEGERI PADANG           | 104  | 104   |
| 5754  | 3642076   | 45028    | 594.777778        | humanities | SENI RUPA MURNI           | 45.0     | 364.0          | ISI YOGYAKARTA                      | 812  | 812   |
| 1055  | 3642092   | 10558    | 576.222222        | humanities | DESAIN INTERIOR           | 41.0     | 364.0          | ISI YOGYAKARTA                      | 473  | 473   |
| 112   | 3222102   | 1039     | 588.444444        | humanities | ILMU HUKUM                | 48.0     | 322.0          | UNIVERSITAS ISLAM NEGERI JAKARTA    | 105  | 105   |


Berdasarkan tabel di atas, sistem menampilkan jurusan yang relevan dengan skor rata-rata nilai yang dimasukkan oleh pengguna. Sistem rekomendasi ini menyajikan 10 program studi yang belum pernah dipilih oleh pengguna, dengan variasi skor rata-rata nilai mulai dari yang lebih rendah hingga lebih tinggi dibandingkan skor input pengguna. Dengan demikian, pengguna dapat melihat berbagai pilihan jurusan yang sesuai dengan kemampuan mereka berdasarkan rentang skor rekomendasi dari nilai terendah hingga tertinggi

## Visualisasi Metrik
![image](https://github.com/user-attachments/assets/73e7103d-4501-4fc7-98d3-07ea463610e9)

Grafik di atas menunjukkan tren Root Mean Squared Error (RMSE) selama proses pelatihan model terhadap jumlah epoch. Terlihat bahwa nilai RMSE pada data pelatihan (train) mengalami penurunan yang cukup signifikan seiring bertambahnya epoch, menunjukkan bahwa model semakin baik dalam mempelajari pola dari data latih. Namun, nilai RMSE pada data pengujian (test) relatif stabil dan tidak menunjukkan penurunan berarti setelah beberapa epoch awal. Perbedaan yang cukup jelas antara kurva pelatihan dan pengujian ini mengindikasikan adanya gejala overfitting, di mana model terlalu menyesuaikan diri terhadap data pelatihan dan kurang mampu melakukan generalisasi terhadap data baru. Oleh karena itu, diperlukan strategi seperti early stopping, regularisasi, atau peningkatan kualitas data untuk mengatasi masalah ini.

# Evaluation
1. Model Content Based Filtering
   
Hasil dari penerapan metode Content-Based Filtering menunjukkan bahwa sistem rekomendasi mampu memberikan output yang cukup akurat. Dari 5 rekomendasi yang dihasilkan, sebagian besar memiliki kesamaan tema atau kata kunci dengan jurusan target yang diberikan oleh pengguna. Untuk mengukur kinerja sistem, digunakan metrik evaluasi Precision@5, yaitu proporsi rekomendasi relevan yang muncul dalam lima rekomendasi teratas. Metrik ini sesuai digunakan karena fokus sistem adalah memberikan saran jurusan yang paling relevan bagi pengguna. Rumus dari metrik Recommender System Precision (RSP) adalah sebagai berikut:
   
$RSP = \frac{RR}{RA}$
   
  Keterangan:
  
  - RR = Jumlah rekomendasi yang relevan atau sesuai dengan preferensi pengguna
  - RA = Total jumlah rekomendasi yang dihasilkan oleh model
  
Untuk pengujian pada jurusan dengan id_major = 3612135 (SASTRA PRANCIS), sistem menghasilkan 5 rekomendasi, dengan 4 di antaranya relevan, seperti jurusan Sastra Prancis dan Pendidikan Bahasa Prancis. Hasil evaluasi programatik menunjukkan bahwa Precision@5 = 0.8, artinya 80% dari rekomendasi yang diberikan sistem sesuai dengan preferensi pengguna. Ini menunjukkan bahwa sistem sudah cukup baik dalam memahami dan menyarankan jurusan yang berkaitan, meskipun masih ada ruang untuk perbaikan.
  
  Berikut tampilan input user dan hasil rekomendasi berdasarkan input tersebut:
  
  - Tabel 1. Data Jurusan dengan Id 3612135 :
  
| id\_major | university\_name        | major\_name    |
| --------- | ----------------------- | -------------- |
| 3612135   | UNIVERSITAS GADJAH MADA | SASTRA PRANCIS |
  
  - Tabel 2. 5 Rekomendasi Jurusan, Berdasarkan Target Jurusan dengan Id 3612135
    
| id\_major | university\_name              | major\_name               |
| --------- | ----------------------------- | ------------------------- |
| 3562281   | UNIVERSITAS NEGERI SEMARANG   | SASTRA PRANCIS            |
| 3232135   | UNIVERSITAS NEGERI JAKARTA    | PENDIDIKAN BAHASA PRANCIS |
| 3562242   | UNIVERSITAS NEGERI SEMARANG   | PENDIDIKAN BAHASA PRANCIS |
| 3622296   | UNIVERSITAS NEGERI YOGYAKARTA | PENDIDIKAN BAHASA PRANCIS |
| 3332144   | UNIVERSITAS PADJADJARAN       | SASTRA INGGRIS            |

*Evaluasi Model: Precision*
Untuk mengevaluasi kinerja sistem rekomendasi ini, digunakan metrik Precision@5, yang menghitung proporsi rekomendasi yang relevan dibandingkan dengan jumlah rekomendasi total (k=5). Dalam contoh evaluasi berikut:

- Recommended IDs: [3562281, 3232135, 3562242, 3622296, 3332144]

- Relevant IDs: [3562281, 3232135, 3562242, 3622296]

Maka nilai Precision dapat dihitung sebagai:

$Precision = \frac{4}{5}$ = 0.8

Hasil ini menunjukkan bahwa 80% dari rekomendasi yang diberikan sesuai dengan preferensi atau jurusan yang relevan, yang menandakan performa sistem yang cukup baik dalam konteks Content-Based Filtering.

2. Model Collaborative Filtering
   
Metrik Root Mean Squared Error (RMSE) digunakan untuk mengevaluasi performa model Collaborative Filtering dalam menghasilkan rekomendasi. Pemilihan metrik ini didasarkan pada karakteristik data yang berupa nilai numerik, yaitu rating, sehingga diperlukan ukuran yang dapat menunjukkan seberapa akurat model dalam memprediksi rating dengan kesalahan sekecil mungkin. Dalam konteks pengembangan sistem rekomendasi yang efektif dan efisien berbasis rating pengguna, RMSE dinilai tepat karena fokus utamanya adalah meminimalkan tingkat kesalahan prediksi. Selain itu, RMSE memberikan interpretasi yang jelas dan intuitif karena nilainya berada dalam skala yang sama dengan rating yang digunakan, serta merepresentasikan rata-rata kesalahan prediksi yang telah diakarkan.

  Adapun rumus dari Root Mean Squared Error (RMSE) adalah sebagai berikut:
  
$$
RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}
$$
  
  keterangan :
  
$n$: jumlah data

$y_i$: nilai aktual (rating asli dari pengguna)

$\hat{y}_i$: nilai prediksi dari model

  Metrik ini bekerja dengan menghitung akar dari rata-rata kuadrat selisih antara nilai prediksi dan nilai aktual, sehingga semakin kecil nilai RMSE, semakin baik performa model.
  
  Root Mean Squared Error (RMSE) merupakan metrik evaluasi yang menghitung akar kuadrat dari rata-rata selisih kuadrat antara nilai yang diprediksi dan nilai aktual. Nilai RMSE yang lebih rendah mengindikasikan bahwa model memiliki tingkat kesalahan prediksi yang kecil, sehingga kualitas prediksinya lebih baik. Oleh karena itu, RMSE sering digunakan untuk menilai performa model regresi maupun sistem rekomendasi. Visualisasi berikut menunjukkan hasil perhitungan RMSE pada model sistem rekomendasi jurusan menggunakan pendekatan collaborative filtering.
  
![image](https://github.com/user-attachments/assets/73e7103d-4501-4fc7-98d3-07ea463610e9)

Grafik di atas menggambarkan perkembangan nilai Root Mean Squared Error (RMSE) pada data pelatihan dan pengujian selama proses training model. Terlihat bahwa nilai RMSE pada data pelatihan menurun secara konsisten, menunjukkan bahwa model mampu mempelajari data dengan baik. Namun, nilai RMSE pada data pengujian cenderung stabil dan tidak mengalami penurunan signifikan. Hal ini menunjukkan bahwa meskipun model semakin akurat terhadap data latih, performanya terhadap data uji tidak meningkat, yang mengindikasikan kemungkinan terjadinya overfitting. Kondisi ini menunjukkan perlunya evaluasi ulang terhadap kompleksitas model atau penerapan teknik untuk meningkatkan generalisasi, seperti regularisasi atau early stopping.
