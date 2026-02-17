import numpy as np

def assign_windows(df, window_size):
    """
    Assigns a window ID to each packet based on its relative time.

    Parameters:
    - df: DataFrame with a 'relative_time' column (seconds since first packet)
    - window_size: Size of each window in seconds

    Returns:
    - DataFrame with an additional 'window_id' column
    """
    df = df.copy()
    df["window_id"] = np.floor(df["relative_time"] / window_size).astype(int)
    return df