import os

# Import configuration classes for different environments
from .default import Config
from .development import DevelopmentConfig
from .testing import TestingConfig
from .production import ProductionConfig

# Define a dictionary to map configuration names to classes
configurations = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Determine the current configuration based on the FLASK_CONFIG environment variable
config_name = os.getenv('FLASK_CONFIG', 'development')
ConfigClass = configurations.get(config_name, DevelopmentConfig)

# Create an instance of the appropriate configuration class
config = ConfigClass()
