import logging
import os

def initialize_custom_logger():
    
    """
    Creates and returns a custom logger instance tailored for the anomaly detection system.
    
    Returns:
    - Custom logger object
    """
    # Create 'logs' directory if it doesn't exist
    logs_directory = 'logs'
    os.makedirs(logs_directory, exist_ok=True)

    custom_logger = logging.getLogger('custom_anomaly_detection_logger')
    custom_logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

    # Create a file handler for logging to a file in the 'logs' directory
    log_file_path = os.path.join(logs_directory, 'custom_anomaly_detection.log')
    file_handler = logging.FileHandler(log_file_path)

    # Define the logging format
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_formatter)

    # Add the file handler to the custom logger
    custom_logger.addHandler(file_handler)

    return custom_logger
