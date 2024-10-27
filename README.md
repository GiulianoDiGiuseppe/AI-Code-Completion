
# WORKFLOW

![Alt text](./images/Workflow.svg)

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
python -m scripts.0_create_dataset
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

## Step 5: Data Filter and Classification

The process generates a large number of code completion samples. For example, running the pipeline on **three moderately-sized repositories** resulted in  **more than 1000 samples** . To ensure the dataset is manageable, a subset of the generated samples will be **manually selected** based on relevance, diversity, and quality. This allows for fine-tuning of the dataset for the specific task while avoiding redundancy or overly similar samples.

In addition to filtering, it is essential to **assign a taxonomy type** to each completion sample based on its nature. This assignment helps to categorize the completions according to their functionality, allowing for better analysis and understanding of the dataset.

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

This taxonomy can help determine the composition of the dataset and provide insights into which models excel in specific areas. By categorizing code completion types and assigning the corresponding taxonomy to each completion sample, we can identify patterns and strengths in the underlying data, enabling more targeted training and optimization of models for various tasks.

### Assigning Human Scores

For each generated completion, a **HumanScoreX** will be assigned to evaluate its quality on a scale from  **1 to 5** , where:

* **1** : Poor quality - does not meet basic requirements.
* **2** : Fair quality - partially meets requirements but has significant issues.
* **3** : Good quality - meets requirements but may have minor flaws.
* **4** : Very good quality - mostly meets requirements with few issues.
* **5** : Excellent quality - fully meets all requirements and expectations.

This scoring will help in the evaluation process of the model and provide insights into areas that require improvement.

## Step 6 : Configuring Model Parameters

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
python -m src.generate_results
```

#### Output

Upon running the command, a folder named `experiments` will be created in the project directory. This folder will contain the following files:

* **`parameters.yaml`** : A YAML file that includes the parameters used for the code completion model.
* **`results.xlsx`** : An Excel file that contains the results of the code completion tasks. The structure of this file will include the following columns:

  * **`prefix`** : The input text that precedes the code completion.
  * **`suffix`** : The context that follows the code completion.
  * **`label`** : The expected output or correct completion for the given input.
  * **`taxonomy`** : The assigned category for the type of code completion, based on the custom taxonomy defined for this project.
  * **`GeneratedX`** : Columns that will store the generated completions from the model, where **`X`** ranges from 1 to the total number of selected samples generated by the model.
  * **`HumanScoreX`** : Columns that will store the quality score assigned to each generated completion, reflecting its assessed quality based on the scale outlined earlier.

Ensure you have the necessary dependencies installed and your environment set up correctly before running the code.

# Step 7: Model Evaluation

This section outlines the proposed automatic metrics for evaluating the quality of the code completion model. The goal is to assess the model's performance and identify which metrics correlate best with human judgment.

## Correlating Metrics with Human Judgment

To determine which of the proposed metrics aligns best with human judgment, follow these steps:

1. **Compute Metrics** : Implement calculations for **BLEU** and **ROUGE** on your model’s predictions. These metrics will help quantify the similarity between the generated outputs and the reference texts.

* **BLEU** : Measures n-gram overlap to evaluate the accuracy of model predictions.
* **ROUGE** : Assesses recall by comparing n-grams and longest common subsequences.

2. **Human Evaluation** : Gather a sample of model outputs and evaluate them based on your judgment. Score them on a predefined scale (e.g., 1 to 5) to quantify your assessment of their quality.

### Running the Code

To execute the code for generating code completion results, use the following command in your terminal:

```bash
python -m src.2_metrics
```

## Results

The matrix displays the meancompletion mean_HumanScore1, BLEU, and ROUGE-L metrics for different categories (Taxonomy), calculated by comparing the model-generated text with reference texts; the values are derived by averaging the scores of all samples within each category.

| **Taxonomy** | **mean_HumanScore1** | **mean_BLEU** | **mean_ROUGE-L** | **count** |
| ------------------ | -------------------------- | ------------------- | ---------------------- | --------------- |
| CST                | 3.700000                   | 0.184298            | 0.334092               | 10              |
| DMT                | 5.000000                   | 0.285744            | 0.000000               | 1               |
| FIM                | 2.333333                   | 0.170557            | 0.315785               | 15              |
| LDU                | 2.000000                   | 0.067566            | 0.291205               | 4               |

# Simplifications

* **Focus Area** :The analysis targeted Python code from a private repository with notable clarity issues.
* **Lengthy Prompts** : Overly long prompts were ineffective for generating meaningful completions.
* **Trigger Limitations** : Triggers used were mainly suited for single-line completions, restricting their effectiveness for full functions.
* **Model Tested** : Only one model was tested,  **tiny_starcoder_py** .

# Conclusion

* Higher HumanScores **correlate** with better BLEU scores, particularly for **CST **.
* The positive trend in HumanScores aligns with increased ROUGE-L metrics, especially for  **CST** .
* **DMT** 's metrics are based on a single sample, limiting reliability. While a greater sample count in **FIM** and **CST** provides more reliable insights into model performance.
* **CST** and **DMT** shows balanced metrics, indicating consistent code quality.

## Future Work

In future work, we will focus on improving the dataset creation with particular emphasis on the following aspects:

* **More Useful and Selected Triggers** : Optimize the activation mechanisms to ensure a more effective and relevant data collection process.
* **Management of Docstring Generation** : Experiment with methods for automatic docstring generation, acknowledging that this evaluation may be more complex.
* **Multi-line Code Completion** : Test and enhance capabilities for completing multi-line code blocks.
* **Model Comparison** : Experiment with various models while increasing the amount of text sent to analyze and compare their performance.
* **Support for Other Programming Languages** : Extend testing and application of the model to additional programming languages.
* **Exploring Optimal Hyperparameters** : Investigate and determine the best hyperparameters for improved model performance.
* **Model for Code Taxonomy Classification** : Develop a model to classify the taxonomy of code to identify which areas are worth improving and which are less critical.
