import numpy as np
import pandas as pd
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
    {"id": 0, "name": "MacBook Air M2", "tags": ["student", "office"]},
    {"id": 1, "name": "Dell XPS 13", "tags": ["office"]},
    {"id": 2, "name": "ASUS ROG Zephyrus", "tags": ["gaming"]},
    {"id": 3, "name": "HP Pavilion 15", "tags": ["student"]},
    {"id": 4, "name": "Lenovo Legion 5", "tags": ["gaming"]},
    {"id": 5, "name": "Acer Swift 3", "tags": ["student", "office"]},
]

@lru_cache(maxsize=1)
def get_stats_summary():
    """Sử dụng Caching để giảm độ trễ khi Dashboard truy vấn liên tục [cite: 21]"""
    total_steps = np.sum(counts)
    # Tính tỉ lệ thưởng bằng Vectorization tránh vòng lặp for
    rates = np.divide(rewards, counts, out=np.zeros_like(rewards), where=counts!=0)
    return total_steps, rates

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
        if total_steps < N_ARMS:
            indices = np.random.choice(N_ARMS, 3, replace=False)
        else:
            confidence = np.sqrt(2 * np.log(total_steps + 1) / (counts + 1e-5))
            ucb_values = rates + confidence
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

if __name__ == '__main__':
    app.run(debug=True)