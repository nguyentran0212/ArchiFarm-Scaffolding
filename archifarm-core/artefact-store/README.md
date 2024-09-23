# Artefact Store

This component is responsible for providing an interface for storing experiment results. This interface would be leveraged by the workflow engine to store experiment results after each experiment run.  

Example: artefact store can be a MongoDB instance, whose REST API is used by workflow engine to store experiment results. ArchiFarm does not mandate database type and schemas. 
