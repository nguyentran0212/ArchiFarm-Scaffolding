# Prototyping Tools

Prototyping tool is responsible for setting the architectural parameters of a distillation before running an experiment. Generally, setting architectural parameters means generating a new prototype on the fly (e.g., sending DLT network architecture to a prototyping tool as parameter, receiving a prototype DLT network with corresponding architecture as the output). A server for calling tool is provided.

## How to adapt this code

1. Add the code of your prototyping tools in this folder. 
2. Modify the `prototyping_server.py` to import and call your tools.
