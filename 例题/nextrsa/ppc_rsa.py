# coding=utf-8
import socket
import thread
import hashlib
import random
import time
import primefac
import os
import hide
import logging
#cheat detect preload
successdn=[]
files = os.listdir("success/")
for filename in files:
    print "load",filename
    seed = int(hashlib.sha256(filename).hexdigest()[0:8], 16)
    p = primefac.nextprime(seed)
    q=0xab724df05ca87067ce1573550a6a05f41f93e910b0380c71cdc5de940ef790a475f5c3d512354bc57b3410e7f5158fb287f79397353acb169ef583260eec76f4c46d21e4cb43426e3c66ba9b75d3c1b009ff1f9a0fea9c7d9815eadc5f7ac776d6dcae3c1fa3de865253623b4121e6b4f51deea0b7ae9ca84aad5fe83ba56451L
    e=65537
    d=primefac.modinv(e,(p-1)*(q-1))
    if d<0:
        d+=(p-1)*(q-1)
    successdn.append((d,p*q))
def error(conn):
    conn.send("sorry!\n")
    conn.close()
def ok(conn):
    conn.send("ok!\n")
def proof(conn):
    conn.send("Firstly, please give me the proof of your work!\n")
    x=chr(random.randint(0,0xff))+chr(random.randint(0,0xff))+chr(random.randint(0,0x1f))
    conn.send("x=chr(random.randint(0,0xff))+chr(random.randint(0,0xff))+chr(random.randint(0,0x1f))\n")
    conn.send("hashlib.sha256(x).hexdigest()[0:8]=='"+hashlib.sha256(x).hexdigest()[0:8]+"'\n@ x.encode('hex')=")
    rec_x=conn.recv(1024).strip()
    if rec_x==x.encode("hex"):
        ok(conn)
    else:
        error(conn)



def problem_brute_256bit(conn):
    conn.send("=next-rsa=\n")
    n = 0xc4606b153b9d06d934c9ff86a3be5610266387d82d11f3b4e354b1d95fc7e577
    e = 0x10001
    conn.send("# n="+hex(n).replace("L","")+"\n")
    conn.send("# e="+hex(e).replace("L","")+"\n")
    m=random.randint(0x100000000000,0xffffffffffff)
    c=pow(m,e,n)
    conn.send("# c="+hex(c).replace("L","")+"\n")
    conn.send("@ m=")
    rec_m=conn.recv(1024).strip()
    if rec_m==hex(m).replace("L",""):
        ok(conn)
    else:
        error(conn)
def problem_wiener_attack(conn):
    conn.send("=next-rsa=\n")
    n=0x92411fa0c93c1b27f89e436d8c4698bcf554938396803a5b62bd10c9bfcbf85a483bd87bb2d6a8dc00c32d8a7caf30d8899d90cb8f5838cae95f7ff5358847db1244006c140edfcc36adbdcaa16cd27432b4d50d2348b5c15c209364d7914ef50425e4c3da07612cc34e9b93b98d394b43f3eb0a5a806c70f06697b6189606eb9707104a7b6ff059011bac957e2aae9ec406a4ff8f8062400d2312a207a9e018f4b4e961c943dfc410a26828d2e88b24e4100162228a5bbf0824cf2f1c8e7b915efa385efeb505a9746e5d19967766618007ddf0d99525e9a41997217484d64c6a879d762098b9807bee46a219be76941b9ff31465463981e230eecec69691d1L
    e=0x6f6b385dd0f06043c20a7d8e5920802265e1baab9d692e7c20b69391cc5635dbcaae59726ec5882f168b3a292bd52c976533d3ad498b7f561c3dc01a76597e47cfe60614f247551b3dbe200e2196eaa001a1d183886eeacddfe82d80b38aea24de1a337177683ed802942827ce4d28e20efef92f38f1b1a18c66f9b45f5148cceabfd736de8ac4a49e63a8d35a83b664f9f3b00f822b6f11ff13257ee6e0c00ca5c98e661ea594a9e66f2bd56b33d9a13f5c997e67a37fcf9a0c7f04d119fe1ba261127357e64a4b069aefed3049c1c1fe4f964fd078b88bedd064abea385cfebd65e563f93c12d34eb6426e8aa321033cfd8fe8855b9e74d07fe4f9d70de46fL
    conn.send("# n="+hex(n).replace("L","")+"\n")
    conn.send("# e="+hex(e).replace("L","")+"\n")
    m = random.randint(0x100000000000, 0xffffffffffff)
    c = pow(m, e, n)
    conn.send("# c=" + hex(c).replace("L","") + "\n")
    conn.send("@ m=")
    rec_m = conn.recv(1024).strip()
    if rec_m == hex(m).replace("L",""):
        ok(conn)
    else:
        error(conn)
