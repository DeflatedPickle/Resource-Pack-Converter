def modify_json(f):
    lines = []
    for line in f:
        if len(line) > 0:
            lines.append(line)
    return lines
