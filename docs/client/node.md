# Node

---

In the FEO platform, all data is indexed to a Node. Each node represents the geographic centroid of a modelled region. Nodes are used to represent useful physical and administrative boundaries and can range from individual physical assets through to entire countries and continents. This flexibility allows FEO users to access data at all levels of aggregation via the FEO platform .

![OSeMOSYS Global: An open-source, open data global electricity system model generator](../assets/images/node.png)
*The image shows how nodes represent the geographic centroid of a modeled region. The edges represent where there is interconnection between the nodes. Source: OSeMOSYS Global: An open-source, open data global electricity system model generator*

In the physics of systems modelling, Nodes are discrete units around which the continuity of energy and materials is constrained. In other words, at every node in a systems model, the input plus supply to the node must equal the output plus demand.

To access data for nodes, you can use this [Jupyter Notebook on Github](https://github.com/transition-zero/feo-client-examples/blob/main/feo-client-examples/0_nodes.ipynb).

See also: [Geometry](./geometry.md)

---

## ::: feo.client.node.Node
    handler: python
