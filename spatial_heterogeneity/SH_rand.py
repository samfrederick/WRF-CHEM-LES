import numpy as np
import time
from functools import wraps
import multiprocessing

# Timing function for testing module performance
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

# Original SH module
@timeit
def SH(f):
    m=np.mean(f)
    G=0
    d1=f.shape[0]
    d2=f.shape [1]
    f =np.hstack((f, f))
    f =np.vstack((f, f))

    for y1 in range(d1+1):
        for y2 in range(y1+1,y1+d1+1):
            for x1 in range(d2+1):
                for x2 in range(x1+1,x1+d2+1):
                    fbar=f[y1:y2,x1:x2]
                    G+= abs(np.mean(fbar)-m)

    G = G/(d1*d1*d2*d2)
    
    return G

# Modified SH module - Compute SH with random collection of array subset permutations
#@timeit
def SH_random(f, n_permutations, permutation_array=None):
    """Compute the spatial heterogeneity metric from a random subset of permutations
    """
    m=np.mean(f)
    G=0
    d1=f.shape[0]
    d2=f.shape[1]
    total_permutes = d1*d2*(d1+1)*(d2+1)
    
    if permutation_array is None:
        permutation_array = SH_permutations(f)

    f =np.hstack((f,f))
    f =np.vstack((f,f))
    rng = np.random.default_rng()
    random_permuation_idx = rng.choice(total_permutes, size=n_permutations, replace=False)
    random_permutations = permutation_array[random_permuation_idx, :]
    f_permutes = np.empty((n_permutations, f.flatten().shape[0]))
    f_permutes[:] = np.nan

    i = 0
    for permute in random_permutations:
        x1 = permute[0]
        x2 = permute[1]
        y1 = permute[2]
        y2 = permute[3]
        f_subset = f[y1:y2,x1:x2].flatten()

        f_permutes[i, 0:f_subset.shape[0]] = f_subset
        i += 1
        
    G = abs(np.nanmean(f_permutes, axis=1)-m).sum()

    return total_permutes*G/(n_permutations*d1*d1*d2*d2)

@timeit
def SH_permutations(f):
    """Generate all permutations (subsets of f) for the SH metric"""
    d1=f.shape[0]
    d2=f.shape[1]
    total_permutes = d1*d2*(d1+1)*(d2+1)
    f =np.hstack((f,f))
    f =np.vstack((f,f))
    permutation_array = np.zeros((total_permutes, 4)).astype(int)
    count = 0
    for y1 in range(d1+1):
        for y2 in range(y1+1,y1+d1+1):
            for x1 in range(d2+1):
                for x2 in range(x1+1,x1+d2+1):
                    permutation_array[count, 0] = x1
                    permutation_array[count, 1] = x2
                    permutation_array[count, 2] = y1
                    permutation_array[count, 3] = y2

                    count += 1
                
    return permutation_array

def parallel_SH_random(args):
    array, n_permutations, permutation_array = args
    return SH_random(array, n_permutations, permutation_array=permutation_array)

def Compute_Percent_Error(SH_estimate, SH_star):
    
    # Compute the percent error between metric value estimated by SH_random and true SH
    SH_error = 100*(SH_estimate-SH_star)/SH_star
    print(f'Percent error: {SH_error:3.2f}% calculating SH with {n_permutations} out of {total_permutes} total permutations')

#@timeit
def SH_random_serial_ensemble(n_estimates, array, n_permutations, permutation_array):
    # Serial method for computing ensemble of SH estimates. The mean value of the
    # ensemble is taken to be the final estimate of SH metric.
    SH_estimates = np.zeros(n_estimates)
    SH_estimates[:] = np.nan
    for i in range(n_estimates):
        SH_estimates[i] = SH_random(array, n_permutations, permutation_array=permutation_array)
    SH_estimate = SH_estimates.mean()
    return SH_estimate, SH_estimates

if __name__ == '__main__':

    # Test metric on a 10x10 array
    d1, d2 = 20, 20
    array = np.random.random((d1, d2))
    total_permutes = d1*d2*(d1+1)*(d2+1)
    n_permutations = 100

    # The code can either be throttled by the number of permutations to loop over 
    # and compute the heterogenity for, or the size of the array, which makes the 
    # permuation for loop more costly
    #G = SH_random(array, n_permutations)

    """
    # Note that we can pre-compute the permutation array and pass it to SH_random
    # This has the benefit of speeding up computation if calculating SH multiple 
    # times for arrays of the same size (e.g., calculating SH for each x-y plane
    # in a 3-d computational domain - the dimensions of the x-y plane array wont
    # change so we can pre-compute all the permutations (subsets of f) and pass
    # that to the SH_random method).
    permutation_array = SH_permutations(array)
    np.save(f'{d1}x{d2}_permutation_array.npy', permutation_array)
    """


    print('Loading permutation array')
    load_start = time.time()
    permutation_array = np.load(f'{d1}x{d2}_permutation_array.npy').astype(int)
    load_end = time.time()
    print(f'Permutation array load time: {load_end - load_start:3.2f} seconds')
    #G = SH_random(array, n_permutations, permutation_array=permutation_array)

    n_estimates = 100
    

    """
    # Parallel method for computing ensemble of SH estimates. Note that this 
    # method is really not competitive with the serial ensemble (below) at small
    # iterations (e.g., n_estimates < ~1000)
    start_time = time.perf_counter()
    pool_obj = multiprocessing.Pool()
    args = n_estimates*[(array, n_permutations, permutation_array)]
    SH_estimates = np.array(pool_obj.map(parallel_SH_random, args))
    SH_estimate = SH_estimates.mean()
    end_time = time.perf_counter()
    print(f'Parallel run time: {end_time-start_time:3.4f}')
    """

    SH_estimate, SH_estimates = SH_random_serial_ensemble(n_estimates, array, n_permutations, permutation_array)
    std_err = SH_estimates.std() / np.sqrt(n_estimates)
    print(f'Spatial heterogeneity estimate 95% CI: {SH_estimate:3.5f} +/- {1.959*std_err:3.2e}')


    # The true value of the spatial heterogeneity metric
    #SH_star = SH(array)

    #Compute_Percent_Error(SH_estimate, SH_star)

    """
    SH_star = SH(array)
    
    G_sample= np.zeros(100)
    RelError_sample = np.zeros(100)
    for j in range(100):
        G_estimates = np.zeros(n_estimates)
        for i in range(n_estimates):
            G_estimates[i] = SH_random(array, n_permutations, permutation_array=permutation_array)
        G_sample[j] = G_estimates.mean()
        RelError_sample[j] = 100*(G_estimates.mean()-SH_star)/SH_star
    
    import pandas as pd
    print(pd.DataFrame(G_sample).describe())
    print(pd.DataFrame(RelError_sample).describe())
    """