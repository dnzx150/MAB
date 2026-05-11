from bandit_base import BanditAgent 
import numpy as np

class EpsilonGreedy(BanditAgent):
    def __init__(self, num_arms, epsilon=0.1):
        super().__init__(num_arms)
        self.epsilon = epsilon

    def select_arm(self):
        """Nếu tung xúc xắc < epsilon thì chọn đại, ngược lại chọn máy tốt nhất"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.num_arms)
        return np.argmax(self.q_values)

class UCB1(BanditAgent):
    def __init__(self, num_arms, c=2.0):
        super().__init__(num_arms)
        self.c = c
        self.total_steps = 0

    def select_arm(self):
        """Chọn máy dựa trên điểm hiện tại cộng với 'chỉ số tò mò'"""
        self.total_steps += 1
        for arm in range(self.num_arms):
            if self.n_counts[arm] == 0: return arm # Thử máy mới trước
            
        # Công thức UCB: Q(a) + c * sqrt(log(T) / N(a))
        exploration_bonus = self.c * np.sqrt(np.log(self.total_steps) / self.n_counts)
        return np.argmax(self.q_values + exploration_bonus)