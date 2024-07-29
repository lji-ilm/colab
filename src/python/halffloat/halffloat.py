from numpy import float16
from bitstring import BitArray

class halffloat:
    CBACK = "\033[40m"
    CRED    = '\33[31m'
    CCYAN = '\33[36m'
    CMAGENTA = '\33[35m'
    CGREEN  = '\33[32m'
    CBLUE   = '\33[34m'
    CEND      = '\33[0m'

    def __init__(self, v, LITTLE_ENDIAN=True):
        assert type(v) == float16
        self._updateValue(v)

    def _updateValue(self, v):
        self._v = v
        self._bytes = v.tobytes()
        self._hex = self._bytes.hex().upper()
        self._bits = BitArray()

        if LITTLE_ENDIAN:
            self._lo = self._bits[:8]
            self._hi = self._bits[8:]
        else:
            self._hi = self._bits[:8]
            self._lo = self._bits[8:]

    def __str__(self):
        hexstr = "0x" + self._hex
        return (str(v) 
                + hexstr 
                + "|"
                + self.CCYAN
                + self._hi[0]
                + self.CBLUE
                + self._hi[1:6]
                + self.CRED
                + self._hi[6:]
                + " "
                + self._lo
                + self.CEND)
