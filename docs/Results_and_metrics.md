# Overview of `1_generate_results.py`

The script is designed to generate text based on input prefixes and suffixes using a pre-trained language model. It processes data, interacts with the model, and saves the generated results to an Excel file.

## Key Components

1. **Configuration Management** :

* Loads settings from a YAML configuration file (`config.yaml`), including dataset paths, model activation settings, and text generation parameters.

1. **Text Generation Function (`generate_text`)** :

* Iterates through input data to extract the last N words from a "Prefix" and the first N words from a "Suffix."
* Formats the input with special tokens to guide the model's generation process.
* Uses a `try-except` block for error handling during text generation.
* Saves the generated outputs along with original inputs to an Excel file, including a timestamp in the filename.

1. **Model Handling (`ModelHandler` Class)** :

* Manages the loading and usage of a pre-trained language model.
* Initializes with a specified model checkpoint and parameters, detecting available hardware (GPU/CPU).
* Includes methods to load the model and tokenizer from Hugging Face.
* Generates text by encoding input, applying an attention mask, and extracting relevant portions of the output based on defined markers.

## Models Involved

* **Hugging Face Transformer Model** :
* Utilizes `AutoModelForCausalLM` for causal language modeling tasks, enabling the generation of coherent and contextually appropriate text.
* Employs `AutoTokenizer` for converting text into token IDs for model input and decoding the output.

# Overview of `2_metrics.py`

This script evaluates the quality of generated text using two commonly used metrics in natural language processing: BLEU and ROUGE. It reads an Excel file containing generated texts, computes the metrics for each entry, and saves the results in new Excel files.

## Key Components

1. **Imports and NLTK Setup**:

   - **Libraries**:
     - Imports necessary libraries, including `pandas` for data handling and `nltk` for natural language processing.
     - Imports `sentence_bleu` and `SmoothingFunction` for computing the BLEU score.
     - Uses `rouge_scorer` from the `rouge_score` package for calculating ROUGE metrics.
   - **Resource Initialization**: Downloads NLTK resources for tokenization.
2. **Data Loading**:

   - Defines the path to the Excel file containing generated texts and loads it into a DataFrame.
3. **Metric Calculation Function (`compute_metrics`)**:

   - This function takes a reference text and a generated text as input and calculates:
     - **BLEU Score**: A measure of how closely the generated text matches the reference text, adjusted with a smoothing function to account for shorter texts.
     - **ROUGE-L Score**: Measures the overlap of the longest common subsequence between the reference and generated texts, capturing recall and precision.
4. **Metrics Computation**:

   - Initializes new columns in the DataFrame to store BLEU and ROUGE-L scores.
   - Iterates through the DataFrame, computing metrics for each generated text against its corresponding reference label.
   - Saves the computed metrics back into the DataFrame.
5. **Aggregation and Saving Results**:

   - Groups the DataFrame by a specified category (`Taxonomy`) and calculates the mean of BLEU and ROUGE-L scores for each group.
   - Saves both the detailed DataFrame (with metrics) and the aggregated results to new Excel files.
6. **Display of Results**:

   - Optionally prints the first few rows of the DataFrames to the console for quick inspection.
