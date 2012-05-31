import re
from mrjob.job import MRJob
import datetime

#LINE_REGEX=re.compile("^(\d*\.\d*\.\d*\.\d*) (.*) (.*) \[(\d*\/[A-z]*\/[\d:]*) -(\d*)\] \"([A-z]*?) (.*?) (.*?)\" (\d*?) (\d*?) (\d*?)us \"(.*?)\" \"(.*)\"$")
#LINE_REGEX=re.compile('^(?P<remote_ip>[^ ]+) (?P<local_ip>[^ ]+) (?P<server_name>[^ ]+) (?P<user>[^ ]+) \[(?P<date>[^ ]+) (?P<date2>[^ ]+)\] "(?P<conn_status>[^ ]+) (?P<request>[^ ]+) (?P<http_type>[^ ]+)" (?P<init_retcode>[^ ]+) (?P<byte>[^ ]+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)" (?P<pid>[^ ]+)/(?P<tid>[^ ]+) (?P<req_sec>[^ ]+)/(?P<req_time>[^ ]+)')
#LINE_REGEX=re.compile('^(?P<remote_ip>[a-zA-Z0-9., ]*[^ ]+[, ]?) (?P<local_ip>[^ ]+) (?P<server_name>[^ ]+) (?P<user>[^ ]+) \[(?P<date>[^ ]+) (?P<date2>[^ ]+)\] "(?P<conn_status>[^ ]+) (?P<request>[^ ]+) (?P<http_type>[^ ]+)" (?P<init_retcode>[^ ]+) (?P<byte>[^ ]+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)" (?P<pid>[^ ]+)/(?P<tid>[^ ]+) (?P<req_sec>[^ ]+)/(?P<req_time>[^ ]+)')
LINE_REGEX=re.compile('^(?P<remote_ip>[a-zA-Z0-9., \-]*[^ ]+[, ]?) (?P<local_ip>[^ ]+) (?P<server_name>[^ ]+) (?P<user>[^ ]+) \[(?P<date>[^ ]+) (?P<date2>[^ ]+)\] "(?P<conn_status>[^ ]+) (?P<request>[^ ]+) ?(?P<http_type>[^ ]+)?" (?P<init_retcode>[^ ]+) (?P<byte>[^ ]+) "(?P<referrer>[^"]+)?" "(?P<user_agent>[^"]+)" (?P<pid>[^ ]+)/(?P<tid>[^ ]+) (?P<req_sec>[^ ]+)/(?P<req_time>[^ ]+)')
URL_REGEX=re.compile("^http[s]?://(.*?)/.*")

class AnalyzeLogs(MRJob):

    def mapper(self, lines, key):

        m = LINE_REGEX.match(key)
        if m:
            groups = m.groupdict() 
        else:
            groups = None

        dic = {}
        if groups:
            for key,value in groups.iteritems():
                if key == 'date':
                    dt=datetime.datetime.strptime(value, '%d/%b/%Y:%H:%M:%S')
                    month = dt.strftime("%m/%Y")
                    day = dt.strftime("%m/%d/%Y")
                    dic['MONTH'] = month
                    dic['DAY'] = day
                    dic['HOUR'] = dt.strftime("%H")
                    dic['TEN'] = dt.strftime("%H:%M")[:-1]
                    dic['MIN'] = dt.strftime("%H:%M")
                elif key == 'request':
                    if value:
                        url = value.split('?')[0]
                    else:
                        url = "None"
                    dic['URL'] = url
                elif key == 'referrer':
                    if value:
                        refer = value.split('?')[0]
                        rm = URL_REGEX.match(refer)
                        if rm:
                            refer = rm.groups()[0]
                    else:
                        refer = "None"
                    dic['REFERRER'] = refer
                elif key == 'remote_ip':
                    dic['REMOTE_IP'] = value
                elif key == 'req_sec':
                    dic['RESPONSE_TIME_SEC'] = value
                elif key == 'init_retcode':
                    dic['INIT_RETCODE'] = value
        else:
            yield ("NONE-ALL", key), 1

        for key,value in dic.iteritems():
            yield (key,value), 1

    def reducer(self, key, value):
        yield key, sum(value)

if __name__ == '__main__':
    AnalyzeLogs.run()

