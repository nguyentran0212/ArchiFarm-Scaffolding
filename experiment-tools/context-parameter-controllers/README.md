# Context Parameter Controller Tools

This directory contain tools for setting and resetting contextual parameters in an Architecture Farming experiments (e.g., changing network parameters of a testbed infrastructure to specify the network constraint). These tools are accessed by the ArchiFarm core via REST API. A server for calling tool is provided. 

## How to adapt this code

1. Add the code of your experiment tools in this folder. 
2. Modify the `tool_server.py` to import and call your tools.
