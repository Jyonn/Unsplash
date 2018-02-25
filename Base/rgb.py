""" Adel Liu 180223

#RGB字符串转化为RGB类
"""


class RGB:
    hex_base = '0123456789ABCDEF'

    @classmethod
    def switch_hex_to_dec(cls, s):
        ans = 0
        for i, c in enumerate(s):
            if c not in cls.hex_base:
                s[i] = '0'
            ans = (ans << 4) + cls.hex_base.index(s[i])
        return ans

    def __init__(self, s):
        if s[0] == '#':
            s = s[1:]
        s = s[:6]
        s = s.upper()
        s += '0' * (6-len(s))
        self.R = self.switch_hex_to_dec(s[0:2])
        self.G = self.switch_hex_to_dec(s[2:4])
        self.B = self.switch_hex_to_dec(s[4:6])
        self.RGB = [self.R, self.G, self.B]
        self.s = '#%s' % s

    @classmethod
    def dist(cls, c1, c2):
        if not isinstance(c1, RGB):
            return 0xffff
        if not isinstance(c2, RGB):
            return 0xffff
        return pow(c1.R - c2.R, 2) + pow(c1.G - c2.G, 2) + pow(c1.B - c2.B, 2)

    def __str__(self):
        return self.s
