def timestamp_to_seconds(timestamp):
    h, m, s = timestamp.split(":")
    s = s.split(".")[0]
    seconds = int(h) * 60 * 60 + int(m) * 60 + int(s)
    return seconds
