import numpy as np
from flask import Flask, render_template, request, jsonify
from functools import lru_cache

app = Flask(__name__)

# --- CẤU HÌNH DỮ LIỆU ---
N_ARMS = 6
# Sử dụng mảng NumPy để tối ưu hóa tính toán Vectorization [cite: 20]
counts = np.zeros(N_ARMS, dtype=np.int32)
rewards = np.zeros(N_ARMS, dtype=np.float32)
dislikes = np.zeros(N_ARMS, dtype=np.int32)

# Lịch sử để vẽ biểu đồ
history = {
    "eg": {"likes": [0], "dislikes": [0], "steps": [0]},
    "ucb": {"likes": [0], "dislikes": [0], "steps": [0]}
}
current_algo = "eg"

LAPTOPS = [
    {
        "id": 0, "name": "MacBook Air M2", "tags": ["student", "office"],
        "category": "Student / Office", "cpu": "Apple M2 8-core",
        "ram": "8 GB", "gpu": "GPU 8-core tích hợp", "price": "28.990.000₫"
    },
    {
        "id": 1, "name": "Dell XPS 13", "tags": ["office"],
        "category": "Office", "cpu": "Intel Core i7-1360P",
        "ram": "16 GB", "gpu": "Intel Iris Xe", "price": "35.990.000₫"
    },
    {
        "id": 2, "name": "ASUS ROG Zephyrus G14", "tags": ["gaming"],
        "category": "Gaming", "cpu": "AMD Ryzen 9 7940HS",
        "ram": "16 GB", "gpu": "NVIDIA RTX 4060 8 GB", "price": "42.990.000₫"
    },
    {
        "id": 3, "name": "HP Pavilion 15", "tags": ["student"],
        "category": "Student", "cpu": "Intel Core i5-1240P",
        "ram": "8 GB", "gpu": "Intel Iris Xe", "price": "18.990.000₫"
    },
    {
        "id": 4, "name": "Lenovo Legion 5", "tags": ["gaming"],
        "category": "Gaming", "cpu": "AMD Ryzen 7 7840HS",
        "ram": "16 GB", "gpu": "NVIDIA RTX 4060 8 GB", "price": "38.990.000₫"
    },
    {
        "id": 5, "name": "Acer Swift 3", "tags": ["student", "office"],
        "category": "Student / Office", "cpu": "AMD Ryzen 5 7530U",
        "ram": "16 GB", "gpu": "AMD Radeon tích hợp", "price": "20.990.000₫"
    },
]

@lru_cache(maxsize=1)
def get_stats_summary():
    """Sử dụng Caching để giảm độ trễ khi Dashboard truy vấn liên tục [cite: 21]"""
    total_steps = int(np.sum(counts))
    # Tính tỉ lệ thưởng bằng Vectorization tránh vòng lặp for
    rates = np.divide(rewards, counts, out=np.zeros_like(rewards), where=counts != 0)
    # Trả về bản sao để tránh cache mutation khi caller xử lý mảng
    return total_steps, rates.copy()

def select_arms():
    total_steps, rates = get_stats_summary()
    
    if current_algo == "eg":
        # Epsilon-Greedy logic [cite: 9, 10]
        epsilon = 0.2
        if np.random.rand() < epsilon:
            indices = np.random.choice(N_ARMS, 3, replace=False)
        else:
            indices = np.argsort(rates)[-3:]
    else:
        # UCB1 logic [cite: 11, 12]
        if total_steps == 0:
            indices = np.random.choice(N_ARMS, 3, replace=False)
        else:
            # Arm chưa thử (N_t(a)=0) nhận ∞ → UCB1 ưu tiên khám phá trước khi khai thác
            ucb_values = np.where(
                counts > 0,
                rates + np.sqrt(2 * np.log(total_steps + 1) / np.maximum(counts, 1)),
                np.inf
            )
            indices = np.argsort(ucb_values)[-3:]
            
    return [LAPTOPS[int(i)] for i in indices]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/switch-algo', methods=['POST'])
def switch():
    global current_algo
    data = request.json
    current_algo = data.get('algo', 'eg')
    profile = data.get('profile', 'default')
    
    # Cơ chế "Mồi" dữ liệu (Prior Knowledge) dựa trên Profile chọn 
    if profile != 'default':
        for i, laptop in enumerate(LAPTOPS):
            if profile in laptop['tags']:
                rewards[i] += 2 # Giả lập 2 lượt Like sẵn
                counts[i] += 2
    
    get_stats_summary.cache_clear()
    return jsonify({"status": "success", "algo": current_algo})

