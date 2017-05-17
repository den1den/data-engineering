// Load in the nodes
LOAD CSV WITH HEADERS FROM "file:///stations.csv" as row
CREATE (n:Station)
set n = row

// Load in the edges
LOAD CSV WITH HEADERS FROM "file:///edges.csv" as row
MATCH (s1:Station),(s2:Station)
WHERE row.source_id = s1.node_id AND row.target_id = s2.node_id
CREATE (s1)-[:Train {startTime:row.start_time, endTime:row.end_time}]->(s2)
