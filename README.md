# PornAnalizer
PornAnalizer is a script which analyzes the frequency of keywords in Pornhub's 
top rated videos. It currently analyzes words from the first 30 pages of the
top rated section. The data is then displayed using d3 to produce a word cloud.

## Running
Make sure you have Python 3 installed then simply run `./pornAnalizer.py`
This will produce a file called results.csv. Now host a webserver, perhaps run 
`python3 -m http.server` and navigate to it. The word cloud will display after
a few seconds (depending on the size of your data).

## CSV Format
The CSV Format is 'size,text' where size corresponds to the size of the text and
text is the actual word being displayed. The header names are irrelevant, but a
header line must be present. Running `./pornAnalizer.py` will produce a csv 
file with the correct format.

## Isn't This Gross and Amoral?
That's a matter of opinion. I personally find the results interesting.
However, if this data truly repulses you please look somewhere else.

## Screenshots
![screenshot](/res/word_bubble.png)
