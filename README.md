# http\_api\_exporter

This is a very simple http server lib designed to export APIs in python.

The lib is based on tornado.

## Usage

```
from http_api_exporter import ApiHttpServer #import the class

def function():                    #define the functions you want to export
    ...

# Then you have two choices to bind the server with functions.


app = ApiHttpServer({"route" : function})
app.start()

# or

app = ApiHttpServer()
app.bind("route", function)
app.start()

# Finally, you have two ways to pass the args.

{                                   #pass the args as a list named "Input"
   Input: [args] 
}

{                                   #pass the args as a dict
    arg: value,
    arg0: value,
    ...
}

{                                   #combine both
    Input: [args],
    arg0: value,
    ...
}
```

## API

Class __SimpleApiServer__:
* The simplist api server. Designed to easily bind functions to routes' post method.
    * __\_\_init\_\___(function\_dict=None, welcome\_page="Python APIs are providing.", debug=False) :
        * Initialize the class.        
            * __function\_dict__ : A dictionary which is composed by "Route" as keys and functions as values.
            * __welcome\_page__ : A string that allow you modify the welcome page, which can be visited at the root route('\\').
            * __debug__ : Enable debug log stdout, default is `False`.
    * __bind__(self, route=None, function=None, dictionary=None) :
        * Bind the function.
            * __route__ : The route to call the corresponding function.
            * __function__ : The corresponding function.
            * __dictionary__ : If "dictionary" is not `None`, then the "route" and the "function" will be ignored. And unfold the dict that keys as routes and values as functions.
    * __add\_periodic_task__(self, function, interval) :
        * Add periodic task to application, task will be execute every `interval` millisecond. This function should be called before `start()`
            * __function__ : The task expected to execute.
            * __interval__ : The interval between two executions in milliseconds.
    * __start__(port=80, retry=0) :
        * Start the server.
            * __port__ : Choose which port to listen on.
            * __retry__ : How many times to retry if the port has been used, default is `0` which means no retry.


Class __ApiHttpServer__:
* An alias of `SimpleApiServer` because of compatibility, and will be removed in the future(maybe v2.0.0).

## Example

```
from http_api_exporter import ApiHttpServer

def test_function(arg0, arg1):
    #do nothing
    return {
        "a" : 1
    }

if __name__ == "__main__":
    app = ApiHttpServer({"/test", test_function})
    app.start()
    
# then post url http://localhost/
```

## Attention

Your function must returns a dictionary which could be jsonified or has no returned value.

## What's more

### DONE

bind the functions to routes.

support function without return.

support function without parameters.

support pass parameters by "Input" array.

support pass parameters by dictionary form.

support pass parameters by both of the above.

support periodic tasks.

### TODO

anything else if anyone need.