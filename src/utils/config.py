import yaml
import os

class ConfigLoader:
    """Centralized configuration manager for the entire platform."""
    
    @staticmethod
    def load(config_path="config.yaml"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Missing {config_path}!")
        with open(config_path, "r") as file:
            return yaml.safe_load(file) 
