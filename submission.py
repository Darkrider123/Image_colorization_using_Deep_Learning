import os

import tensorflow as tf
from keras.models import Sequential
import cv2
import numpy as np
from tqdm import tqdm

from data_loader import load_samples
from data_loader import PredictionsGenerator
from paths import TEST_SAMPLES_DIR
from preprocessing import preprocess_image_predicting
from custom_metrics import CUSTOM_METRICS
from config import PREDICTION_BATCH_SIZE, GROUND_THRUTH_SIZE
from exeptions import GroundTruthSizeError

def compile_custom_objects():
    custom_objects = dict()

    for custom_metric in CUSTOM_METRICS:
        custom_objects[custom_metric.__name__] = custom_metric
    
    return custom_objects


def load_model(model_path):
    return tf.keras.models.load_model(model_path, custom_objects=compile_custom_objects())
    

def make_submission(model:Sequential, output_dir):
    inputs_as_batches = (
        PredictionsGenerator(
            samples_dir=TEST_SAMPLES_DIR,
            batch_size=PREDICTION_BATCH_SIZE,
            preprocessing_procedure=preprocess_image_predicting,
        )
    )


    raw_inputs_as_batches = (
        PredictionsGenerator(
            samples_dir=TEST_SAMPLES_DIR,
            batch_size=PREDICTION_BATCH_SIZE,
        )
    )


    ids = load_samples(TEST_SAMPLES_DIR)
    ids = [os.path.basename(elem) for elem in ids]

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


    id_idx = 0
    for inputs_as_batch, raw_inputs_as_batch in tqdm(zip(inputs_as_batches, raw_inputs_as_batches), desc="Predicting image batches", total=len(inputs_as_batches)):
        predictions = np.array(model(inputs_as_batch, training=False))

        if GROUND_THRUTH_SIZE[2] == 3:
            for prediction in predictions:
                cv2.imwrite(os.path.join(output_dir, ids[id_idx]), prediction)
                id_idx += 1
        elif GROUND_THRUTH_SIZE[2] == 2:
            for prediction, raw_input in zip(predictions, raw_inputs_as_batch):
                cv2.imwrite(os.path.join(output_dir, ids[id_idx]) , cv2.cvtColor(np.concatenate([raw_input, prediction], axis=2), cv2.COLOR_YCrCb2BGR))
                id_idx += 1
        else:
            raise GroundTruthSizeError(GROUND_THRUTH_SIZE)


def load_and_make_submission(model_path):
    model = load_model(model_path)
    make_submission(model, os.path.join(os.path.dirname(model_path), "Image Predictions"))

    
      