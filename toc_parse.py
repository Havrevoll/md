from pathlib import Path
import bitstring
import argparse
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("binfile", nargs='?')
    args = parser.parse_args()


    with open(Path(args.binfile), 'rb')  as f:

        # Information we need:
        # - Location of freemap
        # - Number of tracks
        # - Next free track
        # - a map of each track: A list of fragments for each track. And the type (SP, SP Mono, LP2 or LP4). So a list of lists. Or a linked list? Too primitive or convenient?
        #       - Sum the track fragments to find the total length of each track.
        # - A corresponding list of each track name and disc name.
        # A list of all 255 positions in fragment map. Which is free, which is taken? A function that returns the next free fragment?
        # What if a track consists of several fragments, one of them being 20 seconds long? What if I split the track in the middle of that fragment? But Track fragments are a different map than the audio fragments.

        # Do: Read a cue file and find the information about each track's position.
        # 

        f.seek(0x30) # Find location of freemap
        freemap = f.read(1)

        f.seek(0x13b)
        code = f.read(1) # Read the type of track. Will be 0xA6 if it is SP stereo, 0xA2 if it is LP2.

        f.seek(0x13c) # Find location of end of track
        end_enc[-1] = f.read(3)
        

        f.seek(0x1f) # Write new number of tracks
        f.write(len(end_enc).to_bytes(1,byteorder='big'))

        f.seek(0x31) # Write links to track fragment map, 1 to number of tracks
        f.write(bytes(range(1,len(start_enc)+1)))
        # start_pos = 0x130
        l = b''
        track =b''
        for a,b in zip(start_enc,end_enc):
            l = l + a + code + b +  bytes.fromhex('00') # Create track fragment map
            track = track + bytes.fromhex('00')*6 + bytes.fromhex('01')+ bytes.fromhex('20') # Create timestamps map