# -*- coding : utf-8 -*-
# python 3.7
# __author__ = 'https://github.com/findneo'

import gmpy2
import requests
import json
import binascii

def factordb(n):
    api="http://factordb.com/api.php"
    r=requests.get(api,params={'query':n})
    res=json.loads(r.content)
    if res['status'] == "FF":
        p,q=res['factors'][0][0],res['factors'][1][0]
        [p,q]=map(int,[p,q])
        # print('\n'.join([hex(p),hex(q)]))
        return p,q
    else:
        print("not fully factored!")

n1=0xcfc59d54b4b2e9ab1b5d90920ae88f430d39fee60d18dddbc623d15aae645e4e50db1c07a02d472b2eebb075a547618e1154a15b1657fbf66ed7e714d23ac70bdfba4c809bbb1e27687163cb09258a07ab2533568192e29a3b8e31a5de886050b28b3ed58e81952487714dd7ae012708db30eaf007620cdeb34f150836a4b723
e1=0xfae3a
c1=0x81523a330fb15125b6184e4461dadac7601340960840c5213b67a788c84aecfcdc3caf0bf3e27e4c95bb3c154db7055376981972b1565c22c100c47f3fa1dd2994e56090067b4e66f1c3905f9f780145cdf8d0fea88a45bae5113da37c8879c9cdb8ee9a55892bac3bae11fbbabcba0626163d0e2e12c04d99f4eeba5071cbea
p1,q1=factordb(n1)
# p1=0xe5d7acdf77ca09e4391f21cea16c01cd2302d1a1df3983d413e9ee91fce8d9184ec0d0ca1608dbed748ed905a2beddc00168a1245f27f67e1240073c3d097965
# q1=0xe76aed4830504369c7c12070490f18900b80da1035ef82991dd35c52fd51731025c4498e8998bd026b9898963b6b69ded47b1dd96c264eac9d875756fd1b29e7

n2=0xd45304b186dc82e40bd387afc831c32a4c7ba514a64ae051b62f483f27951065a6a04a030d285bdc1cb457b24c2f8701f574094d46d8de37b5a6d55356d1d368b89e16fa71b6603bd037c7f329a3096ce903937bb0c4f112a678c88fd5d84016f745b8281aea8fd5bcc28b68c293e4ef4a62a62e478a8b6cd46f3da73fa34c63
e2=0x1f9eae
c2=0x4d7ceaadf5e662ab2e0149a8d18a4777b4cd4a7712ab825cf913206c325e6abb88954ebc37b2bda19aed16c5938ac43f43966e96a86913129e38c853ecd4ebc89e806f823ffb802e3ddef0ac6c5ba078d3983393a91cd7a1b59660d47d2045c03ff529c341f3ed994235a68c57f8195f75d61fc8cac37e936d9a6b75c4bd2347
p2,q2=factordb(n2)[::-1]
# p2=0xeae0dfb99949af5175c425e22ec3c2e5b73cec0b70510dcc0ccd368ca6e868146c8783fa4aee0548fc725a3c3b0e46e44ec60357d3e6f4a5207e8a8ddf9c1225
# q2=0xe76aed4830504369c7c12070490f18900b80da1035ef82991dd35c52fd51731025c4498e8998bd026b9898963b6b69ded47b1dd96c264eac9d875756fd1b29e7

assert(q1==q2)
q=q1
# n1,n2均可分解，且有一个公因数
# 由于gcd(e,phi)==14，将 (flag**e)%n = c 看作 (((flag**14)%n) ** (e//14) ) % n == c
# 分别记 e//14为e1,e2 , (flag**14)%n1 为 f1 , (flag**14)%n2 为 f2,则 pow(f1,e1,n1)==c1,pow(f2,e2,n2)==c2 且 gcd(e1,phi1)==gcd(e2,phi2)==1。可求得 f1,f2
e1=e1//14;e2=e2//14
phi1=(p1-1)*(q1-1);phi2=(p2-1)*(q2-1)
d1=gmpy2.invert(e1,phi1);d2=gmpy2.invert(e2,phi2)
f1=pow(c1,d1,n1);f2=pow(c2,d2,n2)

# 记 flag**14 为 f3,则有同余方程组 f3 % n1 == f1; f3 % n2 == f2。其中f1,f2,n1,n2已知，可求模lsm(n1,n2)意义下的解 f3。
# 参考 https://findneo.github.io/180727rsa-attack/#%E4%B8%AD%E5%9B%BD%E5%89%A9%E4%BD%99%E5%AE%9A%E7%90%86。
def GCRT(mi, ai):
    # mi,ai分别表示模数和取模后的值,都为列表结构
    assert (isinstance(mi, list) and isinstance(ai, list))
    curm, cura = mi[0], ai[0]
    for (m, a) in zip(mi[1:], ai[1:]):
        d = gmpy2.gcd(curm, m)
        c = a - cura
        assert (c % d == 0) #不成立则不存在解
        K = c // d * gmpy2.invert(curm // d, m // d)
        cura += curm * K
        curm = curm * m // d
        cura %= curm
    return (cura % curm, curm) #(解,最小公倍数)
f3,lsm = GCRT([n1,n2],[f1,f2])
assert(f3%n1==f1);assert(f3%n2==f2);assert(lsm==p1*p2*q)


# assert(flag**14 % lsm == f3)
# 此时求出的 f3 满足上式。其中 lsm==p1*p2*q 有5个约数: 1, p1*q即n1 ,p2*q即n2, p1*p2记作n3, lsm。
# 上式可看作 pow(flag**2,7,lsm)==f3，等价于 pow(flag**2,7,n1)==f3%n1,pow(flag**2,7,n2)==f3%n2,pow(flag**2,7,n3)==f3%n3
# 由于 gcd(7,n1)==7,gcd(7,n2)==7。所以尝试选取 pow(flag**2,7,n3)==f3%n3 计算 flag**2 的值
n3=p1*p2
c3=f3%n3
phi3=(p1-1)*(p2-1)
assert(gmpy2.gcd(7,phi3)==1)
d3=gmpy2.invert(7,phi3)
m3=pow(c3,d3,n3)
if gmpy2.iroot(m3,2)[1] == 1:
    flag=gmpy2.iroot(m3,2)[0]
    print(binascii.unhexlify(hex(flag)[2:]))
# b'EIS{Comm0n_Div15or_plus_CRT_is_so_easy|cb2733b9e69ab3a9bd526fa1}'
