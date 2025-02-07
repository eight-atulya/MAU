import logging

def setup_logging():
    # logging.basicConfig(
    #     level=logging.DEBUG,  # Use DEBUG for more verbosity during development
    #     format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    #     datefmt="%Y-%m-%d %H:%M:%S",
    # )
    # logging.info("Logging is set up.")
    logging.basicConfig(
    level=logging.INFO,  # Change from DEBUG to INFO
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.info("Logging is set up.")

