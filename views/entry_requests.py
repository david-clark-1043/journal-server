import sqlite3
import json

from models import Entry
from models import Mood

def get_all_entries():
    
    with sqlite3.connect("./journal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM Entries e
        JOIN Moods m
            ON e.mood_id = m.id
        """)

        # Initialize an empty list to hold all animal representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])

            # Create a Location instance from the current row
            mood = Mood(row['id'], row['mood_label'])

            # Add the dictionary representation of the location to the animal
            entry.mood = mood.__dict__

            # Add the dictionary representation of the animal to the list
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def get_single_entry(id):
    """gets information for a single entry

    Args:
        id (int): id of the entry you want to get information about

    Returns:
        object: the entry object
    """
    with sqlite3.connect("./journal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM Entries e
        JOIN Moods m
            ON e.mood_id = m.id
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'],
                            data['mood_id'], data['date'])
        
        # Create a Location instance from the current row
        mood = Mood(data['mood_id'], data['mood_label'])

        # Add the dictionary representation of the location to the animal
        entry.mood = mood.__dict__

        return json.dumps(entry.__dict__)
