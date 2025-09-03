# AI-Powered Recommendation Platform for E-commerce

--- 

## Section 1 : Blueprint - Foundation of a Recommendation System

### 1.1.  Business Problem and Project Goals

Sebelum Sistem engenering. Dimulai dengan memahami masalah bisnis yang ingin diselesaikan. Dalam konteks Ecommerce, tujuan utamanya adalah untuk meningkatkan pengalaman belanja pelanggan, yang mana secara langsung mendorong performa bisnis. Sistem rekomendasi dirancang dengan teknis yang baik sebenrnya bertujuan untuk mendorong pendapatan bisnis. 

#### Business Goals and Indikator Kerja Utama

Tujuan utamanya adalah membuat sistem rekomendasi yang bisa tepat sasaran merekomendasi sesuai dengan kebutuhan dan keinginan user. Dengan ini beberapa matriks bisnis bisa meningkat, seperti :

1. CTR (Click-Through Rate) : Simplenya CTR itu ngukur yang direkomendasi itu di klik apa engga sama pelanggan. Orang bakal klik iklan atau rekomendasi yang sesuai dengan minat dan keinginan mereka.
2. CVR (Conversion Rate) : Ini ngukur apakah setelah direkomendasi, dan diklik, pelanggan beli apa engga, kalo dari awal rekomendasi sesuai kemungkinan pelanggan bakal beli.
3. AOV (Average Order Value) : Ngukur nilai tiap pesanan tiap order. Ngukur seberapa banyak user keluar duit sekali transaksi. Strategi utamanya adalah menampilkan rekomendasi produk lain yang relevan dengan rekomendasi pertama.
4. Retention : Selain menarik, sistem rekomendasi yang baik overall bikin pelanggan nyaman dan trust. Ini bakal bikin pelanggan betah buat belanja.

#### Use Cases

Kalo di ecommerce, biasanya ada beberapa use case yang bisa diimplementasikan. Diantaranya :

1. Use Case 1 : Recommended for You, sangat disesuaikan dengan kebutuhan dan keinginan personal pelanggan
2. Use Case 2 : Similar Items, rekomendasi item lain saat checkout. 
3. Use Case 3 : Frequently Bought Together, rekomendasi item yang sering dibeli bersama (Paketan).

#### Kendala Produksi

Beberpa kendala yang akan dihadapi dalam produksi :

1. Latensi : Demi kenyamanan, sistem harus cepat dalam memberikan rekomendasi.
2. Skalabilitas : Sistem harus dapat menangani lalu lintas besar dan skala yang terus meningkat seiring waktu.
3. Cold Start : Sistem harus mampu memberikan rekomendasi yang relevan bahkan untuk pelanggan dan item baru yang masuk tanpa riwayat apapun.
4. Fairness : Sistem tidak boleh memberikan rekomendasi yang itu itu aja dan ga variatif yang juga biasanya terlalu fokus ke produk populer, yang mana ini ga adil dan malah ga ngebantu penjualan.

#### Nilai MLOps

MLOps adalah workflow pembuatan sistem berbasi ML yang efektif dan efisien dengan berfokus membangun sistem yang :

1. Automatic, semua operasi yang berkaitan dengan ML harus otomatis, seperti data, training, deployment, dan monitoring.
2. Scalable, sistem dengan mudah di skala.
3. Maintainable, sistem dengan mudah diupdate dan di maintain.
4. Observability, sistem mampu dilihat dan dimonitor dengan mudah.

### 1.2. Arsitektur Tingkat Tinggi

#### Diagram Arsitektur

Kedua diagram berikut memberikan gambaran lengkap dan detail dari arsitektur sistem yang dibangun.

##### Diagram Poses Overall

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*8taz9zqDDAWag0Wrype2jg.png)

Detail : https://excalidraw.com/#json=R8ss_xTzW_fJX6t4azhf9,xzMzIwZBle6zsNMUogq9qA

##### Diagram Kerja MLOps System

![](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*Xe-DDPItEJPNXmORldBpGg.png)

Detail : https://excalidraw.com/#json=1i9_cOnWZf5mY64mTgfzX,M30C-4f5uacPxIQ4h_Y_wg


#### Rincian Komponen

