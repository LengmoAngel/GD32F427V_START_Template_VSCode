import os
import re

def main(tpl_file, dst_file):
    cFileList = []
    hPathList = []
    sFileList = []
    ldFileList = []

    dList = ["."]
    hPathList.extend(dList)
    d_sp = False
    with open(tpl_file, "r") as lines:
            for line in lines:
                searchObj = re.search( r'^\s*(GD32_CMSIS_LIBRARY_DIR.*)\s*=\s*([^\s]+)$', line)
                if searchObj:
                    d_tmp = searchObj.group(2)
                    print("GD32F4xx CMSIS: %s" % d_tmp)
                    # dList.insert(0, d_tmp)
                    hPathList.append(d_tmp)

                searchObj = re.search( r'^\s*(GD32_SP_LIBRARY_DIR.*)\s*=\s*([^\s]+)$', line)
                if searchObj:
                    d_sp = searchObj.group(2)
                    print("GD32F4xx_standard_peripheral: %s" % d_sp)
                    dList.insert(0, d_sp)

    for d in dList:
        for root,dirs,files in os.walk(d):
            for file in files:
                file_path = os.path.join(root, file) #.decode('gbk').encode('utf-8')
                file_path = os.path.relpath(file_path).replace('\\', '/')
                if file.endswith(".c"):
                    cFile = file_path
                    cFileList.append(cFile)
                if file.endswith(".h"):
                    hPath = os.path.dirname(file_path)
                    if hPathList.count(hPath) == 0:
                        hPathList.append(hPath)
                if file.endswith(".s"):
                    sFile = file_path
                    if not sFile.startswith('..'):
                        sFileList.append(sFile)
                if file.endswith(".ld"):
                    ldFile = file_path
                    ldFileList.append(ldFile)
    print("C sources:\n\t", '\n\t'.join(cFileList))
    print("header dirs:\n\t", '\n\t'.join(hPathList))
    print("asm files:\n\t", '\n\t'.join(sFileList))
    print("ld files:\n\t", '\n\t'.join(ldFileList))

    cFileStr = "C_SOURCES += "
    hPathStr = "C_INCLUDES += "
    sFileStr = "ASM_SOURCES += "
    ldFileStr = "LDSCRIPT += "
    for listStr in cFileList:
        cFileStr += " \\\n" + listStr
        # cFileStr += "C_SOURCES += " + listStr + "\n"
    for listStr in hPathList:
        hPathStr += " \\\n-I" + listStr
        # hPathStr += "C_INCLUDES += -I" + listStr + "\n"
    for listStr in sFileList:
        sFileStr += " \\\n" + listStr
        # sFileStr += "ASM_SOURCES += " + listStr + "\n"
    for listStr in ldFileList:
        ldFileStr += " \\\n" + listStr
        # ldFileStr += "LDSCRIPT += " + listStr + "\n"

    cFileStr = cFileStr.replace(d_sp, '$(GD32_SP_LIBRARY_DIR)')

    try:
        f = open(tpl_file, "r")
        fileStr = f.read()
        f.close()
        fileStr = fileStr.replace("@@C_SOURCES@@", cFileStr)
        fileStr = fileStr.replace("@@C_INCLUDES@@", hPathStr)
        fileStr = fileStr.replace("@@ASM_SOURCES@@", sFileStr)
        fileStr = fileStr.replace("@@LDSCRIPT@@", ldFileStr)
        f = open(dst_file, "w")
        f.write(fileStr)#.decode('gbk').encode('utf-8'))
        f.close()
    finally:
        f.close()


if __name__ == '__main__':
    main("./support_files/Makefile.template", "./Makefile")