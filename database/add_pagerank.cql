USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///documents.csv" AS row
MATCH (d:Document {id: toInteger(row.ID)})
SET d.PageRank = row.pagerank;