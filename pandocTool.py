import os

def md2html(filename):
    #cmd = 'pandoc ' + filename + ' -s --highlight-style tango' #generate too much html tags
    cmd = 'pandoc ' + filename 
    output = os.popen(cmd).read()
    #append <link rel="stylesheet" href="http://www.tanglei.name/pandoc_highlight_style_tango.css" type="text/css" />
    return output

#print md2html('test.md')
