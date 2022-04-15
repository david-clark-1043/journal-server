import sqlite3
import json

from models import Entry
from models import tag
from models import Entry_tag

def get_all_entry_tags():
    with sqlite3.connect("./journal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id            
        FROM EntryTags et
        """)

        dataset = db_cursor.fetchall()

        entry_tags = []

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row
            entry_tag = Entry_tag(row['id'], row['entry_id'], row['tag_id'])

            entry_tags.append(entry_tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entry_tags)

def get_all_entry_tags_for_entry(entry_id):
    with sqlite3.connect("./journal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id            
        FROM EntryTags et
        WHERE et.entry_id = ?
        """, ( entry_id, ))

        dataset = db_cursor.fetchall()

        entry_tags = []

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row
            entry_tag = Entry_tag(row['id'], row['entry_id'], row['tag_id'])

            entry_tags.append(entry_tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entry_tags)

def create_entry_tag(entry_id, tag_id):
    with sqlite3.connect("./journal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO EntryTags
                (entry_id, tag_id)
            VALUES
                (?, ?)
            """, ( entry_id, tag_id ))

def delete_entry_tag(id = "", entry_id = ""):
    with sqlite3.connect("./journal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if id:
            db_cursor.execute("""
                DELETE FROM EntryTags
                WHERE id = ?
                """, ( id, ))
        elif entry_id:
            db_cursor.execute("""
                DELETE FROM EntryTags
                WHERE entry_id = ?
                """, ( entry_id, ))

def update_tags_for_entry(new_entry):
    with sqlite3.connect("./journal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # get all entry_tags for this entry_id
        entry_tags = get_all_entry_tags_for_entry(new_entry["id"])
        entry_tags = json.loads(entry_tags)
        # """
        #     new_entry.tags = [1, 2, 3]
        #     entry_tags = [1, 4]
        # """
        # # need to
        # """
        #     new_entry.tags = [tagId1, tagId2]
        #     each entry_tag in entry_tags
        #         id, entry_id, tag_id // where entry_id = new_entry.id
        # """
        # - remove entry_tags that are no longer correct
        # '''
        #     iterate over new_entry.tags
        #         each step iterate over entry_tags to compare
        #         add ones that don't exist?
        # '''
        for tag_id in new_entry["tags"]:
            found = False
            for entry_tag in entry_tags:
                if entry_tag["tagId"] == tag_id:
                    found = True
            if found:
                pass
            else:
                create_entry_tag(new_entry["id"], tag_id) 

        # - add entry_tags that are new
        # '''
        #     iterate over entry_tags
        #         each step iterate over new_entry.tags to compare
        #         delete ones that don't exist?
        # '''
        for entry_tag in entry_tags:
            found = False
            for tag_id in new_entry["tags"]:
                if entry_tag["tagId"] == tag_id:
                    found = True
            if found:
                pass
            else:
                delete_entry_tag(entry_tag["id"]) 
        # - do nothing if entry_tag relationship already exists
