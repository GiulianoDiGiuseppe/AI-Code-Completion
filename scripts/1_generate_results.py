import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm


from src.AI_models.hugging_face_model import ModelHandler
from src.utils.logger_utils import logger
from src.utils.configuration_utils import load_yaml

config=load_yaml('config.yaml')
df_dataset = pd.read_excel(config['path_dataset_evaluation'])
model_handler = ModelHandler(config['model_activation'], config['models_configuration']['parameters'])

def generate_text(df_dataset, model_handler, config, output_folder):
    # Ensure tqdm is used with pandas
    tqdm.pandas()

    # Use tqdm for progress monitoring
    for index, row in tqdm(df_dataset.iterrows(), total=df_dataset.shape[0], desc="Generating Text"):
        try:
            # Split the prefix and suffix into words
            prefix_words = row['Prefix'].split()  # Split the prefix text into words
            suffix_words = row['Suffix'].split()  # Split the suffix text into words

            # Select the last N words from the Prefix and the first N words from the Suffix
            prefix_last_n_words = prefix_words[-config['padding_input_model']['word_prefix']:]  # Last N words from the Prefix
            suffix_first_n_words = suffix_words[:config['padding_input_model']['word_suffix']]  # First N words from the Suffix

            # Compose the final string with <fim_prefix>, <fim_suffix>, and <fim_middle>
            input_text = f"<fim_prefix> {' '.join(prefix_last_n_words)} <fim_suffix> {' '.join(suffix_first_n_words)} <fim_middle>"

            # Generate the text using the model
            generated_texts = model_handler.generate(input_text)
            for i in range(len(generated_texts)):
                df_dataset.at[index, 'Generated'+str(i)] = generated_texts[i]
        except Exception as e:
            print(f"Error generating text for index {index}: {e}")

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the DataFrame to a CSV file with the timestamp
    output_file = os.path.join(output_folder, f"generated_texts_{timestamp}.xlsx")
    df_dataset.to_excel(output_file, index=False)

    print(f"Generated texts saved to: {output_file}")

if __name__ == "__main__":
    generate_text(df_dataset, model_handler, config, "result")
