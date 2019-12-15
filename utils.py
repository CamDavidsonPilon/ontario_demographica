# utils.py

def hdi(cdf, p):
    n = cdf.shape[0]
    for delta in range(1, 100):
        l = 0
        while l + delta < n:
            u = l + delta
            if 0.975 * p < (cdf.iloc[u] - cdf.iloc[l]):
                return (cdf.index[l], cdf.index[u])

            l+=1
