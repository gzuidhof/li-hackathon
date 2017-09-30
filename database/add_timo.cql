USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///documents.csv" AS row
MATCH (d:Document {id: toInteger(row.ID)})
SET d.Verdict = row.Verdict, d.VerdictText = row.Verdict_Text, d.InstanceType = row.InstanceType;