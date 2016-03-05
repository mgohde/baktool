#!/usr/bin/env python
import os
import sys
import bakplugin

def getbasedir():
  bdir=os.getenv("BAKTOOL_BASE")
  if bdir==None:
    print("WARNING: BAKTOOL_BASE not set!")
    return ""
  return bdir


def print_usage():
  print("Usage: baktool.py bakdeffile <action>")
  print("Run backups in a flexible fashion.")
  print("\nWhere <action> is one of the following:")
  print("\tbackup\tRun a backup job.")
  print("\trestore\tRestore from backups.")
  print("\tplugins\tList all loaded plugins.")


def tokenize(filename):
  f=open(filename, 'r')
  contents=f.read()
  f.close()
  toks=contents.splitlines()
  ret_toks=[]
  
  for t in toks:
    if t[len(t)-1]==':':
      ret_toks.append([t.strip(':').strip()])
    else:
      ret_toks[len(ret_toks)-1].append(t.strip)
  return ret_toks


def findtok(toklist, block_name):
  for t in toklist:
    if t[0]==block_name:
      return t[1:]
  return []


def run_backup(filename):
  toks=tokenize(filename)
  bakext=findtok(toks, "filetype")
  srcdir=findtok(toks, "srcdir")
  destdir=findtok(toks, "destdir")
  logfile=findtok(toks, "logfile")
  argdict['filetype']=bakext
  argdict['srcdir']=srcdir
  argdict['destdir']=destdir
  argdict['logfile']=logfile
  
  baktype=findtok(toks, "baktype")
  plugins=bakplugin.getcanhandle(baktype[0])
  if len(plugins)==0:
    print("ERROR: Couldn't find plugin to handle task: "+baktype[0])
    return
  
  p=plugins[0][0]()
  p.backup(argdict)


def run_restore(filename):
  toks=tokenize(filename)
  bakext=findtok(toks, "filetype")
  srcdir=findtok(toks, "srcdir")
  destdir=findtok(toks, "destdir")
  logfile=findtok(toks, "logfile")
  restorepath=findtok(toks, "restorepath")
  argdict['filetype']=bakext
  argdict['srcdir']=srcdir
  argdict['destdir']=destdir
  argdict['logfile']=logfile
  argdict['restorepath']=restorepath
  
  baktype=findtok(toks, "baktype")
  plugins=bakplugin.getcanhandle(baktype[0])
  if len(plugins)==0:
    print("ERROR: Couldn't find plugin to handle task: "+baktype[0])
    return
  
  p=plugins[0][0]()
  p.restore(argdict)


def show_plugins():
  for p in bakplugin.plugin_list:
    print(p[1]+" "+p[2])


def main(argv):
  sys.path.append(".")
  sys.path.append(getbasedir()+"/plugins")
  sys.path.append(getbasedir()+"/baktool")
  
  bakplugin.load_plugin_file(getbasedir()+"/plugins/plugins.list")
  
  if len(argv)==0:
    print_usage()
    return
  
  action=argv[0]
  
  if action=="backup":
    run_backup(argv[1])
  elif action=="restore":
    run_restore(argv[1])
  elif action=="plugins":
    show_plugins()
  else:
    print_usage()

if __name__=="__main__":
  main(sys.argv[1:])