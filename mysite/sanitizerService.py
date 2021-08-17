def sanitize(dirtyString):
    """
            snaitize input string
            Replace <>'"\'\";()% with space.
    """
    if(dirtyString != None):
        dirtyString = dirtyString.replace("<", "")
        dirtyString = dirtyString.replace(">", "")
        dirtyString = dirtyString.replace("'", "")
        dirtyString = dirtyString.replace('"', "")
        dirtyString = dirtyString.replace("\\'", "")
        dirtyString = dirtyString.replace('\\"', "")
        dirtyString = dirtyString.replace("(", "")
        dirtyString = dirtyString.replace(")", "")
        dirtyString = dirtyString.replace(";", "")
        dirtyString = dirtyString.replace("%", "")
        dirtyString = dirtyString.replace("?", "")
        dirtyString = dirtyString.replace("|", "")
        dirtyString = dirtyString.replace(":", "")
        dirtyString = dirtyString.replace("~", "")
        dirtyString = dirtyString.replace("+", "")
        dirtyString = dirtyString.replace("-", "")
        dirtyString = dirtyString.replace("#", "")
        dirtyString = dirtyString.replace("&", "")
        dirtyString = dirtyString.replace("[", "")
        dirtyString = dirtyString.replace("]", "")
        dirtyString = dirtyString.replace("{", "")
        dirtyString = dirtyString.replace("}", "")

    cleanString = dirtyString

    return cleanString