---
title: Crop Guard AI
emoji: 🌱
colorFrom: green
colorTo: green
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---

# 🌱 Crop Guard AI

**Crop Guard** is an AI-powered agricultural diagnostic tool built for smallholder farmers. It analyzes crop leaf images, identifies diseases using a Vision Transformer (ViT), and provides localized, organic, and accessible treatment recommendations via a lightweight Large Language Model (Qwen2.5 3B GGUF).

---

## 🚀 Features

- **Vision Diagnosis:** Uses a fine-tuned `google/vit-base-patch16-224` to accurately classify 38 plant health and disease conditions (based on PlantVillage).
- **Organic Agronomist AI:** Synthesizes the raw machine label into a localized context, passing it to a highly quantized LLM (`Qwen2.5-3B-Instruct-GGUF`) that runs entirely within the Gradio container.
- **Responsive UI:** Built with Gradio Blocks and custom CSS to deliver a premium, mobile-friendly interface for field use.
- **English-Only Diagnosis:** Strict constraints ensure the AI provides treatments focusing on natural remedies like neem oil and wood ash.

---

## 🛠️ Project Structure

- `app.py`: The core Gradio application combining the vision and text pipelines.
- `requirements.txt`: The specific Python dependencies (includes pre-compiled CPU wheels for `llama-cpp-python` to prevent Hugging Face Spaces build timeouts).
- `SETUP_GUIDE.md`: A detailed developer guide covering dataset preparation and model fine-tuning.

---

## 💻 Local Testing

You can run this project locally to test the interface or make modifications.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Usefulmech/crop-guard.git
   cd crop-guard
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the app:**
   ```bash
   python app.py
   ```
   *(Note: The first time you run this, it will download the 4.3GB LLM weights. Please be patient!)*

---

## 🌐 Deploying to Hugging Face via GitHub Sync

Yes, you can manage this project on GitHub and automatically sync it to Hugging Face Spaces! This is the best way to handle deployments.

### Step-by-Step GitHub Sync

1. **Create a Space on Hugging Face:**
   - Name: `CropGuard-AI`
   - SDK: `Gradio`
   - Hardware: `Free CPU` (or `T4 GPU`)

2. **Connect via GitHub Actions:**
   You can push your code to your GitHub repository and set up a GitHub Action to automatically push to your Hugging Face Space whenever you commit to `main`.
   
   Create a file in your repo at `.github/workflows/sync_to_hub.yml`:

   ```yaml
   name: Sync to Hugging Face hub
   on:
     push:
       branches: [main]
     workflow_dispatch:

   jobs:
     sync-to-hub:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
           with:
             fetch-depth: 0
             lfs: true
         - name: Push to hub
           env:
             HF_TOKEN: ${{ secrets.HF_TOKEN }}
           run: git push https://your-hf-username:$HF_TOKEN@huggingface.co/spaces/your-hf-username/CropGuard-AI main
   ```

3. **Add your HF_TOKEN Secret:**
   - Go to your Hugging Face Account Settings -> Access Tokens, and generate a new token with **write** permissions.
   - Go to your GitHub Repository -> Settings -> Secrets and Variables -> Actions -> **New repository secret**.
   - Name it `HF_TOKEN` and paste your token.

Now, every time you `git push` to your GitHub repo, the changes will automatically be deployed to your Hugging Face Space!
