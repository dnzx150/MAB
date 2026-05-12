# 🎓 Hệ Thống Gợi Ý Laptop — Multi-Armed Bandit (MAB)

> **Thư gửi sinh viên:**  
> File này được viết như một hướng dẫn từng bước từ thầy/cô gửi đến em. Hãy đọc **từ trên xuống dưới**, làm theo **từng bước một** và **đừng bỏ qua bất kỳ phần nào**. Mỗi phần đều có lý do. Nếu em bị kẹt ở đâu, hãy đọc lại phần [Xử Lý Lỗi Thường Gặp](#-xử-lý-lỗi-thường-gặp) trước khi hỏi.

---

## 📋 Mục Lục

| # | Phần | Thời gian ước tính |
|---|---|---|
| 1 | [Đây là dự án gì?](#-đây-là-dự-án-gì) | 5 phút đọc |
| 2 | [Chuẩn bị môi trường](#-bước-1-chuẩn-bị-môi-trường) | 10–15 phút |
| 3 | [Tải và chạy dự án](#-bước-2-tải-và-chạy-dự-án) | 5 phút |
| 4 | [Sử dụng Web Demo](#-bước-3-sử-dụng-web-demo) | 15 phút thực hành |
| 5 | [Hiểu cấu trúc dự án](#-bước-4-hiểu-cấu-trúc-dự-án) | 10 phút đọc |
| 6 | [Những thay đổi so với repo gốc](#-bước-5-những-thay-đổi-so-với-repo-gốc) | 10 phút đọc |
| 7 | [Lý thuyết cần nắm](#-bước-6-lý-thuyết-cần-nắm) | 20 phút đọc |
| 8 | [Xử lý lỗi thường gặp](#-xử-lý-lỗi-thường-gặp) | Tham khảo khi cần |
| 9 | [Câu hỏi bảo vệ](#-câu-hỏi-bảo-vệ-đồ-án) | Tham khảo khi cần |

---

## 🧠 Đây Là Dự Án Gì?

Đây là **Web Demo** cho đồ án tốt nghiệp về **Hệ thống Gợi ý Laptop** ứng dụng thuật toán **Multi-Armed Bandit (MAB)**.

### Bài toán được giải quyết

Khi em mở Shopee hay Tiki tìm laptop, có hàng trăm sản phẩm hiện ra. Làm sao hệ thống biết gợi ý cái nào phù hợp với em nhất — nhất là khi em mới dùng lần đầu, chưa có lịch sử mua hàng?

Câu trả lời của dự án này: **để hệ thống tự học thông qua phản hồi trực tiếp của em** (Like / Dislike) theo thời gian thực, không cần dữ liệu lịch sử.

### Demo trông như thế nào?

```
┌────────────────────────────────────────────────────┐
│  🎯 Chọn nhu cầu: [Gaming ▼]  [ε-Greedy] [UCB1]  │
│                   [▶ START]    [⟳ RESET]           │
├───────────────────────┬────────────────────────────┤
│  📈 Biểu đồ ε-Greedy │  📈 Biểu đồ UCB1           │
│  (Cumulative Likes)   │  (Cumulative Likes)         │
├──────────┬────────────┴┬───────────────────────────┤
│ 🎮Gaming │ 💼Office    │ 🎓Student                  │
│ ASUS ROG │ Dell XPS 13 │ HP Pavilion               │
│ i9 / 16G │ i7 / 16GB   │ i5 / 8GB                  │
│ RTX 4060 │ Iris Xe     │ Iris Xe                   │
│ 42.99M₫  │ 35.99M₫     │ 18.99M₫                   │
│ [👍 Like] │ [👍 Like]   │ [👍 Like]                  │
│ [👎 Dis] │ [👎 Dis]    │ [👎 Dis]                   │
└──────────┴─────────────┴───────────────────────────┘
```

Mỗi lần em nhấn Like/Dislike → biểu đồ cập nhật ngay → hệ thống thông minh hơn → lần sau gợi ý tốt hơn.

### Hai thuật toán được so sánh

| Thuật toán | Ý tưởng đơn giản | Khi nào dùng |
|---|---|---|
| **ε-Greedy** | 20% lượt thử ngẫu nhiên, 80% chọn laptop tốt nhất đang biết | Khi cần đơn giản, dễ hiểu |
| **UCB1** | Tính điểm thông minh: vừa dựa trên Like, vừa dựa trên "chưa được thử đủ" | Khi cần hiệu quả cao hơn |

---

## 🛠 Bước 1: Chuẩn Bị Môi Trường

> **Thầy/cô nhắn:** Em cần làm đúng phần này trước. Bỏ qua sẽ gặp lỗi sau.

### 1.1 — Kiểm tra Python

Mở **Command Prompt** (Windows: nhấn `Win + R` → gõ `cmd` → Enter).

Gõ lệnh:
```
python --version
```

**Nếu thấy `Python 3.x.x` (ví dụ `Python 3.11.4`)** → Tốt, chuyển sang bước 1.2.

**Nếu thấy lỗi `'python' is not recognized`** → Cần cài Python:
1. Truy cập: https://www.python.org/downloads/
2. Tải phiên bản **Python 3.11** (khuyến nghị) hoặc 3.10, 3.12
3. Chạy file cài đặt vừa tải
4. ⚠️ **Quan trọng:** Tích vào ô **"Add Python to PATH"** ở màn hình đầu tiên — nếu bỏ qua bước này sẽ phải cài lại
5. Nhấn **"Install Now"**
6. Đóng Command Prompt, mở lại, gõ lại `python --version`

---

### 1.2 — Cài đặt thư viện

Vẫn trong Command Prompt, gõ **từng lệnh** sau (gõ xong nhấn Enter, chờ xong rồi gõ lệnh tiếp):

```
pip install flask
```

Chờ thấy dòng `Successfully installed flask-...` thì tiếp tục:

```
pip install numpy
```

Chờ thấy `Successfully installed numpy-...`.

**Xác nhận cài thành công** — gõ lệnh này:
```
python -c "import flask, numpy; print('✅ Cài đặt thành công! Flask:', flask.__version__, '| NumPy:', numpy.__version__)"
```

Kết quả mong đợi (số version có thể khác):
```
✅ Cài đặt thành công! Flask: 3.0.3 | NumPy: 1.26.4
```

Nếu thấy dòng này → sẵn sàng sang Bước 2.

---

## 📥 Bước 2: Tải Và Chạy Dự Án

### 2.1 — Mở đúng thư mục

Em cần di chuyển Command Prompt vào đúng thư mục chứa file `app.py`. Dùng lệnh `cd` (change directory):

```
cd đường-dẫn-đến-thư-mục
```

**Ví dụ thực tế** — nếu em clone repo vào Desktop:
```
cd C:\Users\TenCuaEm\Desktop\MAB
```

Nếu em dùng máy Mac/Linux:
```
cd ~/Desktop/MAB
```

**Kiểm tra em đang đúng chỗ** — gõ lệnh liệt kê file:

Windows:
```
dir
```

Mac/Linux:
```
ls
```

Em phải thấy danh sách gồm có: `app.py`, `bandit_base.py`, `algorithms.py`, `laptops_normalized.csv` và thư mục `templates`.

> **Nếu không thấy các file này** → em chưa vào đúng thư mục. Kiểm tra lại đường dẫn.

---

### 2.2 — Khởi động server

Gõ lệnh:
```
python app.py
```

Em sẽ thấy thông báo tương tự (không cần giống hệt, chỉ cần thấy dòng `Running on http://127.0.0.1:5000`):

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

> ⚠️ **Quan trọng:** Cửa sổ Command Prompt này **phải luôn mở** trong khi em dùng ứng dụng. Đóng nó = tắt server = web không hoạt động.

---

### 2.3 — Mở ứng dụng trên trình duyệt

Mở **Google Chrome** hoặc **Firefox**.

Gõ vào thanh địa chỉ (address bar):
```
http://127.0.0.1:5000
```

Nhấn Enter. Giao diện Web Demo sẽ hiện ra.

> 💡 **Mẹo:** Em cũng có thể gõ `http://localhost:5000` — hai địa chỉ này giống nhau hoàn toàn.

---

## 🖥 Bước 3: Sử Dụng Web Demo

> Em hãy thực hành đúng theo các kịch bản dưới đây. Đây là dữ liệu thực nghiệm em sẽ cần để điền vào báo cáo.

### Kịch bản A — Chạy cơ bản, quen giao diện (5 phút)

**A1.** Không chọn gì cả, nhấn thẳng nút **▶ START** màu xanh lá.

**A2.** 3 thẻ laptop xuất hiện. Quan sát thông tin trên mỗi thẻ:
- Badge màu ở góc trái trên: phân khúc (🔴 Gaming / 🔵 Office / 🟢 Student)
- Giá ở góc phải trên
- Tên laptop
- CPU, RAM, GPU
- Nút 👍 Like và 👎 Dislike

**A3.** Nhấn 👍 **Like** trên laptop đầu tiên. Quan sát:
- Biểu đồ bên trên cập nhật ngay (đường tăng thêm 1 điểm)
- 3 laptop mới xuất hiện thay thế

**A4.** Thực hiện thêm 9 lần Like hoặc Dislike tùy ý. Sau 10 lần, chụp màn hình biểu đồ.

---

### Kịch bản B — So sánh hai thuật toán (10 phút)

> Đây là thực nghiệm quan trọng nhất — kết quả này sẽ đi vào báo cáo.

**B1.** Nhấn **⟳ RESET** → xác nhận "OK" → hệ thống về 0.

**B2.** Nhấn nút **ε-Greedy** (nút nền trắng viền xanh dương).

**B3.** Nhấn **▶ START**.

**B4.** Trong 20 lượt tiếp theo: **giả lập hành vi người dùng thích Gaming** — Like laptop Gaming (ASUS ROG, Lenovo Legion), Dislike laptop khác.

**B5.** Chụp màn hình biểu đồ sau lượt thứ 20. Ghi lại tổng số Likes.

**B6.** Nhấn **⟳ RESET** → xác nhận.

**B7.** Nhấn nút **UCB1** (nút nền trắng viền vàng).

**B8.** Nhấn **▶ START**.

**B9.** Lặp lại đúng chiến lược ở B4: 20 lượt, Like Gaming, Dislike các loại khác.

**B10.** Chụp màn hình và ghi tổng Likes.

**Điền kết quả vào bảng này (dán vào báo cáo):**

| Thuật toán | Tổng Likes sau 20 lượt | Nhận xét |
|---|---|---|
| ε-Greedy | *(điền vào đây)* | |
| UCB1 | *(điền vào đây)* | |

---

### Kịch bản C — Kiểm tra Prior Knowledge (5 phút)

> "Prior Knowledge" = hệ thống được "mồi" trước một số dữ liệu dựa trên Profile người dùng chọn.

**C1.** Nhấn **⟳ RESET**.

**C2.** Từ dropdown **"Chọn nhu cầu"**, chọn **"Gaming & Đồ họa"**.

**C3.** Nhấn **UCB1** → nhấn **▶ START**.

**C4.** Quan sát 3 laptop đầu tiên được gợi ý.

**Kết quả kỳ vọng:** ASUS ROG Zephyrus và Lenovo Legion phải xuất hiện vì hệ thống đã tự động gán 2 điểm Like cho các laptop có tag "gaming" trước khi bắt đầu.

**C5.** Nhấn **⟳ RESET** → đổi sang Profile **"Học sinh - Sinh viên"** → lặp lại. Lần này MacBook Air M2 và Acer Swift 3 phải xuất hiện.

---

### Kịch bản D — Kiểm tra Reset không reload trang (2 phút)

**D1.** Chạy 5 lượt bất kỳ để biểu đồ có dữ liệu.

**D2.** Để ý **URL trên thanh địa chỉ** của trình duyệt (`http://127.0.0.1:5000`).

**D3.** Nhấn **⟳ RESET** → xác nhận.

**D4.** Quan sát: biểu đồ về 0, laptop cards biến mất, URL **không thay đổi**, trang **không bị nhấp nháy/reload**.

> Đây là điểm kỹ thuật quan trọng: Reset hoạt động bằng cách cập nhật dữ liệu trực tiếp, không yêu cầu tải lại trang — khác với cách làm thông thường `location.reload()`.

---

## 📁 Bước 4: Hiểu Cấu Trúc Dự Án

```
repo/
│
├── app.py                  ← ⭐ File quan trọng nhất
│                              Chứa: server Flask, logic MAB, tất cả API
│
├── bandit_base.py          ← Lớp cơ sở OOP cho thuật toán
│                              (BanditAgent, EpsilonGreedy, UCB1 class)
│
├── algorithms.py           ← Phiên bản OOP của thuật toán
│                              (không được app.py dùng trực tiếp,
│                               dùng để tham khảo lý thuyết)
│
├── laptops_normalized.csv  ← Dữ liệu 150 dòng laptop đã chuẩn hóa
│                              (dự phòng cho Contextual Bandit tương lai)
│
├── templates/
│   └── index.html          ← ⭐ Giao diện người dùng
│                              Chứa: HTML, Bootstrap 5, Chart.js, JavaScript
│
├── README.md               ← File này (hướng dẫn tổng thể)
├── CHANGES.md              ← Ghi lại 7 thay đổi so với repo gốc
├── STUDENT_GUIDE.md        ← Hướng dẫn chi tiết + lý thuyết chuyên sâu
└── THESIS.md               ← Khung đồ án tốt nghiệp 35 trang
```

### Luồng hoạt động khi em nhấn "Like"

```
Em nhấn 👍 Like
      │
      ▼
JavaScript (index.html)
   fetch('/feedback', {laptop_id: 2, reward: 1})
      │
      ▼
Flask Route /feedback (app.py)
   counts[2] += 1
   rewards[2] += 1
   lịch sử biểu đồ cập nhật
   cache_clear()
      │
      ▼
JavaScript gọi /api/stats
   nhận lại lịch sử mới nhất
      │
      ▼
Chart.js cập nhật biểu đồ ngay lập tức
      │
      ▼
JavaScript gọi /get-recommendations
   Flask chạy MAB (ε-Greedy hoặc UCB1)
   trả về 3 laptop tốt nhất theo thuật toán
      │
      ▼
JavaScript render 3 thẻ laptop mới
```

---

## 🔄 Bước 5: Những Thay Đổi So Với Repo Gốc

> Phần này giải thích tại sao code trong repo này **khác** so với repo gốc ban đầu tại `github.com/dnzx150/MAB`. Hiểu được những thay đổi này sẽ giúp em trả lời câu hỏi bảo vệ tốt hơn.

### Thay đổi 1 — Xóa import thừa (`app.py` dòng 2)

| | Code |
|---|---|
| **Trước** | `import pandas as pd` |
| **Sau** | *(đã xóa)* |

**Tại sao?** `pandas` được import nhưng không được dùng ở bất kỳ đâu trong file. Đây gọi là "dead import" — gây tốn bộ nhớ và gây nhầm lẫn cho người đọc code.

---

### Thay đổi 2 — Sửa lỗi UCB1 chia cho 0 (`app.py`)

| | Code |
|---|---|
| **Trước** | `confidence = np.sqrt(2 * np.log(t+1) / (counts + 1e-5))` |
| **Sau** | `ucb_values = np.where(counts > 0, rates + np.sqrt(...), np.inf)` |

**Tại sao?** Khi laptop chưa được thử lần nào (`counts = 0`), mẫu số bằng 0 → chia cho 0. Code cũ dùng `+ 1e-5` (thêm số rất nhỏ) để tránh lỗi, nhưng đây **sai về lý thuyết UCB1**: laptop chưa thử phải có điểm = **vô cực (+∞)** để được ưu tiên tuyệt đối. Code mới dùng `np.inf` — đúng với lý thuyết.

---

### Thay đổi 3 — Sửa `@lru_cache` trả về mutable object (`app.py`)

| | Code |
|---|---|
| **Trước** | `return total_steps, rates` |
| **Sau** | `return total_steps, rates.copy()` |

**Tại sao?** `@lru_cache` lưu chính object `rates` vào bộ nhớ đệm. Nếu ai đó vô tình sửa array `rates` bên ngoài → dữ liệu trong cache bị nhiễm. `.copy()` trả về bản sao tách biệt, tránh bug tiềm ẩn này.

---

### Thay đổi 4 — Bổ sung thông tin laptop (`app.py`)

| | Trước | Sau |
|---|---|---|
| Trường có trong dict | `id, name, tags` | `id, name, tags, category, cpu, ram, gpu, price` |

**Tại sao?** Route `/get-recommendations` trả về dict laptop dưới dạng JSON cho Frontend. Nếu thiếu `cpu`, `ram`, `gpu`, `price` thì giao diện card không có gì để hiển thị ngoài tên.

---

### Thay đổi 5 — Sửa Reset không reload trang (`index.html`)

| | Code |
|---|---|
| **Trước** | `await fetch('/reset', ...); location.reload();` |
| **Sau** | `chart.data.labels = [0]; chart.update('none');` *(không có reload)* |

**Tại sao?** `location.reload()` tải lại toàn bộ trang — phá hủy biểu đồ, xóa trạng thái JS, gây nhấp nháy. Yêu cầu đề bài là reset "trơn tru không cần reload". Code mới cập nhật trực tiếp dữ liệu Chart.js mà không reload.

---

### Thay đổi 6 — Thêm bảo vệ trong `sendFeedback()` (`index.html`)

| | Code |
|---|---|
| **Trước** | Gọi `chartEg.data...` trực tiếp |
| **Sau** | `if (!isStarted) return;` *(kiểm tra trước)* |

**Tại sao?** Nếu `sendFeedback()` chạy trước khi nhấn START, `chartEg` chưa được khởi tạo (= `undefined`) → lỗi `TypeError` làm chết trang. Guard này ngăn điều đó.

---

### Thay đổi 7 — Nâng cấp giao diện Laptop Card (`index.html`)

| | Trước | Sau |
|---|---|---|
| Thông tin hiển thị | Chỉ tên laptop | Badge phân khúc + Giá + CPU/RAM/GPU |
| Layout | Đơn giản | Flexbox, canh đều, nút luôn ở cuối |

**Tại sao?** Card cũ không đủ thông tin để người dùng quyết định Like/Dislike có ý nghĩa. Feedback có ý nghĩa → dữ liệu tốt → MAB học nhanh hơn.

---

## 📚 Bước 6: Lý Thuyết Cần Nắm

> Em cần hiểu phần này để trả lời câu hỏi của hội đồng. Đọc kỹ, đừng học thuộc lòng — hãy hiểu bằng hình ảnh.

### 6.1 — Reinforcement Learning là gì?

Hãy nghĩ đến cách em học chơi một trò chơi điện tử mới mà không có hướng dẫn:
- Em **thử** các nút bấm khác nhau
- Khi làm đúng, game **thưởng** (điểm tăng, nhân vật không chết)
- Khi làm sai, game **phạt** (mất mạng, thua)
- Theo thời gian, em **học** được cách chơi tốt hơn

Đây chính là Reinforcement Learning:

```
Tác nhân (Agent)  →  Hành động (Action)  →  Môi trường (Environment)
        ↑                                              │
        └──────────── Phần thưởng (Reward) ←──────────┘
```

Trong dự án của em:
- **Agent** = hệ thống MAB
- **Action** = gợi ý một laptop
- **Environment** = người dùng (em)
- **Reward** = Like (+1) hoặc Dislike (0)

---

### 6.2 — Multi-Armed Bandit là gì?

Tên "Multi-Armed Bandit" (máy đánh bạc nhiều tay) đến từ hình ảnh casino:

```
Trước mặt em có 6 máy đánh bạc:
  [Máy 1] [Máy 2] [Máy 3] [Máy 4] [Máy 5] [Máy 6]
     ?%      ?%      ?%      ?%      ?%      ?%
  (tỉ lệ ra tiền chưa biết)

Em có 30 lượt kéo. Kéo máy nào để kiếm nhiều tiền nhất?
```

Ánh xạ sang hệ thống gợi ý laptop của em:

| Casino | Hệ thống của em |
|---|---|
| Máy đánh bạc | Một mẫu laptop |
| Kéo tay máy | Hiển thị laptop cho người dùng |
| Ra tiền | Like = 1 |
| Không ra tiền | Dislike = 0 |
| Tỉ lệ ra tiền (ẩn) | Xác suất Like thực sự (chưa biết) |

---

### 6.3 — Vấn đề cốt lõi: Exploration vs. Exploitation

Đây là câu hỏi khó nhất trong MAB, và em **phải** giải thích được khi bảo vệ:

**Giả sử sau 5 lượt đầu:**
```
MacBook Air M2   → 3 Like / 0 Dislike → tỉ lệ 100%
Dell XPS 13      → 0 Like / 2 Dislike → tỉ lệ 0%
ASUS ROG         → chưa thử lần nào
HP Pavilion      → chưa thử lần nào
Lenovo Legion    → chưa thử lần nào
Acer Swift 3     → chưa thử lần nào
```

**Câu hỏi:** Lượt tiếp theo gợi ý laptop nào?

**Chỉ Khai thác (Pure Exploitation):**
→ Luôn gợi ý MacBook Air M2 (đang 100%)

**Vấn đề:** 5 lượt quá ít để kết luận. MacBook Air có thể chỉ may mắn. ASUS ROG chưa được thử — biết đâu người dùng thích Gaming hơn? Ta đang bỏ lỡ thông tin quan trọng.

**Chỉ Khám phá (Pure Exploration):**
→ Chọn ngẫu nhiên mỗi lượt

**Vấn đề:** Lãng phí lượt vào Dell XPS đã biết là kém (0%). Không tận dụng được gì từ những gì đã học.

**→ Cần cân bằng:** Vừa khai thác laptop đang tốt, vừa khám phá laptop chưa biết.

---

### 6.4 — Epsilon-Greedy hoạt động thế nào?

**Ý tưởng:** Tung đồng xu. Nếu ra mặt ngửa (20% = ε): khám phá ngẫu nhiên. Còn lại (80%): khai thác cái tốt nhất.

**Công thức:**
```
Tại mỗi lượt t:
  Tung r ~ Uniform(0, 1)
  
  Nếu r < ε (= 0.2):
    → Chọn ngẫu nhiên 3 laptop bất kỳ  [EXPLORATION]
  
  Nếu r ≥ ε (= 0.2):
    → Chọn 3 laptop có tỉ lệ Like cao nhất  [EXPLOITATION]
```

**Code tương ứng:**
```python
if np.random.rand() < 0.2:
    indices = np.random.choice(N_ARMS, 3, replace=False)   # Ngẫu nhiên
else:
    indices = np.argsort(rates)[-3:]                        # Top 3 tốt nhất
```

**Hạn chế:** ε = 0.2 **cố định** — sau 1000 lượt vẫn tốn 200 lượt vào khám phá ngẫu nhiên dù đã biết rất rõ laptop nào tốt.

---

### 6.5 — UCB1 hoạt động thế nào?

**Ý tưởng:** Không random. Tính điểm thông minh cho mỗi laptop dựa trên 2 thành phần:

```
Điểm UCB1 = (Tỉ lệ Like hiện tại) + (Bonus khám phá)
           = Q(a)  +  c × √(ln(t) / N(a))
```

**Giải thích bằng số** (ví dụ: t = 10, c = √2 ≈ 1.41):

```
MacBook Air:  Q = 0.75, N = 8  → Bonus = 1.41 × √(ln10/8) = 0.76  → UCB = 1.51
ASUS ROG:     Q = 0.50, N = 1  → Bonus = 1.41 × √(ln10/1) = 2.14  → UCB = 2.64 ✓ (cao nhất!)
HP Pavilion:  Q = 0.00, N = 0  → N = 0 → UCB = ∞ (vô cực)        → UCB = ∞   ✓ (tuyệt đối!)
```

→ Dù MacBook Air đang có tỉ lệ Like cao (0.75), HP Pavilion chưa được thử → UCB = ∞ → **phải thử HP Pavilion trước**.

**Tại sao N(a) = 0 → UCB = ∞?**
Vì laptop chưa được thử **hoàn toàn chưa biết** — ta không có cơ sở gì để nói nó tệ. Phải thử ít nhất một lần trước khi so sánh.

---

### 6.6 — Tại sao NumPy? Tại sao cần Vectorization?

**Cách chậm (Python thuần):**
```python
# Tính tỉ lệ Like cho từng laptop — xử lý tuần tự
rates = []
for i in range(6):                    # 6 vòng lặp Python
    if counts[i] > 0:
        rates.append(rewards[i] / counts[i])
    else:
        rates.append(0.0)
```

**Cách nhanh (NumPy Vectorization):**
```python
# Tính đồng thời cho tất cả 6 laptop — chạy ở tầng C, không qua Python
rates = np.divide(rewards, counts, out=np.zeros_like(rewards), where=counts != 0)
```

Cả hai cho kết quả như nhau, nhưng NumPy nhanh hơn ~50 lần khi dataset lớn vì thực thi ở ngôn ngữ C thay vì qua trình thông dịch Python.

---

### 6.7 — `@lru_cache` là gì?

```python
@lru_cache(maxsize=1)
def get_stats_summary():
    # Hàm này tốn ~10μs để chạy
    ...
    return total_steps, rates.copy()
```

**Không có cache:** Mỗi lần Dashboard hỏi → tính lại từ đầu → ~10μs.

**Có cache:** Lần đầu hỏi → tính → lưu vào RAM. Các lần sau → lấy từ RAM ngay → ~1μs.

**Khi nào xóa cache?** Khi có Like/Dislike mới (dữ liệu thay đổi), hệ thống gọi `cache_clear()`. Lần sau sẽ tính lại với dữ liệu mới, rồi cache lại.

---

## 🐛 Xử Lý Lỗi Thường Gặp

### Lỗi: `'python' is not recognized`
```
'python' is not recognized as an internal or external command
```
**Nguyên nhân:** Python chưa cài, hoặc cài nhưng không tích "Add to PATH".  
**Giải quyết:** Cài lại Python, **nhớ tích "Add Python to PATH"**.

---

### Lỗi: `ModuleNotFoundError: No module named 'flask'`
```
ModuleNotFoundError: No module named 'flask'
```
**Nguyên nhân:** Flask chưa được cài.  
**Giải quyết:**
```
pip install flask
```

---

### Lỗi: `Address already in use` (port 5000)
```
OSError: [Errno 98] Address already in use
```
**Nguyên nhân:** Đang có một instance Flask khác chạy ở port 5000.  
**Giải quyết (Windows):** Mở Command Prompt mới, gõ:
```
netstat -ano | findstr :5000
```
Tìm số PID trong cột cuối, rồi:
```
taskkill /PID [số PID] /F
```
Sau đó chạy lại `python app.py`.

**Hoặc đơn giản hơn:** Khởi động lại máy tính.

---

### Lỗi: `This site can't be reached` trên trình duyệt
**Nguyên nhân:** Server Flask chưa chạy hoặc đã bị đóng.  
**Giải quyết:** Quay lại Command Prompt, kiểm tra xem `python app.py` có đang chạy không. Nếu cửa sổ đã đóng, mở lại và chạy lại.

---

### Biểu đồ không hiện, không cập nhật
**Bước kiểm tra:**
1. Nhấn **F12** → chọn tab **Console**
2. Xem có dòng lỗi màu đỏ không
3. Nếu thấy `chartEg is not defined` → em chưa nhấn **START** trước khi Like
4. Đúng thứ tự: Chọn thuật toán → **START** → mới nhấn Like/Dislike

---

### Muốn thay đổi epsilon từ 0.2 sang giá trị khác
Mở `app.py`, tìm dòng:
```python
epsilon = 0.2
```
Đổi thành giá trị em muốn (ví dụ `0.1`). Lưu file. Flask tự động restart.

---

## 🎤 Câu Hỏi Bảo Vệ Đồ Án

> Đây là những câu hội đồng hay hỏi nhất. Em hãy đọc và tự tập trả lời bằng lời của mình — **không học thuộc lòng**, hãy hiểu để nói tự nhiên.

---

**Câu 1: "Em giải thích Exploration-Exploitation Tradeoff là gì?"**

Gợi ý trả lời: *"Đây là đánh đổi cốt lõi của MAB. Nếu chỉ khai thác — luôn gợi ý laptop đang có điểm cao nhất — hệ thống có thể bỏ lỡ laptop tốt hơn nhưng chưa được thử đủ lần. Nếu chỉ khám phá ngẫu nhiên — không tận dụng được gì từ dữ liệu đã học. ε-Greedy cân bằng bằng xác suất cố định 20%, còn UCB1 cân bằng bằng công thức tự điều chỉnh dựa trên số lần đã thử."*

---

**Câu 2: "Tại sao UCB1 gán N(a)=0 là vô cực, không phải một số lớn?"**

Gợi ý trả lời: *"Vì vô cực là chuẩn xác về lý thuyết. Arm chưa thử bao giờ phải được ưu tiên tuyệt đối — không có arm đã thử nào có thể vượt qua điểm vô cực, dù arm đó tốt đến đâu. Nếu dùng một số lớn hữu hạn như 1e-5, khi tổng số lượt t đủ lớn, bonus khám phá của arm đã thử có thể vượt qua nó — arm chưa thử bị bỏ qua, vi phạm nguyên tắc UCB1."*

---

**Câu 3: "Tại sao dùng `.fill(0)` để reset thay vì gán lại mảng mới?"**

Gợi ý trả lời: *"Vì `counts`, `rewards` là biến global được Flask dùng ở nhiều route khác nhau. Nếu gán lại như `counts = np.zeros(6)`, biến local mới được tạo nhưng tham chiếu global vẫn trỏ array cũ — dữ liệu không thực sự bị xóa. `.fill(0)` sửa in-place — tất cả tham chiếu đến array đó đều thấy giá trị mới ngay lập tức."*

---

**Câu 4: "Sự khác biệt giữa ε-Greedy và UCB1 trong thực nghiệm là gì?"**

Gợi ý trả lời: *"Trong thực nghiệm của em với 20 lượt, UCB1 tích lũy được [điền số] Likes so với ε-Greedy là [điền số]. UCB1 hội tụ nhanh hơn vì nó khám phá có chủ đích — ưu tiên laptop ít được thử thay vì random. ε-Greedy tốn 20% lượt vào khám phá ngẫu nhiên, kể cả khi đã biết rõ laptop nào tốt."*

---

**Câu 5: "Hệ thống này giải quyết Cold Start như thế nào?"**

Gợi ý trả lời: *"Hệ thống MAB hỗ trợ giảm thiểu đáng kể Cold Start theo hai cách. Thứ nhất, không cần dữ liệu lịch sử — hệ thống học ngay từ lượt tương tác đầu tiên. Thứ hai, UCB1 đảm bảo mọi laptop đều được thử ít nhất một lần trước khi bắt đầu khai thác — thông qua cơ chế gán UCB = ∞ cho laptop chưa thử. Ngoài ra, cơ chế Prior Knowledge cho phép 'mồi' dữ liệu ban đầu dựa trên Profile người dùng khai báo."*

---

**Câu 6: "NumPy Vectorization giúp gì trong hệ thống này?"**

Gợi ý trả lời: *"NumPy Vectorization thay thế vòng lặp Python bằng tính toán song song ở tầng C. Với 6 laptop hiện tại, sự khác biệt không đáng kể. Nhưng đây là thiết kế hướng đến khả năng mở rộng — khi dataset lên 1000 laptop, NumPy nhanh hơn ~50 lần. Đây cũng là lý do tại sao các thư viện ML như TensorFlow, PyTorch đều xây dựng trên NumPy."*

---

## 📌 Tóm Tắt Nhanh (Quick Reference)

```
Khởi động:    cd [thư-mục-dự-án]  →  python app.py
Truy cập:     http://127.0.0.1:5000
Dừng server:  Ctrl + C trong Command Prompt

Thứ tự đúng: 1. Chọn Profile  2. Chọn thuật toán  3. START  4. Like/Dislike

File quan trọng nhất:
  app.py         → logic MAB, server Flask
  index.html     → giao diện, biểu đồ, JavaScript

Thay đổi epsilon:   app.py → epsilon = 0.2  → đổi số
Thay đổi c (UCB1):  bandit_base.py → UCB1(num_arms, c=2.0) → đổi c
Thêm laptop:        app.py → N_ARMS += 1 → thêm dict vào LAPTOPS
```

---

*README này được biên soạn kèm theo đồ án tốt nghiệp — Khoa CNTT — Năm học 2024–2025.*  
*Xem thêm: `CHANGES.md` (chi tiết sửa đổi) · `STUDENT_GUIDE.md` (lý thuyết chuyên sâu) · `THESIS.md` (khung báo cáo)*
