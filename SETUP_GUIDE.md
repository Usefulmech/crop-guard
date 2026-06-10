# Crop Guard: End-to-End Setup Guide

This guide covers everything you need from local UI testing to preparing your dataset, fine-tuning your vision model, and deploying to Hugging Face Spaces.

## 1. Local UI Testing & Virtual Environment

You should absolutely use a Virtual Environment (venv) when testing locally to avoid conflicting with other Python projects on your machine.

**To test the UI locally, follow these steps in your terminal (PowerShell):**

1. **Create the virtual environment:**
   ```powershell
   python -m venv venv
   ```
2. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\activate
   ```
3. **Install the dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```powershell
   python app.py
   ```
   > [!TIP]
   > The first time you run `app.py`, it will download the base ViT model (~340MB) and the Qwen LLM weights (~4.3GB). If you *only* want to test the UI layout without waiting for the massive LLM download, open `app.py`, find the `hf_hub_download` line for Qwen, and temporarily comment out the `try...except` block setting `llm = None`. 

## 2. Dataset Preparation (PlantVillage)

To make Crop Guard accurate for diseases, you need to fine-tune it on the PlantVillage dataset.

1. **Get the Dataset (The Kaggle Way)**: You do **not** need to download this to your local computer! Since you are using Kaggle Notebooks, you have two extremely easy options to get the data directly into your environment:
   
   - **Option A (Kaggle Native)**: In your Kaggle Notebook, click **"Add Data"** on the right-side panel. Search for `PlantVillage` and click `+` to add it. It will instantly appear in your notebook's `/kaggle/input/` directory!
   - **Option B (Hugging Face via Code)**: You can download it directly inside your Python code using the `datasets` library from the Hugging Face hub (e.g., `nateraw/plant-village`).

2. **Structure**: If you use Option A (Kaggle Native), the folders will already be arranged. If you use Option B, the `load_dataset("nateraw/plant-village")` command handles the structure for you automatically.

3. **Mapping**: Keep track of the exact folder names or class labels. These 38 names will become the keys for the `LABEL_TRANSLATOR` dictionary inside your `app.py`!

## 3. Fine-Tuning the Vision Model

Since you only have a few days for the hackathon, the fastest way to fine-tune the `google/vit-base-patch16-224` model is by using **Hugging Face AutoTrain** or a simple Google Colab notebook.

**Option A: The No-Code Way (AutoTrain)**
1. Go to [Hugging Face AutoTrain](https://huggingface.co/autotrain).
2. Create a new Image Classification project.
3. Upload your PlantVillage dataset.
4. Select `google/vit-base-patch16-224` as the base model.
5. Train and push directly to your Hugging Face Hub profile!

**Option B: Python / Kaggle Notebook**
If you want to script it, use the `transformers` library inside a Kaggle Notebook (which gives you free access to P100/T4 GPUs!). Here is a high-level snippet of what the training script looks like:
```python
from transformers import AutoImageProcessor, AutoModelForImageClassification, Trainer, TrainingArguments
from datasets import load_dataset

# 1. Load dataset
dataset = load_dataset("imagefolder", data_dir="path/to/dataset")

# 2. Load processor & base model
processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = AutoModelForImageClassification.from_pretrained(
    "google/vit-base-patch16-224", 
    num_labels=38, 
    ignore_mismatched_sizes=True
)

# 3. Define training arguments & Trainer
training_args = TrainingArguments(
    output_dir="./vit-plantvillage",
    per_device_train_batch_size=16,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=3,
    push_to_hub=True,
    hub_model_id="your-username/cropguard-vit"
)

trainer = Trainer(model=model, args=training_args, train_dataset=dataset["train"], eval_dataset=dataset["val"])
trainer.train()
```

## 4. Deployment Steps (Hugging Face Spaces)

Once your UI is tested and your model is fine-tuned, you are ready to deploy.

1. **Create the Space**: Log into Hugging Face, click your profile picture, and select **New Space**.
2. **Configure the Space**: 
   - Give it a name (e.g., `CropGuard-AI`).
   - Choose **Gradio** as the Space SDK.
   - For hardware, select the **Free CPU** tier (or **T4 GPU** if you have it available).
3. **Upload Files**: Upload your local `app.py` and `requirements.txt` into the "Files" tab of your new space.
4. **Update the App File**: If you fine-tuned your model and pushed it to the hub (e.g., `your-username/cropguard-vit`), make sure you change `VISION_MODEL_ID = "your-username/cropguard-vit"` in the `app.py` file before uploading!
5. **Build**: The space will automatically begin building. It will install the dependencies from `requirements.txt` (including the CPU wheel for `llama-cpp-python`) and start the Gradio server. 

> [!NOTE]  
> The first boot on Hugging Face Spaces will take a few minutes as it downloads the 4.3GB LLM weights. Subsequent boots will be much faster.
