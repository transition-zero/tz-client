# FEO Python Client Quickstart Guide

The FEO Python Client allows users to programmatically access data on the Future Energy Outlook platform, using commands in python.

## Installation

The FEO Python Client may be pip installed as follows:

    pip install feo-client

## Authentication

To use the FEO Python Client, you will need to be authenticated with the FEO platform. To do so, you should will need to use the command-line utility provided as part of the FEO Python Client package.

First, make sure that you are in the environment in which you installed the `feo-client` python package. If you used a virtual environment, enable it:

    source .venv/bin/activate

To log in to the FEO platform from your device, then type:

    feo auth login

You should be provided with a link to a webpage where you can authenticate. If it is successful, your command line should return:

    Checking for authentication.............Authenticated!

To confirm that it worked correctly, use:

    feo auth test

## First use case: accessing nodes

A key concept within the FEO platform is that of "`Nodes`". Nodes represent geographic areas or energy assets which may be used in modelling. For instance, a node could represent a particular country, a sub-region or state within a country, or a particular power unit.

To access data on the FEO platform using the python client, you can use the different classes in the client which provide access to different types of data on the platform. For instance, to access `Node` data, you would use the following:

    from feo.client import Node

To access a particular node by its id:

    node = Node.get(id="IDN")
    print(node.name)

    > "Indonesia"

To search for a node based on its alias, use the following. This returns a list of possible nodes.

    results = Node.search(alias="Indonesia")
    for i, result in enumerate(results):
        print(f"{i+1}: {result.name} - {result.id}")

##

There are a number of other classes to use to access different types of data on the platform:

- `Model` - to access different models
-
