from __init__ import ApiHttpServer

def test_function_no_params():
    return {
        "result" : True
    }
    
def test_function_no_return():
    pass

def test_function_params(paramone, paramtwo):
    return {
        "result" : True
    }

app = ApiHttpServer()
app.bind(diction = {
    "test_1" : test_function_no_params,
    "test_2" : test_function_no_return,
    "test_3" : test_function_params
})
app.start(8080)