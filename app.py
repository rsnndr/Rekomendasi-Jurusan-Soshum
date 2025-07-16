import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(layout="wide", page_title="Sistem Rekomendasi Jurusan Soshum")

st.title("🎓 Sistem Rekomendasi Jurusan Soshum")

st.write(
    """
    Dasbor ini membantu siswa SMA yang baru lulus dalam memilih jurusan
    perguruan tinggi di bidang Sosial dan Humaniora (Soshum) yang sesuai dengan minat dan kemampuan mereka.
    Kami menggunakan kombinasi **Content-Based Filtering** dan **Collaborative Filtering**
    untuk memberikan rekomendasi yang personal dan relevan.
    """
)

# --- Fungsi Pemuatan dan Persiapan Data (Cache agar Cepat) ---
@st.cache_data
def load_and_prepare_data():
    try:
        universitas_df = pd.read_csv('universities.csv')
        major_df = pd.read_csv('majors.csv')
        score_humanities_df = pd.read_csv('score_humanities.csv')
    except FileNotFoundError:
        st.error("File dataset (universities.csv, majors.csv, score_humanities.csv) tidak ditemukan. Pastikan semua file berada di direktori yang sama.")
        st.stop()

    # 1. Penghapusan Kolom 'Unnamed: 0'
    universitas_df = universitas_df.drop(['Unnamed: 0'], axis=1, errors='ignore')
    major_df = major_df.drop(['Unnamed: 0'], axis=1, errors='ignore')
    score_humanities_df = score_humanities_df.drop(['Unnamed: 0', 'id_second_major', 'id_second_university'], axis=1, errors='ignore')

    # 2. Rename Nama Kolom
    score_humanities_df = score_humanities_df.rename(columns={"id_first_major" : "id_major", "id_first_university" : "id_university"})

    # 3. Menghitung Nilai Rata-rata
    score_cols = ['score_eko', 'score_geo', 'score_kmb', 'score_kpu', 'score_kua', 'score_mat', 'score_ppu', 'score_sej', 'score_sos']
    score_humanities_df['rata_rata_nilai'] = score_humanities_df[score_cols].mean(axis=1)
    score_humanities_df.drop(score_cols, axis=1, inplace=True)

    # 4. Menggabungkan 3 Dataset
    merged_data = pd.merge(score_humanities_df, major_df, on='id_major', how='left')
    merged_data = pd.merge(merged_data, universitas_df[['id_university', 'university_name']], left_on='id_university_x', right_on='id_university', how='left')
    merged_data.drop(['id_university_x', 'id_university_y'], axis=1, inplace=True)

    # 5. Data Filtering (hapus 'science')
    merged_data_clean = merged_data[merged_data['type'] != 'science'].copy()

    # 6. Penanganan Missing Value
    merged_data_clean = merged_data_clean.dropna()

    # 7. Penanganan Kolom Duplikat untuk Content-Based
    p_content_based = merged_data_clean.drop_duplicates('id_major').copy()

    return universitas_df, major_df, score_humanities_df, merged_data_clean, p_content_based

# --- Panggil Fungsi Pemuatan Data ---
universitas_df_orig, major_df_orig, score_humanities_df_orig, merged_data_clean_final, p_content_based_final = load_and_prepare_data()

# --- Persiapan Data untuk Content-Based Filtering ---
@st.cache_resource
def prepare_content_based_model(df_for_cb):
    id_major_list = df_for_cb['id_major'].tolist()
    nama_Univ_list = df_for_cb['university_name'].tolist()
    nama_Prodi_list = df_for_cb['major_name'].tolist()

    data_for_cb_model = pd.DataFrame({
        'id_major': id_major_list,
        'university_name': nama_Univ_list,
        'major_name': nama_Prodi_list
    })

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(data_for_cb_model['major_name'])
    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_df = pd.DataFrame(cosine_sim, index=data_for_cb_model['id_major'], columns=data_for_cb_model['id_major'])

    return data_for_cb_model, cosine_sim_df

data_for_cb_model, cosine_sim_df_cb = prepare_content_based_model(p_content_based_final)

