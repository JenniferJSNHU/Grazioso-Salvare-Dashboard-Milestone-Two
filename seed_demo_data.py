"""Import 10,000 shelter records from animals.json into Atlas without duplicates."""

import json
from collections import Counter
from getpass import getpass
from pathlib import Path

from pymongo import MongoClient, UpdateOne

# load the 10,000 numbered shelter records from the exported JSON file
file_path = Path(__file__).resolve().parent / "animals.json"
if not file_path.exists():
    raise SystemExit("animals.json must be in the same folder as this script.")

with file_path.open(encoding="utf-8") as file:
    data = json.load(file)

records = [
    {key: value for key, value in record.items() if key != "_id"}
    for record in data
    if isinstance(record, dict) and type(record.get("rec_num")) is int
]
record_numbers = [record["rec_num"] for record in records]
if len(records) != 10000 or set(record_numbers) != set(range(1, 10001)):
    raise SystemExit(
        "Expected exactly one record for each rec_num from 1 through 10000."
    )

# ask for the Atlas connection without saving credentials in the script
atlas_uri = getpass("Paste your Atlas connection URI (hidden): ").strip()
if not atlas_uri.startswith(("mongodb+srv://", "mongodb://")):
    raise SystemExit("Invalid MongoDB connection string.")

atlas = MongoClient(atlas_uri, serverSelectionTimeoutMS=15000)
try:
    atlas.admin.command("ping")
    target = atlas["aac"]["animals"]

    # stop if existing numbered records have ambiguous duplicate record numbers
    existing = list(target.find({}, {"rec_num": 1}))
    existing_numbers = [
        item["rec_num"] for item in existing if type(item.get("rec_num")) is int
    ]
    duplicates = [number for number, n in Counter(existing_numbers).items() if n > 1]
    if duplicates:
        raise SystemExit(
            f"Atlas already has duplicate rec_num values: {duplicates[:10]}"
        )

    # insert missing records without changing records that already exist
    inserted = 0
    for start in range(0, len(records), 200):
        batch = records[start : start + 200]
        result = target.bulk_write(
            [
                UpdateOne(
                    {"rec_num": record["rec_num"]},
                    {"$setOnInsert": record},
                    upsert=True,
                )
                for record in batch
            ],
            ordered=False,
        )
        inserted += result.upserted_count

    numbered_count = target.count_documents({"rec_num": {"$gte": 1, "$lte": 10000}})
    total_count = target.count_documents({})
    print(f"Added {inserted} shelter records.")
    print(f"Numbered shelter records in Atlas: {numbered_count}")
    print(f"Total documents in Atlas: {total_count}")
    if total_count != 10000:
        print("Extra documents (such as a test animal) remain untouched.")
        print("We can review them separately before removing or archiving anything.")
finally:
    atlas.close()
