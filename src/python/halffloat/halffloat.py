from numpy import float16
from bitstring import Bits, BitArray

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
        self._LITTLE_ENDIAN = LITTLE_ENDIAN
        self._updateValue(v)        

    def _updateValue(self, v):
        self._v = v
        self._bytes = v.tobytes()
        self._hex = self._bytes.hex().upper()
        self._bits = Bits(self._bytes)

        if self._LITTLE_ENDIAN:
            self._lo = self._bits[:8]
            self._lostr = self._bits.bin[:8]
            self._hi = self._bits[8:]
            self._histr = self._bits.bin[8:]
        else:
            self._hi = self._bits[:8]
            self._histr = self._bits.bin[:8]
            self._lo = self._bits[8:]
            self._lostr = self._bits.bin[8:]

    @property
    def negative(self):
        return self._hi[0]
    
    @property
    def exponent(self):
        return self._hi[1:6].unpack("uint:5")[0]
    
    def _unpack_binary_fraction(self, b, length):
        current_frac = 0.5
        step = 0.5
        sum = 0
        for i in range(length):
            if b[i]:
                sum = sum + current_frac
            current_frac = current_frac * step
        return sum
        
    @property
    def mantissa(self):
        m = BitArray(self._lo)
        m.prepend(self._hi[6:8])
        return self._unpack_binary_fraction(m, len(m))

    @property
    def significand(self):
        return self.mantissa + 1
    
    @property
    def power(self):
        return self.exponent - 15
    
    @property
    def formula(self):
        fo = f"2^{self.power}*(1+{self.significand})"
        if self.negative:
            fo = "-1*" + fo
        fo = f"{self._v} = " + fo
        return fo

    @property
    def hex_and_bits(self):
        hexstr = "0x" + self._hex
        return (str(self._v)
                + " " 
                + hexstr 
                + "|"
                + self.CCYAN
                + self._histr[0]
                + self.CBLUE
                + self._histr[1:6]
                + self.CRED
                + self._histr[6:]
                + " "
                + self._lostr
                + self.CEND)

    def __str__(self):
        return self.hex_and_bits
