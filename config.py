import cv2
import multiprocessing

#DATA CONFIG
INPUT_SIZE = (150, 150, 1)
GROUND_TRUTH_SIZE = (150, 150, 3)

#PREPROCESSING CONFIG
INTERPOLATION_RESIZE = cv2.INTER_LANCZOS4
INTERPOLATION_ROTATE = cv2.INTER_LINEAR
NOISE_PERCENTAGE = 0.1
NOISE_MEAN = 0
NOISE_DEVIATION = 255 / 2
MAX_DEGREE_OF_LEFT_RIGHT_ROTATION = 30

#ML CONFIG
EPOCHS = 500
EARLY_STOPPING_PATIENTE_IN_EPOCHS = 100
TRAINING_BATCH_SIZE = 16
PREDICTION_BATCH_SIZE = 8

#OPTIMIZATIONS CONFIG
NR_OF_PROCESSES_PER_GENERATOR = multiprocessing.cpu_count()
