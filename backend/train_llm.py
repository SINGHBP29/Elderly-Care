from backend.remainder import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
import pandas as pd

def preprocess_data(data):
    """
    Preprocess the dataset for training.
    """
    # Assuming the dataset has a column named 'text' for training
    if 'text' not in data.columns:
        raise ValueError("Dataset must contain a 'text' column.")
    return data['text'].tolist()

def train_llm(data):
    """
    Train a language model on the provided data.
    """
    # Load a pre-trained tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")

    # Tokenize the data
    tokenized_data = tokenizer(data, truncation=True, padding=True, return_tensors="pt")

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10,
        save_total_limit=2,
        logging_dir="./logs",
    )

    # Define a Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_data,
    )

    # Train the model
    trainer.train()

    # Save the model
    model.save_pretrained("./trained_model")
    tokenizer.save_pretrained("./trained_model")
    print("Model training complete and saved!")

if __name__ == "__main__":
    # Load the dataset
    dataset = load_dataset()

    if dataset is not None:
        # Preprocess the data
        text_data = preprocess_data(dataset)

        # Train the LLM
        train_llm(text_data)