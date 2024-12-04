import logging

# Create a logger for this module
logger = logging.getLogger(__name__)


def calculate_mtm_score(nutrition: list) -> float:
    """
    Calculate the MTM score for a recipe based on its nutritional values.

    Parameters:
    ----------
    nutrition : list
        Nutritional values in the format:
        [calories, fat, sugar, sodium, protein, saturated_fat, carbs].

    Returns:
    -------
    float
        The calculated MTM score (0 to 100).
    """
    if not isinstance(nutrition, (list, tuple)) or len(nutrition) < 7:
        logger.warning("Invalid nutrition data: %s", nutrition)
        return 0.0

    # Extract nutritional components
    calories, fat, sugar, sodium, protein, saturated_fat, carbs = nutrition
    score = 0

    # Boost score for high protein and balanced carbs
    if protein > 8:
        score += 30
    if 35 <= (carbs / (calories / 4) * 100) <= 75:
        score += 30
    if protein > 10 and 35 <= (carbs / (calories / 4) * 100) <= 65:
        score += 15

    # Penalize for unhealthy factors
    if saturated_fat > 15:
        score -= 10
    if fat > 35:
        score -= 5
    if sugar > 35:
        score -= 5
    if sodium > 5:
        score -= 5

    # Reward moderate calorie range
    if 200 <= calories <= 900:
        score += 25
    elif calories > 1500:
        score -= 5

    # Reward balanced fat and protein
    if 15 <= fat <= 25 and 10 <= protein <= 20:
        score += 10

    final_score = max(0, min(100, score))  # Keep score within bounds

    return final_score
