#! /usr/bin/python

def get_html():

    import pandas as pd
    from urllib import urlretrieve
    import os, subprocess, csv, json

    rootdir = os.getcwd() + '/'
    with open(rootdir + 'states2.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            stateabbrevs = row


    for st in stateabbrevs:
        tree = os.walk(rootdir +'/data/' + st + '/bills/' + st)
        for root, dirs, files in tree:
            for f in files:
                with open(root + '/' + f, 'r') as billfile:
                    subpath = '/' + '/'.join(root.split('/')[-3:]) + '/'
                    savedir = rootdir + 'html' + subpath
                    if not os.path.exists(savedir): os.makedirs(savedir)
                    try:
                        bill = json.load(billfile)
                        itemtype = bill['versions'][-1]['mimetype']
                        if itemtype == 'text/html':
                            url = bill['versions'][-1]['url']
                            saveloc = savedir + f.replace(' ','_') + '.html'
                            urlretrieve(url, saveloc)
                    except:
                        pass

        bucketloc = str("s3://zipf/states/")
        p = subprocess.Popen(["s3cmd", "put", "--recursive", str(rootdir + "html/"), bucketloc])
        p.communicate()
        p2 = subprocess.Popen(["rm", "-rf", str(rootdir + "html")])
        p2.communicate()
        p3 = subprocess.Popen(["mkdir", str(rootdir + "html")])
        p3.communicate()
        p4 = subprocess.Popen(["echo",st])
        p4.communicate()