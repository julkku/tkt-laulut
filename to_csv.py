import glob
import csv

def norm_name(s):
    out = []
    in_name = False

    for i in reversed(s):
        if i == ".":
            in_name = True
            continue
        if i == "/":
            break
        if in_name:
            out.append(i)

    return "".join(reversed(out)).lower()


def split_song(s):
    has_title = False
    title = ""
    has_melody = False
    melody = ""
    lyrics = []

    in_lyrics = False

    for line in s.split("\n"):
        if len(line.strip()) == 0 and not in_lyrics:
            in_lyrics = True
            continue
        if in_lyrics:
            lyrics.append(line)

        if not has_title:
            has_title = True
            title = line.strip()
        elif not has_title:
            has_melody = True
            melody = line.strip()

    return "\n".join(lyrics), title, melody

def main():
    with open("songs.csv", "w", newline="") as out:
        c = csv.writer(out)
        for path in glob.glob("songs/*.txt"):
            with open(path, "r") as file:
                song, title, melody = split_song(file.read())
                c.writerow((norm_name(path), song, title, melody))

if __name__ == "__main__":
    main()