1. API Gateway (NGINX)
Bisa dibilang ini adalah pintu depan sistem. Semua request dari user (misalnya minta rekomendasi produk) lewat sini dulu. Tugasnya:
- Nentuin request itu mau diarahkan ke layanan mana.
- Ngebatesin request biar nggak kebanyakan (rate limiting).
- Cek awal apakah user sudah terotentikasi.

2. Recommendation Service (FastAPI)
Ini adalah otak utama sistem. Dia yang bikin rekomendasi lewat 3 tahap:
- Candidate Generation → nyari banyak kandidat item yang mungkin cocok.
- Ranking → ngasih skor ke tiap item.
- Re-ranking → menyusun ulang hasil biar lebih personal/tepat.

3. Feature Store (Feast + Redis). 
Anggap ini gudang data cepat. Dia nyimpen data penting tentang user & item (misalnya riwayat belanja, kategori produk, rating). Bedanya, dia dirancang biar aksesnya super cepat buat kebutuhan real-time.

4. MLflow
Ini semacam notebook lab riset + gudang model. Dipakai data scientist buat:
- Nge-track eksperimen (model mana performanya lebih bagus).
- Menyimpan & berbagi model.
- Register model yang siap dipakai di produksi.

5. Airflow
Ini adalah penjadwal otomatis. Kerjanya:
- Ngelola pipeline data (misalnya update data setiap malam).
- Menjalankan training ulang model secara rutin (misalnya seminggu sekali).

6. Kubernetes.
Bisa dibilang ini manajer besar yang ngatur semua layanan. Dia pastiin setiap komponen (API, layanan rekomendasi, database) jalan lancar, bisa diskalakan kalau user makin banyak, dan tetap sehat kalau ada error.

7. Prometheus & Grafana
Ini adalah mata dan telinga sistem:
- Prometheus ngumpulin metrik (misalnya berapa request per detik, latency, error rate).
- Grafana menampilkan metrik itu dalam bentuk dashboard yang gampang dibaca.
- Kalau ada masalah (misalnya server overload), sistem bisa kirim alert ke tim.

Jadi kalau disimpulkan:
User masuk lewat NGINX → Recommendation Service → ambil data dari Feature Store → model dari MLflow → pipeline diatur Airflow → semuanya dikelola Kubernetes → kesehatan sistem dipantau Prometheus & Grafana.


#### Teknologi


|Kategori|Teknologi|Peran Utama|
|---|---|---|
|**Backend & API**|Python 3.10+, FastAPI|Real-time inference service, performa tinggi, dokumentasi API otomatis.|
|**Data Streaming**|Kafka (Redpanda)|Ingestion event pengguna (clicks, views, purchases) secara real-time.|
|**Penyimpanan Data**|PostgreSQL, MongoDB, MinIO (S3)|Postgres untuk data master (user, item), Mongo untuk log, MinIO sebagai data lake.|
|**Feature Store**|Feast, Redis, Parquet|Feast untuk orkestrasi, Redis sebagai online store (latensi rendah), Parquet sebagai offline store.|
|**Orkestrasi Pipeline**|Apache Airflow|Menjalankan pipeline ETL batch dan retraining model secara terjadwal.|
|**Pemodelan ML**|Scikit-learn, Implicit, LightGBM, Sentence-Transformers|Item-Item CF, ALS (Candidate Gen), LGBMRanker (Ranking), Embeddings (Content-based).|
|**MLOps & CI/CD**|MLflow, Optuna, GitHub Actions, Docker, Kubernetes, Helm|Pelacakan eksperimen, HPO, CI/CD otomatis, containerization, orkestrasi.|
|**Observability**|Prometheus, Grafana, Great Expectations, EvidentlyAI|Monitoring metrik, visualisasi dashboard, validasi data, deteksi drift.|

---

## Setup

Docker dan Docker compose 

```bash
docker --version 
docker compose version
```

.env file

```bash
cp .env.example .env
```

[`Docker Compose`](deploy/docker/docker-compose.yml) berisi skrip untuk mengaktifkan beberapa service di sistem kita secara paralel dan otomatis. kaya Postgres, MangoDB, Redis, Redpanda, MinIO, MLflow, Prometheus, dan Grafana. Hanya dengan satu commnand

```bash
docker compose -f deploy/docker/docker-compose.yml up -d
```

Cek container aktif

