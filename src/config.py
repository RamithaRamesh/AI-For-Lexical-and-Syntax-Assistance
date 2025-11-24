# src/config.py
import os
from pathlib import Path
import random
import numpy as np
import tensorflow as tf

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

BASE_DIR = Path.cwd()

DATASET_DIR = BASE_DIR / "datasets"
PROCESSED_DIR = BASE_DIR / "processed"
MODEL_DIR = BASE_DIR / "models"

DATASET_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

MAX_LEN = 32