# TOC-split

## Introduction

A script for split a single track into multiple gapless tracks on a Minidisc.

## Procedure

1. If you have the album as several files, join them with shntool:
   1. `shntool join .flac -o wav`
   2. `shntool cue *.flac | cuebreakpoints -i cue >joined.cue `
   3. If you plan to record in SP mode and the recording is too long, you can shave it down to the maximum length with: `shntool split -l 74:58`
2. If you already have the album as one file and one cue file (named album.cue in this example), extract the timing information with: `cuebreakpoints album.cue > album_times.cue`
3. Add the album as one track with Web MiniDisc Pro (https://web.minidisc.wiki).
4. Enter Homebrew mode and download the TOC binary file.
5. run the script: `python3 toc.py toc.bin album.cue`
   - A backup of the original bin file is automatically created. If something goes wrong, you can always revert to that. 
6. Upload the newly updated TOC binary file and reset the MD recorder by removing the USB cable and the battery/power cable as instructed when you entered homebrew mode.
7. Now the continuous track has been split, and you can continue with naming the tracks using the normal method by exporting the TOC as csv file outside homebrew mode. 

## To do
- Automatic track titles from the cue file.

Suggestions, corrections and error reports are welcome!