# Dokumentasi Payment Service

## Deskripsi
API Payment Service sebagai provider data pembayaran dari pengguna. Payment Service berperan untuk memperharui status pemesanan di Order Service dan status pengguna di User Service dalam sistem pemesanan dan pengelolaan restoran. Sehingga dapat diakses oleh service lain, misalnya pada user-service untuk mengcek atau update status pembayaran.

## Dokumentasi API

### 1. **POST /payments**
   - **Deskripsi:** Memproses pembayaran baru serta memeperbaharui status pembayaran pesanan pengguna
   - **Contoh Request:**
     ```bash
     POST /payments
     Content-Type: application/json
     {
      "order_id": 1,
      "user_id": 1,
      "amount": 20000
      }
     ```
   - **Contoh Response:**
     ```json
     {
       "message":"Pembayaran diproses", 
       "payment_id": 1
     }
     ```

   - **Contoh Error (Data tidak lengkap):**
     ```json
     {
       "error": "order_id, user_id, dan amount wajib diisi"
     }
     ```
Setelah pembayaran diproses, mengirim PUT ke Order Service dan User Service maka akan mengupdate status pesanan menjadi "paid"
     

### 2. **GET /payments/{payment_id}** 
   - **Deskripsi:** Mengambil data pembayaran berdasarkan id pembayaran dan mengecek status pembayaran
   - **Contoh Request:**
     ```bash
     GET /payments/1
     ```
   - **Contoh Response:**
     ```json
     {
      "id": 1,
      "order_id": 1,
      "user_id": 1,
      "amount": 20000
      "status": "paid"
     }
     ```

   - **Contoh Error (Data tidak lengkap):**
     ```json
     {
       "error": "Pembayaran tidak ditemukan"
     }
     ```

## Komunikasi Antar Layanan
Menu Service berperan sebagai **provider** untuk menyediakan informasi data status pembayaran dan menyediakan API untuk membuat atau memperharui pembayaran serta sebagai **consumer (order service & user service)** untuk menerima update status setelah pembayaran yaitu pada **Order Service** akan dikirim update status pesanan yang sudah dibayar dengan PUT /orders/{id}/payment dan pada **User SErvice** akan dikirim update status pengguna sudah menyelesaikan pembayaran dengan PUT /users/{id}/payment-service.

### Alur Komunikasi:
1. Pengguna melakukan pembayaran: Payment service menerima dari dari order_id, user_id, dan amount.
2. Setelah data diterima, payment service akan menyimpan informasi mengenai pembayaran, memberi tahu Order Service untuk mengupdate status pesanan menjadi "paid", dan memberi tahu User Service bahwa user sudah melakukan pembayaran.

## Instalasi
1. Clone repo ini:  
   `git clone https://github.com/dzakyyuddinb/restoapp-uts-iae`
2. Install dependensi:  
   `pip install -r requirements.txt`

## Penggunaan
Jalankan server:  
`python app.py`

Server akan berjalan di `http://localhost:5004`