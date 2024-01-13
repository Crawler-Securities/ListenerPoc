import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def slope(x1, y1, x2, y2):
    """Calculate the slope between two points."""
    return (y2 - y1) / (x2 - x1)

def is_valid_head_and_shoulders(left, head, right, df, column, slope_threshold, height_ratio_threshold):
    """Check if the identified peaks satisfy the Head and Shoulders pattern criteria."""
    left_height = df[column].iloc[left]
    head_height = df[column].iloc[head]
    right_height = df[column].iloc[right]

    # Check if the head is the highest peak
    if not (left_height < head_height and right_height < head_height):
        return False

    # Check if shoulders are at a similar level
    if abs(left_height - right_height) / head_height > height_ratio_threshold:
        return False

    # Check the slopes
    if slope(left, left_height, head, head_height) > -slope_threshold or \
       slope(head, head_height, right, right_height) < slope_threshold:
        return False

    return True

def find_head_and_shoulders(df, column='Close', slope_threshold=0.2, height_ratio_threshold=0.1, min_distance=5, shoulder_search_range=5):
    patterns = []
    peaks, _ = find_peaks(df[column], distance=min_distance)

    for i in range(len(peaks)):
        head_peak = peaks[i]
        head_height = df[column].iloc[head_peak]

        # Search for left and right shoulders within the specified range
        left_candidates = peaks[np.where((peaks < head_peak) & (peaks >= head_peak - shoulder_search_range))]
        right_candidates = peaks[np.where((peaks > head_peak) & (peaks <= head_peak + shoulder_search_range))]

        for left_peak in left_candidates:
            for right_peak in right_candidates:
                if is_valid_head_and_shoulders(left_peak, head_peak, right_peak, df, column, slope_threshold, height_ratio_threshold):
                    pattern_range = df.index[left_peak], df.index[right_peak]
                    patterns.append((pattern_range, (left_peak, head_peak, right_peak)))

    return patterns