```bash
docker compose ps
``` 

Hasilnya adalah daftar kontainer yang berjalan, termasuk `postgres_db`, `mongo_db`, `redis_cache`, `redpanda_kafka`, `minio_s3`, `mlflow_server`, `prometheus_monitor`, dan `grafana_dashboard`.

---

## Section 2 : Data Flow - Data Ingestion and Processing

Tahapan ini intinya extract data dari sumber, preprocessing dan penyiapan untuk model, serta load sesuai skema data.


### 2.1. Pemilihan Dataset

[Retailrocket recommender system dataset](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset?select=events.csv) dipilih untuk dataset projek ini. Since kebutuhan kita itu informasi interaksi user dengan produk untuk itung interest rate mereka. Dataset ecommerce pada umumnya cuman ada rating sama reviuw itu ga cukup. Kita perlu informasi user behavior seperti product view, add to chart and purchase. Makanya kita pake dataset it. di data card nya ada tiga, tapi yang kita perlu cuman satu yaitu `events.csv` yang punya fitur `timestampt`, `visitor id` (user) dan `event` (`add_to_chart`, `view` and `transaction`). 

### 2.2. Generator Data Sintesis

Script [generate_events.py](data/generators/generate_events.py) akan melakukan simulasi data streaming dimana tujuan utamanya adalah ngecek pipeline aliran data streaming dari user, tapi digenerate.

Untuk menjalankannya :

```bash
python data/generators/event_generator.py
```

### 2.3. Strategi Penyimpanan Data

Data akan disimpan dalam beberapa tempat berbeda sesuai dengan jenis data, seperti:

- PostgreSQL : dipake buat simpen data yang rapi dan penting, kaya transaksi, daftar barang dan akun user. Dan akan dipanggil jika perlu langsung dengan mudah.
- MangoDB : dipake buat simpen data yang acak dan fleksibel, misal log aktivitas user dan event. karena datanya lebih gede dan berubah ubah lebih enak handle pake nosql.
- MinIO : semua data, inituh kaya arsip, semua data dari statis, stream, rawnya, hasil processing dan feature engeneeringnya. semua disimpen kesini, dan dipake buat analisis dan model. Cepet buat backend tapi lama buat serving ke frontend. Makanya kita tetep pake postgre sama mango.

### 2.4. Skema Data

PostgreSQL Scheme Entity Relationship Diagram (ERD)

<img src='https://miro.medium.com/v2/resize:fit:4800/format:webp/1*DYm8qIcqHOmBZovNzEGW9g.png' width=400>

[`postgres_schema.sql`](data/schema/postgres_schema.sql) akan membuat tabel sesuai dengan skema ERD di atas. 

Setupnya :

```bash
# Install kalo belum
sudo apt update
sudo apt install postgresql postgresql-contrib
```
```bash
# Start service
sudo systemctl start postgresql
```

```bash
# Check status
pg_isready
```

```bash
# Login
sudo -u postgres psql
```

```bash
# Buat database
CREATE DATABASE recommendation_db;
```

```bash
# Masuk ke DB
\c recommendation_db
```

kalo udah tinggal jalanin skrip postgres_schema.sql

```bash
# Jalankan skrip
\i data/schema/postgres_schema.sql
```

### 2.4. Pipeline Data Ingestion

Untuk data stream real time kita bakal pake Kafka. Sedangkan data statis/batch dari kaggle kita bakal pake apache Airflow.

**Ingestion Real Time dengan Kafka : [`user_event.avsc`](`data/schema/user_event.avsc`)**

Data real time dari frontend atau Ecommerce akan di publish ke Kafka dalam format .avsc (Avro format) untuk mastiin kafka bisa ngerti struktur data yang dikirim dengan segala aturannya. .

**Ingestion Batch dengan Airflow : [`ingestion_batch.py`](dags/ingestion_batch.py)**

Airflow DAG itu adalah alur kerja yang bisa dijadwalkan. Extract data mentah menjadi csv, Validate kesesuaian data dengan Great Expectation. dan kalo lolos masuk ke Data Lake (MinIO) ke dalam format Parquet. 

---

## Section 3 : Feature Store dengan Feast

