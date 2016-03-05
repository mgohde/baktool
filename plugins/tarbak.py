# tarbak -- Defines a full tar backup script.

import bakplugin
import os

class_name="tarbak"
type_str=bakplugin.PLUGIN_TYPE_BACKUPRUNNER


class tarbak(bakplugin.BackupTool):
  name="tarbak"


  def backup(self, args):
    baktool=bakplugin.getcanhandle(".tar.gz")
    
    if len(baktool)==0:
      print("ERROR: Couldn't find handler for .tar.gz archives.")
      return
    
    # Ignore the backup extension
    srcdirs=args['srcdir']
    destdir=args['destdir']
    logfile=args['logfile']
    
    bakp=baktool[0][0]()
    lf=open(logfile[0], "w")
    
    for s in srcdirs:
      fname=bakp.compress(s, destdir[0])
      bakplugin.logbackup(lf, fname)
    
    lf.close()
    return
  
  
  def restore(self, args):
    # Start  by getting the backup log:
    logfile=args['logfile']
    restorepath=args['restorepath']
    
    logtokens=bakplugin.readlog(logfile[0])
    
    baktool=bakplugin.getcanhandle(".tar.gz")
    if len(baktool)==0:
      print("ERROR: Couldn't find handler for .tar.gz archives.")
      return
    
    bakp=baktool[0][0]()
    
    for t in logtokens:
      bakp.extract(t[0], restorepath[0])
    return
  
  
  def can_handle(backuptype):
    return backuptype=="full/targz"
  