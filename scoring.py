def normalize_scores(similarity):
    """
    Normalize similarity score to a 0-100 scale.
    """
    return round(similarity * 100)


def assign_tier(score):
    """
    Assign a tier label based on the normalized score.
    """
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Average"
    else:
        return "Below Average" 