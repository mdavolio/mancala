
# http://stackoverflow.com/a/9475354/2601448
def split_string(line, nth):
    """Split string every nth character"""
    return [int(line[i:i+nth]) for i in range(0, len(line), nth)]
