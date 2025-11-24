
README - Typo Generator + Transformer-Based Auto-Correct Model
==============================================================

This project generates large typo datasets for Python, Java, and C keywords, processes
them into numerical form, and trains a character-level Transformer model to correct
typos automatically.

-----------------------------------------
1. PROJECT STRUCTURE
-----------------------------------------

The project consists of three major components:

1. Typo Generation
   - Creates realistic keyboard-based typos using operations like:
     swap, delete, replace with neighbor key, transpose, double char, etc.
   - Output: CSV files stored in /typo_datasets/

2. Dataset Processing
   - Builds vocabulary per language.
   - Encodes typo → correct pairs into numerical arrays.
   - Saves .npy files in /processed/

3. Transformer Model Training
   - Trains a multi-layer character Transformer for each language.
   - Saves model weights + config + vocabulary.

-----------------------------------------
2. HOW TO RUN THE PROJECT
-----------------------------------------

Make sure you have Python 3.8+ and install dependencies:

```
pip install numpy pandas tensorflow scikit-learn keras
```

-----------------------------------------
A. Generate Typo Datasets
-----------------------------------------

Run the code block that contains:

```
LANG_KEYWORDS = { ... }
generate_typos_for_language(...)
```

This will output files like:

```
typo_datasets/typo_data_python.csv
typo_datasets/typo_data_java.csv
typo_datasets/typo_data_c.csv
```

-----------------------------------------
B. Process the CSVs Into Encoded Arrays
-----------------------------------------

Run the second part:

```
processed/python_X.npy
processed/python_Yin.npy
processed/python_Yout.npy
...
```

Each language creates:

- X.npy → encoder input
- Yin.npy → decoder input
- Yout.npy → decoder expected output
- *_stoi.npy / *_itos.npy → vocabulary mappings

-----------------------------------------
C. Train the Transformer Model
-----------------------------------------

Run the "TRAIN ONE LANGUAGE" section.

It will:

- Load typo CSV
- Build vocab
- Encode full dataset
- Train a Transformer for 30 epochs
- Save:

```
models/typo_model_python/model.weights.h5
models/typo_model_python/config.json
models/typo_model_python/model_settings.json
models/typo_model_python/metadata.json
```

Same for Java and C.

-----------------------------------------
3. HOW TO LOAD THE TRAINED MODEL
-----------------------------------------

You will need:

- model_settings.json → vocab + max_len
- config.json → transformer architecture
- model.weights.h5 → weights

Example:

```
with open("config.json") as f:
    config = json.load(f)

model = CharacterTransformer.from_config(config)
model.build(config["build_config"]["input_shape"])
model.load_weights("model.weights.h5")
```

-----------------------------------------
4. HOW TO PERFORM INFERENCE
-----------------------------------------

Steps:

1. Load char2idx and idx2char from model_settings.json
2. Encode typo using start/end tokens
3. Run Transformer (greedy decoding)
4. Convert output index sequence to characters

-----------------------------------------
5. IMPORTANT NOTES
-----------------------------------------

- MAX_LEN is auto-calculated based on longest token.
- Each language has an independent vocabulary.
- The typo generator produces between **30–600 typos per word** based on length.
- Training time depends on dataset size and GPU availability.

-----------------------------------------
6. OUTPUT DIRECTORIES SUMMARY
-----------------------------------------

/typo_datasets/
    typo_data_python.csv
    typo_data_java.csv
    typo_data_c.csv

/processed/
    python_X.npy, python_Yin.npy, python_Yout.npy, python_stoi.npy ...

/models/
    typo_model_python/
        model.weights.h5
        config.json
        model_settings.json
        metadata.json