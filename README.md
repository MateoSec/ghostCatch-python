# ghostCatch-python
Python to disable AJP connectors in Apache Tomcat to remediate CVE-2020-1938 (Ghostcat)!
                                  
Currently written for:
Python 2.7

Requires: 
pip install progress

Usage: python ghostCatch.py <flag1> <flag2>

      -help   is the flag for usage
              Example: python ghostCatch.py -help

      -path   is the flag to specify path"
              Example: python ghostCatch.py -path /myPath

              To search entire system for server.xml files: 
              python ghostCatch.py -path default




