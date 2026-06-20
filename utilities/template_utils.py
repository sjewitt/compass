# test of jinja template function calling
# https://stackoverflow.com/questions/6036082/call-a-python-function-from-jinja2


class Funcs():
    
    @staticmethod
    def replace_empty_string(str_in):
        if not str_in:
            return "[empty]"
        return str_in
    

    @staticmethod
    def truncate_displayed_text(long_test:str):
        truncated_length = 30
        if len(long_test) > truncated_length:
            # https://stackoverflow.com/questions/663171/how-do-i-get-a-substring-of-a-string-in-python
            return '%s...' % long_test[:truncated_length]
        return long_test