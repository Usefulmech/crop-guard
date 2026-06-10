# =====================================================================
#  CROP GUARD FINE-TUNING PIPELINE: ViT ON PLANTVILLAGE (KAGGLE ENGINE)
# =====================================================================

# 1. Install required ecosystem dependencies directly into the kernel
# !pip install -q datasets transformers evaluate accelerate huggingface_hub

import os
import torch
import numpy as np
import evaluate
from PIL import Image
from datasets import Dataset, DatasetDict, Features, ClassLabel, Image as DatasetImage
from transformers import AutoImageProcessor, AutoModelForImageClassification, TrainingArguments, Trainer
from huggingface_hub import notebook_login

# --- STEP 1: HUGGING FACE AUTHENTICATION ---
# Execute this to sign into your HF account. Make sure to use a Write token!
print("[System] Initializing Hub Handshake...")
# notebook_login()

# --- STEP 2 & 3: LOAD DATASET VIA HUGGING FACE ---
import os
from datasets import load_dataset, DatasetDict

print("[System] Locating the exact nested folder in Kaggle...")

# Automatically hunt down the folder containing the 38 classes
base_kaggle_path = "/kaggle/input"
correct_data_dir = None

for root, dirs, files in os.walk(base_kaggle_path):
    # The real data folder will have lots of subdirectories (the 38 classes)
    if len(dirs) > 10:
        correct_data_dir = root
        break

if correct_data_dir is None:
    raise ValueError("Could not find the dataset folders. Make sure you clicked '+ Add Data' in Kaggle!")

print(f"[System] Found dataset correctly nested at: {correct_data_dir}")
print("[System] Loading PlantVillage dataset natively...")

# Load using the exact path we just found
raw_dataset = load_dataset("imagefolder", data_dir=correct_data_dir)

# Since the Kaggle dataset doesn't have a pre-made validation split, we split the "train" data ourselves:
dataset_splits = raw_dataset["train"].train_test_split(test_size=0.2, seed=42)
dataset = DatasetDict({
    "train": dataset_splits["train"],
    "val": dataset_splits["test"]
})

# Extract the automatically generated labels
class_names = dataset["train"].features["label"].names
num_labels = len(class_names)
id2label = {idx: name for idx, name in enumerate(class_names)}
label2id = {name: idx for idx, name in enumerate(class_names)}

print(f"✓ Successfully loaded {len(dataset['train'])} training images and {len(dataset['val'])} validation images across {num_labels} classes.")


# --- STEP 4: MODEL RESOLUTION & TENSOR TRANSFORMS ---
MODEL_ID = "google/vit-base-patch16-224"
image_processor = AutoImageProcessor.from_pretrained(MODEL_ID)

def transform_batch(batch):
    """Transforms raw image paths into network-ready image arrays on the fly."""
    images = [img.convert("RGB") for img in batch["image"]]
    inputs = image_processor(images=images, return_tensors="pt")
    inputs["label"] = batch["label"]
    return inputs

# Apply transforms across validation splits
dataset["train"].set_transform(transform_batch)
dataset["val"].set_transform(transform_batch)

# --- STEP 5: INITIALIZE NETWORK LAYERS WITH MAPPING HOOKS ---
print(f"[System] Loading backbone weights for {MODEL_ID}...")
model = AutoModelForImageClassification.from_pretrained(
    MODEL_ID,
    num_labels=num_labels,
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True # Safely overrides head classification layer
)

# --- STEP 6: CONFIGURE EVALUATION MATRIX & METRICS ---
metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# --- STEP 7: SET KAGGLE RUNTIME ARGUMENTS ---
training_args = TrainingArguments(
    output_dir="vit-plant-disease-advisor",
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_steps=100,
    num_train_epochs=3,
    learning_rate=2e-5,
    remove_unused_columns=False,
    report_to="none",
)

# --- STEP 8: PIPELINE RUNTIME EXECUTION ---
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["val"],
    compute_metrics=compute_metrics
)

print("[System] Training pipeline active. Executing forward optimization sweeps...")
trainer.train()

print("[System] Training cycle completed. Pushing definitive checkpoint artifacts to the Hub...")
# trainer.push_to_hub(commit_message="End of fine-tuning sweep on Kaggle PlantVillage data.")
print("🏁 Pipeline processing complete! Check your Hugging Face profile for the repository.")
