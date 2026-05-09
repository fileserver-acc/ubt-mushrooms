from ultralytics import YOLO
import sys

model_name = sys.argv[1]
dataset_path = sys.argv[2]
epochs = sys.argv[3]

model = YOLO(model_name)
results = model.train(data=dataset_path, epochs=int(epochs))
