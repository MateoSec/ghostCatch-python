# -*- coding: utf-8 -*-
import sys
from sys import platform
import fnmatch
import os
from progress.spinner import Spinner

basePath = ""

#Check if path or help flags have been provided
if((len(sys.argv) > 1)):
    userEntry = sys.argv[1]
    if("-help" in userEntry):
        print ""
        print "Usage: python ghostcatch.py <flag> <path>"
        print ""
        print "      -help   is the flag for usage"
        print "              Example: python ghostcatch.py -help"
        print ""
        print ""
        print "      -path   is the flag to specify path"
        print "              Example: python ghostcatch.py -path /myPath"
        print ""
        print "              To search entire system for server.xml files: "
        print "              python ghostcatch.py -path default"
        print ""
        exit(0)
    if("-path" in userEntry):
        if(len(sys.argv)>2):
            if("default" in str(sys.argv[2])):
                if((sys.platform.startswith("mac")) or (sys.platform.startswith("darwin")) or (sys.platform.startswith("linux"))):
                    print ""
                    print "Using default path of '/'"
                    print ""
                    basePath = "/"
                if(sys.platform.startswith("window")):
                    print ""
                    print "Using default of 'c:\\'"
                    print ""
                    basePath = "c:\\"
            elif(sys.argv[2]!=None):
                print "Using path specified:" + str(sys.argv[2])
                print ""
                basePath = str(sys.argv[2])
        else:
            print ""
            print "You added the -path flag but did not specify a path."
            print "python ghostcatch.py -help for usage."
            print ""
            exit(0)
else:
    print ""
    print "Usage: python ghostcatch.py <flag> <path>"
    print ""
    print "      -help   is the flag for usage"
    print "              Example: python ghostcatch.py -help"
    print ""
    print ""
    print "      -path   is the flag to specify path"
    print "              Example: python ghostcatch.py -path /myPath"
    print ""
    print "              To search entire system for server.xml files: "
    print "              python ghostcatch.py -path default"
    print ""
    exit(0)

#This took a while to make
print """                                  
                                   
                                   @@@@@@@@@@@@@@@@@@@@@@
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                         @@@@@@@@@@@@%  @@@@@@@@@@@@@@@@@@  @@@@
                 @@@@@@@@@@@@@@@@@@@@% \  @@@@@@@@@@@@@@@ / @@@@@
               @/''''''''''#@@@@@@@@@@  \   @@@@(@@@@@@@ /  @@@@@@
              @/   ......   @@@@@@@@@       \\\\     //      ,@@@@@@@
             @.  .@@@@@@@(  @@@@@@@          \\\\   //        @@@@@@@
            @&   @@@@@@@@@@@@@@@@    ,///// ///    /// //// @@@@@@@@
            @,  .@@@@@@@@@@@@@@@#    ,//// ////   /// ////   @@@@@@@@
            @/   @@@@@@@@@@@@@@@     //// ////.  /// ///    @@@@@@@@
            @    /@@@@@@@@@@@*       //////.  __  ////      @@@@@@@@@
            @*       #@@@/               ...  \/ ...       &@@@@@@@
             @*                            ..-'-..      %@@@@@@@
              @&                                       @@@@@@@@&
                @@.                 \   \        \   \ @@@@@@@                         
                @@@&                 |  |         |  |  (@@@@@
                    @@@@\             ***          *** @@@
         ______	________@@___@__@_____________ @ @@@@@@@_
        (______ \  \%\   \%\   \%\   \%\   \%\\ @@     //
               | \  \%\   \%\   \%\   \%\   \%\\@_____//
               | L|'''''''''''''''''''''''''''''||___||
               |__|     o=========o     o====o  | ....| 
                  |     |  -==-   |     | =o |  | |=O||
     =============|     o=========o     o====o  | |=O||
                  |_____________________________|_____|
                  
============================================================================
=                     Okay, who brought the cat?                           =
============================================================================
"""

print "Retrieving all files named server.xml."
print "Maybe grab a coffee -- this may take a minute."
print "                   "
print "       \\\\\\\\    "
print "       ////        "
print "       \\\\\\\\    "
print "       ____        "
print "     C|    |       "
print "       \__/        "
print ""


serverXMLPaths = []

#Homespun spinner using progress library
spinner = Spinner('Checking for lurking Ghostcats...')
state = 'processing'
while state != 'FINISHED':
    for root, dirnames, filenames in os.walk(basePath):
        for filename in fnmatch.filter(filenames, 'server.xml'):
            serverXMLPaths.append(os.path.join(root, filename))
        spinner.next()
    state = 'FINISHED'
print ""

