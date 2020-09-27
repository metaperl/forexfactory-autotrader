

def mygen(i):

    for v in i:
        if v < 5:
            yield v


if a := mygen([12,34,5]):
    print(a)

