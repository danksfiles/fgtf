class Strategy:
    def generate_signal(self, regime, price_history):
        raise NotImplementedError

class TrendFollowing(Strategy):
    def generate_signal(self, regime, price_history):
        # Trend-following logic
        # Placeholder logic for now
        if price_history[-1] > price_history[0]:
            return "BUY"
        else:
            return "SELL"

class MeanReversion(Strategy):
    def generate_signal(self, regime, price_history):
        # Mean-reversion logic
        # Placeholder logic for now
        if price_history[-1] < sum(price_history) / len(price_history):
            return "BUY"
        else:
            return "SELL"
