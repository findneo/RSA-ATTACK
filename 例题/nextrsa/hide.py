flag="flag{s1mp13_rs4_f0r_y0u_+_h4pp9_f0r_qwb}"
import re
def check_teamtoken(teamtoken):
    if len(teamtoken)!=32:
        return False
    if (re.match(r"[a-fA-F0-9]{32,32}", teamtoken))==None:
        return False
    return True