def problem_LLL_attack(conn):
    conn.send("=next-rsa=\n")
    n = 0x79982a272b9f50b2c2bc8b862ccc617bb39720a6dc1a22dc909bbfd1243cc0a03dd406ec0b1a78fa75ce5234e8c57e0aab492050906364353b06ccd45f90b7818b04be4734eeb8e859ef92a306be105d32108a3165f96664ac1e00bba770f04627da05c3d7513f5882b2807746090cebbf74cd50c0128559a2cc9fa7d88f7b2dL
    e=3
    conn.send("# n=" + hex(n).replace("L","") + "\n")
    conn.send("# e=" + hex(e).replace("L","") + "\n")
    base=0xfedcba98765432100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    c=0x381db081852c92d268b49a1b9486d724e4ecf49fc97dc5f20d1fad902b5cdfb49c8cc1e968e36f65ae9af7e8186f15ccdca798786669a3d2c9fe8767a7ae938a4f9115ae8fed4928d95ad550fddd3a9c1497785c9e2279edf43f04601980aa28b3b52afb55e2b34e5b175af25d5b3bd71db88b3b31e48a177a469116d957592cL
    conn.send("# c=" + hex(c).replace("L", "") + "\n")
    conn.send("# b=" + hex(base).replace("L","") + "\n")
    conn.send("# m=b+x (x:64bit)\n")
    conn.send("@ x=")
    rec_x = conn.recv(1024).strip()
    if rec_x == "0x33686739766d336b":
        ok(conn)
    else:
        error(conn)
def problem_np_nq(conn):
    conn.send("=next-rsa=\n")
    n = 0x78e2e04bdc50ea0b297fe9228f825543f2ee0ed4c0ad94b6198b672c3b005408fd8330c36f55d36fb129d308c23e5cb8f4d61aa7b058c23607cef83d63c4ed0f066fc0b3c0062a2ac68c75ca8035b3bd7a320bdf29cfcf6cc30377743d2a8cc29f7c588b8043412366ab69ec824309cb1ef3851d4fb14a1f0a58e4a1193f5518fa1d0c159621e1f832b474182593db2352ef05101bf367865ad26efe14fce977e9e48d3310a18b67991958d1a01bd0f3276a669866f4deaef2a68bfaefd35fe2ba5023a22c32ae8b2979c26923ee3f855363f18d8d58bb1bc3b7f585c9d9f6618c727f0f7b9e6f32af2864a77402803011874ed2c65545ced72b183f5c55d4d1L
    e = 0x10001
    conn.send("# n=" + hex(n).replace("L","") + "\n")
    conn.send("# e=" + hex(e).replace("L","") + "\n")
    npp=0x78e2e04bdc50ea0b297fe9228f825543f2ee0ed4c0ad94b6198b672c3b005408fd8330c36f55d36fb129d308c23e5cb8f4d61aa7b058c23607cef83d63c4ed0f066fc0b3c0062a2ac68c75ca8035b3bd7a320bdf29cfcf6cc30377743d2a8cc29f7c588b8043412366ab69ec824309cb1ef3851d4fb14a1f0a58e4a1193f5a58ee70a59ac06b64dbe04b876ff69436b78cf03371f2062707897bf4e580870e42b5e62709b69f6d4939ac5641ea0f29de44aaee8f2fcd0f66aaa720b584f7c801e52ce7cd41db45ceb99ebd7b51bef8d0cd2deb5c50b59f168276c9c98d46a1c37bd3d6ef81f2c6e89028680a172e00d92dd8b392135112dd16efab57d00b26b9L
    conn.send("# nextprime(p)*nextprime(q)=" + hex(npp).replace("L","") + "\n")
    m = random.randint(0x100000000000, 0xffffffffffff)
    c = pow(m, e, n)
    conn.send("# c=" + hex(c).replace("L","") + "\n")
    conn.send("@ m=")
    rec_m = conn.recv(1024).strip()
    if rec_m == hex(m).replace("L",""):
        ok(conn)
    else:
        error(conn)
