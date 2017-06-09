# http\_api\_exporter

This is a very simple http server lib designed to export APIs in python.

The lib is based on tornado.

## Usage

```
from http_api_exporter import ApiHttpServer #import the class

def function():                    #define the functions you want to export
    ...

# Then you have two choices to bind the server with functions.


app = ApiHttpServer({"Route" : function})
app.start()

# or

app = ApiHttpServer()
app.bind("Route", function)
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

__ApiHttpServer.\_\_init\_\_(functionDict = dict(), WelcomePage = "Python APIs are providing.", debug = False) :__

initialize an instance.
    
&emsp;&emsp;args __:__

&emsp;&emsp;&emsp;functionDict __:__ A dictionary which is composed by "Route" as keys and functions as values.

&emsp;&emsp;&emsp;WelcomePage __:__ A string that allow you modify the welcome page, which can be visited at the root route('\\').

&emsp;&emsp;&emsp;debug __:__ Enable debug log output, default is `False`.

<br />

__ApiHttpServer.bind(self, route = None, function = None, diction = None) :__

Bind the function.
    
&emsp;&emsp;args __:__

&emsp;&emsp;&emsp;route __:__ The route to call the corresponding function.

&emsp;&emsp;&emsp;function __:__ The corresponding function.

&emsp;&emsp;&emsp;diction __:__ If "diction" is not none, then the "route" and the "function" will be ignored. And unfold the dict that keys as routes and values as functions.

<br />

__ApiHttpServer.start(port = 80, retry = 0) :__

Start the server.
    
&emsp;&emsp;args __:__

&emsp;&emsp;&emsp;port __:__ Choose which port to listen on.

&emsp;&emsp;&emsp;retry __:__ How many times to retry if the port has been used.

## Example

```
from http_api_exporter import ApiHttpServer

def testFunction(arg0, arg1):
    #do nothing
    return {
        "a" : 1
    }

if __name__ == "__main__":
    app = ApiHttpServer({"/", testFunction})
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

### TODO

anything else if anyone need.