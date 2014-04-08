def x_cluster_embed(F):

    import numpy as np
    import scipy as sp
    # from sklearn.cluster import MiniBatchKMeans

    n = np.shape(F)[0]
    baseconv = 0.001

    E = np.empty((n,4))

    for i in range(4):
        v0 = np.random.randn(n,1)
        E[:,i] = pic(F, v0, baseconv/n, 5000)

    # km = MiniBatchKMeans(n_clusters=k)
    # km.fit_transform(E)
    return E


def pic(F, v0, conv, maxit):

    import numpy as np
    import scipy as sp

    n = np.shape(F)[0]
    vt = v0
    dt = np.ones((n,1))
    dtp = np.zeros((n,1))

    i = 0

    while(max(abs(dt-dtp)[0]) > conv and i < maxit):
        # print i
        vtp = vt
        dtp = dt
        # print np.shape(vt)
        # print 'affinity'
        vt = affinity_mat(F, vt)
        # print np.shape(vt)
        vt = vt / sum(vt)
        # print np.shape(vt)
        dt = abs(vt - vtp)

        i += 1

    return [x[0] for x in vt.tolist()]


def affinity_mat(F, vt):
    import numpy as np
    import scipy as sp
    from scipy.sparse import csr_matrix, spdiags

    # print np.shape(F)
    # outer = F * F.T
    n = np.shape(F)[0]
    nvec = []
    for i in range(n):
        val = F[i]*F[i].T
        nvec.append(val.toarray()[0][0])
    print np.shape(nvec)
    N = spdiags(nvec,0,n,n)
    # N = csr_matrix(ndiag)

    # d1 = np.dot(N, np.ones((np.shape(outer)[0],1)))
    # d2 = np.dot(F.T, d1)
    # d3 = np.dot(F, d2)
    d = np.dot(N, np.dot(F, np.dot(F.T, np.dot(N, np.ones((np.shape(F)[0],1))))))

    ddiag = np.diag(d.T.tolist()[0])
    Dinv = np.linalg.inv(ddiag)
    
    # in1 = np.dot(N, vt)
    # in2 = np.dot(F.T, in1)
    # in3 = np.dot(F, in2)
    # in4 = np.dot(N, in3)
    in4m = np.matrix(np.dot(N, np.dot(F, np.dot(F.T, np.dot(N, vt)))))
    # print np.shape(Dinv)
    # print np.shape(in4m)
    return Dinv * in4m.T











