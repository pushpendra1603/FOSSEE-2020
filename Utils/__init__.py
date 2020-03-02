def __getUniqueId():
    i = 1
    while True:
        yield i
        i += 1


circleId = __getUniqueId()
lineId = __getUniqueId()