# --- Fungsi Rekomendasi Content-Based ---
def get_content_based_recommendations(id_major, similarity_data, items, k=5):
    if id_major not in similarity_data.index:
        return pd.DataFrame(columns=['id_major', 'university_name', 'major_name'])

    index = similarity_data.loc[:, id_major].to_numpy().argpartition(range(-1, -k - 1, -1))[::-1]
    closest = similarity_data.columns[index]
    closest = closest.drop(id_major, errors='ignore') # Hapus jurusan input dari rekomendasi

    recomen = items[items['id_major'].isin(closest)].head(k)
    return recomen

# --- Persiapan Data dan Model untuk Collaborative Filtering ---
class RecommenderNet(tf.keras.Model):
    def __init__(self, num_user, num_prodi, embedding_size, **kwargs):
        super(RecommenderNet, self).__init__(**kwargs)
        self.num_user = num_user
        self.num_prodi = num_prodi
        self.embedding_size = embedding_size
        self.user_embeddings = layers.Embedding(
            num_user, embedding_size, embeddings_initializer='he_normal',
            embeddings_regularizer=keras.regularizers.l2(1e-6)
        )
        self.user_bias = layers.Embedding(num_user, 1)
        self.prodi_embedding = layers.Embedding(
            num_prodi, embedding_size, embeddings_initializer='he_normal',
            embeddings_regularizer=keras.regularizers.l2(1e-6)
        )
        self.prodi_bias = layers.Embedding(num_prodi, 1)

    def call(self, inputs):
        user_vector = self.user_embeddings(inputs[:, 0])
        user_bias = self.user_bias(inputs[:, 0])
        prodi_vector = self.prodi_embedding(inputs[:, 1])
        prodi_bias = self.prodi_bias(inputs[:, 1])

        dot_user_prodi = tf.tensordot(user_vector, prodi_vector, 2)
        x = dot_user_prodi + user_bias + prodi_bias
        return tf.nn.sigmoid(x)

@st.cache_resource
def train_collaborative_model_and_prepare_data(df_cf_raw):
    df_cf_processed = df_cf_raw.copy() # Pastikan bekerja dengan salinan

    id_peserta = df_cf_processed['id_user'].unique().tolist()
    user_to_user_encoded = {x: i for i, x in enumerate(id_peserta)}
    user_encoded_to_user = {i: x for i, x in enumerate(id_peserta)}

    code_prodi = df_cf_processed['id_major'].unique().tolist()
    prodi_to_prodi_encoded = {x: i for i, x in enumerate(code_prodi)}
    prodi_encoded_to_prodi = {i: x for i, x in enumerate(code_prodi)}

    df_cf_processed['user'] = df_cf_processed['id_user'].map(user_to_user_encoded)
    df_cf_processed['prodi'] = df_cf_processed['id_major'].map(prodi_to_prodi_encoded)

    num_user = len(user_to_user_encoded)
    num_prodi = len(prodi_encoded_to_prodi)
    min_nilai_mah = df_cf_processed['rata_rata_nilai'].min()
    max_nilai_mah = df_cf_processed['rata_rata_nilai'].max()

    df_shuffled = df_cf_processed.sample(frac=1, random_state=42)

    x = df_shuffled[['user', 'prodi']].values
    y = df_shuffled['rata_rata_nilai'].apply(lambda val: (val - min_nilai_mah) / (max_nilai_mah - min_nilai_mah)).values

    train_indices = int(0.8 * df_shuffled.shape[0])
    x_train, x_val = x[:train_indices], x[train_indices:]
    y_train, y_val = y[:train_indices], y[train_indices:]

    model_cf = RecommenderNet(num_user, num_prodi, 50)
    model_cf.compile(
        loss=tf.keras.losses.BinaryCrossentropy(),
        optimizer=keras.optimizers.Adam(),
        metrics=[tf.keras.metrics.RootMeanSquaredError()]
    )

    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.2, patience=5, min_lr=1.5e-5
    )
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", min_delta=0, patience=12, verbose=0, mode="auto",
        baseline=None, restore_best_weights=True
    )

    with st.spinner("Melatih model Collaborative Filtering (ini mungkin memakan waktu)..."):
        history = model_cf.fit(
            x=x_train,
            y=y_train,
            batch_size=64,
            epochs=100,
            validation_data=(x_val, y_val),
            callbacks=[reduce_lr, early_stop],
            verbose=0 # Sembunyikan output pelatihan di konsol
        )
    return (model_cf, history, num_user, num_prodi, min_nilai_mah, max_nilai_mah,
            user_to_user_encoded, user_encoded_to_user,
            prodi_to_prodi_encoded, prodi_encoded_to_prodi,
            df_shuffled)

