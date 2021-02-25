import logging.config

import pkg_resources
import yaml

config_path = pkg_resources.resource_filename(__name__, 'config/log_config.yaml')
with open(config_path, "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

logger.debug("Logging initialized.")
