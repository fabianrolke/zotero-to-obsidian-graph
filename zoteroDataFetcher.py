import sqlite3 as sql


def getAllData(path):
    sqlData = sql.connect(path)

    return sqlData.execute("""
SELECT
    an.itemID,              -- 0
    an.comment,             -- 1
    an.text,                -- 2
    an.authorName,          -- 3
    an.parentItemID,       -- 4

    at.itemID,             -- 5
    at.path,               -- 6   (attachment path)
    at.parentItemID,       -- 7

    it.itemID,             -- 8
    it.key,                -- 9   (THIS is correct item key)

    ci.itemID,             -- 10
    ci.collectionID,      -- 11

    co.collectionID,      -- 12
    co.parentCollectionID, -- 13
    co.collectionName,     -- 14

    it.dateAdded,          -- 15
    it.dateModified,       -- 16

    id.fieldID,            -- 17
    iv.value,              -- 18

    an.position            -- 19

FROM itemAttachments at

LEFT JOIN itemAnnotations an
    ON an.parentItemID = at.itemID

LEFT JOIN items it
    ON at.itemID = it.itemID

LEFT JOIN collectionItems ci
    ON at.itemID = ci.itemID

LEFT JOIN collections co
    ON ci.collectionID = co.collectionID

LEFT JOIN itemData id
    ON it.itemID = id.itemID

LEFT JOIN itemDataValues iv
    ON id.valueID = iv.valueID
""").fetchall()