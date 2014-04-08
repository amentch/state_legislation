def get_html_mt():
    import pandas as pd
    from urllib import urlretrieve
    import os, subprocess, csv, json
    from multiprocessing import Pool
    from multiprocessing.dummy import Pool as ThreadPool
    
    def multi_arg(tup):
        url = tup[0]
        saveloc = tup[1]
        urlretrieve(url, saveloc)
    
    
    rootdir = os.getcwd() + '/'
    with open(rootdir + 'states2.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            stateabbrevs = row


    for st in stateabbrevs:
        urls = []
        savelocs = []
        tree = os.walk(rootdir +'/data/' + st + '/bills/' + st)
        for root, dirs, files in tree:
            for f in files:
                with open(root + '/' + f, 'r') as billfile:
                    subpath = '/' + '/'.join(root.split('/')[-3:]) + '/'
                    savedir = rootdir + '/html' + subpath
                    if not os.path.exists(savedir): os.makedirs(savedir)
                    try:
                        bill = json.load(billfile)
                        itemtype = bill['versions'][-1]['mimetype']
                        if itemtype == 'text/html':
                            urls.append(bill['versions'][-1]['url'])
                            savelocs.append(savedir + f.replace(' ','_') + '.html')
                    except:
                        pass
        if len(urls) > 0:            
            zipped = zip(urls, savelocs)
            pool = ThreadPool(8)
            results = pool.map(multi_arg, zipped)
            pool.close()
            pool.join()
            
            bucketloc = str("s3://zipf/states/")
            p = subprocess.Popen(["s3cmd", "put", "--recursive", str(rootdir + "/html/"), bucketloc])
            p.communicate()
            p2 = subprocess.Popen(["rm", "-rf", str(rootdir + "html")])
            p3 = subprocess.Popen(["mkdir", str(rootdir + "html")])
            p4 = subprocess.Popen(["echo",st])
