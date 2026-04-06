import json
from model import run_step

with open("parameters.json") as f:
    PARAMS = json.load(f)


def simulate(M=1, steps=5):

    state = {
        "waste_input": 1.0,
        "toxic": 0.6,
        "salinity": 0.5,
        "nutrient": 0.3,
        "D0": 0.5
    }

    microbial = (1.0, 1.0)

    history = []

    for t in range(steps):
        state, microbial, result = run_step(
            state, microbial, M, PARAMS
        )
        history.append(result)

    return history[-1]


# ✅ ここが問題だった部分
def simulate_country(row, M, params=None):

    base = simulate(M)

    return {
        "country": row["country"],
        "Yield": base["Yield"] * row["yield_base"],
        "Cost": base["Cost"] * (row["cost_base"] / 1000),
        "CO2": base["CO2"] * (row["co2_base"] / 1000)
    }


if __name__ == "__main__":

    on = simulate(M=1)
    off = simulate(M=0)

    print("MBT ON :", on)
    print("MBT OFF:", off)