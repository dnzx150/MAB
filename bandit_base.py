import numpy as np


class BanditAgent:
    def __init__(self, num_arms):
        self.num_arms = num_arms

        # ✅ dùng dtype để giảm memory + tăng tốc
        self.q_values = np.zeros(num_arms, dtype=np.float32)
        self.n_counts = np.zeros(num_arms, dtype=np.int32)

        # ✅ tránh append list (chậm) → dùng numpy buffer
        self.reward_history = np.empty(10000, dtype=np.float32)
        self._history_size = 0

    def update_q_values(self, arm, reward):
        """Cập nhật điểm dựa trên phản hồi của người dùng (O(1))"""
        self.n_counts[arm] += 1
        n = self.n_counts[arm]

        # ✅ incremental update tối ưu
        self.q_values[arm] += (reward - self.q_values[arm]) / n

        # ✅ lưu history nhanh hơn list.append
        if self._history_size >= len(self.reward_history):
            # auto resize (gấp đôi)
            self.reward_history = np.resize(self.reward_history, len(self.reward_history) * 2)

        self.reward_history[self._history_size] = reward
        self._history_size += 1


class EpsilonGreedy(BanditAgent):
    def __init__(self, num_arms, epsilon=0.1):
        super().__init__(num_arms)
        self.epsilon = epsilon

        # ✅ random generator nhanh hơn
        self.rng = np.random.default_rng()

    def select_arm(self):
        if self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.num_arms))

        return int(np.argmax(self.q_values))


class UCB1(BanditAgent):
    def __init__(self, num_arms, c=2.0):
        super().__init__(num_arms)
        self.c = c
        self.total_steps = 0

    def select_arm(self):
        self.total_steps += 1

        # ✅ vector hóa check arm chưa thử
        untried = np.where(self.n_counts == 0)[0]
        if untried.size > 0:
            return int(untried[0])

        # ✅ tránh tính log nhiều lần
        log_t = np.log(self.total_steps)

        # ✅ tránh chia 0 + vector hóa
        exploration_bonus = self.c * np.sqrt(log_t / self.n_counts)

        return int(np.argmax(self.q_values + exploration_bonus))