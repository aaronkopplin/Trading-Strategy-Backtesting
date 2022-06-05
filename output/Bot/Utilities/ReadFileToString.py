def read(filename: str) -> str:
    # open text file in read mode
    text_file = open(filename, "r")

    # read whole file to a string
    data = text_file.read()

    # close file
    text_file.close()

    return data
