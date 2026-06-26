from scipy.signal import butter, filtfilt, find_peaks

def apply_lowpass_filter(data_array, cutoff=0.05, order=2):
    b, a = butter(order, cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data_array)
    return filtered_data

def isolate_noise(raw_data_array, filtered_data_array):
    return raw_data_array - filtered_data_array

def detect_extrema(filtered_data_array, min_distance=10):
    peaks, _ = find_peaks(filtered_data_array,distance=min_distance)
    troughs, _ = find_peaks(-filtered_data_array,distance=min_distance)
    return peaks, troughs