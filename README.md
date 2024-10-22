
# Setup

## Step 1: Create a Virtual Environment with Python 3.12

**PowerShell:**

```powershell
# Navigate to your project directory
cd path\to\your\project

# Create a virtual environment
python -m venv env

# Activate the environment
.\env\Scripts\Activate.ps1
```

**Command Prompt (CMD):**

```cmd
REM Create a virtual environment
python -m venv env

REM Activate the environment
.\env\Scripts\activate.bat
```

**macOS Terminal:**

```bash
# Navigate to your project directory
cd path/to/your/project

# Create a virtual environment
python3.12 -m venv env

# Activate the environment
source env/bin/activate
```

## Step 2: Install the Requirements

To install the requirements, make sure you're within the activated virtual environment and have a `requirements.txt` file listing all your dependencies.

```bash
# Install the dependencies listed in the requirements.txt file
pip install -r requirements.txt
```

## Step 3: Configure the `config.yaml` File

You need to edit the `config.yaml` file to include your dataset and adjust settings according to your needs. Here is an example configuration:

```yaml
dataset_git : 
  - https://github.com/GiulianoDiGiuseppe/Financial-Update
  - https://github.com/GiulianoDiGiuseppe/Trenitalia-api-search
  - https://github.com/GiulianoDiGiuseppe/Dasboard-with-DB-from-Notion
folder_save_dataset : ['data' ,'repositories']
programming_language : 
  python :
    triggers : ['await', 'assert', 'raise', 'del', 'lambda', 'yield', 'return','print','logger',
            'logging','while', 'for', 'if', 'elif', 'else', 'global', 
            'or', 'is', 'with', 'except', '.', '+', '-', '*', '%', ".",
             '|', '^', '==', '!=', '<=', '>=', '+=', '-=', '=', '<', '>', 
            ';', ',', '[', '(', '{', '~']
    extensions : ['.py']
    comment : '#'
    comment_multiline : ['"""','"""']
    comment_singleline : ['#']
```

Replace `path/to/your/dataset` and `path/to/output/directory` with the actual paths on your system. Adjust `dataset_git`, `folder_save_dataset`, and their values according to the specific requirements of your scripts.

## Step 4: Creation Dataset

The creation of dataset is an **ETL pipeline** designed to extract, transform, and load Python code from Git repositories. The pipeline processes repositories to create a dataset of code completions, splitting code into `prefix`, `middle`, and `suffix` for tasks like code completion or machine learning.

After modifying the `config.yaml`, run the data generation scripts in the `scripts` folder:

```bash
python -m scripts.create_dataset
```

The data to be collected is obtained from the following repositories:

- YouTube-Video-Classification-on-Twitter-and-Homeworks
- Diode
- HASHCODE-2020-Qualification-Round

### Key Steps in the Pipeline

1. **Extraction**: Clone repositories from the URLs specified in the configuration file.

   - 
   - **`library`**: Contains all import statements.
   - **`functions`**: A dictionary with function names as keys and the corresponding function code as values.
   - **`classes`**: A dictionary where each key is a class name. Each class includes:

     - **`init`**: The code for the constructor `__init__`.
     - **`methods`**: A dictionary containing method names as keys and their corresponding code.
   - **`global`**: Contains the global code that is neither part of a function nor a class.
2. **Transformation**: Parse Python files to extract functions, classes, and global variables, and build input-output pairs for code completion.
3. **Dataset Creation**: Split code using predefined triggers into three parts:

   - **Prefix**: Code before the cursor
   - **Middle**: Code to be completed (up to the end of the current line, not beyond).
   - **Suffix**: Remaining code after the cursor.

   The `middle` section is selected based on specific **trigger characters** and always spans up to the end of the line where the trigger is found. If no valid trigger is found in a line, it will be skipped. Note that **empty lines are never considered** as a trigger.

   Example **trigger characters**:

   - `=`, `(`, `:`, `.`, `,`, `+`, `-`, `*`, `/`