@app.route('/get-recommendations', methods=['POST'])
def recommend():
    return jsonify(select_arms())

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    idx = int(data.get('laptop_id'))
    reward = int(data.get('reward'))
    
    counts[idx] += 1
    if reward == 1:
        rewards[idx] += 1
    else:
        dislikes[idx] += 1
        
    # Cập nhật lịch sử biểu đồ
    h = history[current_algo]
    h["likes"].append(h["likes"][-1] + (1 if reward == 1 else 0))
    h["dislikes"].append(h["dislikes"][-1] + (1 if reward == 0 else 0))
    h["steps"].append(h["steps"][-1] + 1)
    
    get_stats_summary.cache_clear()
    return jsonify({"status": "success"})

@app.route('/api/stats')
def get_stats():
    return jsonify(history)

@app.route('/reset', methods=['POST'])
def reset():
    """Cơ chế Reset đồng bộ bằng lệnh fill(0) của NumPy [cite: 23]"""
    global counts, rewards, dislikes, history
    counts.fill(0)
    rewards.fill(0)
    dislikes.fill(0)
    for k in history:
        history[k] = {"likes": [0], "dislikes": [0], "steps": [0]}
    get_stats_summary.cache_clear()
    return jsonify({"status": "reset"})

@app.route('/load-demo', methods=['POST'])
def load_demo():
    """
    Nạp sẵn dữ liệu mô phỏng 20 lượt tương tác của một người dùng Gaming.
    Dùng để demo Case Study mà không cần nhấn Like/Dislike thủ công.
    """
    global counts, rewards, dislikes, history, current_algo

    # --- Reset sạch trước ---
    counts.fill(0)
    rewards.fill(0)
    dislikes.fill(0)
    for k in history:
        history[k] = {"likes": [0], "dislikes": [0], "steps": [0]}

    # --- Kịch bản: Người dùng thích Gaming, không thích Office/Student ---
    # (laptop_id, reward)  1=Like  0=Dislike
    interactions = [
        # Lượt 1–6: khám phá ban đầu (cả hai thuật toán đều random lúc đầu)
        (3, 0),  # HP Pavilion   → Dislike
        (0, 0),  # MacBook Air   → Dislike
        (2, 1),  # ASUS ROG      → Like ✓
        (5, 0),  # Acer Swift 3  → Dislike
        (4, 1),  # Lenovo Legion → Like ✓
        (1, 0),  # Dell XPS 13   → Dislike
        # Lượt 7–12: hệ thống bắt đầu học
        (2, 1),  # ASUS ROG      → Like ✓
        (4, 1),  # Lenovo Legion → Like ✓
        (0, 1),  # MacBook Air   → Like (thử lại)
        (2, 1),  # ASUS ROG      → Like ✓
        (3, 0),  # HP Pavilion   → Dislike
        (4, 1),  # Lenovo Legion → Like ✓
        # Lượt 13–20: hệ thống hội tụ — Gaming chiếm ưu thế
        (2, 1),  # ASUS ROG      → Like ✓
        (4, 1),  # Lenovo Legion → Like ✓
        (1, 0),  # Dell XPS 13   → Dislike
        (2, 1),  # ASUS ROG      → Like ✓
        (4, 1),  # Lenovo Legion → Like ✓
        (5, 0),  # Acer Swift 3  → Dislike
        (2, 1),  # ASUS ROG      → Like ✓
        (4, 1),  # Lenovo Legion → Like ✓
    ]

    # Ghi đồng thời vào cả hai lịch sử eg và ucb để cả 2 biểu đồ hiển thị
    for algo in ["eg", "ucb"]:
        h = history[algo]
        for laptop_id, reward in interactions:
            counts[laptop_id] += 1
            if reward == 1:
                rewards[laptop_id] += 1
            else:
                dislikes[laptop_id] += 1
            h["likes"].append(h["likes"][-1] + reward)
            h["dislikes"].append(h["dislikes"][-1] + (1 - reward))
            h["steps"].append(h["steps"][-1] + 1)
        # Reset counts/rewards giữa 2 algo để không cộng dồn
        counts.fill(0)
        rewards.fill(0)
        dislikes.fill(0)

    # Ghi lại lần cuối với dữ liệu tổng hợp thực tế
    for laptop_id, reward in interactions:
        counts[laptop_id] += 1
        if reward == 1:
            rewards[laptop_id] += 1
        else:
            dislikes[laptop_id] += 1

    current_algo = "eg"
    get_stats_summary.cache_clear()

    # Trả về tóm tắt để Frontend hiển thị
    rates = np.divide(rewards, counts, out=np.zeros_like(rewards), where=counts != 0)
    summary = [
        {"id": i, "name": LAPTOPS[i]["name"], "category": LAPTOPS[i]["category"],
         "likes": int(rewards[i]), "total": int(counts[i]),
         "rate": round(float(rates[i]), 2)}
        for i in range(N_ARMS)
    ]
    return jsonify({"status": "demo_loaded", "interactions": len(interactions), "summary": summary})

if __name__ == '__main__':
    app.run(debug=True)