from Cheetah.Template import Template
from optparse import OptionParser
import os
import re
import operator

#The default number of results to show
DEFAULT_SHOW_NUM = {
'URL' : 10,
'REFERRER' : 10,
'REMOTE_IP' : 10,
"RESPONSE_TIME_SEC": 20,
#"MIN": 20,
}


def analyze_output(output_dir):
    """ Take the raw hadoop output and analyze it grabbing the data we want to show """
    listing = os.listdir(output_dir)
    dic = {}
    for output_file in listing:
        f = open('./%s/%s'%(output_dir,output_file))
        for i in f.readlines():
            tmp_st = re.sub("[\[\]\"\,\n]","",i)
            try:
                type_of_record, key,value  = re.sub(" {2,5}|\t"," ",tmp_st).split(' ')
            except:
                print i
                continue
        
            if type_of_record in dic:
                dic[type_of_record][key] =  int(value)
            else:
                #TODO: Fix this
                dic[type_of_record] = {}
                dic[type_of_record][key] =  int(value)
        f.close()
        #list to be set will be in the format
        #[key,[list_of_names,list_of_countscount]]
        #i.e
        #['URL',['list_of_urls','list_of_url_counts']]
        complete_list=[]
        for key,value in dic.iteritems():
            # If we want to show results via counts rather than alphabetically (ie url counts vs dates)
            if key in DEFAULT_SHOW_NUM:
                end = DEFAULT_SHOW_NUM[key]
                sort_by = 1
                reverse = True
            else:
                end = None
                sort_by = 0
                reverse = False
            sorted_x = sorted(value.iteritems(), key=operator.itemgetter(sort_by), reverse=reverse)
            k = [i[0] for i in sorted_x[0:end]]
            v = [i[1] for i in sorted_x[0:end]]
            complete_list.append([key,[k,v]])

    return complete_list
    


def create_html(complete_list):
    """ Create the graph.html file using cheetah template"""
    path = os.path.join('./', 'show_apache_graphs.tmpl')
    template_var = { 'types': complete_list }
    
    tmpl = Template( file = path, searchList = (template_var,) )
    
    html_file = open('./graphs.html','w')
    html_file.write(str(tmpl))
    html_file.close()

def start_web_server():
    """ Quick easy access to see the graphs"""
    import SimpleHTTPServer
    import SocketServer
    
    PORT = 8000
    
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    
    print "serving at port", PORT
    httpd.serve_forever()


def main():
    parser = OptionParser()
    parser.add_option("-o", "--outputdir", dest="outputdir",
                      help="The hadoop process outputdir", metavar="outputdir")
    parser.add_option("-S", "--webserver",
                      dest="simplehttp", 
                      help="Start a simple http server on port 8000 to quickly access graphs at http://localhost:8000/graphs.html, to enable this option \
                            pass in -S true")
    (options, args) = parser.parse_args()


    complete_list = analyze_output(options.outputdir)
    create_html(complete_list)
    if options.simplehttp:
        start_web_server()




#if main == __init__:
main()
