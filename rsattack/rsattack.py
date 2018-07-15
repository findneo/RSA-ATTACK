# -*- coding: utf-8 -*-
# by https://findneo.github.io/

import gmpy2
import libnum
from Crypto.PublicKey import RSA
import ContinuedFractions, Arithmetic


def rsa_decrypt(e, c, p, q):
    phi = (p - 1) * (q - 1)
    n = p * q
    try:
        d = gmpy2.invert(e, phi)
        return pow(c, d, n)
    except Exception as e:
        print "e and phi are not coprime!"
        raise e


def rabin_decrypt(c, p, q, e=2):
    n = p * q
    mp = pow(c, (p + 1) / 4, p)
    mq = pow(c, (q + 1) / 4, q)
    yp = gmpy2.invert(p, q)
    yq = gmpy2.invert(q, p)
    r = (yp * p * mq + yq * q * mp) % n
    rr = n - r
    s = (yp * p * mq - yq * q * mp) % n
    ss = n - s
    return (r, rr, s, ss)


def common_modulus(n, e1, e2, c1, c2):
    """
    ref:
    ∵gcd(e1,e2)==1,∴由扩展欧几里得算法，存在e1*s1+e2*s2==1
    ∴m==m^1==m^(e1*s1+e2*s2)==((m^e1)^s1)*((m^e2)^s2)==(c1^s1)*(c2^s2)
    """
    assert (libnum.gcd(e1, e2) == 1)
    _, s1, s2 = gmpy2.gcdext(e1, e2)
    # 若s1<0，则c1^s1==(c1^-1)^(-s1)，其中c1^-1为c1模n的逆元。
    m = pow(c1, s1, n) if s1 > 0 else pow(gmpy2.invert(c1, n), -s1, n)
    m *= pow(c2, s2, n) if s2 > 0 else pow(gmpy2.invert(c2, n), -s2, n)
    return m % n


def small_msg(e, n, c):
    print time.asctime(), "Let's waiting..."
    for k in xrange(200000000):
        if gmpy2.iroot(c + n * k, e)[1] == 1:
            print time.asctime(), "...done!"
            return gmpy2.iroot(c + n * k, 3)[0]


def wiener_hack(e, n):
    # https://github.com/pablocelayes/rsa-wiener-attack
    frac = ContinuedFractions.rational_to_contfrac(e, n)
    convergents = ContinuedFractions.convergents_from_contfrac(frac)
    for (k, d) in convergents:
        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            s = n - phi + 1
            discr = s * s - 4 * n
            if (discr >= 0):
                t = Arithmetic.is_perfect_square(discr)
                if t != -1 and (s + t) % 2 == 0:
                    print("Hacked!")
                    return d
    return False


def gcd(a, b):
    return a if not b else gcd(b, a % b)


def gcd2(a, b):
    while not b:
        a, b = b, a % b
        return a


def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    else:
        x, y, q = egcd(b, a % b)
        return y, x - a / b * y, q


def oracle():
    return lsb == 'odd'


def partial(c, e, n):
    k = n.bit_length()
    decimal.getcontext().prec = k  # for 'precise enough' floats
    lo = decimal.Decimal(0)
    hi = decimal.Decimal(n)
    for i in range(k):
        if not oracle(c):
            hi = (lo + hi) / 2
        else:
            lo = (lo + hi) / 2
        c = (c * pow(2, e, n)) % n
        # print i, int(hi - lo)
    return int(hi)


def egcd2(a, b):
    # https://blog.csdn.net/wyf12138/article/details/60476773
    if b == 0:
        return (1, 0, a)
    x, y = 0, 1
    s1, s2 = 1, 0
    r, q = a % b, a / b
    while r:
        m, n = x, y
        x = s1 - x * q
        y = s2 - y * q
        s1, s2 = m, n
        a, b = b, r
        r, q = a % b, a / b
    return (x, y, b)


def CRT(mi, ai):
    # mi,ai分别表示模数和取模后的值,都为列表结构
    # Chinese Remainder Theorem
    # lcm=lambda x , y:x*y/gcd(x,y)
    # mul=lambda x , y:x*y
    # assert(reduce(mul,mi)==reduce(lcm,mi))
    # 以上可用于保证mi两两互质
    assert (isinstance(mi, list) and isinstance(ai, list))
    M = reduce(lambda x, y: x * y, mi)
    ai_ti_Mi = [a * (M / m) * gmpy2.invert(M / m, m) for (m, a) in zip(mi, ai)]
    return reduce(lambda x, y: x + y, ai_ti_Mi) % M


def GCRT(mi, ai):
    assert (isinstance(mi, list) and isinstance(ai, list))
    curm, cura = mi[0], ai[0]
    for (m, a) in zip(mi[1:], ai[1:]):
        d = gmpy2.gcd(curm, m)
        c = a - cura
        assert (c % d == 0)
        K = c / d * gmpy2.invert(curm / d, m / d)
        cura += curm * K
        curm = curm * m / d
    return cura % curm, curm


def read_pubkey_file(pub_file):
    with open(pub_file, 'r') as f:
        key = RSA.importKey(f)
        n, e = key.n, key.e
    return (n, e)


def display(m):
    if isinstance(m, int) or isinstance(m, long) or type(m) == type(
            gmpy2.mpz()):
        print libnum.n2s(m)
    else:
        print str(type(m))


if __name__ == '__main__':
    print GCRT([6, 5, 14], [4, 3, 4])
