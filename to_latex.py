#!/usr/bin/python3
from os import listdir
from os.path import isfile, join
from io import StringIO
from collections import OrderedDict
from sys import stderr
import re
import csv

# indentation and spacing
SONG_NUMBER_SEP = "\\hspace{2pt}"
SONGTITLE_INDENT = "20pt"
SONGTITLE_PRE_SKIP = "\\vspace{5pt}"
SONGTITLE_POST_SKIP = "\\[6pt]"
VERSE_SKIP = "10pt"


def index_hack(name):
    """Hack indexing to work with åäö."""
    prefix = name
    prefix = re.sub("[åÅ]", "zza", prefix, re.U)
    prefix = re.sub("[äÄ]", "zzb", prefix, re.U)
    prefix = re.sub("[öÖ]", "zzc", prefix, re.U)
    return prefix + "@" + name


def line_hack(line, is_line=True):
    """Replace problematic characters with latex commands."""
    if line is None:
        return line
    line = line.replace("#", "\\#")
    line = line.replace("%", "\\%")
    line = line.replace("_", "\\_")
    line = line.replace("&", "\\&")
    line = line.replace("|", "\\|")
    line = line.replace("@", "\\@")
    line = line.replace("$", "\\$")
    line = line.replace("€", "\\euro{}")
    line = line.replace("+", "\\texttt{+}")
    line = line.replace(";,;", ":,:")
    line = line.replace(";:;", ":,:")
    line = line.replace(";.;", ":,:")
    line = line.replace(":;:", ":,:")

    if not is_line:
        return line

    # place :,: and # modifiers before line start
    if line.startswith(":,:"):
        line = "\\hspace{0pt-\\widthof{:,: }}" + line
    if line.startswith("\\# :,:"):
        line = "\\hspace{0pt-\\widthof{\\# }-\\widthof{:,: }}" + line
    elif line.startswith("\\# "):
        line = "\\hspace{0pt-\\widthof{\\# }}" + line
    elif line.startswith("A: "):
        line = "\\hspace{0pt-\\widthof{A: }}" + line
    elif line.startswith("B: "):
        line = "\\hspace{0pt-\\widthof{B: }}" + line
    if line:
        line += "\\\\"
    return line


def generate_song(data):
    out = []

    title = line_hack(data["title"], False)
    melody = line_hack(data["melody"], False)
    lyrics = data["lyrics"]
    index = line_hack(str(data["number"]), False)

    out.append("%")
    out.append("% " + title)
    out.append("%")
    # set the section name to show in header
    out.append(("\\sectionmark{{ {0}. }}%").format(index))

    # wrap title and first verse in the same minipage to prevent pagebreak between them
    out.append("\\noindent\\begin{minipage}{\\linewidth}")
    out.append(SONGTITLE_PRE_SKIP)

    # song number offset by correct amount
    out.append("{{\\large\\bf {0}.{1}}}"
        .format(index, SONG_NUMBER_SEP, SONGTITLE_INDENT))

    # song title in parbox for line wrapping
    t = "\\parbox[t]{{0.85\\linewidth}}{{\\raggedright {{\\large\\bf {}}}".format(title)
    if melody is not None:
        t += "\\\\[2pt]\\small\\emph{{{0}}}\\{1}}}".format(melody, SONGTITLE_POST_SKIP)
    else:
        t += "\\{0}}}".format(SONGTITLE_POST_SKIP) # close \leftline\parbox
    out.append(t)

    # add index entry for title and any alternate titles
    for name in [title] + data["alternate_titles"]:
    	out.append("\\index{{{}}}".format(index_hack(name)))

    first = True

    for verse in lyrics:
        # start a new minipage if not the first verse
        if not first:
            out.append("\\noindent\\begin{minipage}{\\linewidth}")
        else:
            first = False

        # wrap lines in verse block
        out.append("\\begin{verse}")
        for line in verse:
            out.append("\t" + line_hack(line))
        out.append("\\end{verse}")

        # close minipage and add verse spacing
        out.append("\\end{minipage}\\\\[" + VERSE_SKIP + "]")

    if (data["story"]):
        out.append("\\emph{{ {0} }}\\\\[{1}]"
          .format(line_hack(data["story"]), VERSE_SKIP))

    return "\n".join(out)


def main(order_file, songs_file):
    order = OrderedDict()

    with open(order_file, "r", newline="") as f:
        f.readline()
        for row in csv.reader(f):
            for i, a in enumerate(row):
                row[i] = a.strip()

            if len(row[4]):
                alts = []
                for i in csv.reader(StringIO(row[4])):
                    for j in i:
                        alts.append(j)
            else:
                alts = []

            if row[5] in order:
                print("There is already a song with id: \"{}\".".format(row[5]), file=stderr)
                continue

            order[row[5]] = {
                "number": row[0] if len(row[0]) else None,
                "title": row[3],
                "melody": row[9],
                "alts": alts,
                "story": row[12]
            }

    lyrics = {}
    with open(songs_file, "r", newline="") as f:
        f.readline()
        for row in csv.reader(f):
            lines = row[1].split("\n")
            lines = [i.strip() for i in lines]
            lines = "\n".join(lines)
            lines = lines.split("\n\n")
            lines[:] = [i.split("\n") for i in lines]
            lyrics[row[0].strip()] = lines

    count = 0
    data = []

    for i, d in order.items():
        if i not in lyrics:
            print("\"{}\" doesn't have lyrics.".format(i), file=stderr)
            continue

        if d["number"] is None:
            number = count
        else:
            number = d["number"]
        count += 1

        title = d["title"]
        melody = d["melody"] if len(d["melody"]) else None

        data.append({
            "title": d["title"],
            "alternate_titles": d["alts"],
            "number": number,
            "melody": "(" + d["melody"] + ")" if len(d["melody"]) else None,
            "lyrics": lyrics[i],
            "story": d["story"]
        })

    for i in data:
        print(generate_song(i))

if __name__ == "__main__":
    from sys import argv
    main(argv[1], argv[2])
