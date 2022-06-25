import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
class ThresholdValueError(Exception):
    """Exception raised for error in missing threshold value.

    Attributes:
        message -- explanation of the error

    Returns:
        None
    """

    def __init__(self, message="Missing threshold value. Use '.set_threshold' method to set a threshold."):
        self.message = message
        super().__init__(self.message)
