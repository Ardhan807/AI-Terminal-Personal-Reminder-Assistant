# AI Terminal Personal Reminder Assistant
## Deskripsi Proyek
AI Terminal Personal Reminder Assistant adalah AI agent terminal yang memanfaatkan AI API + Google Calendar API yang mampu memahami bahasa alami berbahasa Indonesia untuk membuat reminder otomatis, menyimpannya ke file lokal, sinkron dengan Google Calendar, serta menghapus reminder kembali baik dari file maupun kalender. Agen juga dapat merespons secara interaktif (chat-style) bila tidak ada perintah manajemen pengingat.
## Cara Menjalankan Projek
- Clone repo
  ```
  git clone https://github.com/Ardhan807/AI-Terminal-Personal-Reminder-Assistant.git
  cd AI-Terminal-Personal-Reminder-Assistant
  ```
- Istall dependencies
  ```
  pip install -r requirements.txt
  ```
- Tambahkan OpenRouter API Key, Buat file bernama .env pada root folder dan isi:
  ```
   OPENROUTER_API_KEY=masukkan_api_key_kamu_disini
  ```
- Konfigurasi Google Calendar API
1. Buka Google Cloud Console
2. Aktifkan "Google Calendar API"
3. Buat OAuth Client Credential
4. Unduh file credentials.json dan simpan di root project
- Jalankan Program
  ```
  python main.py
  ```
## Struktur Proyek
```
AI-Personal-Reminder-Assistant
│
├─ reminders.txt                # Penyimpanan reminder lokal
├─ credentials.json             # Google OAuth Credential (dibutuhkan)
├─ token.json                   # Token login (dibuat otomatis)
│
├─ .env                         # Konfigurasi OpenRouter API
├─ main.py                      # UI terminal interaktif
├─ agent.py                     # OpenRouter communication handler
├─ tools.py                     # Core logic: parsing, sync, scheduling
├─ requirements.txt
└─ README.md
```
## Catatan Penting
- Wajib menambahkan file credentials.json agar sinkronisasi Google Calendar bekerja.
- File token.json akan dibuat otomatis setelah otorisasi pertama kali.
- Harus mengisi .env dengan OpenRouter API key sebelum menjalankan aplikasi.
- Koneksi internet diperlukan untuk pemrosesan AI dan Google API.
- Reminder tetap tersimpan lokal meskipun tidak terhubung ke internet.
  
