# This module contains classes and functions related to 
# running backup plugins.
import sys
import os
import importlib
import datetime

class ArchiveTool:
  name=None
  
  
  def can_handle(self, ext):
    return 0
  
  
  def compress(self, src, dest):
    return "" # For filename


  def extract(self, src, dest):
    return

  
  def __init__(self):
    return


class BackupTool:
  name=None
  
  
  def backup(self, args):
    return
  
  
  def restore(self, args):
    return
  
  
  def can_handle(backuptype):
    return 0


  def __init__(self):
    return


plugin_list=[]
PLUGIN_TYPE_ARCHIVE="ArchiveTool"
PLUGIN_TYPE_BACKUPRUNNER="BackupTool"


def loadplugin(plugin_name):
  plugin=importlib.import_module(plugin_name)
  
  plugin_class_name=""
  try:
    plugin_class_name=plugin.class_name
  except(AttributeError):
    print("ERROR: Couldn't load plugin: "+plugin_name)
    return
  
  plugin_class=getattr(plugin, plugin_class_name)
  p=plugin_class()
  if p.name==None:
    print("ERROR: Plugin didn't export a name: "+plugin_name)
    return
  
  plugin_list.append([plugin_class, p.name, plugin.type_str])


def load_plugin_file(filename):
  try:
    f=open(filename, "r")
    contents=f.read()
    lines=contents.splitlines()
    
    for l in lines:
      loadplugin(l)
  except(IOError):
    print("Plugin file doesn't exist.")
    return


def getoftype(plugin_type):
  ret_list=[]
  for p in plugin_list:
    if p[2]==plugin_type:
      ret_list.append(p)
  
  return ret_list


def getcanhandle(ext):
  ret_list=[]
  for p in plugin_list:
    pl=p[0]()
    if pl.can_handle(ext):
      ret_list.append(p)
  return ret_list


# Implement some common utility functions:


def logbackup(logfile, bakfilename):
  logfile.write(bakfilename+" "+str(datetime.date.today())+"\n")


def readlog(logfilename):
  f=open(logfilename, "r")
  contents=f.read()
  f.close()
  
  lines=contents.splitlines()
  retlist=[]
  
  for l in lines:
    toks=l.split()
    filename=toks[0]
    datetoks=toks[1].split('-')
    d=datetime.date(int(datetoks[0]), int(datetoks[1]), int(datetoks[2]))
    retlist.append([filename, d])
    
  return retlist
