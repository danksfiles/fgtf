import random

def generate_price_tick(current_price, fg_value):
    """
    Generates a new price tick based on the current price and Fear & Greed value.
    Higher fear leads to more volatility and a downward bias.
    """
    # Higher fear = more volatility and downward bias
    volatility = 0.01 + (100 - fg_value) * 0.0001
    bias = -0.001 if fg_value < 30 else 0.001 if fg_value > 70 else 0
    return current_price * (1 + random.uniform(-volatility, volatility) + bias)

def generate_mock_data(current_price):
    """
    Generates a mock data point, including a chance for a black swan event.
    """
    # 5% chance of a black swan event (flash crash)
    if random.random() < 0.05:
        return {"fg_value": 5, "price": current_price * 0.9}  # Flash crash
    
    # Normal data generation
    fg_value = random.randint(0, 100)
    price = generate_price_tick(current_price, fg_value)
    return {"fg_value": fg_value, "price": price}
