import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from unicodedata import normalize
from markdown2 import Markdown


def do_strings_match(x, y):
    """
    Returns True if they match (by Zeb)
    """
    x, y = get_normalized_strings(x, y)
    if x == y:
        return True
    else:
        return False


def get_normalized_strings(x, y):
    """
    Returns processed strings to see if they match
    """
    x, y = normalize('NFKD', x.upper().lower()), normalize('NFKD', y.upper().lower())
    return x, y


def is_possible_match(x, y):
    x, y = get_normalized_strings(x, y)
    if x in y:
        return True
    

def list_entries():
    """
    Returns a list of all names of encyclopedia entries. 
    by cs50 staff
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    by cs50 staff.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    by cs50 staff.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def return_markdowned_content(title):
    """
    Converts md files into html. 
    Use {{ your_variable|safe }} in any html files that use said content. 
    """
    markdowner = Markdown()
    return markdowner.convert(get_entry(title))
