import os
import pandas as pd
from datetime import datetime
import logging
from mau.llm import provider_lmstudio, provider_openai, provider_ollama
from mau.utils.logger import setup_logging
from mau.plugins.output_format_plugin import output_as_csv
import openai

logger = logging.getLogger(__name__)

# mau/data_pipeline/data_pipeline.py

import os

def ensure_file(file_path: str, default_content: str):
    """Create the file with default content if it does not exist."""
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(default_content)
        print(f"Created default prompt file: {file_path}")

def load_prompt(file_path: str, default_content: str = "Default prompt content"):
    """
    Load the prompt file. If it doesn't exist, create it using the provided default content.
    """
    if not os.path.exists(file_path):
        print(f"Prompt file not found: {file_path}. Creating default file.")
        ensure_file(file_path, default_content)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def get_last_completed_cycle(session_id: str, excel_output_path: str) -> int:
    if not os.path.exists(excel_output_path):
        return 0
    df = pd.read_excel(excel_output_path)
    if df.empty:
        return 0
    return int(df["Cycle Number"].max())

def generate_layer002_response(identity_prompt: str, task_prompt: str, layer001_response: str,
                               provider, model: str, temperature: float) -> str:
    combined_prompt = f"Layer 1 Response: {layer001_response}\n\n{task_prompt}"
    try:
        # Using the provider's non-streaming mode for simplicity
        messages = [
            {"role": "system", "content": identity_prompt},
            {"role": "user", "content": combined_prompt}
        ]
        # For demonstration, we use openai.ChatCompletion.create directly.
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=False,
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error during LLM call: {e}")
        return None

def save_output_layer002(identity_prompt: str, task_prompt: str, response: str, cycle_number: int, session_id: str,
                         output_dir_md: str, output_dir_excel: str):
    os.makedirs(output_dir_md, exist_ok=True)
    os.makedirs(output_dir_excel, exist_ok=True)
    md_output_path = os.path.join(output_dir_md, f"response_L002_session_{session_id}_cycle_{cycle_number}.md")
    with open(md_output_path, "w", encoding="utf-8") as f:
        f.write(f"Input:\n{task_prompt}\n\nOutput:\n{response}")
    excel_output_path = os.path.join(output_dir_excel, f"response_L002_session_{session_id}.xlsx")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_new = pd.DataFrame({
        "Session ID": [session_id],
        "Cycle Number": [cycle_number],
        "Timestamp": [timestamp],
        "Identity Prompt": [identity_prompt],
        "Task Prompt": [task_prompt],
        "Generated Response": [response]
    })
    if os.path.exists(excel_output_path):
        df_existing = pd.read_excel(excel_output_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_excel(excel_output_path, index=False)
    # Call CSV output plugin if enabled
    output_as_csv(df_combined, session_id)

def run_data_generation_mode(config: dict, output_formats: list):
    # Load the identity and task prompts with default content in case they are missing.
    identity_prompt = load_prompt(config["identity_prompt_path"], "You are a helpful AI tasked with improving responses.")
    task_prompt = load_prompt(config["task_prompt_path"], "Please improve the following response.")
    
    session_id = "1000_methods_biofabrication_L002"  # Or derive this from config/input if desired

    # Get the last completed cycle from the Excel output to resume from there
    last_completed_cycle = get_last_completed_cycle(session_id)

    # Loop through the data from Layer 001 and process it in Layer 002, resuming from the last completed cycle
    for index, row in pd.read_excel(config["layer_001_input_path"]).iterrows():
        cycle_number = row['Cycle Number']
        if cycle_number <= last_completed_cycle:
            continue
        layer001_response = row['Generated Response']
        response = generate_layer002_response(identity_prompt, task_prompt, layer001_response, model=config["model"], temperature=config.get("temperature", 0.7))
        if response:
            save_output_layer002(identity_prompt, task_prompt, response, cycle_number, session_id)
            print(f"Cycle {cycle_number} completed for Layer 002.")
        else:
            print(f"Cycle {cycle_number} failed for Layer 002.")

if __name__ == "__main__":
    # For standalone testing
    setup_logging()
    run_data_generation_mode({
        "layer_001_input_path": "path/to/layer_001.xlsx",
        "output_dir_md": "outputs_md/layer_002",
        "output_dir_excel": "outputs_excel/layer_002",
        "identity_prompt_path": "prompts/Identity_L002.md",
        "task_prompt_path": "prompts/task_002.md",
        "provider": "lmstudio",
        "provider_config": {"base_url": "http://localhost:1234/v1", "api_key": "lm-studio"},
        "model": "model-identifier",
        "temperature": 0.7
    }, ["markdown", "excel", "csv"])
