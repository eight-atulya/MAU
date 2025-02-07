# mau/data_pipeline/layer_1.py
import os
import openai
import pandas as pd
from datetime import datetime

def ensure_dir(directory: str):
    """Ensure that the directory exists; if not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory exists: {directory}")

def ensure_file(file_path: str, default_content: str):
    """Ensure that the file exists; if not, create it with default content."""
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(default_content)
        print(f"Created default file: {file_path}")
    else:
        print(f"File exists: {file_path}")

def load_file(file_path: str) -> str:
    """Load the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Loaded file: {file_path} (content length: {len(content)})")
    return content

def generate_response(client, identity_prompt: str, task_prompt: str, model: str) -> str:
    """Call the LM Studio API to generate a response using the given prompts."""
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": identity_prompt},
                {"role": "user", "content": task_prompt}
            ],
            temperature=0.8
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in API call: {e}")
        return None

def save_response(identity_prompt: str, task_prompt: str, response: str,
                  cycle_number: int, session_id: str,
                  output_dir_md: str, output_dir_excel: str):
    """Save the generated response to a Markdown file and update an Excel log."""
    # Save to Markdown file
    md_filename = f"response_session_{session_id}_cycle_{cycle_number}.md"
    md_path = os.path.join(output_dir_md, md_filename)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(response)
    print(f"Saved Markdown: {md_path}")

    # Prepare data for Excel file
    excel_filename = f"response_session_{session_id}.xlsx"
    excel_path = os.path.join(output_dir_excel, excel_filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "Session ID": [session_id],
        "Cycle Number": [cycle_number],
        "Timestamp": [timestamp],
        "Identity Prompt": [identity_prompt],
        "Task Prompt": [task_prompt],
        "Generated Response": [response]
    }
    df_new = pd.DataFrame(data)
    
    if os.path.exists(excel_path):
        df_existing = pd.read_excel(excel_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
        
    df_combined.to_excel(excel_path, index=False)
    print(f"Saved Excel: {excel_path}")

def get_last_cycle(output_dir_md: str, session_id: str) -> int:
    """Return the highest cycle number already saved in the Markdown output directory."""
    cycles = []
    for filename in os.listdir(output_dir_md):
        if filename.startswith(f"response_session_{session_id}_cycle") and filename.endswith(".md"):
            try:
                # Expecting filenames like response_session_<session_id>_cycle_<number>.md
                cycle_str = filename.split('_')[-1].split('.')[0]
                cycles.append(int(cycle_str))
            except Exception:
                continue
    return max(cycles) if cycles else 0

def run_layer1(config: dict):
    """
    Run the Layer 1 data generator.
    
    Expected keys in config:
      - identity_dir: Directory for identity prompt files.
      - task_dir: Directory for task prompt files.
      - output_dir_md: Directory to save generated Markdown files.
      - output_dir_excel: Directory to save/update the Excel log.
      - identity_prompt_file: Filename for the identity prompt (e.g., "Identity_L001.md").
      - task_prompt_file: Filename for the task prompt (e.g., "task_001.md").
      - model: Model identifier (e.g., "llama-3.2-1b-instruct").
      - provider_config: Dict with keys "base_url" and "api_key" for LM Studio.
    """
    # Read configuration values
    identity_dir = config.get("identity_dir")
    task_dir = config.get("task_dir")
    output_dir_md = config.get("output_dir_md")
    output_dir_excel = config.get("output_dir_excel")
    identity_prompt_file = config.get("identity_prompt_file", "Identity_L001.md")
    task_prompt_file = config.get("task_prompt_file", "task_001.md")
    model = config.get("model")
    provider_conf = config.get("provider_config", {})
    base_url = provider_conf.get("base_url")
    api_key = provider_conf.get("api_key")

    print("Configuration:")
    print(f"  identity_dir: {identity_dir}")
    print(f"  task_dir: {task_dir}")
    print(f"  output_dir_md: {output_dir_md}")
    print(f"  output_dir_excel: {output_dir_excel}")
    print(f"  identity_prompt_file: {identity_prompt_file}")
    print(f"  task_prompt_file: {task_prompt_file}")

    # Ensure directories exist
    ensure_dir(identity_dir)
    ensure_dir(task_dir)
    ensure_dir(output_dir_md)
    ensure_dir(output_dir_excel)

    # Build full paths for prompt files
    identity_path = os.path.join(identity_dir, identity_prompt_file)
    task_path = os.path.join(task_dir, task_prompt_file)

    print(f"Full identity path: {identity_path}")
    print(f"Full task path: {task_path}")

    # Ensure the prompt files exist; if not, create them with default content.
    ensure_file(identity_path, "Default identity prompt: You are a helpful AI.")
    ensure_file(task_path, "Default task prompt: Please improve the following response.")

    # Load prompt contents
    identity_prompt = load_file(identity_path)
    task_prompt = load_file(task_path)

    # Set up LM Studio client
    client = openai.OpenAI(base_url=base_url, api_key=api_key)

    # Prompt user for session ID and cycles
    session_id = input("Enter session ID (unique name for this run): ")
    last_cycle = get_last_cycle(output_dir_md, session_id)
    if last_cycle > 0:
        print(f"Resuming from cycle {last_cycle + 1}")
    else:
        print("Starting from cycle 1")

    while True:
        try:
            cycle_count = int(input("Enter the total number of cycles you want to run: "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # Run cycles
    for cycle in range(last_cycle + 1, cycle_count + 1):
        print(f"\nRunning cycle {cycle}...")
        response = generate_response(client, identity_prompt, task_prompt, model)
        if response:
            save_response(identity_prompt, task_prompt, response, cycle, session_id, output_dir_md, output_dir_excel)
            print(f"Cycle {cycle} completed.\n")
        else:
            print(f"Cycle {cycle} failed. Skipping.\n")

if __name__ == "__main__":
    # Example configuration for Layer 1
    config = {
        "identity_dir": "D:/data_generator_01/identity_prompts/",
        "task_dir": "D:/data_generator_01/task_prompts/",
        "output_dir_md": "D:/data_generator_01/outputs_md/layer_001",
        "output_dir_excel": "D:/data_generator_01/outputs_excel/layer_001",
        "identity_prompt_file": "Identity_L001.md",
        "task_prompt_file": "task_001.md",
        "model": "llama-3.2-1b-instruct",
        "provider_config": {
            "base_url": "http://localhost:1234/v1",
            "api_key": "lm-studio"
        }
    }
    run_layer1(config)
