from Components.anomaly_detection import Isolation_Forest_Anomaly_Detection
from Components.logger import initialize_custom_logger
from Components.utils import data_stream_generate
from Components.config_parser import parseconfig

# Initialize logger
logger = initialize_custom_logger()

def main():
    """
    Main entry point for the anomaly detection process.

    This function initializes the Isolation Forest Anomaly Detection object,
    generates synthetic streaming data, and initiates the visualization of anomalies.

    Returns:
    None
    """

    try:
        # Parse configuration from config file
        num_samples, window_size, contamination_rate = parseconfig('config.ini')

        # Initialize anomaly detection object
        detector = Isolation_Forest_Anomaly_Detection(window_size=window_size, contamination=contamination_rate)
        # Generate a synthetic data stream
        data_stream = data_stream_generate(n_samples=num_samples)
        # Visualize anomalies in the data stream
        detector.visualizing(data_stream)
        # Log successful completion of anomaly detection
        logger.info("Anomaly detection process completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during anomaly detection: {e}", exc_info=True)

if __name__ == "__main__":
    main()