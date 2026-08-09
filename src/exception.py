import sys  
import logging

def error_massege(error, error_details:sys):
    _,_, exc_tb=error_details.exc.info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_massage="Error occured in python script name is [{0}] line numer [{1}] and error massage is [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_massage
class CustomeException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init__(error_massege)
        self.error_message=error_message(error_message, massage_error_details=error_details)
        
    def __str__(self):
        return self.error_message
    

    