import pandas as pd
import pytest


@pytest.fixture
def sample_cars_df():
    return pd.DataFrame(
        {
            "car_make": ["Toyota", "Toyota", "Ford", "Ford"],
            "car_model": ["Corolla", "Corolla", "Focus", "Focus"],
            "Revenue": [1000, 1200, 900, 1100],
            "Total Cost": [700, 800, 600, 650],
            "Profit": [300, 400, 300, 450],
            "car_id": [1, 2, 3, 4],
            "Branch Location": [
                "Boston, Massachusetts",
                "Boston, Massachusetts",
                "Dallas, Texas",
                "Dallas, Texas",
            ],
            "car_rented_length_percent": [0.5, 0.6, 0.7, 0.8],
            "rental_days": [10, 12, 8, 9],
        }
    )