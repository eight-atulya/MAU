import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def output_as_csv(df: pd.DataFrame, session_id: str):
    try:
        csv_dir = os.path.join("outputs_csv")
        os.makedirs(csv_dir, exist_ok=True)
        csv_path = os.path.join(csv_dir, f"response_L002_session_{session_id}.csv")
        df.to_csv(csv_path, index=False)
        logger.info(f"CSV output saved to {csv_path}")
    except Exception as e:
        logger.error(f"Failed to output CSV: {e}")
