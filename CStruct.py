# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 19:40:57 2016

@author: Christophe
"""

import struct, collections

class CStruct(object):

    def __init__(self, typename, format_defn, lead_char="!"):
        self.names = []
        fmts = [lead_char]
        for line in format_defn.splitlines():
            name, fmt = line.split()
            self.names.append(name)
            fmts.append(fmt)
        self.formatstr = ''.join(fmts)
        self.struct = struct.Struct(self.formatstr)
        self.named_tuple_class = collections.namedtuple(typename, self.names)

    def object_from_bytes(self, byte_str):
        atuple = self.struct.unpack(byte_str)
        return self.named_tuple_class._make(atuple)

if __name__ == "__main__":
    # do this once
    pkt_def = """\
        u1 B
        u2 H
        u4 I"""
    cs = CStruct("Packet1", pkt_def)
    # do this once per incoming packet
    o = cs.object_from_bytes(b"\xF1\x00\xF2\x00\x00\x00\xF4")
    print(o)
    print(o.u4)