def problem_yafu_cheat_check(conn,address,teamtoken):
    (ip,port)=address
    conn.send("=next-rsa=\n")
    q=0xab724df05ca87067ce1573550a6a05f41f93e910b0380c71cdc5de940ef790a475f5c3d512354bc57b3410e7f5158fb287f79397353acb169ef583260eec76f4c46d21e4cb43426e3c66ba9b75d3c1b009ff1f9a0fea9c7d9815eadc5f7ac776d6dcae3c1fa3de865253623b4121e6b4f51deea0b7ae9ca84aad5fe83ba56451L
    seed=int(hashlib.sha256(ip).hexdigest()[0:8],16)
    p=primefac.nextprime(seed)
    n=p*q
    e=0x10001
    conn.send("# n=" + hex(n).replace("L","") + "\n")
    conn.send("# e=" + hex(e).replace("L","") + "\n")
    m = random.randint(0x100000000000, 0xffffffffffff)
    c = pow(m, e, n)
    conn.send("# c=" + hex(c).replace("L","") + "\n")
    conn.send("@ m=")
    rec_m = conn.recv(1024).strip()
    if rec_m == hex(m).replace("L",""):
        d=primefac.modinv(e,(p-1)*(q-1))
        if d<0:
            d+=(p-1)*(q-1)
        successdn.append((d,n))
        f=open("success/"+ip,"a")
        f.write("teamtoken:"+teamtoken+"\n"+"time:"+time.strftime('%Y%m%d%H%M%S')+"\nm:"+hex(m).replace("L","")+"\nd:"+hex(d).replace("L","")+"\nn:"+hex(n).replace("L","")+"\n\n")
        f.close()
        ok(conn)
        return 0
    else:
        for (cheat_d,cheat_n) in successdn:
            print "cheat!"
            rec_m_int=int(rec_m[0:],16)
            if rec_m_int==pow(c,cheat_d,cheat_n):
                f=open("cheat/"+ip,"a")
                f.write("teamtoken:"+teamtoken+"\n"+"time:"+time.strftime('%Y%m%d%H%M%S')+"\nm:"+hex(rec_m_int).replace("L","")+"\nd:"+hex(cheat_d).replace("L","")+"\nn:"+hex(cheat_n).replace("L","")+"\n\n")
                f.close()
                ok(conn)
                return 1
        error(conn)
        return 0
