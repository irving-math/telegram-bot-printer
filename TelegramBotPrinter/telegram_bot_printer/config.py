import pkg_resources
import toml


class Config:

    @classmethod
    def get_configuration(cls):
        config_path = pkg_resources.resource_filename(__name__, 'config/config.toml')
        config_json = toml.load(config_path)
        return config_json
