# tkt-laulut
Laulattaako? No hätä, käpistelijät auttavat.

Super Virallinen IRC: #tkt-laulut (@IRCnet)

* Step 0: Install python >=3.4 and texlive-full
* Step 1: run `./build.sh`
* Step 2: ???
* Step 3: Profit!

# Song format
All songs must be inside songs directory (no subdirectories), one song per file.

* First line, songs name
* Seconds line, melody of the song (may be left empty)
* Rest of the lines, lyrics of the song
  * Seperate verses with a single empty line
  * Empty lines at beginning and end are ignored
  * Use `:,:` to signify a repeated part of a song (see `drunken_sailor.txt` and many others)
  * Use `# ` to signify foresinger or similiar (see `kalmarevisan.txt`)
  * Songs with lots of very similiar verses,
    don't write every verse completely (see `henkilokunta.txt`, and `kun_mä_kuolen.txt` and many others)
  * Extra directions inside usually inside parentheses

# Ordering format
* CSV with optional quoting (aka. excel style)
* Column 0, song number if special, empty otherwise
* Column 1, song file without .txt
* Column 2+, Alternative names for the song (used in index)

# How to help
`Fork -> Add songs -> Pull Request`

Always remember to first check if a song exists, before adding it.
Alternative names can be added to the ordering file.

# Song requests
* ???