def problem_e_3_brute(conn):
    conn.send("=next-rsa=\n")
    n = 0x7003581fa1b15b80dbe8da5dec35972e7fa42cd1b7ae50a8fc20719ee641d6080980125d18039e95e435d2a60a4d5b0aaa42d5c13b0265da4930a874ddadcd9ab0b02efcb4463a33361a84df0c02dfbd05c0fdc01e52821c683bd265e556412a3f55e49517778079cb1c1c1c22ef8a6e0bccd5e78888ff46167a471f6bff25664a34311c5cb8d6c1b1e7ac2ab0e6676d594734e8f7013b33806868c151316d0cf762a50066c596244fd70b4cb021369aae432e174da502a806e7a8ab13dad1f1b83ac73c0e9e39648630923cbd5726225f17cc0d15afadb7d2c2952b6e092ffc53dcff2914bfddedd043bbdf9c6f6b6b5a6269c5bd423294b9deac4f268eaadbL
    e=3
    conn.send("# n=" + hex(n).replace("L","") + "\n")
    conn.send("# e=" + hex(e).replace("L","") + "\n")
    c=0xb2ab05c888ab53d16f8f7cd39706a15e51618866d03e603d67a270fa83b16072a35b5206da11423e4cd9975b4c03c9ee0d78a300df1b25f7b69708b19da1a5a570c824b2272b163de25b6c2f358337e44ba73741af708ad0b8d1d7fa41e24344ded8c6139644d84dc810b38450454af3e375f68298029b7ce7859f189cdae6cfaf166e58a22fe5a751414440bc6bce5ba580fd210c4d37b97d8f5052a69d31b275c53b7d61c87d8fc06dc713e1c1ce05d7d0aec710eba2c1de6151c84d7bc3131424344b90e3f8947322ef1a57dd3a459424dd31f65ff96f5b8130dfd33111c59f3fc3a754e6f98a836b4fc6d21aa74e676f556aaa5a703eabe097140ec9d98L
    conn.send("# c=" + hex(c).replace("L", "") + "\n")
    conn.send("@ m=")
    rec_m = conn.recv(1024).strip()
    m = 0xcf54ad6301f83d4c7a151d7706739935471171f3c67d13850ae75118f13f5531eef5ef2ebf58277c22b5d89476d713e3a697d7cd71f2ac23671bb78053fdeeff1b372d7f31946568b5bbb04140ad25d6212dd9c9e9e7L
    if rec_m == hex(m).replace("L", ""):
        ok(conn)
    else:
        error(conn)
def problem_gcd_attack(conn):
    conn.send("=next-rsa=\n")
    n1=0xb4e9991d2fac12b098b01118d960eb5470261368e7b1ff2da2c66b4302835aa845dd50a4f749fea749c6d439156df6faf8d14ce2a57da3bac542f1843bfc80dfd632e7a2ef96496a660d8c5994aea9e1b665097503558bc2756ab06d362abe3777d8c1f388c8cd1d193955b70053382d330125bdc2cdc836453f1a26cec1021cbb787977336b2300f38c6ba881a93d2a2735f8f0d32ea2d0e9527eb15294dd0867c8030d1f646bd121c01706c247cd1bf4aa209d383ffb748b73ec1688dc71812675834b4b12d27a63b5b8fcc47394d16897ff96af49f39d8d5b247553fbf8fac7be08aab43d9ce5659cd5cfaf7d73edbcfe854d997ae4b28d879adf86641707L
    n2=0xc31344c753e25135d5eed8febaa57dd7020b503a5569bdd4ae6747b5c36436dc1c4d7ead77bfc1034748bcc630636bae1c8f4ca5dee8246b3d6f3e8b14e16487733b14ec8e587e07a7a6de45859d32d241eaf7746c45ff404f1a767ab77e8493ae8141fee0bcf4e9b7c455415b6945fa60de928b01dfa90bbf0d09194f93db7a1663121d281c908f0e38237f63c2b856f99c6029d993f9afb5fbbb762044d97943ff34023486c4cf1db9ffdc439d9f5ff331b606374c7133d61e4614fac3ea7faaf54563338b736282658e7925b224577091831351a28679a8d6f8e7ba16685b2769bb49b79f8054b29c809d68aca0f2c5e3f1fd0e3ef6c21f756e3c44a40439L
    e1=65537
    e2=65537
    conn.send("# n1=" + hex(n1).replace("L", "") + "\n")
    conn.send("# e1=" + hex(e1).replace("L", "") + "\n")
    m1 = random.randint(0x100000000000, 0xffffffffffff)
    c1 = pow(m1, e1, n1)
    conn.send("# c1=" + hex(c1).replace("L", "") + "\n")
    conn.send("# n2=" + hex(n2).replace("L", "") + "\n")
    conn.send("# e2=" + hex(e2).replace("L", "") + "\n")
    m2 = random.randint(0x100000000000, 0xffffffffffff)
    c2 = pow(m2, e2, n2)
    conn.send("# c2=" + hex(c2).replace("L", "") + "\n")

    conn.send("@ m1=")
    rec_m1 = conn.recv(1024).strip()
    if rec_m1 == hex(m1).replace("L", ""):
        ok(conn)
    else:
        error(conn)
    conn.send("@ m2=")
    rec_m2 = conn.recv(1024).strip()
    if rec_m2 == hex(m2).replace("L", ""):
        ok(conn)
    else:
        error(conn)
