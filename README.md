
# Multifunctional AI Utility (MAU)

MAU is a modular framework for working with local Large Language Models (LLMs). It provides multiple pipelines, including an interactive **Conversation Mode** and a **Data Generation Pipeline**. Currently, Layer 1 of the data generator is implemented. The system automatically creates necessary directories and prompt files if they are missing.

---

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running Conversation Mode](#running-conversation-mode)
  - [Running Data Generation (Layer 1)](#running-data-generation-layer-1)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Interactive Conversation:** Engage in real-time dialogue between multiple AI agents.
- **Data Generation:** Generate structured data (Markdown files and Excel logs) using prompt files.
- **Automatic Setup:** Directories and prompt files are automatically created if they do not exist.
- **Modular and Extensible:** Easily add new pipelines (e.g., additional layers) or providers.
- **Configurable:** Use a JSON configuration file to customize file paths, model parameters, and provider settings.
- **Logging and Debugging:** Debug messages assist in tracing execution and verifying file paths.

---

## Directory Structure

A suggested project structure is as follows:

```

MAU/
├── README.md
├── run.py
├── requirements.txt
├── config/
│   ├── config.json
│   └── schema.json
├── mau/
│   ├── __init__.py
│   ├── cli.py
│   ├── config_models.py
│   ├── conversation/
│   │   ├── __init__.py
│   │   ├── conversation_manager.py
│   │   └── conversation_runner.py
│   ├── data_pipeline/
│   │   ├── __init__.py
│   │   ├── data_pipeline.py
│   │   └── layer_1.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── llm_provider.py
│   │   ├── provider_lmstudio.py
│   │   ├── provider_openai.py
│   │   ├── provider_ollama.py
│   │   └── ai_being.py
│   ├── plugins/
│   │   └── output_format_plugin.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── config_utils.py
└── tests/
    ├── __init__.py
    ├── test_conversation.py
    └── test_data_pipeline.py


```

---

## Prerequisites

- **Python 3.12** (or later)
- **LM Studio** (or your chosen LLM provider) running locally (e.g., at `http://localhost:1234/v1`)
- Required Python packages:
  - `openai`
  - `pandas`
  - `openpyxl`
  - `prompt_toolkit`
  - `rich`
  - `pydantic` (if using configuration models)
  - (Additional packages as needed)

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/eight-atulya/MAU.git
   cd MAU


2. **Create and Activate a Virtual Environment:**
    
    ```bash
    python -m venv venv
    # On Unix/Mac:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```
    
3. **Install Dependencies:**
    
    ```bash
    pip install -r requirements.txt
    ```
    
    _Ensure your `requirements.txt` includes packages such as `openai`, `pandas`, `openpyxl`, `prompt_toolkit`, etc._
    

---

## Configuration

The configuration file (`config/config.json`) controls settings for the different pipelines. Below is an example configuration:

```json
{
  "conversation": {
    "agent1": {
      "name": "eight.atulya",
      "provider": "lmstudio",
      "model": "deepseek-r1-distill-llama-8b",
      "system_prompt": "config/agent1_system_prompt.md",
      "temperature": 1.0,
      "ctx_size": 8888,
      "provider_config": {
        "base_url": "http://localhost:1234/v1",
        "api_key": "lm-studio"
      }
    },
    "agent2": {
      "name": "Anurag",
      "provider": "lmstudio",
      "model": "deepseek-r1-distill-llama-8b",
      "system_prompt": "config/agent2_system_prompt.md",
      "temperature": 0.8,
      "ctx_size": 8888,
      "provider_config": {
        "base_url": "http://localhost:1234/v1",
        "api_key": "lm-studio"
      }
    },
    "settings": {
      "use_markdown": true,
      "allow_termination": false,
      "initial_message": "config/initial_message.md"
    }
  },
  "data_pipeline": {
    "layer_001_input_path": "path/to/layer_001.xlsx",
    "output_dir_md": "outputs_md/layer_002",
    "output_dir_excel": "outputs_excel/layer_002",
    "identity_prompt_path": "prompts/Identity_L002.md",
    "task_prompt_path": "prompts/task_002.md",
    "provider": "lmstudio",
    "provider_config": {
      "base_url": "http://localhost:1234/v1",
      "api_key": "lm-studio"
    },
    "model": "llama-3.2-1b-instruct",
    "temperature": 0.7
  },
  "data_pipeline_layer1": {
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
  },
  "output_formats": ["markdown", "excel", "csv"]
}

```

Adjust the paths and values as needed for your environment.

---

## Usage

MAU uses a unified command-line interface (CLI) through the `run.py` script. You can choose different modes:

### Running Conversation Mode

Start an interactive conversation between AI agents:

```bash
python run.py --mode conversation --config config/config.json
```

Follow the on-screen prompts to configure the conversation.

### Running Data Generation (Layer 1)

Layer 1 uses prompt files to generate responses and logs them as Markdown and Excel files. To run the Layer 1 data generator:

```bash
python run.py --mode data-generation-layer1 --config config/config.json
```

**What Happens:**

- **Automatic Setup:**  
    The program automatically creates necessary directories and prompt files if they are missing. For example, it will create:
    
    - `D:/data_generator_01/identity_prompts/Identity_L001.md`
    - `D:/data_generator_01/task_prompts/task_001.md`
- **Session & Cycle Input:**  
    You will be prompted to enter a unique session ID and the total number of cycles to run.
    
- **Data Generation:**  
    For each cycle, the LM Studio API is called with the loaded prompts, and responses are saved:
    
    - As Markdown files in the specified output directory.
    - In an Excel log (which is created or updated).

### Running Other Modes

If additional data generation layers (e.g., Layer 2) are implemented, you can run them similarly. For example:

```bash
python run.py --mode data-generation --config config/config.json
```

_(Ensure your configuration file contains the corresponding sections.)_

---

## Troubleshooting

- **Missing Modules:**  
    If you see errors like `ModuleNotFoundError: No module named 'openpyxl'`, install it via:
    
    ```bash
    pip install openpyxl
    ```
    
- **Configuration Issues:**  
    Verify that `config/config.json` includes all required sections (e.g., `"data_pipeline_layer1"`).
    
- **Prompt Files Not Loading:**  
    The system creates missing prompt files with default content. Check the console output for directory and file creation messages.
    
- **LM Studio Connection:**  
    Ensure your LM Studio server is running and accessible at the `base_url` provided in the configuration.
    

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Write tests for your changes.
4. Submit a pull request with a clear description.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://chatgpt.com/c/LICENSE) file for details.

---

## Additional Notes

- **Extensibility:**  
    MAU is designed to be modular. You can add new pipelines or agents by extending the configuration and updating the corresponding modules.
    
- **Logging:**  
    Debug messages are provided throughout the code to help trace execution and verify that files and directories are correctly handled. You can adjust the logging level in `mau/utils/logger.py`.
    

Enjoy using MAU for your LLM experiments, and feel free to reach out with any questions or suggestions!
