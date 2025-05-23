import pandas as pd
from scipy import signal
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

channels = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

def extract_bands(df, channels=channels, fs=128, window_size=32):
    logger.info("Starting preprocessing...")
    try:
        missing_cols = [col for col in channels if col not in df.columns]
        if missing_cols:
            logger.error(f"Missing columns: {missing_cols}")
            raise ValueError(f"Missing columns: {missing_cols}")
        
        bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 12),
            'beta': (12, 30)
        }
        band_powers = {band: [] for band in bands}
        timestamps = []
        window_indices = []
        eye_states = []

        logger.info(f"Processing {len(df)} rows in windows of {window_size} samples")
        for start in range(0, len(df), window_size):
            end = min(start + window_size, len(df))
            window = df.iloc[start:end]
            if len(window) < window_size // 2:
                logger.warning(f"Skipping partial window at index {start}")
                continue
            window_powers = {band: [] for band in bands}
            for channel in channels:
                signal_data = window[channel].values
                freqs, psd = signal.welch(signal_data, fs=fs, nperseg=min(window_size, len(signal_data)))
                for band, (low, high) in bands.items():
                    idx = (freqs >= low) & (freqs <= high)
                    power = np.mean(psd[idx]) if idx.any() else 0
                    window_powers[band].append(power)
            for band in bands:
                band_powers[band].append(np.mean(window_powers[band]))
            timestamps.append(pd.Timestamp('2025-05-22 10:53:00') + pd.Timedelta(seconds=start/fs))
            window_indices.append(start // window_size + 1)
            eye_states.append(window['eye_state'].mode().iloc[0] if 'eye_state' in window else 0)

        result = pd.DataFrame({
            'id': window_indices,
            'timestamp': timestamps,
            'alpha': band_powers['alpha'],
            'beta': band_powers['beta'],
            'theta': band_powers['theta'],
            'delta': band_powers['delta'],
            'user_id': 'emotiv_user_20250522'
        })
        eye_state_path = '~/ritual_abacus/data/emotiv_eye_state_20250522.csv'
        eye_state_df = pd.DataFrame({
            'id': window_indices,
            'timestamp': timestamps,
            'eye_state': eye_states
        })
        eye_state_df.to_csv(eye_state_path, index=False)
        logger.info(f"Saved eye_state data to {eye_state_path}")
        return result

    except Exception as e:
        logger.error(f"Preprocessing failed: {str(e)}")
        raise

input_file = '~/ritual_abacus/data/eeg_headset_emotiv.csv'
output_file = '~/ritual_abacus/data/processed_emotiv_eeg_data_20250522.csv'

try:
    logger.info(f"Loading input file: {input_file}")
    df = pd.read_csv(input_file)
    logger.info(f"Input data shape: {df.shape}")
    processed_df = extract_bands(df)
    processed_df.to_csv(output_file, index=False)
    logger.info(f"Processed data saved to {output_file}")
    logger.info("Columns: %s", processed_df.columns.tolist())
    logger.info("Sample Data:\n%s", processed_df.head())
except Exception as e:
    logger.error(f"Script execution failed: {str(e)}")
    raise
