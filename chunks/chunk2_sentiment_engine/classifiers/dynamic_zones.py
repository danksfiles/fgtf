from typing import Dict, Tuple
from src.models.regime import SentimentZone

def get_sentiment_zone(score: float, thresholds: Dict[SentimentZone, Tuple[float, float]]) -> SentimentZone:
    """
    Classifies a sentiment score into a sentiment zone based on dynamic thresholds.

    Args:
        score: The composite sentiment score, ranging from -1.0 to 1.0.
        thresholds: A dictionary defining the lower and upper bounds for each zone.
                    Example: {
                        SentimentZone.EXTREME_FEAR: (-1.0, -0.6),
                        SentimentZone.FEAR: (-0.6, -0.2),
                        ...
                    }

    Returns:
        The corresponding SentimentZone.
    """
    for zone, (lower_bound, upper_bound) in thresholds.items():
        if lower_bound <= score < upper_bound:
            return zone
    
    # Handle edge case for the upper bound of the highest zone
    last_zone = list(thresholds.keys())[-1]
    if score == thresholds[last_zone][1]:
        return last_zone

    raise ValueError(f"Score {score} is outside the defined threshold ranges.")

def get_default_thresholds() -> Dict[SentimentZone, Tuple[float, float]]:
    """
    Returns the default, static thresholds for sentiment zones.
    These can be overridden by a dynamic mechanism later.
    """
    return {
        SentimentZone.EXTREME_FEAR: (-1.0, -0.6),
        SentimentZone.FEAR: (-0.6, -0.2),
        SentimentZone.NEUTRAL: (-0.2, 0.2),
        SentimentZone.GREED: (0.2, 0.6),
        SentimentZone.EXTREME_GREED: (0.6, 1.0),
    }
