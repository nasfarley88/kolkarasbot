import os
import re
from urllib.request import urlopen
from fuzzywuzzy import process
from fuzzywuzzy.fuzz import WRatio, ratio
"""Functions that probe the wiki and produce results. """

def filename_to_lore_cmd(filename):
    return "/lore_{}".format(
        (
            filename
            .replace("-", "_")
            .replace(".md", "")
        ))

def lore_cmd_to_filename(cmd):
    return "{}.md".format(
        (
            cmd
            .replace("/lore_", "")
            .replace("_", "-")))


def get_all_entries(location):
    entries = set(os.listdir("wiki/{}".format(location)))
    exclude_entries = {"Lore.md", "_Footer.md", "_Header.md", "_Sidebar.md"}
    entries = entries.difference(exclude_entries)

    return entries

def filename_to_name(filename):
    return (filename
            .replace("-", " ")
            .replace(".md", ""))

# TODO change to a make this a 'view' which takes entries and a header. Then
# get_index will just view all entries. This will also allow for paging, if
# this is ever needed.
async def get_index():
    """Get index from the wiki. """
    # TODO think seriously about whether I want the url here
    raw_entries = get_all_entries("lore")
    entries = ["> {} \n        - {}".format(
        "{name} (<a href=\"{url}\">view</a>)".format(
            url=construct_url_from_path("wiki/lore/"+x),
            name=filename_to_name(x)
        ), filename_to_lore_cmd(x)) for x in raw_entries]
    entries.sort()

    output_string = "<b>Index:</b>\n{}".format("\n".join(entries))

    return output_string

def markdown_to_telegram(markdown):
    # Change bullet points
    data = re.sub(r" ?\* ", r"- ", markdown)

    # Bold up links
    data = re.sub(r"\[(.*?)\]\(.*?\)", r"*\1*", data)

    # Remove formatting for tags
    data = re.sub(r"\[\[(.*?)\]\]", r"\1", data)

    return data

# TODO make markdown_to_html function
# will include:
# [[http://abasdf.dshfsd]] becomes <a...> </a>
# [[tag]] becomes point to special page
# [abd](abd) is bold, maybe with list of commands to search references at the end of the 'document'?


def fuzzy_search_results(search_term, location="lore"):
    def custom_match(s1, s2):
        """A custom matching function which weights strings which match ratio.

        Check the code."""

        main_match = 100*WRatio(s1, s2)
        ratio_match = ratio(s1, s2)

        return main_match + ratio_match

    return process.extract(
        search_term,
        get_all_entries(location),
        scorer=custom_match)

def fuzzy_search(*args, **kwargs):
    return fuzzy_search_results(*args, **kwargs)[0][0]

def construct_url_from_path(path):
    """Constructs url for wiki from path. """
    base_url = get_wiki_address()
    formatted_path = (path
                      .replace("wiki/", "")
                      .replace(".md", ""))
    return base_url+formatted_path

def get_wiki_address():
    ip = urlopen('http://ip.42.pl/raw').read().decode('utf-8')
    return "http://{}:4567/".format(ip)