# --- Panggil Fungsi Pelatihan Model CF ---
(model_cf, history_cf, num_user_cf, num_prodi_cf, min_nilai_mah_cf, max_nilai_mah_cf,
 user_to_user_encoded_cf, user_encoded_to_user_cf,
 prodi_to_prodi_encoded_cf, prodi_encoded_to_prodi_cf,
 df_cf_model_ready) = train_collaborative_model_and_prepare_data(merged_data_clean_final)


# --- Navigasi Tab ---
tab1, tab2 = st.tabs(["Rekomendasi Jurusan", "Analisis Kinerja Model"])

with tab1:
    st.header("✨ Rekomendasi Jurusan")
    st.write("Dapatkan rekomendasi jurusan Soshum berdasarkan preferensi Anda atau pola dari pengguna lain.")

    reco_type = st.radio(
        "Pilih Jenis Rekomendasi:",
        ("Rekomendasi Serupa (Content-Based)", "Rekomendasi Pribadi (Collaborative Filtering)")
    )

    if reco_type == "Rekomendasi Serupa (Content-Based)":
        st.subheader("Rekomendasi Jurusan Serupa (Content-Based Filtering)")
        st.write("Temukan jurusan lain yang memiliki karakteristik serupa dengan jurusan yang Anda minati.")

        # Buat daftar opsi untuk selectbox dengan format nama_jurusan (nama_universitas)
        major_options_cb = data_for_cb_model.apply(lambda row: f"{row['major_name']} ({row['university_name']})", axis=1).tolist()
        major_id_map_cb = {f"{row['major_name']} ({row['university_name']})": row['id_major'] for _, row in data_for_cb_model.iterrows()}

        selected_major_display_cb = st.selectbox(
            "Pilih Jurusan yang Anda Minati:",
            options=major_options_cb,
            index=0
        )

        selected_major_id_cb = major_id_map_cb.get(selected_major_display_cb)

        if selected_major_id_cb:
            st.write("---")
            st.write(f"Anda memilih: **{selected_major_display_cb}**")
            st.write("#### 5 Rekomendasi Jurusan Serupa:")
            recommendations_cb = get_content_based_recommendations(selected_major_id_cb, cosine_sim_df_cb, data_for_cb_model, k=5)
            if not recommendations_cb.empty:
                st.dataframe(recommendations_cb[['major_name', 'university_name', 'id_major']])
            else:
                st.write("Tidak ada rekomendasi yang ditemukan untuk jurusan ini.")

    elif reco_type == "Rekomendasi Pribadi (Collaborative Filtering)":
        st.subheader("Rekomendasi Jurusan Pribadi (Collaborative Filtering)")
        st.write("Dapatkan rekomendasi berdasarkan pola preferensi pengguna lain yang mirip dengan Anda.")

        # Ambil daftar ID pengguna unik
        user_ids_cf = df_cf_model_ready['id_user'].unique().tolist()
        selected_user_id_cf = st.selectbox(
            "Pilih ID Pengguna (untuk melihat rekomendasi):",
            options=user_ids_cf,
            index=0 # Default ke pengguna pertama
        )

        if selected_user_id_cf:
            st.write("---")
            st.write(f"Memperlihatkan rekomendasi untuk pengguna: **{selected_user_id_cf}**")

            st.write("##### Jurusan Pilihan Pengguna Ini (berdasarkan skor tertinggi):")
            prodi_pick_by_user_cf = df_cf_model_ready[df_cf_model_ready['id_user'] == selected_user_id_cf].sort_values(
                by='rata_rata_nilai', ascending=False
            ).head(5) # Tampilkan 5 teratas
            for row in prodi_pick_by_user_cf.itertuples():
                st.write(f"- **{row.major_name}** di {row.university_name} (Skor rata-rata: {row.rata_rata_nilai:.2f})")

            # --- Logika Rekomendasi Collaborative Filtering ---
            prodi_not_pick_cf = df_cf_model_ready[~df_cf_model_ready['id_major'].isin(prodi_pick_by_user_cf['id_major'].values)]['id_major']
            prodi_not_pick_cf = list(
                set(prodi_not_pick_cf).intersection(set(prodi_to_prodi_encoded_cf.keys()))
            )

            if prodi_not_pick_cf:
                prodi_not_pick_encoded_cf = [[prodi_to_prodi_encoded_cf.get(x)] for x in prodi_not_pick_cf]
                user_encoder_cf = user_to_user_encoded_cf.get(selected_user_id_cf)
                user_prodi_array_cf = np.hstack(
                    ([[user_encoder_cf]] * len(prodi_not_pick_encoded_cf), prodi_not_pick_encoded_cf)
                )

                ratings_model_cf = model_cf.predict(user_prodi_array_cf).flatten()
                top_ratings_indices_cf = ratings_model_cf.argsort()[-10:][::-1] # 10 Rekomendasi Teratas

                recommended_prodi_ids_cf = [
                    prodi_encoded_to_prodi_cf.get(prodi_not_pick_encoded_cf[x][0]) for x in top_ratings_indices_cf
                ]

                st.write("---")
                st.write("##### 10 Rekomendasi Jurusan Teratas untuk Pengguna Ini:")
                # Pastikan tidak ada duplikasi jika ada di dataframe yang digabungkan
                recommended_univ_cf = df_cf_model_ready[df_cf_model_ready['id_major'].isin(recommended_prodi_ids_cf)].drop_duplicates(subset=['id_major'])
                # Urutkan berdasarkan urutan dari top_ratings_indices_cf
                ordered_recommendations = [
                    (major_id, major_name, univ_name)
                    for major_id in recommended_prodi_ids_cf
                    for _, row in recommended_univ_cf.iterrows()
                    if row['id_major'] == major_id
                    for major_name, univ_name in [(row['major_name'], row['university_name'])]
                ]
                # Filter out potential duplicates if any (though drop_duplicates above should handle it)
                unique_ordered_recommendations = []
                seen_major_ids = set()
                for major_id, major_name, univ_name in ordered_recommendations:
                    if major_id not in seen_major_ids:
                        unique_ordered_recommendations.append(f"- **{major_name}** di {univ_name}")
                        seen_major_ids.add(major_id)

                for reco_str in unique_ordered_recommendations:
                    st.write(reco_str)

            else:
                st.write("Tidak ada jurusan yang belum dipilih untuk direkomendasikan bagi pengguna ini.")

