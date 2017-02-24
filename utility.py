
# http://stackoverflow.com/a/9475354/2601448
def split_string(line, n):
    return [int(line[i:i+n]) for i in range(0, len(line), n)]
