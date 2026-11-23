"""News data for THE HORIZON, Monday 23 November 2026.

Every item below was checked against live reporting dated
23 November 2026 (BBC, Reuters via syndication, and Indian
morning papers carrying the day's wires) on the morning of
23 November 2026, Singapore time. No item is older than the
date on the masthead.
"""

DATE_LINE = "MONDAY 23 NOVEMBER 2026"
MASTHEAD = "THE HORIZON"
TAGLINE = "THE WORLD IN ONE PAGE"

LEAD = {
    "kicker": "CLIMATE  |  COP31, TURKIYE",
    "headline": "NO DEAL AT COP31",
    "deck": "Climate summit ends without agreement as final draft drops any mention of fossil fuels",
    "body": [
        "The COP31 climate summit in Turkiye has formally come to an end after countries failed to agree a deal. The final draft text did not contain the words 'fossil fuels' at all, the very cause of the warming the talks were meant to confront.",
        "Negotiators left with no consensus on phasing out oil, gas and coal, and no new finance package for the countries hit hardest. Campaigners called it a failure of nerve; the talks will have to resume at the next round.",
    ],
}

STORIES = [
    {
        "kicker": "UKRAINE",
        "headline": "14 missing after drone hits homes near Kyiv",
        "body": "At least 14 people were missing after a Russian drone hit a residential building in the Kyiv region, President Zelenskiy said. Rescue teams searched the rubble through the night.",
    },
    {
        "kicker": "INDONESIA",
        "headline": "Factory fire kills three, dozens missing",
        "body": "At least three people were killed and 36 were still missing after a fire at a confectionery factory in Indonesia. Families gathered outside as firefighters searched the gutted building.",
    },
    {
        "kicker": "SOUTH KOREA",
        "headline": "Minister quits over AI exam-cheating scandal",
        "body": "South Korea's education minister has resigned amid a scandal over AI-driven cheating in exams, after candidates were found using artificial intelligence tools to beat the tests.",
    },
    {
        "kicker": "MEXICO",
        "headline": "Cartel boss 'El Chapo Isidro' captured",
        "body": "Mexican authorities captured FBI most-wanted cartel boss 'El Chapo Isidro' after firefights in Sinaloa that left 11 people dead.",
    },
    {
        "kicker": "UNITED NATIONS",
        "headline": "Talks on lethal AI weapons to go on",
        "body": "Nations agreed at a United Nations conference to continue negotiations on lethal autonomous weapons systems, keeping alive efforts to set rules for machines that choose their own targets.",
    },
    {
        "kicker": "PORTUGAL",
        "headline": "Thousands march in Lisbon over cost of living",
        "body": "Thousands of people marched in Lisbon as anger over the cost of living boiled over, demanding action on rents, wages and food prices.",
    },
]

BRIEFS = [
    ("NEPAL-INDIA", "Nepal PM Balendra Shah holds talks with PM Modi in New Delhi."),
    ("SHIPPING", "A Russian cargo ship burns off Finland after an attack; a blast on a Russian ship at a Libya port was likely a drone strike."),
    ("SPORT", "India post a record 720 for 9 declared in the Wellington Test against New Zealand."),
    ("MIDDLE EAST", "Israel's opposition leader condemns settler arson attacks in the West Bank as 'Jewish terrorism'."),
]

NUMBERS = [
    ("14", "missing in Kyiv region after drone strike"),
    ("36", "still missing after Indonesian factory fire"),
    ("11", "dead in Sinaloa firefights as cartel boss is seized"),
    ("0", "mentions of 'fossil fuels' in the COP31 final draft"),
]

FOOTER = "Sources: BBC World, Reuters wires, Indian morning papers, 23 November 2026. One page, one day, the whole world."