Di modelling pipeline, ada dua jalur, training sama serving(inferensi). Training pipeline akan dijalankan setiap kali ada perubahan data atau model. Sedangkan serving pipeline akan dijalankan setiap kali ada request dari user. Masalahnya, kedual jalur ini ga selalu sama, beda transformasi, beda tipe, beda query. Perbedaan ini bikin prediksi meleset (training serving skew). 

Feast menyelesaikan masalah dengan FeatuerView yang mana kita definisikan satu kali cara transformasi data dan menyimpannya di feature store. dan Feast bisa pakai itu buat offline training dataset maupun untuk online feature retrieval. 

Setup :


1. Init repo :

    ```bash
    feast init feature_repo
    cd feature_repo
    ```

2. Konfigurasi [`feature_store.yaml`](feature_repo/faeture_repo/feature_store.yaml)

    ```YAML
    project: reco_platform
    registry: data/registry.db
    provider: local
    online_store:
        type: redis
        connection_string: "localhost:6379"
    offline_store:
        type: file
    entity_key_serialization_version: 2
    ```

3. Definisikan tiap entitas dan feature view di [`feature_repo.py`](feature_repo/faeture_repo/example_repo.py)

4. Setelah mendefinisikan fitur, terapkan perubahan ke _registry_ Feast:

    ```bash
    feast apply
    ```

    Perintah ini akan memindai file, mendaftarkan objek, dan menyiapkan tabel yang diperlukan di _online store_ (Redis).

5. Materialize the feature views, materialisasi artinya mindahin data fitur terbaru dari offline store (misal dari parquet dan postgresql) ke online store (Redis) buat inferensi realtime, Tujuannya cuman biar latensi modelling lebih cepet. Disinilah kita bakal pake Airflow DAG (Work scheduler) yang bakal ototmatis jalan tiap waktu yang ditentukan. Skript [`feature_materialization_dag.py`](dags/feature_materialization_dag.py) bakal handle ini.

---

## Section 4 : Model - Multi Stage Modelling

### 3.1. Tahap 1 : Pemilihan Kandidat (Recall Tinggi)

Tujuan tahap ini adalah memilih dan mengambil beberapa ratus item yang kira kira relevan dari katalog. Teknik yang dipake adalah CF dan ALS

**CF (Item Collaborative Filtering) : [`item_item_cf.py`](ml/candidate/item_item_cf.py)**

yang mana akan dipake buat nyari item mirip, berdasarkan pola interaksi user lain. 

**Alternating Least Squares (ALS) : [`als.py`](ml/candidate/als.py)** 

Sangat efektif untuk data umpan balik implisit. ALS memfaktorkan matriks interaksi pengguna-item menjadi matriks laten pengguna dan item.


**Content-Based (Embeddings):** 

Penting untuk mengatasi masalah _cold-start_ item baru. Disini kita akan menghasilkan _embedding_ dari deskripsi teks item menggunakan `sentence-transformers` dan mengindeksnya di **FAISS** untuk pencarian tetangga terdekat yang cepat (_Approximate Nearest Neighbor_ - ANN).
    
### 3.2. Tahap 2 : Pemeringkatan (Presisi Tinggi) dengan LightGBM

Dari kandidat item dari katalog tadi. Kita baal kasih skor tiap kandidat dengan LGBMRangker. Supaya urutannya paling relevan buat user. Dia bakal liat fitur lengkap dari user, item dan konteks, dan kasi skor sebagai label. Terakhri supaya kita ngerti kenapa model milih item itu. Kita pake SHAP untuk XAI untuk transparansi. Skrip [`train_ranker.py`](ml/ranker/train_ranker.py) bakal handle ini.

### 3.3. Tahap 3 : Rerank dengan Metriks Bisnis

Tahap terakhir adalah menerapkan logika non-ML untuk memastikan rekomendasi yang tetap on point. Beberapa aturannya adalah :

- **Diversifikasi:** Pastikan tidak semua item berasal dari kategori yang sama.
    
- **Filter:** Hapus item yang stoknya habis atau yang baru saja dibeli pengguna.
    
- **Boosting:** Naikkan posisi item yang sedang diskon atau memiliki margin keuntungan tinggi.


### 3.4. Tahap 4 : Pelacakan Eksperimen dan HPO dengan MLflow dan Optuna