def problem_same_n(conn):
    conn.send("=next-rsa=\n")
    n = 0xace2aa1121d22a2153389fba0b5f3e24d8721f5e535ebf5486a74191790c4e3cdd0316b72388e7de8be78483e1f41ca5c930df434379db76ef02f0f8cd426348b62c0155cdf1d5190768f65ce23c60a4f2b16368188954342d282264e447353c62c10959fee475de08ec9873b84b5817fecb74899bedde29ef1220c78767f4de11ef1756404494ae1ce4af184cbc1c7c6de8e9cd16f814bca728e05bc56b090112f94fff686bf8122a3b199eb41080860fa0689ed7dbc8904184fb516b2bbf6b87a0a072a07b9a26b3cda1a13192c03e24dec8734378d10f992098fe88b526ce70876e2c7b7bd9e474307dc6864b4a8e36e28ce6d1b43e3ab5513baa6fa559ffL
    e1 = 0xac8b
    e2 = 0x1091
    conn.send("# c1=pow(m,e1,n),c2=pow(m,e2,n)\n")
    conn.send("# n=" + hex(n).replace("L", "") + "\n")
    m = random.randint(0x100000000000, 0xffffffffffff)
    conn.send("# e1=" + hex(e1).replace("L", "") + "\n")
    c1 = pow(m, e1, n)
    conn.send("# c1=" + hex(c1).replace("L", "") + "\n")
    conn.send("# e2=" + hex(e2).replace("L", "") + "\n")
    c2 = pow(m, e2, n)
    conn.send("# c2=" + hex(c2).replace("L", "") + "\n")
    conn.send("@ m=")
    rec_m = conn.recv(1024).strip()
    if rec_m == hex(m).replace("L", ""):
        ok(conn)
    else:
        error(conn)
