def main():
    print(trim_html('https://g.redditmedia.com/oJxcIX_hs5tQroxsY5d4VK0zCvPp0r4YUzPURkuhCXY.gif?w=728&fm=mp4&mp4-fragmented=false&s=965a8f95402db8b8b1f14c80616592e6'))

def trim_html(in_):
    out = in_
    if in_.split('.gif', 1)[0] != in_:
        out = in_.split('.gif', 1)[0] + '.gif'
    if in_.split('.jpg', 1)[0] != in_:
        out = in_.split('.jpg', 1)[0] + '.jpg'
    if in_.split('.png', 1)[0] != in_:
        out = in_.split('.png', 1)[0] + '.png'
    return out

if __name__ == "__main__":
    main()
