# Flask Hub 🚀

Một web app đa chức năng viết bằng **Flask (Python)** với frontend dùng HTML + CSS + JavaScript (fetch API).  
Dự án gồm 3 chức năng chính:

---

## 🧰 Chức năng

### 1. 🎭 Fake Profile Generator
Sinh dữ liệu profile giả theo quốc gia (locale), có cả thông tin cha mẹ.

### 2. 🖼️ Media Gallery (X / Twitter)
Tìm kiếm ảnh/video theo keyword hoặc username từ mạng xã hội X.

### 3. 🌍 Universal Media Downloader
Nhập **URL từ X, TikTok, Facebook, Instagram,...** để trích xuất và hiển thị media (không cần tải về server).

---

## 🚀 Deploy backend Flask lên [Render.com](https://render.com)

### Cách triển khai:
1. Push toàn bộ project này lên GitHub
2. Vào [https://render.com](https://render.com)
3. Chọn **“New Web Service”**
4. Kết nối với repo GitHub
5. Render tự động:
   - Cài thư viện từ `requirements.txt`
   - Đọc file `render.yaml`
   - Chạy `python app.py`
6. Truy cập link dạng `https://your-app.onrender.com`

📌 Hỗ trợ miễn phí 100% trên gói Free Tier!

---

## 🌐 Dùng custom domain (ví dụ: `lam.io.vn`)

1. Vào Render dashboard → App → Settings → **Custom Domains**
2. Thêm tên miền của bạn (ví dụ `lam.io.vn`)
3. Render cung cấp bản ghi DNS
4. Thêm bản ghi vào trang quản lý DNS tên miền
5. Xong! Render cấp luôn SSL (HTTPS)

---

## 🧪 Thử local

```bash
pip install -r requirements.txt
python app.py
```

Truy cập tại: http://localhost:5000

---

## 📁 Cấu trúc thư mục

```
.
├── app.py
├── requirements.txt
├── render.yaml
├── utils/
│   ├── profile_faker.py
│   ├── gallery_fetcher.py
│   └── media_downloader.py
├── templates/
│   ├── index.html
│   ├── profile_faker.html
│   ├── media_gallery.html
│   └── media_downloader.html
├── static/
│   └── css/
│       └── style.css
```

---

## 🧠 Công nghệ dùng

- Python Flask
- Faker
- yt-dlp
- snscrape
- HTML + JavaScript (Fetch API)
