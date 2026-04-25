def country_score(row):
    return (
        0.3 * (row["Yield"] / 3.0) +
        0.3 * (-row["CO2"] / 1000) +
        0.2 * (-row["Cost"] / 500) +
        0.2 * (row["IRR"] / 100)
    )