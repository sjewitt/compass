# this needs to be typed properly, as this is of the form:
# [{title:str, ...}]
def get_sector_title_from_data(title_data:list) -> str:
    _title = ""
    for item in title_data:
        _title += item["title"] + " "
    return _title.strip()
