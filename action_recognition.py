# action_recognition.py

import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.utils import to_categorical
from datetime import datetime

class ActionRecognitionModel:
    def __init__(self, data_path='MP_Data', actions=['hello', 'thanks', 'iloveyou'],
                 no_sequences=30, sequence_length=30):
        self.data_path = data_path
        self.actions = np.array(actions)
        self.no_sequences = no_sequences
        self.sequence_length = sequence_length
        self.label_map = {label: num for num, label in enumerate(actions)}
        self.model = None

#loads data from files & organizes into sequences and corresponding labels, converts them into Numpy arrays 
    def _load_data(self):
        sequences, labels = [], []

        for action in self.actions:
            for sequence in range(self.no_sequences):
                window = []
                for frame_num in range(self.sequence_length):
                    res = np.load(os.path.join(self.data_path, action, str(sequence), "{}.npy".format(frame_num)))
                    window.append(res)
                sequences.append(window)
                labels.append(self.label_map[action])

        X = np.array(sequences)
        y = to_categorical(labels).astype(int)

        return X, y
#creates a sequential model with an LSTM layer followed by a dense output layer ( (RNN) layer known for its ability to capture long-term dependencies in sequential data.)
    def _create_model(self):
        model = Sequential() #  sequential neural network model(relu model to learn complex relationships and patterns in the data.)
        model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 1662))) # 30 time steps (frames) and each time step contains 1662 features
        model.add(LSTM(128, return_sequences=True, activation='relu'))#Increasing the units in this layer can allow the model to capture more complex temporal patterns.
        model.add(LSTM(64, return_sequences=False, activation='relu')) #his layer is commonly used as the final LSTM layer in a sequence prediction task
        model.add(Dense(64, activation='relu')) #Dense layers are fully connected layers where each neuron is connected to every neuron in the previous and next layers.
        model.add(Dense(32, activation='relu'))# Additional dense layers can further extract and learn complex features from the data.
        model.add(Dense(self.actions.shape[0], activation='softmax')) #Softmax activation is used for multi-class classification tasks

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#Compiles the model with the Adam optimizer, categorical cross-entropy loss (suitable for multi-class classification), and accuracy as the metric for evaluation during training.
        return model
#Trains the model using a specified number of epochs (iterations through all training samples)
    def train_model(self, epochs=2000):
        X, y = self._load_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

        self.model = self._create_model()

        log_dir = os.path.join('Logs', datetime.now().strftime("%Y%m%d-%H%M%S"))
        tb_callback = TensorBoard(log_dir=log_dir)

        try:
            self.model.fit(X_train, y_train, epochs=epochs, callbacks=[tb_callback], validation_data=(X_test, y_test))
        except KeyboardInterrupt:
            print("\nTraining interrupted. Saving current model...")
            self.model.save('action.h5')
            print("Model saved.")

if __name__ == "__main__":
    # Example usage
    model_instance = ActionRecognitionModel()
    model_instance.train_model()
