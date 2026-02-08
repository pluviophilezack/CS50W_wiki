import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


# The optional parameter "original_title" is the file that is going to be edited in the scenario of edit_page() 
def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def edit_entry(original_title, edited_title, edited_content):
    """
    Edit an encyclopedia entry. original_title help this function find the original file.
    The function delete the original file anyway and replace it with edited_title and edited_content.
    """
    original_filename = f"entries/{original_title}.md"
    if default_storage.exists(original_filename):
        default_storage.delete(original_filename)
    edited_filename = f"entries/{edited_title}.md"
    default_storage.save(edited_filename, ContentFile(edited_content))
    




def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
