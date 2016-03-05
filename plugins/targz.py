# targz -- A plugin to handle the creation ot tar.gz archives.

import bakplugin
import os

class_name="targz"
type_str=bakplugin.PLUGIN_TYPE_ARCHIVE

class targz(bakplugin.ArchiveTool):
  name="targz"
  
  
  def can_handle(self, ext):
    return ext==".tar.gz"
  
  
  def compress(self, src, dest):
    fnametoks=src.split('/')
    fname=fnametoks[len(fnametoks)-1]
    os.system("tar -czf "+dest+"/"+fname+".tar.gz "+src)
    return fname
  
  
  def extract(self, src, dest):
    os.system("tar -xzf "+src+" -C "+dest)
