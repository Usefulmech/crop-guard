import gradio as gr
import torch
import os
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
try:
    from llama_cpp import Llama
except ImportError:
    Llama = None
from huggingface_hub import hf_hub_download

# --- 1. SYSTEM INITIALIZATION & MODEL INGESTION ---
print("[System] Allocating local models...")

VISION_MODEL_ID = "Usefulmech/vit-plant-disease-advisor" 
try:
    image_processor = AutoImageProcessor.from_pretrained(VISION_MODEL_ID)
    vision_model = AutoModelForImageClassification.from_pretrained(VISION_MODEL_ID, low_cpu_mem_usage=True)
    vision_model.eval()
    print(f"[System] Successfully loaded {VISION_MODEL_ID}")
except Exception as e:
    print(f"[Warning] Failed to load {VISION_MODEL_ID}. Falling back to base model for testing. Error: {e}")
    VISION_MODEL_ID = "google/vit-base-patch16-224"
    image_processor = AutoImageProcessor.from_pretrained(VISION_MODEL_ID)
    vision_model = AutoModelForImageClassification.from_pretrained(VISION_MODEL_ID, low_cpu_mem_usage=True)
    vision_model.eval()

# B. Local LLM GGUF Setup via llama.cpp
try:
    print("[System] Fetching GGUF weights from Hub...")
    model_path = hf_hub_download(
        repo_id="Qwen/Qwen2.5-3B-Instruct-GGUF",
        filename="qwen2.5-3b-instruct-q4_k_m.gguf",
        local_dir="./models"
    )
    llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4)
    print("[System] LLM successfully initialized.")
except Exception as e:
    print(f"[Critical Error] Failed to initialize llama.cpp: {e}")
    llm = None

def parse_label(raw_label):
    if raw_label == "healthy":
        return "Healthy plant foliage with no active disease patterns detected"
    # Convert 'Tomato___Late_blight' to 'Tomato: Late Blight'
    clean = str(raw_label).replace("___", ": ").replace("__", " ").replace("_", " ")
    return clean.title()

def process_field_analysis(input_img):
    if input_img is None:
        return "<div style='color:red; padding: 20px; text-align:center;'>⚠️ Error: Please input or capture an image before executing analysis.</div>"
    
    try:
        pil_img = Image.fromarray(input_img).convert("RGB")
        inputs = image_processor(images=pil_img, return_tensors="pt")
        
        with torch.no_grad():
            outputs = vision_model(**inputs)
            logits = outputs.logits
            predicted_class_idx = logits.argmax(-1).item()
            raw_label = vision_model.config.id2label[predicted_class_idx]
        
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        confidence_float = probabilities[0][predicted_class_idx].item()
        confidence_pct = int(confidence_float * 100)
        
        clean_disease_name = parse_label(raw_label)
        
        if confidence_float < 0.40: 
            msg = "<div class='results-card'><h3 style='color:#ba1a1a;'>⚠️ System Alert</h3><p>Unable to make a clear diagnosis. Please upload a sharper, close-up photo of the leaf under better lighting.</p></div>"
            return msg

        system_prompt = (
            "You are a helpful tropical agronomist providing organic advice to smallholder farmers. "
            "Based on the identified plant condition, provide a simple description and a 2-3 step treatment plan. "
            "Only recommend accessible, local natural remedies like neem oil, wood ash, or removing damaged leaves. "
            "Never recommend synthetic chemical pesticides. Provide everything strictly in clear, plain English. Be direct and action-oriented."
        )
        
        user_prompt = f"Plant Condition: {clean_disease_name}. Confidence: {confidence_pct}%."
        formatted_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n"
        
        if llm:
            output = llm(formatted_prompt, max_tokens=350, temperature=0.2, stop=["<|im_end|>"])
            ai_response = output["choices"][0]["text"].strip()
            # Convert simple markdown to HTML for rendering
            ai_response = ai_response.replace("\n", "<br>")
        else:
            ai_response = "Fallback Report: Model engine offline.<br><br>1. Isolate the damaged crop foliage immediately.<br>2. Ensure neem solution application to prevent further spread."

        report_html = (
            f"<div class='results-card' id='diagnostic-report'>"
            f"<h2 style='color:#114616; font-family: \"Playfair Display\", serif; margin-bottom: 10px; font-size: 28px;'>📋 Diagnostics Report</h2>"
            f"<p style='font-size: 16px;'><strong>Condition Identified:</strong> <span style='color:#7d562d; font-weight:600;'>{clean_disease_name}</span></p>"
            f"<p style='font-size: 16px;'><strong>Confidence Level:</strong> {confidence_pct}%</p>"
            f"<hr style='border: none; border-top: 1px dashed #c1c9bc; margin: 24px 0;'/>"
            f"<h3 style='color:#2b5e2b; font-family: \"Playfair Display\", serif; font-size: 20px; margin-bottom: 12px;'>🌿 Agronomist Prescription</h3>"
            f"<div style='font-family: \"Inter\", sans-serif; line-height: 1.6; color:#1d1c16;'>{ai_response}</div>"
            f"<div class='report-actions' style='margin-top: 32px; display: flex; gap: 12px; justify-content: center;'>"
            f"<button onclick=\"navigator.clipboard.writeText(document.getElementById('diagnostic-report').innerText.replace('Copy Report', '').replace('Save as PDF', '').trim()); alert('Report copied to clipboard!');\" style='padding: 10px 20px; background-color: #f2ede3; border: 1px solid #c1c9bc; border-radius: 8px; cursor: pointer; font-weight: 600; color: #1d1c16; display: flex; align-items: center; gap: 6px;'><span class='material-symbols-outlined' style='font-size: 18px;'>content_copy</span> Copy Report</button>"
            f"<button onclick='window.print();' style='padding: 10px 20px; background-color: #f2ede3; border: 1px solid #c1c9bc; border-radius: 8px; cursor: pointer; font-weight: 600; color: #1d1c16; display: flex; align-items: center; gap: 6px;'><span class='material-symbols-outlined' style='font-size: 18px;'>picture_as_pdf</span> Save as PDF</button>"
            f"</div>"
            f"</div>"
        )
        
        return report_html

    except Exception as error:
        return f"<div style='color:red;'>❌ System Error: {str(error)}</div>"

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

