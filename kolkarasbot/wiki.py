import os
"""Functions that probe the wiki and produce results. """

async def get_index():
    """Get index from the wiki. """
    entries = {
        (x.replace('.md', '')
            .replace('-', ' ')) for x in os.listdir("wiki/lore") }
    exclude_entries = {"Lore", "_Footer", "_Header", "_Sidebar"}
    entries = entries.difference(exclude_entries)
    entries = ["- {}".format(x) for x in entries]
    entries.sort()

    output_string = "*Index:*\n{}".format("\n".join(entries))

    return output_string
