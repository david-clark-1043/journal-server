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
        

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id,
            t.label tag_label              
        FROM EntryTags et
        JOIN Tags t
            ON et.tag_id = t.id
        """)
        
        entry_tags = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])

            # Create a Location instance from the current row
            mood = Mood(row['mood_id'], row['mood_label'])

            # Add the dictionary representation of the location to the entry
            entry.mood = mood.__dict__

            tags = []
            for et_row in entry_tags:
                if et_row["entry_id"] == row["id"]:
                    tags.append(et_row["tag_id"])

            entry.tags = tags
            
            # Add the dictionary representation of the entry to the list
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

        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id,
            t.label tag_label              
        FROM EntryTags et
        JOIN Tags t
            ON et.tag_id = t.id
        """)
        
        entry_tags = db_cursor.fetchall()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'],
                            data['mood_id'], data['date'])
        
        tags = []
        for et_row in entry_tags:
            if et_row["entry_id"] == data["id"]:
                tags.append(et_row["tag_id"])

        entry.tags = tags
        
        # Create a Location instance from the current row
        mood = Mood(data['mood_id'], data['mood_label'])

        # Add the dictionary representation of the location to the entry
        entry.mood = mood.__dict__

        return json.dumps(entry.__dict__)

def delete_entry(id):
    """removes entry from the list

    Args:
        id (int): id of entry to delete
    """
    with sqlite3.connect("./journal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))

def get_entries_by_text(text):

    with sqlite3.connect("./journal.sqlite3") as conn:
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
        WHERE e.entry LIKE ?
        """, ( f"%{text}%", ))

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id,
            t.label tag_label              
        FROM EntryTags et
        JOIN Tags t
            ON et.tag_id = t.id
        """)
        
        entry_tags = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])

            tags = []
            for et_row in entry_tags:
                if et_row["entry_id"] == row["id"]:
                    tags.append(et_row["tag_id"])

            entry.tags = tags

            # Create a Location instance from the current row
            mood = Mood(row['mood_id'], row['mood_label'])

            # Add the dictionary representation of the location to the entry
            entry.mood = mood.__dict__

            # Add the dictionary representation of the entry to the list
            entries.append(entry.__dict__)

    return json.dumps(entries)

def create_journal_entry(new_entry):
    """adds new entry object to the list

    Args:
        entry (dict): entry object to be added

    Returns:
        dict: the entry object as added with the new id key
    """
    with sqlite3.connect("./journal.sqlite3") as conn:
        db_cursor = conn.cursor()
        # creates the entry in entries table
        db_cursor.execute("""
        INSERT INTO entries
            ( concept, entry, mood_id, date )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['moodId'], new_entry['date'], ))

        # get id of the new entry
        id = db_cursor.lastrowid

        for i, entry_tag in enumerate(new_entry["tags"]):
            db_cursor.execute("""
                INSERT INTO EntryTags
                    ( entry_id, tag_id )
                VALUES
                    ( ?, ? );
                """, (id, entry_tag ))
        # Add the `id` property to the entry dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id


    return json.dumps(new_entry)

def update_entry(id, new_entry):
    """changes single entry in the list

    Args:
        id (int): id of entry to change
        new_entry (dict): entry object to be added
    """
    with sqlite3.connect("./journal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE entries
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['moodId'], new_entry['date'],
              id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount


        if rows_affected == 0:
            # Forces 404 response by main module
            return False
        else:
            db_cursor.execute("""
            SELECT
                et.id,
                et.entry_id,
                et.tag_id,
                t.label tag_label              
            FROM EntryTags et
            JOIN Tags t
                ON et.tag_id = t.id
            """)
            
            entry_tags = db_cursor.fetchall()
            
            for i, entry_tag in enumerate(new_entry["tags"]):
                found = False
                for row in entry_tags:
                    # row has et.id, et.entry_id, et.tag_id, tag_label columns
                    # want to update the entryTag rows where entry_id = new_entry
                    if row["entry_id"] == id:
                        if row["tag_id"] == entry_tag:
                            found = True

            # Forces 204 response by main module
            return True
