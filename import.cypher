// Load in the nodes
LOAD CSV WITH HEADERS FROM "file:///stations.csv" as row
CREATE (n:Station)
set n = row;

CREATE INDEX ON :Station(node_id);

// Remove everything
MATCH (n)
DETACH DELETE n;

// Remove all the Trains
MATCH ()-[t:Train]->()
DELETE t;

// Show contents of CSV file
LOAD CSV WITH HEADERS FROM "file:///edges.csv" as row
RETURN row
LIMIT 5;

// Load in the edges/Trains (Last time it took 5 min)
LOAD CSV WITH HEADERS FROM "file:///edges.csv" as row
MATCH (s1:Station),(s2:Station)
WHERE row.source_id = s1.node_id AND row.target_id = s2.node_id
CREATE (s1)-[:Train {startTime:row.start_mod, endTime:row.end_mod, startTimeStr:row.start_time, endTimeStr:row.end_time}]->(s2);