### Dataset Selection

The process generates a large number of code completion samples. For example, running the pipeline on **three moderately-sized repositories** resulted in  **more than 1000 samples** . To ensure the dataset is manageable, a subset of the generated samples will be **manually selected** based on relevance, diversity, and quality. This allows for fine-tuning of the dataset for the specific task while avoiding redundancy or overly similar samples.

### Custom "Taxonomy" of CODE COMPLETION

This document outlines a comprehensive taxonomy for code completions, categorizing different types of coding tasks into a **General** classification and a more detailed **Specific** classification. This taxonomy is designed to help developers prioritize and select tasks based on their complexity and requirements.

| **Code Completion Type**        | **Abbreviation** | **Description**                                                                     | **Complexity Level (1-5)**                                        | **Examples**                                                                                       |
| ------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Function Implementation**     | FIM                    | Completing various types of functions, including standard libraries and custom functions. | 1-2 for well-known libraries<br /> 3-4 for custom functions             | Implementing a sorting function, completing `math.sqrt()`calls.                                        |
| **Control Structures**          | CST                    | Completing loops (for, while) and conditionals (if, switch).                              | 1-2 for simple structures<br /> 3-4 for writing from scratch            | Completing a `for`loop to iterate over a list, building a conditional statement.                       |
| **Error Handling**              | EHC                    | Implementing exception handling mechanisms to manage errors.                              | 2-4 for basic to advanced error handling                                | Using `try`/`except`to catch exceptions, creating custom error classes.                              |
| **Data Management**             | DMT                    | Working with data structures (lists, dictionaries) and APIs.                              | 2-5 for simple data manipulation<br /> 4-5 for complex API integrations | Manipulating a JSON response from an API, implementing a stack or queue.                                 |
| **Documentation & Comments**    | DCC                    | Adding documentation and comments to improve code readability.                            | 1 for basic comments<br /> 2-3 for comprehensive documentation          | Writing docstrings for functions, adding inline comments explaining logic.                               |
| **Testing & Debugging**         | TDB                    | Writing tests (unit, integration) and debugging existing code.                            | 3-4 for writing tests<br /> 4-5 for advanced debugging techniques       | Writing unit tests using `unittest`or `pytest`, using a debugger to trace errors.                    |
| **Library Declaration & Usage** | LDU                    | Declaring and utilizing specific custom libraries and popular libraries in projects.      | 2-5 for well-known libraries<br /> 4-5 for custom library integration   | Importing `numpy`for numerical calculations, integrating a custom logging library for tracking events. |

This taxonomy can help determine the composition of the dataset and provide insights into which models excel in specific areas. By categorizing code completion types, we can identify patterns and strengths in the underlying data, enabling more targeted training and optimization of models for various tasks.

## Step 5 : Configuring Model Parameters

You can configure various model parameters by editing the `config.yaml` file. This allows you to customize the behavior of the code completion model.

```yaml
model_activation : 'bigcode/tiny_starcoder_py'
models_configuration : 
  parameters :
    max_new_tokens: 12  # Maximum number of new tokens to generate in the output.
    min_new_tokens: 2   # Minimum number of new tokens to generate in the output.
    temperature: 0.3    # Controls the randomness of predictions. Lower values make the output more deterministic, while higher values increase randomness.
    top_k: 50           # Limits the sampling pool to the top K most likely next tokens. This reduces the potential randomness in outputs.
    top_p: 0.95         # Implements nucleus sampling. The model considers only the smallest set of tokens whose cumulative probability exceeds p (0.95 in this case).
    repetition_penalty: 1.0  # Penalizes repeated tokens in the output. A value greater than 1 discourages repetition, while values less than 1 encourage it.
    num_return_sequences: 1  # Number of distinct sequences to generate from the same input. Set to 1 for a single output.
    do_sample: true      # Enables sampling. When set to false, the model will use greedy decoding, always choosing the most likely next token.
    early_stopping: true  # Stops the generation process when the model reaches an end-of-sequence token (EOS) if enabled.
    length_penalty: 0.5   # Adjusts the likelihood of generating longer sequences. Values greater than 1 encourage shorter sequences, and values less than 1 encourage longer sequences.
    pad_token_id: 0     # Token ID for the padding token. Replace null with the actual ID if padding is needed.
    eos_token_id: null    # Token ID for the end-of-sequence token. Replace null with the actual ID if needed for proper termination.
    max_time: null        # Maximum time allowed for generating a response. Replace null with an actual time value if time limits are required.
    num_beams: 5         # Number of beams for beam search, which is a technique for generating multiple outputs by exploring the most promising sequences.
    remove_invalid_values: true  # If true, it removes any invalid tokens or sequences from the output, ensuring valid outputs.
        repetition_penalty_range: null  # Defines a range for the repetition penalty. Replace null with a specific value if needed to fine-tune the repetition control.

```

