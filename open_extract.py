import warc
import json
import gzip
from datetime import datetime

def open_warc(path):
    data = []
    with gzip.open(path,mode='rb') as gzf:
        for record in warc.WARCFile(fileobj=gzf):
            data.append(record.payload.read())
    return data[2:]

def open_warc_gen(path):
    with gzip.open(path,mode='rb') as gzf:
        for record in warc.WARCFile(fileobj=gzf):
            yield record.payload.read()
#     return data[2:]


def refactor_url(url):
    parsed = urlparse(url)
    if parsed.netloc == 'www.whitehouse.gov':
        altHost = 'https://obamawhitehouse.archives.gov'
        path = parsed.path
        return altHost+path
    else:
        pass


def extract(data):
    files = []
    for i in data:
        payload = json.loads(i)
        try:
            url   = payload['Envelope']['WARC-Header-Metadata']['WARC-Target-URI']
            archUrl = refactor_url(url)
            ts    = payload['Envelope']['WARC-Header-Metadata']['WARC-Date']
            ts_dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
            title = payload['Envelope']['Payload-Metadata']['HTTP-Response-Metadata']['HTML-Metadata']['Head']['Title']
            title_con = title.split('-')[-1] 
            title_con = title_con.replace(' | The White House', '').strip()
            result = dict(url=url, archive=archUrl, ts=ts, title=title, title_con=title_con )
            if result != 'None' or result != None:
                files.append(result)
        except:
            pass
    return files

def gen_extract(data):
    for i in data:
        try:
            payload = json.loads(i)
        except:
            pass
        try:
            url   = payload['Envelope']['WARC-Header-Metadata']['WARC-Target-URI']
            archUrl = refactor_url(url)
            ts    = payload['Envelope']['WARC-Header-Metadata']['WARC-Date']
            ts_dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
            title = payload['Envelope']['Payload-Metadata']['HTTP-Response-Metadata']['HTML-Metadata']['Head']['Title']
            title_con = title.split('-')[-1]
            title_con = title_con.replace(' | The White House', '').strip()
            result = dict(url=url, archive=archUrl, ts=ts, title=title, title_con=title_con )
            if result != 'None' or result != None:
                yield result
        except:
            pass


def archive_extraction(warc, file_id):
    # files = extract(data)
    data = open_warc(warc)
    with open('extraction{}.json'.format(file_id),'w') as archive:
        d = {}
        document = 0
        for i in gen_extract(data):
            d["{}".format(str(document))] = i
            document += 1
        js = json.dumps(d,ensure_ascii=True)
        archive.write(js)
        print 'wrote {} documents'.format(document)


warc1 = 'OBAMA-WHITEHOUSE-HACKATHON-PRESS-RELEASES-EXTRACTION-WARCS-PART-00000-000000.warc.wat.gz'
warc2 = 'OBAMA-WHITEHOUSE-HACKATHON-PRESS-RELEASES-EXTRACTION-WARCS-PART-00000-000001.warc.wat.gz'


archive_extraction(warc1,'_warc1')
archive_extraction(warc2,'_warc2')
