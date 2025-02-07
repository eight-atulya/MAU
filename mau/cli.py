#!/usr/bin/env python
import argparse
import sys
from mau.utils.logger import setup_logging
from mau.utils.config_utils import load_config
from mau.conversation.conversation_runner import run_conversation_mode
from mau.data_pipeline.data_pipeline import run_data_generation_mode
from mau.data_pipeline.layer_1 import run_layer1  # Import the new module

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="MAU - Multifunctional AI Utility")
    parser.add_argument("--mode", choices=["conversation", "data-generation", "data-generation-layer1"],
                        default="conversation",
                        help="Choose the pipeline mode to run")
    parser.add_argument("-c", "--config", type=str, required=True,
                        help="Path to JSON configuration file")
    args = parser.parse_args()

    config = load_config(args.config)
    
    if args.mode == "conversation":
        run_conversation_mode(config.get("conversation"))
    elif args.mode == "data-generation":
        run_data_generation_mode(config.get("data_pipeline"), config.get("output_formats"))
    elif args.mode == "data-generation-layer1":
        run_layer1(config.get("data_pipeline_layer1"))
    else:
        sys.exit("Unknown mode specified.")

if __name__ == "__main__":
    main()