Setiap proses pelatihan model akan dilacak menggunakan **MLflow** untuk mencatat parameter, metrik (NDCG@10, MAP), dan artefak model. Untuk optimisasi _hyperparameter_, kita akan mengintegrasikan **Optuna**, di mana setiap _trial_ akan dicatat sebagai _nested run_ di dalam MLflow, memberikan pelacakan yang lebih terorganisir.

## Section 5 : Serving Model dengan Microservice FastAPI

### 5.1. Implementasi Rekomendasi Service

Layanan inti dibangun menggunakan **FastAPI** karena kinerjanya yang tinggi dan dukungan _asynchronous_. Skrip [`main.py`](apps/reco_service/main.py) akan menangani permintaan rekomendasi dari pengguna.

Di dunia _microservices_, skema API adalah kontrak. Tanpa kontrak. frontend dev bisa salah manggil endpoint (misalnya kirim userId padahal API butuh user_id). Akhirnya error. Dengan Swagger/OpenAPI. frontend dev tinggal buka dokumentasi otomatis (udah jelas path, parameter, tipe data, contoh response). Tinggal copy-paste request → langsung jalan.

### 5.2. Dokumentasi API (Swagger/OpenAPI) dan Caching

Secara default, FastAPI menyediakan dokumentasi Swagger UI dan OpenAPI yang dapat diakses melalui `/docs` dan `/redoc` endpoint. Kita juga bakal implementasi lapisan *caching* dengan Redis untuk simpen hasil rekomendasi agar next time, latensi bisa berkurang.


**Contoh Request/Response:**

**Request:** ` GET /recommendations/v1/user_123?k=5`

**Response:**


```JSON
{
  "user_id": "user_123",
  "recommendations": [
    {"item_id": "product_45", "score": 0.98},
    {"item_id": "product_72", "score": 0.95},
    {"item_id": "product_11", "score": 0.91},
    {"item_id": "product_88", "score": 0.89},
    {"item_id": "product_23", "score": 0.85}
  ]
}
```

---

## Section 6 : Factory - Automating Ml Lifecycle with MLOps

### 6.1. Pipeline CI/CD dengan Github Actions

Proses ini bakal handle build dan test serta debugging sistem kita secara otomatis dengan github actions. [`ci-cd.yml`](.github/workflows/ci-cd.yml)

### 6.2. Pipeline Retraining dengan Airflow

Proses orkestrasi pelatihan ulang model akan dilakukan dengan DAG Airflow. [`retraining_dag.py`](dags/retraining_dag.py)

### 6.3. Model Drifting Detection dan Observability


- **Monitoring:** Kita akan menyediakan file `prometheus.yml` dan dasbor Grafana JSON untuk memvisualisasikan metrik kunci: latensi API (p95, p99), _throughput_ (RPS), tingkat kesalahan, dan _cache hit-rate_.
    
- **Deteksi Drift:** DAG Airflow harian akan menggunakan **EvidentlyAI** untuk membandingkan distribusi statistik data produksi terbaru dengan data referensi (misalnya, data pelatihan). Jika _drift_ signifikan terdeteksi (misalnya, _Population Stability Index_ > 0.2), sebuah peringatan akan dipicu.
    
---

## Section 7 : Going Live - Deployment, Scaling and Monitoring

### 7.1. Containerization dengan Docker

Setiap _microservice_ akan memiliki `Dockerfile` sendiri, yang dioptimalkan untuk ukuran _image_ yang kecil dan _build_ yang efisien. [Dockerfile](apps/reco_service/Dockerfile)

### 7.2. Orkestrasi dengan Kubernetes dan Helm

Kami akan membuat **Helm chart** untuk mengelola semua manifes Kubernetes sebagai satu paket berversi.

_Chart_ ini akan mencakup _Deployment_, _Service_, _Ingress_, dan _HorizontalPodAutoscaler_ (HPA) untuk menskalakan layanan rekomendasi secara otomatis berdasarkan beban CPU.

### 7.3. Deployment ke Render

Karena cluster Kubernetes penuh bisa jadi mahal dan kompleks untuk proyek portofolio, kita akan mendeploy aplikasi Docker ke platform PaaS yang hemat biaya seperti **Render** atau **Railway**. Ini akan mencakup cara menghubungkan repositori GitHub, membuat layanan web dari `Dockerfile`, dan menyiapkan basis data terkelola.