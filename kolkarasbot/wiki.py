import os
from fuzzywuzzy import process
from fuzzywuzzy.fuzz import WRatio, ratio
"""Functions that probe the wiki and produce results. """

def get_all_entries(location):
    entries = set(os.listdir("wiki/{}".format(location)))
    exclude_entries = {"Lore.md", "_Footer.md", "_Header.md", "_Sidebar.md"}
    entries = entries.difference(exclude_entries)

    return entries

def filename_to_name(filename):
    return (filename
            .replace("-", " ")
            .replace(".md", ""))

async def get_index():
    """Get index from the wiki. """
    entries = get_all_entries("lore")
    entries = {
        filename_to_name(x) for x in entries}
    entries = ["- {}".format(x) for x in entries]
    entries.sort()

    output_string = "*Index:*\n{}".format("\n".join(entries))

    return output_string

def markdown_to_telegram(markdown):
    # Change bullet points
    data = re.sub(r" ?\* ", r"- ", markdown)

    # Bold up links
    data = re.sub(r"\[(.*?)\]\(.*?\)", r"*\1*", data)

    # Remove formatting for tags
    data = re.sub(r"\[\[(.*?)\]\]", r"\1", data)

    return data


def fuzzy_search(search_term, location="lore"):
    def custom_match(s1, s2):
        """A custom matching function which weights strings which match ratio.

        Check the code."""

        main_match = 100*WRatio(s1, s2)
        ratio_match = ratio(s1, s2)

        return main_match + ratio_match

    return process.extractOne(
        search_term,
        get_all_entries(location),
        scorer=custom_match)[0]
