from context import ApiHttpServer
from tornado.testing import AsyncHTTPTestCase
import unittest
import tornado

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

app = ApiHttpServer()
app.bind(diction = {
    "/no_params" : test_function_no_params,
    "/no_return" : test_function_no_return,
    "/two_params" : test_function_two_params
})
application = app._ApiHttpServer__make_app()

class ApiTestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.app = application
        return self.app

    def test_status(self):
        response = self.fetch('/no_params', method='POST')
        self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()
