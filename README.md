# Dokumentasi Restoran App - UTS EAI

## 1. User Service

### Deskripsi
User Service mengelola data pengguna yang melakukan pemesanan di restoran.

### Endpoint
- `GET /users`
  - Menampilkan semua data user.
- `GET /users/<user_id>`
  - Menampilkan detail user berdasarkan ID.
- `POST /users`
  - Menambahkan user baru.
  - Body JSON:
    ```json
    {
      "name": "Nama User",
      "phone": "Nomor Telepon"
    }
    ```
- `PUT /users/<user_id>/payment-status`
  - Update status pembayaran user.
  - Body JSON:
    ```json
    {
      "status": "pending" | "paid" | "failed"
    }
    ```
- `DELETE /users/<user_id>`
  - Menghapus user berdasarkan ID.

### Menjalankan Service
```bash
cd user-service
python app.py
```

---

## 2. Menu Service

### Deskripsi
Menu Service mengelola data menu makanan/minuman yang tersedia.

### Endpoint
- `GET /menus`
  - Menampilkan semua data menu.
- `GET /menus/<menu_id>`
  - Menampilkan detail menu berdasarkan ID.
- `POST /menus`
  - Menambahkan menu baru.
  - Body JSON:
    ```json
    {
      "name": "Nama Menu",
      "price": Harga,
      "stock": Stok
    }
    ```
- `PUT /menus/<menu_id>/update-stock`
  - Update stok menu setelah pemesanan.
  - Body JSON:
    ```json
    {
      "sold_quantity": JumlahTerjual
    }
    ```

### Menjalankan Service
```bash
cd menu-service
python app.py
```

---

## 3. Order Service

### Deskripsi
Order Service mengelola proses pembuatan dan update status pemesanan.

### Endpoint
- `POST /orders`
  - Membuat pemesanan baru.
  - Body JSON:
    ```json
    {
      "user_id": IDUser,
      "menu_ids": [IDMenu1, IDMenu2, ...]
    }
    ```
- `GET /orders/<order_id>`
  - Menampilkan detail order berdasarkan ID.
- `PUT /orders/<order_id>/payment`
  - Update status pembayaran order.
  - Body JSON:
    ```json
    {
      "payment_status": "pending" | "paid" | "failed"
    }
    ```

### Menjalankan Service
```bash
cd order-service
python app.py
```

---

## 4. Payment Service

### Deskripsi
Payment Service memproses pembayaran dan meng-update status pembayaran di Order Service dan User Service.

### Endpoint
- `POST /payments`
  - Membuat dan memproses pembayaran.
  - Body JSON:
    ```json
    {
      "order_id": IDOrder,
      "user_id": IDUser,
      "amount": JumlahPembayaran
    }
    ```
- `GET /payments/<payment_id>`
  - Menampilkan detail pembayaran berdasarkan ID.

### Menjalankan Service
```bash
cd payment-service
python app.py
```

---

# Catatan Tambahan
- Semua service berjalan di local server dengan port berbeda.
- Pastikan service terkait (User, Menu) sudah running sebelum membuat Order atau Payment.
- Tools untuk testing: Postman.
- Database: menggunakan SQLite (otomatis membuat file .db saat dijalankan).

---
# Tanggung Jawab

- User Service: Muhammad Dzakyyuddin Badri - 102022480003
- Order Service: Mohammad Fahrizal Badriansyah - 102022480031
- Menu Service: Karin Trisviasyifa Khairunisa - 102022480002
- Payment Service: Febiani - 102022480001