### Running the Code

To execute the code for generating code completion results, use the following command in your terminal:

```bash
python -m src.code_completion
```

#### Output

Upon running the command, a folder named `experiments` will be created in the project directory. This folder will contain the following files:

* **`parameters.yaml`** : A YAML file that includes the parameters used for the code completion model.
* **`results.xlsx`** : An Excel file that contains the results of the code completion tasks. The structure of this file will include the following columns:
  * **`prefix`** : The input text that precedes the code completion.
  * **`suffix`** : The context that follows the code completion.
  * **`label`** : The expected output or correct completion for the given input.
  * **`result`** : The output generated by the model for the corresponding `prefix` and `suffix`.

Ensure you have the necessary dependencies installed and your environment set up correctly before running the code.

# Model Evaluation

This section outlines the proposed automatic metrics for evaluating the quality of the code completion model. The goal is to assess the model's performance and identify which metrics correlate best with human judgment.

## Proposed Metrics

1. **Exact Match (EM)**: This metric calculates the percentage of instances where the model's output exactly matches the expected output (label). It serves as a straightforward indicator of accuracy.
2. **Character F-score (CHRF)**: This metric evaluates the model's output by comparing n-grams of characters between the predicted and expected results. It is particularly useful for measuring quality in natural language tasks.
3. **BLEU Score**: This metric is commonly used for evaluating machine translation quality. It measures the precision of n-grams in the predicted output against the reference output. A higher BLEU score indicates better alignment with the reference.
4. **ROUGE Score**: This set of metrics is used for evaluating summarization tasks. It measures the overlap between the predicted output and reference output in terms of n-grams, helping to assess the completeness and relevance of the model’s predictions.

## Correlating Metrics with Human Judgment

To determine which of the proposed metrics aligns best with human judgment, follow these steps:

1. **Compute Metrics**: Implement the calculations for the Exact Match, CHRF, and the additional metrics (e.g., BLEU and ROUGE) on your model’s predictions.
2. **Human Evaluation**: Gather a sample of model outputs and evaluate them based on your judgment. Score them on a predefined scale (e.g., 1 to 5) to quantify your assessment.
3. **Correlation Analysis**: Use statistical methods (e.g., Pearson or Spearman correlation) to analyze the correlation between the automatic metrics and your human evaluations.

## Computing Metrics

To compute the proposed metrics, you can use libraries like `nltk`, `sacrebleu`, or `rouge-score`. Below is an example code snippet to get you started:

```python
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
import numpy as np

# Example function to compute metrics
def compute_metrics(predicted, reference):
    # Exact Match
    exact_match = int(predicted == reference)

    # CHRF can be computed using an appropriate library (not shown here)
    # Example for BLEU score
    bleu_score = sentence_bleu([reference.split()], predicted.split())
  
    # Example for ROUGE score
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_scores = scorer.score(reference, predicted)

    return {
        "Exact Match": exact_match,
        "BLEU Score": bleu_score,
        "ROUGE Scores": rouge_scores,
    }
```
