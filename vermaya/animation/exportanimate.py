#!/usr/bin/env python
#
#
#coding=utf-8
import os
import maya.mel
import maya.cmds as cmds

rootpath = os.path.split(os.path.realpath(__file__))[0]

def runmelscript():
    selection = cmds.ls (sl = 1)[0]
    if selection:
        if ":" in selection:
            namespaces = selection.split(":")
            namespace = ""
            for i in range(len(namespaces)-1):
                namespace = namespace + namespaces[i]+":"
            newnamespace = namespace.split(":")[0]
        else:
            newnamespace = ""

        savemelscripts = ["source \"%s/anim_copy.mel\"" % rootpath.replace('\\','/'),
                          "textField -e -text %s usePrefixTF" % newnamespace,
                          "checkBox -e -v 1 usePrefixCB",
                          "as_checkingDirFilesProc;"]
        loadmelscripts = ["usePrefixProc;",
                          "as_pasteAnmProc;",
                          "if (`window - ex \"my_AnmCopyWindow\"`){deleteUI (\"my_AnmCopyWindow\")}",]
        for savemelscript in savemelscripts:
            maya.mel.eval(savemelscript)

        data = u"动画数据保存成功!!!!!"+"\n"

        selectiontofilepath = cmds.referenceQuery (selection, filename = True)
        cmds.file (selectiontofilepath, removeReference = True)

        data = data + u"已移除当前绑定文件!!!!!"+"\n"
        cmds.file (selectiontofilepath, namespace = newnamespace,reference = True)
        data = data + u"已重新参考新的文件!!!!!"+"\n"

        for loadmelscript in loadmelscripts:
            maya.mel.eval (loadmelscript)
        data = data + u"已将动画拷入到新的文件!!!!!"
        print data