def problem_broadcast(conn):
    conn.send("=next-rsa=\n")
    conn.send("# c1=pow(m,e,n1),c2=pow(m,e,n2),c3=pow(m,e,n3)\n")
    e=3
    conn.send("# e=" + hex(e).replace("L", "") + "\n")
    m = random.randint(0x100000000000, 0xffffffffffff)
    patchbit=int("1"*1024,2)
    m+=patchbit
    n1 = 0x43d819a4caf16806e1c540fd7c0e51a96a6dfdbe68735a5fd99a468825e5ee55c4087106f7d1f91e10d50df1f2082f0f32bb82f398134b0b8758353bdabc5ba2817f4e6e0786e176686b2e75a7c47d073f346d6adb2684a9d28b658dddc75b3c5d10a22a3e85c6c12549d0ce7577e79a068405d3904f3f6b9cc408c4cd8595bf67fe672474e0b94dc99072caaa4f866fc6c3feddc74f10d6a0fb31864f52adef71649684f1a72c910ec5ca7909cc10aef85d43a57ec91f096a2d4794299e967fcd5add6e9cfb5baf7751387e24b93dbc1f37315ce573dc063ecddd4ae6fb9127307cfc80a037e7ff5c40a5f7590c8b2f5bd06dd392fbc51e5d059cffbcb85555L
    n2 = 0x60d175fdb0a96eca160fb0cbf8bad1a14dd680d353a7b3bc77e620437da70fd9153f7609efde652b825c4ae7f25decf14a3c8240ea8c5892003f1430cc88b0ded9dae12ebffc6b23632ac530ac4ae23fbffb7cfe431ff3d802f5a54ab76257a86aeec1cf47d482fec970fc27c5b376fbf2cf993270bba9b78174395de3346d4e221d1eafdb8eecc8edb953d1ccaa5fc250aed83b3a458f9e9d947c4b01a6e72ce4fee37e77faaf5597d780ad5f0a7623edb08ce76264f72c3ff17afc932f5812b10692bcc941a18b6f3904ca31d038baf3fc1968d1cc0588a656d0c53cd5c89cedba8a5230956af2170554d27f524c2027adce84fd4d0e018dc88ca4d5d26867L
    n3 = 0x280f992dd63fcabdcb739f52c5ed1887e720cbfe73153adf5405819396b28cb54423d196600cce76c8554cd963281fc4b153e3b257e96d091e5d99567dd1fa9ace52511ace4da407f5269e71b1b13822316d751e788dc935d63916075530d7fb89cbec9b02c01aef19c39b4ecaa1f7fe2faf990aa938eb89730eda30558e669da5459ed96f1463a983443187359c07fba8e97024452087b410c9ac1e39ed1c74f380fd29ebdd28618d60c36e6973fc87c066cae05e9e270b5ac25ea5ca0bac5948de0263d8cc89d91c4b574202e71811d0ddf1ed23c1bc35f3a042aac6a0bdf32d37dede3536f70c257aafb4cfbe3370cd7b4187c023c35671de3888a1ed1303L
    c1=pow(m,e,n1)
    c2=pow(m,e,n2)
    c3=pow(m,e,n3)
    conn.send("# n1=" + hex(n1).replace("L", "") + "\n")
    conn.send("# c1=" + hex(c1).replace("L", "") + "\n")
    conn.send("# n2=" + hex(n2).replace("L", "") + "\n")
    conn.send("# c2=" + hex(c2).replace("L", "") + "\n")
    conn.send("# n3=" + hex(n3).replace("L", "") + "\n")
    conn.send("# c3=" + hex(c3).replace("L", "") + "\n")
    conn.send("@ m=")
    rec_m = conn.recv(1024).strip()
    if rec_m == hex(m).replace("L", ""):
        ok(conn)
    else:
        error(conn)

def remote_sub(conn, address):
    print address,
    (ip,port)=address
    conn.settimeout(20)
    conn.send("====next-rsa====\n")
    conn.send("teamtoken:")
    teamtoken=conn.recv(1024).strip()
    if hide.check_teamtoken(teamtoken)==False:
        error(conn)
    ok(conn)
    print teamtoken
    proof(conn)
    conn.send('\n\ninput format:almost hex(m).replace("L","")\n\n')
    problem_brute_256bit(conn)
    problem_wiener_attack(conn)
    problem_LLL_attack(conn)
    problem_np_nq(conn)
    cheat=problem_yafu_cheat_check(conn, address,teamtoken)
    problem_e_3_brute(conn)
    problem_gcd_attack(conn)
    problem_same_n(conn)
    problem_broadcast(conn)
    f=open("flag/"+ip,"a")
    f.write("time:"+time.strftime('%Y%m%d%H%M%S')+"\ncheat:"+str(cheat)+"\n"+teamtoken+"\n\n")
    conn.send(hide.flag+"\n")
    conn.close()
def remote():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 9999))
    sock.listen(0)
    while True:
        thread.start_new_thread(remote_sub, sock.accept())
if __name__ == '__main__':
    remote()
