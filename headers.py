FIELDS_TO_HEADERS = {
    "server": "server",
    "name": "nume",
    "rank": "rank",
    "lp": "lp",
    "link": "link",
    "winrate": "winrate",
    "toprate": "top4",
    "played": "nr. meciuri",
    "wins": "wins",
    "tops": "nr. top4",
}

DISPLAYED_HEADERS = {
    "server": "Server",
    "nume": "Nume",
    "rank": "Rank",
    "lp": "LP",
    "link": "Link",
    "winrate": "Winrate",
    "top4": "Top4",
    "nr. meciuri": "Nr. Meciuri",
    "wins": "Wins",
    "nr. top4": "Nr. Top4",
}

HEADERS_TO_FIELDS = {v: k for k, v in FIELDS_TO_HEADERS.items()}