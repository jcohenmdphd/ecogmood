#JCohen 09-18-2020
#Identify Coherence Bursts and Calculate AuC
import numpy as np
import pandas as pd
from scipy import stats





def calculate_bursts(coherenceArray, burst_window = 60, percent_max = 0.5)

	"""
    Calculates 
        - cohrenceArray: np.array, coherence array (for a single electrode-electrode pair or brain region-brain region) (coherence x t timepoints)
        - burst_window: number of coherence values preceding an index coherence value over which to average in order to compare and determine if index coherence meets criteria for a burst 
        - percent_max: Proportion of the max coherence by which coherence must increase to be determined a burst (e.g. if max coherence for a time period is 0.8 and burst_threshold set to 0.5, then coherence would need to increase by 0.4 to be considered a burst)
    """

    #Identify Coherence Bursts/Spikes
    max_coh = np.max(coherenceArray) # max coherence over period of interest 
    burst_threshold = percent_max*max_coh #determine burst threshold
    # Calculate the rolling mean of the preceding 'window' values
    rolling_mean = coherenceArray.rolling(window=burst_window).mean()

    # Create a condition for when a burst starts
    start_burst_condition = coherenceArray > (rolling_mean + burst_threshold)

    # Create a condition for continuation of the burst (values > burst_threshold)
    continuation_condition = data > burst_threshold

    burst_count = 0
    total_auc = 0.0
    in_burst = False
    current_burst_auc = 0.0

    # Loop through the array to identify bursts
    for i in range(burst_window, len(coherenceArray)):
        if start_burst_condition[i] and not in_burst:
            # A new burst starts
            in_burst = True
            burst_count += 1
            current_burst_auc = data[i]  # Start the AUC with the first value of the burst
        elif in_burst:
            if continuation_condition[i]:
                # Continue accumulating AUC while in burst
                current_burst_auc += data[i]
            else:
                # End of burst, add the current burst's AUC to total AUC
                total_auc += current_burst_auc
                in_burst = False
    # If a burst is ongoing at the end of the loop, add its AUC
    if in_burst:
        total_auc += current_burst_auc

    return burst_count, total_auc





