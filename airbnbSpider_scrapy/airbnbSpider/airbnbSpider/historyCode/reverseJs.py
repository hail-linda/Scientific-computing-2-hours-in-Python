import re
def reverseJS():
    def b2str(matched):        
        Char = chr(int(matched.group(1),16))
        if Char in ["'", "\\",'"']: # 对特殊字符进行处理
            Char = '\\' + Char
        return Char # 返回就是将匹配到的字符替换完毕的字符

    with open("acw_sc_v2.html", "r+") as f:
        c = "".join(f.readlines())
        res = re.sub(r"\\x(\d[a-zA-Z0-9])", b2str, c) # 最终返回替换好的字符串
        with open("utf8.txt", "w+") as f:
            f.write(res)

reverseJS()