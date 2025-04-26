# User Service

User Service adalah bagian dari sistem Restoran Terintegrasi yang bertanggung jawab untuk mengelola data pengguna, termasuk pendaftaran, pengambilan data, pembaruan status pembayaran, dan penghapusan pengguna.

---

## Teknologi yang Digunakan
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite (database lokal)

## Instalasi

1. **Clone repository**
```bash
https://github.com/username/restoapp-uts-iae.git
```

2. **Masuk ke direktori user-service**
```bash
cd user-service
```

3. **Buat virtual environment** (opsional tetapi direkomendasikan)
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate    # Windows
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Jalankan service**
```bash
python app.py
```

Service akan berjalan di `http://localhost:5001`

---

## Endpoint API

### 1. Get All Users
- **Method:** `GET`
- **URL:** `/users`
- **Response:** List seluruh pengguna

### 2. Get User by ID
- **Method:** `GET`
- **URL:** `/users/<user_id>`
- **Response:** Detail pengguna berdasarkan ID

### 3. Create User
- **Method:** `POST`
- **URL:** `/users`
- **Body:**
```json
{
  "name": "Nama Pengguna",
  "phone": "Nomor Telepon"
}
```
- **Response:** Data pengguna yang baru dibuat

### 4. Update Payment Status
- **Method:** `PUT`
- **URL:** `/users/<user_id>/payment-status`
- **Body:**
```json
{
  "status": "pending" | "paid" | "failed"
}
```
- **Response:** Data pengguna dengan status pembayaran terbaru

### 5. Delete User
- **Method:** `DELETE`
- **URL:** `/users/<user_id>`
- **Response:** Konfirmasi penghapusan pengguna

---

## Struktur Database

Tabel `User`:
- `id`: Integer, Primary Key
- `name`: String
- `phone`: String
- `payment_status`: String

---

## Notes
- Default `payment_status` saat user baru dibuat adalah `unpaid`
- Service ini berkomunikasi dengan Order Service dan Payment Service dalam sistem terintegrasi

---

## Developer
- Mata Kuliah: **Enterprise Application Integration (EAI)**
- Dosen Pengampu: **MUHAMMAD RIZQI SHOLAHUDDIN**