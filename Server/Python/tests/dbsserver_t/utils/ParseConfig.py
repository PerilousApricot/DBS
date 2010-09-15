"""Used to parse the config file and get reader and writer instances informations from it"""

import sys
from WMCore.Configuration import loadConfigurationFile

def echoInfo(configfile): 
    cfg = loadConfigurationFile(configfile)
    wconfig = cfg.section_("Webtools")
    app = wconfig.application
    appconfig = cfg.section_(app)
    service = list(appconfig.views.active._internal_children)[0]
    dbsconfig = getattr(appconfig.views.active, service)   
    print dbsconfig.database
    print dbsconfig.dbowner
    
if __name__ == "__main__":
    echoInfo(sys.argv[1])