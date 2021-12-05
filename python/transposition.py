def transpose(clear, t, spaces=False):
    clear = clear if spaces else clear.replace(" ", "")
    secret = [""]*t
    for i in range(len(clear)):
        secret[i % t] += clear[i]
        print(f"{i % t}: {clear[i]}")
    print(secret)
    return "".join(secret)


def zigzag(clear, t, spaces=False):
    clear = clear if spaces else clear.replace(" ", "")
    secret = [""]*t
    for i in range(len(clear)):
        minimum = min([-(i % -(2*t-2)), i % (2*t-2)])
        secret[minimum] += clear[i]
    return "".join(secret)


print(zigzag("DiesIstEineGeheimeBotschaft", 4, spaces=False))
