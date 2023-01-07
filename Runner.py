import logging

class Runner:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.integrator = Integrator()
        self.input_processor = InputProcessor()
        self.behavioral_output_processor = BehavioralOutputProcessor()
        self.physiological_output_processor = PhysiologicalOutputProcessor()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

        # create a file handler to log errors
        handler = logging.FileHandler('app_log.log')
        handler.setLevel(logging.ERROR)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handler to the logger
        self.logger.addHandler(handler)

class Integrator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
      
class InputProcessor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class BehavioralOutputProcessor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
      
class PhysiologicalOutputProcessor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
 
