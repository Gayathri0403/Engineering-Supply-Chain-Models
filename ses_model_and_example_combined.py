
# Simple Exponential Smoothing (SES) Model with Full Example

class SimpleExponentialSmoothing:
    def __init__(self, alpha):
        """
        Initialize the SES model with smoothing parameter alpha.
        Alpha must be between 0 and 1.
        """
        if not (0 < alpha <= 1):
            raise ValueError("Alpha must be between 0 and 1.")
        self.alpha = alpha

    def forecast(self, demand_series):
        """
        Forecast the next demand value using Simple Exponential Smoothing.

        Parameters:
        - demand_series: list of historical demand values

        Returns:
        - forecast value for the next period
        """
        if not demand_series:
            raise ValueError("Demand series cannot be empty.")
        
        forecast = demand_series[0]
        for actual in demand_series[1:]:
            forecast = self.alpha * actual + (1 - self.alpha) * forecast
        return forecast

# Full Example Usage
if __name__ == "__main__":
    # 12-month historical demand data
    monthly_demand = [120, 135, 150, 145, 160, 155, 170, 165, 180, 175, 190, 185]
    alpha = 0.5

    print("Historical Demand Data:", monthly_demand)
    print(f"Using alpha = {alpha}")

    # Create model and forecast next month
    model = SimpleExponentialSmoothing(alpha=alpha)
    forecast_next = model.forecast(monthly_demand)

    print(f"Forecast for next month (Month 13): {forecast_next:.2f}")
