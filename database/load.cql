USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///documents.csv" AS doc
CREATE (:Document {
    id: toInteger(doc.ID),
    ProcedureType: doc.ProcedureType,
    TopLevelNavigation: split(substring(doc.TopLevelNavigation, 2, size(doc.TopLevelNavigation)-4), ","),
    Authors: split(substring(doc.Authors, 2, size(doc.Authors)-4), ","),
    Classifications: split(substring(doc.Classifications, 2, size(doc.Classifications)-4), ","),
    LawArea: split(substring(doc.LawArea, 2, size(doc.LawArea)-4), ","),
    Sources: split(substring(doc.Sources, 2, size(doc.Sources)-4), ","),
    Topic: split(substring(doc.Topic, 2, size(doc.Topic)-4), ","),
    Summary: doc.Summary_Text,
    Title: doc.Title_Text,
    Timestamp: toInteger(doc.timestamp),
    SearchNumber: doc.SearchNumber
});

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///wetboekenteksten.csv" AS law
CREATE (:Law {
    Law: law.wet,
    Link: law.link,
    Text: law.text
});

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///references.csv" AS ref
MATCH (doc1:Document {id: toInteger(ref.ID)})
MATCH (doc2:Document {SearchNumber: ref.References})
CREATE (doc1)-[r:REFERENCE {Count: toInteger(ref.Counts)}]->(doc2)
;


CREATE INDEX ON :Document(id);
CREATE INDEX ON :Law(link);

schema await
