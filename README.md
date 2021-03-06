# BIMnferer

* Python =< 3.6 
* MondoDB

## Set credentials

To use the scrapper you need to set your credentials o a file named *Credentials.txt* inside src\scrapper\Credentials.txt. 

The file should be set as:

```
Consumer Key: <forgeClientKey>
Consumer Secret: <forgeClientSecret>
```


## Execution

* Optional, create a new environment

```
pip install virtualenv 
virtualenv bimferer
bimferer\Scripts\activate
```

* Install the python scripts dependencies
```
 pip3 install requirements.txt
```

* Create a mongo db in localhost 

https://www.mongodb.com/try/download/community

* Run Scrapper
To execute in windows

```
python3.exe .\src\scrapper\main.py
```

* Run Server
To execute on linux

```
$export FLASK_APP=server.py
python3 -m flask run --host=0.0.0.0
```
* Access the API

Go to http://localhost:5000/apidocs and check the API endpoints available


## Debug 

If you are using VS Code, setup your launch.json to be able to debug the server and the scrapper
```
  {
      // Use IntelliSense to learn about possible attributes.
      // Hover to view descriptions of existing attributes.
      // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
      "version": "0.2.0",
      "configurations": [


          {
              "name": "Python: Server",
              "type": "python",
              "request": "launch",
              "program": "${workspaceFolder}/src/server/server.py",
              "console": "integratedTerminal"
          },
          {
              "name": "Python: Scrapper",
              "type": "python",
              "request": "launch",
              "program": "${workspaceFolder}/src/scrapper/main.py",
              "console": "integratedTerminal"
          }
      ]
  }
```

### Demo

http://3.14.88.102:5000/apidocs/
