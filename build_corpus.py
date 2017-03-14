from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import json
import os

archives = ['extraction_warc1', 'extraction_warc2']


def saveHtml(archives):
    '''this will go through each archive extraction and save the HTML for each link in a seprate directory
    it will create a json log file of what was done, and it will create a json corpus of the content of each 
    link it visited'''
    for archive in tqdm(archives):
        # check our dir structure is setup
        if not os.path.exists(str(archive)):
            os.mkdir(str(archive))
            hdir = str(archive) + '/html'
            os.mkdir(hdir)
            # open a log file
        with open(str(archive)+ '/' + str(archive) + '_log.json','a') as logfile:
            # open the extraction file
            with open(str(archive) + '.json', 'r') as infile:
                # open document store
                with open(str(archive)+ '/' + str(archive) + '_corpus' + '.json', 'a') as docstore:
                    # load extraction
                    arch_js = json.load(infile)
                    for key in tqdm(list(arch_js.keys())):
                        ld = {}
                        log_dict = dict(filename='None', save='None', htmlPath='None', in_corpus='None', errors='None')
                        # log['{}'.format(str(key))]
                        record = arch_js[str(key)]
                        url = record['archive']
                        req = requests.get(url)
                        if req.status_code == 200:
                            html = req.text
                            with open('{}/html/record_{}.html'.format(str(archive), str(key)), 'w') as savefile:
                                savefile.write(html)
                            log_dict['save'] = 'Yes'
                            log_dict['html_path'] = '{}/record_{}.html'.format(str(archive), str(key))
                            log_dict['filename'] = 'record_{}.html'.format(str(key))
                            soup = BeautifulSoup(html)
                            try:
                                sd = {}
                                text = soup.find(class_= 'legacy-content').text
                                soup_dict = dict(text=text, title=record['title_con'], date=record['ts'])
                                sd[str(key)] = soup_dict
                                # append to docstore
                                json.dump(sd, docstore)
                                log_dict['in_corpus'] = 'Yes'
                            except AttributeError:
                                log_dict['in_corpus'] = 'No'
                                log_dict['errors'] = 'AttributeError'
                        else:
                            log_dict['errors'] = 'Server'

                        ld['{}'.format(str(key))] = log_dict
                        json.dump(ld, logfile)



def main():
    saveHtml(archives)
    for i in archives:
        with open(str(archive)+ '/' + str(archive) + '_log.json','r') as lg:
            with open(str(archive)+ '/' + str(archive) + '_corpus.json','r') as docs:
                lglines = lg.read()
                lgfixed = lglines.replace('}}{', '},')
                dclines = docs.read()
                dcfixed = dclines.replace('}}{', '},')
                lgd = json.loads(lgfixed)
                dcd = json.loads(dcfixed)
                with open(str(archive)+ '/' + str(archive) + '_logf.json','w') as fixlog:
                    json.dump(lgd,fixlog)
                with open(str(archive)+ '/' + str(archive) + '_corpusf.json','w') as fixdocs:
                    json.dump(dcd,fixdocs)




main()
