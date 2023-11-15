import configparser
from Components.logger import initialize_custom_logger

# logger initialization
logger = initialize_custom_logger()

def parseconfig(config_file):

    # Parses a configuration file to extract essential parameters like window size, contamination rate, and data path.
    # Returns these parameters as a tuple for further use.
    logger.info(f"Parsing configuration from {config_file}.")

    config = configparser.ConfigParser()
    config.read(config_file)

    # Converts the parameters to their respective data types (integers or floats) for further use.
    anomaly_detection_params = config['AnomalyConfig']
    num_samples = int(anomaly_detection_params.get('num_samples'))
    window_size = int(anomaly_detection_params.get('window_size'))
    contamination_rate = float(anomaly_detection_params.get('contamination_rate'))

    logger.info("Configuration parsed successfully.")

    return num_samples, window_size, contamination_rate