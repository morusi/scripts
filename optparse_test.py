from optparse import OptionParser
#import sys
parser = OptionParser()
parser.add_option("-C", "--create", dest = "iscreate", action = "store_true")
parser.add_option("-h", "--host", dest = "hostnames")
parser.add_option("-t", "--template", dest = "templatenames" )
parser.add_option("-g", "--group", dest = "groupnames" )
parser.add_option("-U", "--update", dest = "isupdate", action = "store_true")

(options, args) = parser.parse_args()

print options + "===" + args