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
To execute in windows

```
python3.exe .\src\server\server.py
```
* Access the API

This implementation has 3 endpoints available

**/api/1/elements/$category**

Return elements per category


**/api/1/elements/categories**

Return all elements of the categories provided in the body of the request.
``` 
"{   "categories":[
      "Ducts",
      "Pipes"
      ]
    }"
```

**/api/1/elements/mep**

Return all MEP elements


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

