def country_score(data):
    return (
        0.3 * data["irr"] +
        0.25 * data["carbon"] +
        0.15 * data["stability"] +
        0.15 * data["scale"] +
        0.15 * data["policy"]
    )

def rank_countries(dataset):
    scores = []
    for country, data in dataset.items():
        score = country_score(data)
        scores.append((country, score))
    return sorted(scores, key=lambda x: x[1], reverse=True)
