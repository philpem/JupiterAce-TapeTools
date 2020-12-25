#!/usr/bin/env python3
#
# tzx2tap.py: Jupiter Ace TZX to TAP converter
#
# Converts TZX files into Jupiter Ace TAP files, which MAME's castool tool can
# convert into WAV files.
#
# Phil Pemberton <philpem@philpem.me.uk>, 25 Dec 2020
#
# Licence: MIT
#

import struct
import sys

class TzxHeader:
    LEN = 10
    def __init__(self, data):
        (sig, major, minor) = struct.unpack_from('<8sbb', data)
        if sig != b'ZXTape!\x1a':
            raise ValueError("TZX data does not contain a valid header")
        self.major_rev = major
        self.minor_rev = minor

    def __repr__(self):
        return "<TZX header version %u.%u>" % (self.major_rev, self.minor_rev)


if len(sys.argv) != 2:
    print("syntax: %s filename" % sys.argv[0], file=sys.stderr)
    sys.exit(1)

datablocks = []

with open(sys.argv[1], 'rb') as f:
    # Read and print the TZX header
    hdr = TzxHeader(f.read(TzxHeader.LEN))
    print(hdr)

    # Read all the blocks in the file
    while True:
        # Format is a block ID, then an arbitrary-format block
        # Unfortunately this means that to skip a block, you need to know its format...
        # ... thankfully Ace TZXes are mostly just description, hwtype and data blocks.
        blkid = f.read(1)
        if len(blkid) == 0:
            break
        blkid = ord(blkid)

        if blkid == 0x10:
            # BLKID 10: Standard speed data block
            pause, datalen = struct.unpack_from('<HH', f.read(4))
            datablk = f.read(datalen)
            print("Standard-speed data: %u bytes, post-pause %u ms" % (datalen, pause))
            datablocks.append(datablk)
        elif blkid == 0x30:
            # BLKID 30: text description
            desclen = ord(f.read(1))
            description = str(struct.unpack_from('%ss'%desclen, f.read(desclen))[0])
            print("Description: ", description)
        elif blkid == 0x33:
            # BLKID 33: hardware type
            nhwids = ord(f.read(1))
            print("Hardware information: %u records" % nhwids)
            hwids = []
            for i in range(nhwids):
                hty, hid, hinf = struct.unpack_from('<bbb', f.read(3))
                print("   Hardware type %u, id %u, flag %u" % (hty, hid, hinf))
        else:
            raise ValueError("Invalid block id %x" % blkid)

# Write all known datablocks to a file
with open(sys.argv[1].replace('.tzx', '.tap'), 'wb') as f:
    for b in datablocks:
        # TAP files don't include the block type byte, but TZX files do -- so drop it
        b = b[1:]
        f.write(struct.pack('<H%ss' % len(b), len(b), b))

