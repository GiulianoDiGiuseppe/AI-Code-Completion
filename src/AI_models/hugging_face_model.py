import yaml
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelHandler:
    def __init__(self, checkpoint: str, param_dict: dict):
        """
        Initialize the ModelHandler with a model checkpoint and parameters.

        :param checkpoint: The model checkpoint to load.
        :param param_dict: Dictionary containing model parameters.
        """
        self.checkpoint = checkpoint
        self.param_dict = param_dict
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Load the model and tokenizer
        self.model = self.load_model(checkpoint)
        self.tokenizer = self.load_tokenizer(checkpoint)

    def load_model(self, checkpoint: str):
        """Load the model from the specified checkpoint."""
        model = AutoModelForCausalLM.from_pretrained(checkpoint).to(self.device)
        return model

    def load_tokenizer(self, checkpoint: str):
        """Load the tokenizer from the specified checkpoint."""
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        return tokenizer

    def generate(self, input_text, skip_special_tokens: bool = False):
        # Encode the input text
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt').to(self.device)
        
        # Calculate the attention mask for the prefix
        attention_mask = torch.ones(input_ids.shape, device=self.device)  # Start with all ones
        if 'pad_token_id' in self.param_dict:
            attention_mask[input_ids == self.param_dict['pad_token_id']] = 0  # Set padding indices to 0 in the mask

        # Generate outputs using the model with the specified parameters
        outputs = self.model.generate(input_ids, pad_token_id=self.tokenizer.eos_token_id, attention_mask=attention_mask, **self.param_dict)

        generated_texts = []
        for output in outputs:
            # Find where the input ends
            input_len = input_ids.shape[-1]  # Get the length of the input (number of tokens in input)

            # Extract the newly generated tokens (after the input)
            new_tokens = output[input_len:].tolist()  # Convert the tensor to a list of token IDs
            
            # Decode only the new tokens
            generated_text = self.tokenizer.decode(new_tokens, skip_special_tokens=skip_special_tokens)
            generated_texts.append(generated_text)

        # Return the newly generated text
        return generated_texts