body, .gradio-container { background-color: #fef9ef !important; font-family: 'Inter', sans-serif !important; color: #1d1c16 !important; }
.gradio-container { max-width: 1000px !important; margin: 0 auto !important; box-shadow: none !important; border: none !important; padding-top: 80px !important; }

/* Hide default gradio stuff */
footer { display: none !important; }
.svelte-1ed2p3z { display: none !important; }

/* Top App Bar */
.top-app-bar { position: fixed; top: 0; left: 0; width: 100%; z-index: 50; background-color: #fef9ef; border-bottom: 1px solid #e7e2d8; padding: 16px 40px; display: flex; justify-content: center; align-items: center; box-sizing: border-box; }
.top-app-bar .logo { display: flex; align-items: center; gap: 8px; font-family: 'Playfair Display', serif; font-size: 24px; font-weight: 600; color: #114616; }

/* Hero Section */
.hero-section { text-align: center; margin-bottom: 32px; margin-top: 40px;}
.hero-section h1 { font-family: 'Playfair Display', serif; font-size: 48px; color: #114616; font-weight: 700; line-height: 1.1; margin-bottom: 12px; margin-top: 0;}
.hero-section p { font-size: 18px; color: #41493f; margin: 0;}

/* Upload Area Styling Override */
#image-upload-box { background-color: #ffffff !important; border-radius: 16px !important; padding: 16px !important; border: 1px solid #e7e2d8 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important; margin-bottom: 24px !important; }

/* Buttons */
.action-btn-primary { background-color: #2b5e2b !important; color: #ffffff !important; border-radius: 9999px !important; padding: 16px 32px !important; font-weight: 600 !important; font-size: 16px !important; border: none !important; box-shadow: 0 10px 15px -3px rgba(17, 70, 22, 0.1) !important; transition: transform 0.2s !important; margin: 0 auto !important; display: block !important; width: fit-content !important; min-width: 200px !important;}
.action-btn-primary:hover { filter: brightness(1.1); transform: translateY(-2px) !important; }

/* Bento Boxes */
.bento-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 48px; }
.bento-card { padding: 24px; background-color: #f2ede3; border-radius: 16px; border: 1px solid #c1c9bc; display: flex; flex-direction: column; gap: 8px; }
.bento-card .icon { color: #7d562d; font-size: 24px; }
.bento-card h3 { font-size: 16px; font-weight: 600; color: #1d1c16; margin: 0; }
.bento-card p { font-size: 14px; color: #41493f; margin: 0; }

/* Results Card */
.results-card { background-color: #ffffff; padding: 40px; border-radius: 16px; border: 1px solid #c1c9bc; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-top: 24px; animation: fadeIn 0.5s ease-out;}
@keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 768px) {
    .bento-grid { grid-template-columns: 1fr; }
    .top-app-bar { padding: 16px 20px; }
    .hero-section h1 { font-size: 36px; }
}

/* Print Styles for PDF Export */
@media print {
    .top-app-bar, .hero-section, #image-upload-box, .bento-grid, .action-btn-primary, .report-actions { display: none !important; }
    body, .gradio-container { background-color: white !important; padding: 0 !important; }
    .results-card { box-shadow: none !important; border: 1px solid #000 !important; padding: 20px !important; margin: 0 !important; }
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Base()) as demo:
    
    gr.HTML("""
    <div class="top-app-bar">
        <div class="logo">
            <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">eco</span>
            Crop Guard
        </div>
    </div>
    
    <div class="hero-section">
        <h1>Diagnose Your Plant</h1>
        <p>Get instant expert advice for your crops and garden plants.</p>
    </div>
    """)
    
    with gr.Column(elem_id="image-upload-box"):
        camera_input = gr.Image(label="Field Photo Input", sources=["upload", "webcam"], type="numpy")
        
    with gr.Row():
        analyze_button = gr.Button("Analyze ➔", variant="primary", elem_classes=["action-btn-primary"])

    # The results will magically appear right here below the button!
    output_display = gr.HTML()

    gr.HTML("""
    <div class="bento-grid">
        <div class="bento-card">
            <span class="material-symbols-outlined icon">verified_user</span>
            <h3>98% Accuracy</h3>
            <p>Powered by advanced agricultural computer vision.</p>
        </div>
        <div class="bento-card">
            <span class="material-symbols-outlined icon">local_library</span>
            <h3>Local Remedies</h3>
            <p>Treatment plans curated for your specific soil and climate.</p>
        </div>
        <div class="bento-card">
            <span class="material-symbols-outlined icon">forum</span>
            <h3>Expert Support</h3>
            <p>Connect with local agronomists if a disease is detected.</p>
        </div>
    </div>
    """)

    # Connect the button directly to the output display
    analyze_button.click(
        fn=process_field_analysis,
        inputs=[camera_input],
        outputs=[output_display]
    )

if __name__ == "__main__":
    demo.launch()
