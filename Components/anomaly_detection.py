import matplotlib.pyplot as plt
import numpy as np
from river.drift import ADWIN
from sklearn.ensemble import IsolationForest
from Components.utils import create_results_folder, save_anomalies_to_csv
from Components.logger import initialize_custom_logger

# logger initialization
logger = initialize_custom_logger()

class Isolation_Forest_Anomaly_Detection:
    def __init__(self, window_size, contamination):
        """
        Initialize the Isolation Forest Anomaly Detection object.

        Parameters:
        - window_size: Size of the rolling window for analysis.
        - contamination: Proportion of outliers to expect in the data.

        Initializes the Isolation Forest model, necessary variables for anomaly detection, and logger.
        """
        self.window_size = window_size
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination, random_state=68)
        self.session_num = 1
        # Store for identified anomalies
        self.anomalies = []  
        self.plot = None
        self.adwin = ADWIN()

        # Logger initialization within the class
        # Implementing the existing logger
        self.logger = logger  

        self.logger.info("Isolation Forest Anomaly Detection object initialized.")

    def rolling_window(self, data):
        """
        Generates a rolling window of data for analysis.

        Parameters:
        - data: The data stream for analysis.

        Yields:
        - i: Index of the rolling window.
        - data[i:i+self.window_size]: Windowed subset of the data.
        """
        for i in range(len(data) - self.window_size + 1):
            yield i, data[i:i+self.window_size]

    def visualizing(self, data_stream):
        """
        Visualizes anomalies in a given data stream using Isolation Forest.

        Parameters:
        - data_stream: The input data stream for anomaly detection and visualization.

        Performs anomaly detection, concept drift detection, and visualization using Isolation Forest.
        """
        self.plot = plt.figure(figsize=(10, 6))
        # Turn on interactive mode
        plt.ion()  

        for i, window_data in self.rolling_window(data_stream):
            if len(window_data) < self.window_size or not plt.fignum_exists(self.plot.number):
                break

            # Execute anomaly detection visualization using the Isolation Forest model.
            try:
                self.logger.info("Performing anomaly detection visualization.")
                self.model.fit(window_data)
                anomaly_scores = self.model.decision_function(window_data)
                anomaly_labels = self.model.predict(window_data)
         
                anomalies = np.where(anomaly_labels == -1)[0]

                # Extend anomaly records and display total anomalies detected and update the count                       
                if anomalies.any():
                    self.anomalies.extend([(anomaly + i * self.window_size, window_data[anomaly][0], -anomaly_scores[anomaly]) for anomaly in anomalies])
                    print(f"Total anomalies found so far: {len(self.anomalies)}")

                # Check for concept drift based on number of anomalies detected
                if self.adwin.update(len(anomalies)):  
                    self.logger.info("Concept drift detected - updating model")
                    print("Concept drift detected - updating model")
                    # Update the model
                    self.model = IsolationForest(contamination=self.contamination, random_state=68)  

                plt.clf()

                # Plot the data window and scatter anomalies based on the Isolation Forest model's anomaly scores.
                plt.plot(range((i + 1) * self.window_size - self.window_size, (i + 1) * self.window_size),
                         window_data[-self.window_size:], color='black')
                plt.scatter(range((i + 1) * self.window_size - self.window_size, (i + 1) * self.window_size),
                            window_data[-self.window_size:], c=-anomaly_scores[-self.window_size:], cmap='coolwarm', marker='o')
                
                # Set title, labels, color range, and display anomalies
                plt.title('Anomaly Detection in Data Stream')
                plt.xlabel('Index')
                plt.ylabel('Value')
                plt.ylim(-4, 4)
                plt.colorbar(label='Score: Anomaly')
                plt.tight_layout()
                plt.pause(0.1)              # Pause to show the updated plot for 0.1 seconds.

            except Exception as e:
                self.logger.error(f"Error occurred: {e}", exc_info=True)
                
        # Deactivate interactive mode
        plt.ioff()  
        # Display the plot until manually closed
        plt.show(block=True)  

        # Save anomalies to CSV at the end of visualization
        create_results_folder()
        save_anomalies_to_csv(self.anomalies,self.session_num)

        # Setup for the subsequent session
        self.session_num += 1  