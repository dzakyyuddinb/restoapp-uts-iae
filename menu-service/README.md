# Dokumentasi Menu Service

## Deskripsi
API Menu Service sebagai provider data menu makanan (digunakan oleh Order Service), dan consumer dari Order Service (untuk update stok makanan) dalam sistem pemesanan dan pengelolaan restoran.

## Dokumentasi API

### 1. **GET /menus**
   - **Deskripsi:** Mendapatkan daftar menu makanan yang tersedia.
   - **Contoh Request:**
     ```bash
     GET /menus
     ```
   - **Contoh Response:**
     ```json
     [
       {
         "id": 1,
         "name": "Nasi Ayam Bakar",
         "price": 18000,
         "stock": 15
       },
       {
         "id": 2,
         "name": "Kwetiau Goreng",
         "price": 20000,
         "stock": 7
       }
     ]
     ```

### 2. **GET /menus/{id}**
   - **Deskripsi:** Mendapatkan detail menu berdasarkan ID menu.
   - **Contoh Request:**
     ```bash
     GET /menus/1
     ```
   - **Contoh Response:**
     ```json
     {
       "id": 1,
       "name": "Nasi Ayam Bakar",
       "price": 18000,
       "stock": 15
     }
     ```

   - **Contoh Error (Menu tidak ditemukan):**
     ```json
     {
       "message": "Menu tidak ditemukan."
     }
     ```

### 3. **POST /menus**
   - **Deskripsi:** Menambahkan menu baru ke dalam daftar menu.
   - **Contoh Request:**
     ```bash
     POST /menus
     Content-Type: application/json
     {
       "name": "Ayam Penyet",
       "price": 25000,
       "stock": 10
     }
     ```
   - **Contoh Response:**
     ```json
     {
       "id": 3,
       "name": "Ayam Penyet",
       "price": 25000,
       "stock": 10
     }
     ```

### 4. **PUT /menus/{id}/update-stock**
   - **Deskripsi:** Memperbarui stok menu berdasarkan ID menu dengan mengurangi jumlah stok yang terjual.
   - **Contoh Request:**
     ```bash
     PUT /menus/1/update-stock
     Content-Type: application/json
     {
       "sold_quantity": 3
     }
     ```
   - **Contoh Response (Stok berhasil diperbarui):**
     ```json
     {
       "message": "Stok berhasil diperbarui.",
       "stock": 12
     }
     ```

   - **Contoh Error (Stok tidak mencukupi):**
     ```json
     {
       "message": "Stok tersedia tidak mencukupi."
     }
     ```

   - **Contoh Error (Jumlah terjual tidak valid):**
     ```json
     {
       "message": "Invalid quantity."
     }
     ```

## Komunikasi Antar Layanan
Menu Service berperan sebagai **provider** untuk menyediakan data menu dan sebagai **consumer** untuk menerima update stok dari Order Service. 

1. **Provider (Menu Service):** Mengirimkan data menu yang tersedia untuk dipilih oleh pengguna.
2. **Consumer (Menu Service):** Menerima update stok makanan setelah pemesanan berhasil.

### Alur Komunikasi:
1. Provider (Menu Service): Memberikan data menu yang bisa dipesan kepada Order Service.
2. Consumer (Menu Service): Menerima update stok makanan setelah pemesanan berhasil dilakukan oleh Order Service.

## Instalasi
1. Clone repo ini:  
   `git clone https://github.com/dzakyyuddinb/restoapp-uts-iae`
2. Install dependensi:  
   `pip install -r requirements.txt`

## Penggunaan
Jalankan server:  
`python app.py`

Server akan berjalan di `http://localhost:5002`