from pathlib import Path
import bitstring
import argparse
import shutil


# bitstring.BitArray("0b"+f"{0x40:014b}"+f"{0x19:06b}"+f"{0x6:04b}").bytes


def read_cuefile(cuefile):
    liste= []
    with open(cuefile) as f:
        for l in f:
            min,sec,fr = l.split(":")
            liste.append(int(min)*60+int(sec)+int(fr)/75)
    return liste        

def convert(gr):
    cluster = gr // (32 * 11)
    gr %= (32 * 11)
    sector = gr // 11
    gr %= 11
     
    return (cluster, sector, gr)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cuefile", nargs='?')
    parser.add_argument("binfile", nargs='?')
    # parser.add_argument("outfile", nargs='?')
    args = parser.parse_args()

    seconds = read_cuefile(Path(args.cuefile))
    groups = [round(a *  88200/512) for a in seconds]
    start = [convert(a+17600) for a in groups]
    end = [convert(a+17600-1) for a in groups[1:]]
    end.append((0,0,0))

    start_enc = [bitstring.BitArray("0b"+f"{a[0]:014b}"+f"{a[1]:06b}"+f"{a[2]:04b}").bytes for a in start]
    end_enc = [bitstring.BitArray("0b"+f"{a[0]:014b}"+f"{a[1]:06b}"+f"{a[2]:04b}").bytes for a in end]

    for i in range(10):
        backupfile = Path(args.binfile+".bak"+str(i)).absolute()
        if not backupfile.exists():
            shutil.copy2(Path(args.binfile).absolute(), backupfile)
            break
        
    with open(Path(args.binfile), 'r+b')  as f:
        f.seek(0x13c) # Find location of end of track
        last_track  = f.read(3)
        end_enc[-1] = last_track

        f.seek(0x1f) # Write new number of tracks
        f.write(len(end_enc).to_bytes(1,byteorder='big'))

        f.seek(0x31) # Write links to track fragment map, 1 to number of tracks
        f.write(bytes(range(1,len(start_enc)+1)))
        # start_pos = 0x130
        l = b''
        track =b''
        for a,b in zip(start_enc,end_enc):
            l = l + a + bytes.fromhex('a6')+b +  bytes.fromhex('00') # Create track fragment map
            track = track + bytes.fromhex('00')*6 + bytes.fromhex('01')+ bytes.fromhex('20') # Create timestamps map
        
        # f.seek(0x92f) # Do something weird because the freemap is not linking to 0. Omit.
        # lastref = int.from_bytes(f.read(1),byteorder='big')
        # if lastref != 0:
        #     f.seek(lastref*8 + 0x130)
        #     last_fragment = f.read(7)
        #     l = l + last_fragment
        #     f.seek(0x92f)
        #     f.write((len(end_enc) + 1).to_bytes(1,byteorder='big'))
        
        f.seek(0x2f)
        if not int.from_bytes(f.read(1),byteorder='big') == 255:
            f.seek(0x2f) # Write next free track, which is number of tracks + 1
            f.write((len(end_enc)+1).to_bytes(1,byteorder='big'))

        f.seek(0x138) # Write the track fragment map
        f.write(l)


        f.seek(0x128f) # Write next free timestamp slot, should be unnecessary.
        f.write((len(end_enc)+1).to_bytes(1,byteorder='big'))

        f.seek(0x1290) # Write track junction map, should be unnecessary.
        f.write(bytes(range(len(start_enc))))

        f.seek(0x1390) # Write timestamps map, should be unnecessary.
        f.write(track)