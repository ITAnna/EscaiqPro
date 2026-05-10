import gradio as gr
from huggingface_hub import InferenceClient
import os

# --- AUTHENTICATION ---
def get_client():
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not token:
        return None
    try:
        return InferenceClient(token=token, model="meta-llama/Meta-Llama-3-8B-Instruct")
    except Exception:
        return None

# --- UI SCALING & COMPACT STYLING ---
custom_css = """
.gradio-container { 
    max-width: 100% !important; 
    padding: 20px 5% !important; 
}
body { background-color: #ffffff; color: #2c3e50; font-size: 18px; }

h1 { color: #008b8b !important; font-size: 4.5em !important; font-weight: 900 !important; text-align: center; margin-bottom: 0px; letter-spacing: -2px; }
h3 { font-size: 1.6em !important; color: #20b2aa !important; margin-bottom: 20px; text-align: center; font-weight: 500; }

.tabs { 
    border: 2px solid #6ae4d9 !important; 
    border-radius: 25px !important; 
    background: #f8ffff !important; 
    padding: 25px !important; 
}

.primary-btn { 
    background: linear-gradient(90deg, #20b2aa 0%, #008b8b 100%) !important; 
    border: none !important; 
    color: white !important; 
    font-weight: 800 !important;
    font-size: 1.8em !important;
    border-radius: 15px !important;
    padding: 20px !important;
    cursor: pointer;
    box-shadow: 0 8px 20px rgba(32, 178, 170, 0.2);
    margin-top: 15px;
    width: 100%;
}

textarea, input, .dropdown { 
    font-size: 1.2em !important; 
    border: 2px solid #6ae4d9 !important; 
    border-radius: 12px !important;
    padding: 15px !important;
}

.report-box { 
    background: #ffffff; 
    border: 2px solid #6ae4d9; 
    border-radius: 20px; 
    padding: 30px;
    min-height: 500px;
    font-size: 1.2em !important;
    line-height: 1.6;
}
"""

class EscaiqApp:
    def analyze(self, text, files, kpi):
        client = get_client()
        if not client:
            return "## ⚠️ ОШИБКА\nТокен HF_TOKEN не найден."

        context = f"KPI Focus: {kpi}\n\n"
        if text and text.strip(): 
            context += f"Proposal content:\n{text}\n\n"
        
        if files:
            for f in files:
                try:
                    with open(f, 'r', encoding='utf-8') as doc:
                        context += f"Doc ({os.path.basename(f)}):\n{doc.read()}\n\n"
                except: continue

        if len(context.strip()) < 30:
            return "## ⚠️ МАЛО ДАННЫХ\nВведите текст или загрузите файлы."

        try:
            response = client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are Escaiq, a Strategic AI for Solana DAOs. Analyze the input and provide a score 0-100 and risk assessment. Be professional and concise."},
                    {"role": "user", "content": context}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"## ⚠️ API ERROR\n{str(e)}"

    def build_prompt(self, goal, metric):
        if not goal: return "### 💡 Введите цель..."
        return f"### 🚀 Optimized Prompt\n```markdown\nAct as a Solana Governance Expert. Evaluate the '{goal}' proposal specifically focusing on '{metric}' impact.\n```"

def launch():
    logic = EscaiqApp()
    
    with gr.Blocks(title="Escaiq DAO Assistant") as demo:
        gr.Markdown("# ESCAIQ")
        gr.Markdown("### STRATEGIC INTELLIGENCE FOR SOLANA DAOs")
        
        with gr.Tabs():
            # 1. ANALYSIS
            with gr.TabItem("STRATEGIC ANALYSIS"):
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Row():
                            kpi = gr.Dropdown(["TVL Growth", "Treasury ROI", "Voter Participation", "Growth Velocity"], label="TARGET KPI", value="TVL Growth", scale=2)
                            fls = gr.File(label="DOCS", file_count="multiple", scale=3)
                        
                        inp = gr.Textbox(label="PROPOSAL DESCRIPTION", placeholder="Paste text here...", lines=6)
                        btn = gr.Button("RUN STRATEGIC AUDIT", variant="primary", elem_classes="primary-btn")
                    
                    with gr.Column(scale=1):
                        out = gr.Markdown("## Intelligence Report\n*Results will appear here...*", elem_classes="report-box")

            # 2. PROMPT BUILDER
            with gr.TabItem("PROMPT BUILDER"):
                gr.Markdown("### 🛠️ STRATEGY RESEARCH CONSTRUCTOR")
                with gr.Row():
                    with gr.Column():
                        g_in = gr.Textbox(label="STRATEGY GOAL", placeholder="e.g. Liquidity Rewards")
                        m_in = gr.Dropdown(label="KPI", choices=["TVL", "ROI", "Governance Health"], value="TVL")
                        btn_p = gr.Button("GENERATE PROMPT", variant="primary", elem_classes="primary-btn")
                    with gr.Column():
                        out_p = gr.Markdown(value="### Generated Result...", elem_classes="report-box")

            # 3. ON-CHAIN DATA
            with gr.TabItem("ON-CHAIN DATA"):
                gr.Markdown("# 🔗 ON-CHAIN PIPELINE")
                gr.Markdown("### STATUS: UPCOMING FEATURE")
                gr.Markdown("Phase 2: Realms (SPL Governance) & Squads API integration.")

        btn.click(logic.analyze, [inp, fls, kpi], out)
        btn_p.click(logic.build_prompt, [g_in, m_in], out_p)

    demo.launch(css=custom_css)

if __name__ == "__main__":
    launch()