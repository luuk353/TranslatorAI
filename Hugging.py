from transformers import T5Tokenizer, T5ForConditionalGeneration

# Define the model name
model_name = "t5-base"

# Load the tokenizer and model from Hugging Face
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_text(input_text):
    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

    # Generate output using the model
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=4, early_stopping=True)

    # Decode the generated output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Example usage
input_text = "Translate English to French: you smell"
generated_text = generate_text(input_text)
print("Generated Text:", generated_text)
