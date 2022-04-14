import sqlite3
import json

from models import Tag

def get_all_tags():
    with sqlite3.connect("./journal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT 
            t.id,
            t.label
        FROM Tags t
        """)

        # Initialize an empty list to hold all animal representations
        tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a Location instance from the current row
            tag = Tag(row['id'], row['label'])

            # Add the dictionary representation of the animal to the list
            tags.append(tag.__dict__)

        # Use `json` package to properly serialize list as JSON
        return json.dumps(tags)