with tab2:
    st.header("📊 Analisis Kinerja Model")
    st.write("Pahami bagaimana model Collaborative Filtering belajar dan seberapa baik kinerjanya.")

    st.subheader("Metrik Pelatihan Model Collaborative Filtering (RMSE)")
    st.write("Grafik di bawah menunjukkan Root Mean Squared Error (RMSE) selama proses pelatihan model.")
    st.write("**RMSE** yang lebih rendah menandakan kinerja model yang lebih baik dalam memprediksi skor rata-rata.")

    fig_metrics, ax_metrics = plt.subplots(figsize=(10, 6))
    ax_metrics.plot(history_cf.history['root_mean_squared_error'], label='RMSE Latih')
    ax_metrics.plot(history_cf.history['val_root_mean_squared_error'], label='RMSE Validasi')
    ax_metrics.set_title('Metrik Model: RMSE')
    ax_metrics.set_ylabel('Root Mean Squared Error')
    ax_metrics.set_xlabel('Epoch')
    ax_metrics.legend()
    ax_metrics.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig_metrics)
    plt.close(fig_metrics)

    st.write(f"**RMSE terakhir pada data latih:** {history_cf.history['root_mean_squared_error'][-1]:.4f}")
    st.write(f"**RMSE terakhir pada data validasi:** {history_cf.history['val_root_mean_squared_error'][-1]:.4f}")

    st.markdown("""
    **Insight:**
    * Jika **RMSE Latih** menurun stabil dan **RMSE Validasi** juga menurun dan mendekati RMSE Latih, ini menunjukkan model belajar dengan baik dan tidak *overfitting*.
    * Jika RMSE Validasi mulai meningkat sementara RMSE Latih terus menurun, model mungkin mengalami *overfitting* pada data pelatihan.
    """)

st.markdown("---")
st.write("### Terima kasih telah menjelajahi Sistem Rekomendasi Jurusan Soshum!")
st.write("Kami harap dasbor ini membantu Anda memahami proses rekomendasi dan memilih jurusan yang tepat.")