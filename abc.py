#!/usr/bin/env python
"""
tail n (default 5) lines of a file
"""
import optparse

def tail(target, lines):
    """tail function to open target file and return lines
    default is to return 5 lines
    function will return a list (char) empty if nothing
    """

    #default line is 5 lines
    if not lines:
        lines=5

    #can not access file exception
    try:
        f=open(target)
    except IOError, error:
        raise SystemExit(error)

    #empty list that will hold results
    results=[]

    #go to end of the file. and get current position
    f.seek(0,2)
    pos=f.tell()-1 #last position is end, so we alway go back 1 postion

    #if file is empty (0) close and return empty list
    if pos<0:
        f.close()
        return []

    #loop the file
    while True:
        #each time, go back 1 postion
        pos-=1
        f.seek(pos)
        #read only 1 char
        char=f.read(1)
        #if char is line end, lines count -1
        if char=='\n':
            lines-=1
        #lines == 0, then close the file and break the loop
        if lines==0:
            f.close()
            break
        #append char to result
        results.append(char)
        #back to begin of file. close and break
        if pos==0:
            f.close()
            break
    #we read from back to begin. so we need to reverse it
    results.reverse()
    #return the list back
    return results

def print_help(prog_name):
    print ("Usage: %s [options] filename" %prog_name)
    print ("Options:")
    print ("\t-l LINE_NUMBER, --lines=LINE_NUMBER optional arg, default is 5 lines")
    raise SystemExit()


def main():
    parser=optparse.OptionParser(add_help_option=False)
    parser.add_option('-l', '--lines', action='store', type='int', dest='line_number')
    options, args = parser.parse_args()
    print options, args[0]
    if not args or len(args)>1:
        print_help(parser.get_prog_name())
    if options.line_number<0 and options.line_number!=None:
        print_help(parser.get_prog_name())
    results = tail(args[0], options.line_number)
    print ''.join(results)


if __name__=='__main__':
    main()
