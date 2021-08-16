def sanitize(dirtyString):
    """
            snaitize input string
            Replace <>'"\'\";()% with space.
    """
    if(dirtyString != None):
        dirtyString = dirtyString.replace("%3C", "")
        dirtyString = dirtyString.replace("%3c", "")
        dirtyString = dirtyString.replace("<", "")  # %3C
        dirtyString = dirtyString.replace("%3E", "")
        dirtyString = dirtyString.replace("%3e", "")
        dirtyString = dirtyString.replace(">", "")  # %3E
        dirtyString = dirtyString.replace("%27", "")
        dirtyString = dirtyString.replace("'", "")  # %27
        dirtyString = dirtyString.replace("%22", "")
        dirtyString = dirtyString.replace('"', "")  # %22
        dirtyString = dirtyString.replace("%5C%27", "")
        dirtyString = dirtyString.replace("\\'", "")  # %5C
        dirtyString = dirtyString.replace("%5C%22", "")
        dirtyString = dirtyString.replace('\\"', "")
        dirtyString = dirtyString.replace("%28", "")
        dirtyString = dirtyString.replace("(", "")  # %28
        dirtyString = dirtyString.replace("%29", "")
        dirtyString = dirtyString.replace(")", "")  # %29
        dirtyString = dirtyString.replace("%3B", "")
        dirtyString = dirtyString.replace("%3b", "")
        dirtyString = dirtyString.replace(";", "")  # %3B
        dirtyString = dirtyString.replace("%25", "")
        dirtyString = dirtyString.replace("%", "")  # %25

    cleanString = dirtyString

    return cleanString

# string = "!@#$%^&*()_+~<>?:|"
# print(sanitize(string))
# !@#$^&*_+~?:|