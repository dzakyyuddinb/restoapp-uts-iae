# Dokumentasi Order Service

## Deskripsi
API Order Service berfungsi untuk mengelola proses pemesanan dalam sistem restoran. Order Service berkomunikasi dengan **User Service** untuk memverifikasi pengguna, **Menu Service** untuk memeriksa ketersediaan menu, dan **Payment Service** untuk memperbarui status pembayaran.

## Dokumentasi API

### 1. **POST /orders**
   - **Deskripsi:** Membuat pesanan baru berdasarkan data pengguna dan menu yang dipilih.
   - **Contoh Request:**
     ```bash
     POST /orders
     Content-Type: application/json
     {
       "user_id": 1,
       "menu_ids": [1, 2]
     }
     ```
   - **Contoh Response:**
     ```json
     {
       "id": 1,
       "user_id": 1,
       "items": [
         {
           "id": 1,
           "name": "Nasi Ayam Bakar",
           "price": 18000,
           "stock": 14
         },
         {
           "id": 2,
           "name": "Kwetiau Goreng",
           "price": 20000,
           "stock": 6
         }
       ],
       "total_price": 38000,
       "status": "pending",
       "created_at": "now"
     }
     ```

### 2. **GET /orders/{id}**
   - **Deskripsi:** Mendapatkan detail pesanan berdasarkan ID pesanan.
   - **Contoh Request:**
     ```bash
     GET /orders/1
     ```
   - **Contoh Response:**
     ```json
     {
       "id": 1,
       "user_id": 1,
       "items": [
         {
           "id": 1,
           "name": "Nasi Ayam Bakar",
           "price": 18000,
           "stock": 14
         },
         {
           "id": 2,
           "name": "Kwetiau Goreng",
           "price": 20000,
           "stock": 6
         }
       ],
       "total_price": 38000,
       "status": "pending",
       "created_at": "now"
     }
     ```

   - **Contoh Error (Pesanan tidak ditemukan):**
     ```json
     {
       "message": "Pemesanan tidak ditemukan."
     }
     ```

### 3. **PUT /orders/{id}/payment**
   - **Deskripsi:** Memperbarui status pembayaran pesanan.
   - **Contoh Request:**
     ```bash
     PUT /orders/1/payment
     Content-Type: application/json
     {
       "payment_status": "paid"
     }
     ```
   - **Contoh Response:**
     ```json
     {
       "id": 1,
       "user_id": 1,
       "items": [
         {
           "id": 1,
           "name": "Nasi Ayam Bakar",
           "price": 18000,
           "stock": 14
         },
         {
           "id": 2,
           "name": "Kwetiau Goreng",
           "price": 20000,
           "stock": 6
         }
       ],
       "total_price": 38000,
       "status": "paid",
       "created_at": "now"
     }
     ```

   - **Contoh Error (Status pembayaran tidak valid):**
     ```json
     {
       "message": "Status pembayaran tidak valid."
     }
     ```

## Komunikasi Antar Layanan

Order Service berperan sebagai **consumer** untuk menerima data menu dari **Menu Service** dan memperbarui stok setelah pemesanan, serta berperan sebagai **provider** untuk memperbarui status pembayaran ke **Payment Service**.

1. **Consumer (Order Service)**: Mengirimkan permintaan ke **Menu Service** untuk memeriksa ketersediaan menu dan memperbarui stok setelah pesanan.
2. **Provider (Order Service)**: Mengirimkan status pembayaran ke **Payment Service** setelah transaksi berhasil.

### Alur Komunikasi:
1. **Order Service** mengirimkan data pesanan ke **Menu Service** untuk memverifikasi ketersediaan stok.
2. **Menu Service** memberikan data stok menu dan mengurangi stok setelah pesanan berhasil.
3. **Order Service** memperbarui status pembayaran ke **Payment Service** setelah proses pembayaran selesai.

## Instalasi
1. Clone repo ini:  
   `git clone https://github.com/dzakyyuddinb/restoapp-uts-iae`
2. Install dependensi:  
   `pip install -r requirements.txt`

## Penggunaan
Jalankan server:  
`python app.py`

Server akan berjalan di `http://localhost:5003`
