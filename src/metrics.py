def calculate_mtm_score(nutrition):
    """
    Calculate the MTM score for a single recipe based on its nutritional values.
    Args:
        nutrition: List of nutritional values
        [calories, fat, sugar, sodium, protein, saturated_fat, carbs].
    Returns:
        MTM score (float).
    """
    if not isinstance(nutrition, (list, tuple)) or len(nutrition) < 7:
        return 0  # Handle invalid nutrition data

    calories, fat, sugar, sodium, protein, saturated_fat, carbs = nutrition
    score = 0

    # Positive factors (boosted for high-quality recipes)
    if protein > 8:
        score += 30  # Increased from 25
    if 35 <= (carbs / (calories / 4) * 100) <= 75:
        score += 30  # Increased from 25

    # Add a bonus for recipes that meet multiple positive criteria
    if protein > 10 and 35 <= (carbs / (calories / 4) * 100) <= 65:
        score += 15  # New bonus

    # Negative factors (further relaxed penalties)
    if saturated_fat > 15:  # Increased threshold
        score -= 10  # Reduced from 15
    if fat > 35:  # Increased threshold
        score -= 5  # Reduced from 8
    if sugar > 35:  # Increased threshold
        score -= 5  # Reduced from 8
    if sodium > 5:  # Increased threshold
        score -= 5  # Reduced from 10

    # Calories scoring (broader range with higher bonuses)
    if 200 <= calories <= 900:  # Broadened range
        score += 25  # Increased from 20
    elif calories > 1500:  # Further increased threshold
        score -= 5  # Reduced penalty

    # Bonus for recipes with balanced nutrition
    if 15 <= fat <= 25 and 10 <= protein <= 20:
        score += 10  # Encourage balance

    return max(0, min(100, score))  # Ensure score is within 0-100
