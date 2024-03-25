'''
@Author: Nikhil Kumar
@Desc: Class to handle the configuration file
'''
import json

# config file path
CONFIG_FILE_PATH = 'src/utility/configs/app_development.json'

class ConfigHandler:
    '''
    Class to handle the configuration file
    @ methdods:
        - load_config: load the configuration file
        - get_database_config: get the database configuration
    '''
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        self.config_file_path = config_file_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file_path, 'r') as file:
            return json.load(file)

    def get_database_config(self):
        return self.config['database']
    
    def get_jwt_config(self):
        return self.config['jwt']


