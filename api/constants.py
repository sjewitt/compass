'''
Constants for mapping compass indexes to strings.
This for use when a competency map for user is downloaded,
so they get more than just a bunch of numbers...

These are the same as in the client-side JS code.
'''

COMPASS_MAPPER = [
    { "quadrant": "Product & service design","sectors":["Ideas & concepts","Prototypes & experiments","UX design","Visual design","Service design"] },
    { "quadrant": "Management & leadership","sectors":["Client & account management","Commercials","Agile PM/coaching","Facilitation"] },
    { "quadrant": "Capability building","sectors":["Innovation capabilities","Leadership readiness","Mentoring & coaching","Innovation training"] },
    { "quadrant": "Transforming organisations","sectors":["Strategy & vision","Culture & experience","Business design & growth","Customer insights"] },
]

RATING_MAPPER = [
    { 'title': 'unrated' },
    { 'title': 'Competely unfamiliar'},
    { 'title': 'Novice'},
    { 'title': 'Foundation'},
    { 'title': 'Competent'},
    { 'title': 'Advanced'},
    { 'title': 'Master'},
]