#If there were server.xml files found, lets check for AJP connectors
if(len(serverXMLPaths) > 0):

    ajpConnector = '<Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />'
    disabledAJPConnector = '<!--<Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />-->'

    ajpWithAddressConnector ='''<Connector protocol="AJP/1.3"
    address="::1"
    port="8009"
    redirectPort="8443" />'''
    disabledAJPWithAddressConnector ='''<!--<Connector protocol="AJP/1.3"
    address="::1"
    port="8009"
    redirectPort="8443" />-->'''

    skipped = 0
    countDisabled = 0
    countDisabledNew = 0

    #First check all files for a couple of common AJP connector configurations and disable them
    for path in range(0, len(serverXMLPaths)):
    
        currentFile = open(serverXMLPaths[path],"r")
        fileContent = currentFile.read()
        currentFile.close()

        if((disabledAJPConnector in fileContent) or (disabledAJPWithAddressConnector in fileContent)):
        
            countDisabled += 1
        
        else:
        
            if (ajpConnector in fileContent):
            
                print "Commenting out AJP connector..." 

                fileContent = fileContent.replace(ajpConnector, disabledAJPConnector)
                
                currentFile = open(serverXMLPaths[path],"w+")
                currentFile.write(fileContent)
                currentFile.close()

                countDisabledNew += 1
            
            elif (ajpWithAddressConnector in fileContent):
                
                print "Commenting out AJP connector..." 

                fileContent = fileContent.replace(ajpWithAddressConnector, disabledAJPWithAddressConnector)
                
                currentFile = open(serverXMLPaths[path],"w+")
                currentFile.write(fileContent)
                currentFile.close()

                countDisabledNew += 1
            
            else:
                fileContentLines = fileContent.split("\n")
                
                # Read each line, when connector and port 8009 and protocol ajp/1.3 found on same line save that line
                # if the line after that line contains /> comment that out
                # if line after that doesn't contain /> continue to next line until finding closing xml

                connectorLines = []
            
                for line in range(0, len(fileContentLines)):
                    
                    content = fileContentLines[line]
                    if(('protocol="AJP/1.3"' in content) and ('<Connector' in content)):
                        
                        connectorLines.append(content)

                        lineAhead=fileContentLines[line+1]
                        lineAheadTwo=fileContentLines[line+2]
                        lineAheadThree=fileContentLines[line+3]
                        lineAheadFour=fileContentLines[line+4]

                        if("/>" in content):
                        
                            #We did it folks
                            print "Got em."
                            fileContent = fileContent.replace(connectorLines[0], "<!--" + connectorLines[0] + "-->")

                            currentFile = open(serverXMLPaths[path],"w+")
                            currentFile.write(fileContent)
                            currentFile.close()   

                            countDisabledNew += 1
                        
                        elif("/>" in lineAhead):
                            
                            connectorLines.append(lineAhead)
                        
                        elif("/>" in lineAheadTwo):
                        
                            connectorLines.append(lineAhead)
                            connectorLines.append(lineAheadTwo)
                        
                        elif("/>" in lineAheadThree):

                            connectorLines.append(lineAhead)
                            connectorLines.append(lineAheadTwo)
                            connectorLines.append(lineAheadThree)
                        
                        elif("/>" in lineAheadFour):

                            connectorLines.append(lineAhead)
                            connectorLines.append(lineAheadTwo)
                            connectorLines.append(lineAheadThree)
                            connectorLines.append(lineAheadFour)

                        else:
                            print "Sorry, not finding any AJP connectors."
                            print "If you believe this to be in error,"
                            print "Please check the following files: "
                            print str(serverXMLPaths)
                            skipped += 1

                # If we found AJP connector across lines, join the lines and use this string to disable the connector
                # If it's already commented out though, just ignore it
                if (len(connectorLines) > 2):
                    
                    connector = "\n".join(connectorLines)

                    if(("<!--" in connector) and ("-->" in connector)):
                        countDisabled +=1
                    else:
                        fileContent = fileContent.replace(connector, "<!--" + connector + "-->")

                        currentFile = open(serverXMLPaths[path],"w+")
                        currentFile.write(fileContent)
                        currentFile.close()   

                        countDisabledNew += 1

    if(countDisabledNew > 0):
        print "------------------------------------------------------------------------"
        print "Completed AJP connector disabling for all server.xml's on system."
        print "------------------------------------------------------------------------"
        print "Total skipped due to not finding AJP connector string:" + str(skipped)
        print "Total already disabled: " + str(countDisabled)
        print "Total newly disabled: " + str(countDisabledNew)
        print "------------------------------------------------------------------------"
        print "Please restart any known Apache Tomcat servers running."
        print "------------------------------------------------------------------------"
        print "Ghostcats successfully captured."
    else:
        print "------------------------------------------------------------------------"
        print "Total skipped due to not finding AJP connector string:" + str(skipped)
        print "Total already disabled: " + str(countDisabled)
        print "Total newly disabled: " + str(countDisabledNew)
        print "------------------------------------------------------------------------"
        print "No Ghostcats lurking here."
        print "------------------------------------------------------------------------"
else:
    print "------------------------------------------------------------------------" 
    print "No Ghostcats lurking here."
    print "------------------------------------------------------------------------" 

print "..."
print ".."
print "."

#TODO automatically restart any Tomcats currently running or processes based out of a Tomcat directory (switch)


