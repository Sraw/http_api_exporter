from context import ApiHttpServer
from tornado.testing import AsyncHTTPTestCase
import unittest
import json

def test_function_no_params():
    return {
        "result" : True
    }
    
def test_function_no_return():
    pass

def test_function_two_params(paramone, paramtwo):
    return {
        "result" : True
    }
    
def test_function_invalid_json_output():
    return "invalid json output"

app = ApiHttpServer()
app.bind(diction = {
    "/no_params" : test_function_no_params,
    "/no_return" : test_function_no_return,
    "/two_params" : test_function_two_params,
    "/invalid_json_output" : test_function_invalid_json_output
})
application = app._ApiHttpServer__make_app()

class ApiTestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.app = application
        return self.app

    def test_no_params_without_body(self):
        response = self.fetch('/no_params', method='POST', allow_nonstandard_methods = True)
        self.assertEqual(response.code, 200)
        
    def test_no_params_with_empty_body(self):
        response = self.fetch('/no_params', method='POST', body = "{}")
        self.assertEqual(response.code, 200)
        
    def test_no_return(self):
        response = self.fetch('/no_return', method='POST', allow_nonstandard_methods = True)
        self.assertEqual(response.code, 200)
        
    def test_two_params_with_only_Input(self):
        response = self.fetch('/two_params', method='POST', body = json.dumps({"Input" : [1, 2]}))
        self.assertEqual(response.code, 200)
    
    def test_two_params_with_both_Input_and_argsDict(self):
        response = self.fetch('/two_params', method='POST', body = json.dumps({"Input" : [1], "paramtwo" : 2}))
        self.assertEqual(response.code, 200)
    
    def test_two_params_with_only_argsDict(self):
        response = self.fetch('/two_params', method='POST', body = json.dumps({"paramone": 1, "paramtwo": 2}))
        self.assertEqual(response.code, 200)
        
    def test_invalid_json_input(self):
        response = self.fetch('/two_params', method='POST', body = "invalid json")
        self.assertEqual(response.code, 400)
        
    def test_missing_params(self):
        response = self.fetch('/two_params', method='POST', body = json.dumps({"paramtwo": 2}))
        self.assertEqual(response.code, 500)
      
    def test_invalid_json_output(self):
        response = self.fetch('/invalid_json_output', method='POST', allow_nonstandard_methods = True)
        self.assertEqual(response.code, 400)    

if __name__ == '__main__':
    unittest.main()
