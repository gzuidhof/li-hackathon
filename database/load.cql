USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///documents.csv" AS row
CREATE (:Document {
    id: toInteger(row.ID),
    ProcedureType: row.ProcedureType,
    TopLevelNavigation: split(substring(row.TopLevelNavigation, 2, size(row.TopLevelNavigation)-4), ","),
    Authors: split(substring(row.Authors, 2, size(row.Authors)-4), ","),
    Classifications: split(substring(row.Classifications, 2, size(row.Classifications)-4), ","),
    LawArea: split(substring(row.LawArea, 2, size(row.LawArea)-4), ","),
    Sources: split(substring(row.Sources, 2, size(row.Sources)-4), ","),
    Topic: split(substring(row.Topic, 2, size(row.Topic)-4), ","),
    Summary: row.Summary_Text,
    Title: row.Title_Text,
    timestamp: row.timestamp
});

CREATE INDEX ON :Document(id);

schema await
