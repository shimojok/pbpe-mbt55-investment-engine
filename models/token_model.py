import numpy as np

def simulate_token_price(P0, demand, supply, alpha=0.01, sigma=0.2):
    steps = 100
    dt = 0.01  # ← 重要（時間刻み）

    prices = [P0]

    for _ in range(steps):
        dW = np.random.normal(0, np.sqrt(dt))

        # ドリフト（暴走しないよう弱める）
        drift = alpha * (demand - supply) * prices[-1] * dt

        # 拡散（ランダム）
        diffusion = sigma * prices[-1] * dW

        new_price = prices[-1] + drift + diffusion

        # 下限（0以下防止）
        new_price = max(new_price, 0.1)

        # 上限（暴走防止：仮に）
        new_price = min(new_price, 100)

        prices.append(new_price)

    return prices