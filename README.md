# tkt-laulut
Laulattaako? No hätä, käpistelijät auttavat.

* Step 0: Install python >=3.4 and texlive-full
* Step 1: run `make`
* Step 2: ???
* Step 3: Profit!

# Data
All lyrics and ordering and everythingelse is within
two csv files, `lyrics.csv` and `ordering.csv`.

The first line of these files is the header, and is skipped.
It should also tell quite well what to put in to the column.

# Song format
* Seperate verses with a single empty line.
* Use `:,: ` to signify a repeated part of a song
    (see `drunken_sailor` and many others).
* `# ` can be used to signify foresinger or similiar
    (see `kalmarevisan`).
* Songs with lots of very similiar verses,
    don't write every verse completely
    (see `henkilokunta`, and `kun_mä_kuolen` and many others).
* Extra directions usually inside parentheses.

# LaTeX
* Be careful with non-ascii non-finnish characters,
    they'll probably break the build.
* Be careful with math characters,
    they need to be surrounded with \( \).
