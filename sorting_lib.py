import numpy as np

#%%
# The counting sort gives as an input an array of integers and retruns sorted array and the order for sorted array
def counting_sort(array):
    aux_array = [0]*1000 # make auxilary array of size 1000, we suppose the ordinal are between 0 and 999, however it can be any range
    order = [0]*len(array)
    # calculate the frequencies 
    for i in array:
        aux_array[i] += 1
    # calculate the cumulative values of the frequencies
    for i in range(1,len(aux_array)):
        aux_array[i] += aux_array[i-1]
    sorted_array = [None]*len(array)
    # put tha values in array to sorted array on the right position and store the order
    for j,i in enumerate(array):
        order[aux_array[i]-1] = j
        sorted_array[aux_array[i]-1] = i
        aux_array[i] += -1
    return sorted_array, order

#%%
# The function gives as an input a sorted array and an index array correspond to the sorted array to generate the subproblems 
def subproblem(sorted_array, index_array):
    # while the sorted_array is already sorted the function looks for consecutive same values to recognize the subproblems 
    problem_list = list()
    problem = [index_array[0]]
    for i in range(1,len(sorted_array)):
        if sorted_array[i] == sorted_array[i-1]:
            problem.append(index_array[i])
        else:
            problem_list.append(problem)
            problem = [index_array[i]]
    problem_list.append(problem)
    return problem_list

#%%
# Recersive function that goes through the columns one by one and sorts the array of the ordinals and finds out the subproblems
# based on the next column to recall itself on each problem in subpromlems 
def alpha_rec(arrays, i):
    # if the size of subproblem is 1, means that the related row is already on the right position
    if arrays.shape[0] == 1:
        return arrays
    else:
        # reorder the ordinals based of the order step from the sorting the current column of the problem 
        sorted_array, order = counting_sort(arrays[:,i])
        arrays = arrays[order,:]
        # finding out the subproblems, recalling the recersice function and concatenate the results
        if (i+1) < arrays.shape[1] :
            list_subproblems = subproblem(sorted_array,list(range(arrays.shape[0])))
            list_array = list()
            for problem in list_subproblems:
                list_array.append(alpha_rec(arrays[problem,:], i+1))
            arrays = np.concatenate(list_array, axis = 0)
        return arrays

#%%
# The function convert the list of words to the matrix of ordinals
def word2array(words_list):        
    max_len = max(map(len, words_list))
    words_num = len(words_list)
    arrays = np.zeros((words_num, max_len+1), dtype=int)
    arrays[:,-1] = range(words_num)
    for i,word in enumerate(words_list):
        arrays[i,range(len(word))] = list(map(ord, word.lower()))
    return arrays

#%%    
# The function wraps up all the above function to convert the words list to matrix, calls the recursive sort on the matrix
# exctracs the order and applys to the words list to return the sorted words list 
def alpha_counting_sort(words_list):
    arrays = word2array(words_list)
    sorted_array = alpha_rec(arrays, 0)
    order = list(map(int, sorted_array[:,-1]))
    return([words_list[i] for i in order])

#%%
# The function generate some random words of different length and size, calls the alpha_counting_sort to plot the running time
import time
chr_vec = np.vectorize(chr)
import matplotlib.pyplot as plt
def plot_time_complexity_alpha_sort():
    # fix n
    n = 50
    time_lists_fixed_n = list()
    # change m from 10 to 10000 with steps of 1000
    for m in range(10,10000,1000):
        time_ = list()
        # repeat timing 10 times and the the average to get robust results
        for i in range(10):
            # generating random ordinals
            ordinals_list = np.random.randint(ord('A'), ord('z')+1, (m,n))
            chr_lists = chr_vec(ordinals_list)
            words_list = list()
            # convert ordinals to words
            for i in range(chr_lists.shape[0]):
                words_list.append("".join(chr_lists[i,:]))
            start_time = time.time()
            sorted_words_list = alpha_counting_sort(words_list)
            end_time = time.time()
            time_.append(end_time - start_time)
        time_lists_fixed_n.append(sum(time_)/10)
    # fix m
    m = 50
    time_lists_fixed_m = list()
    # change n from 10 to 10000 with steps of 1000
    for n in range(10,10000,1000):
        time_ = list()
        # repeat timing 10 times and the the average to get robust results
        for i in range(10):
            # generating random ordinals
            ordinals_list = np.random.randint(ord('A'), ord('z')+1, (m,n))
            chr_lists = chr_vec(ordinals_list)
            words_list = list()
            # convert ordinals to words
            for i in range(chr_lists.shape[0]):
                words_list.append("".join(chr_lists[i,:]))
            start_time = time.time()
            sorted_words_list = alpha_counting_sort(words_list)
            end_time = time.time()
            time_.append(end_time - start_time)
        time_lists_fixed_m.append(sum(time_)/10)
    time_lists_ = list()
    # for m = n 
    # change n from 10 to 1000 with steps of 100
    for m in range(10,1000,100):
        n = m
        time_ = list()
        # repeat timing 10 times and the the average to get robust results
        for i in range(10):
            # generating random ordinals
            ordinals_list = np.random.randint(ord('A'), ord('z')+1, (m,n))
            chr_lists = chr_vec(ordinals_list)
            words_list = list()
            # convert ordinals to words
            for i in range(chr_lists.shape[0]):
                words_list.append("".join(chr_lists[i,:]))
            start_time = time.time()
            sorted_words_list = alpha_counting_sort(words_list)
            end_time = time.time()
            time_.append(end_time - start_time)
        time_lists_.append(sum(time_)/10)
    # PLOT
    fig = plt.figure(figsize=(16,4))
    ax1 = fig.add_subplot(1,3,1)
    plt.plot(range(10,100000,10000),time_lists_fixed_n)
    plt.xlabel('number of words')
    plt.ylabel('Average running time (secs)')
    plt.title('Running time for fixed word lenght')
    ax2 = fig.add_subplot(1,3,2)
    plt.plot(range(10,100000,10000),time_lists_fixed_m)
    plt.xlabel('word lenght')
    plt.ylabel('Average running time (secs)')
    plt.title('Running time for fixed number of words')
    ax3 = fig.add_subplot(1,3,3)
    plt.plot(range(10,1000,100),time_lists_)
    plt.xlabel('word lenght = number of words')
    plt.ylabel('Average running time (secs)')
    plt.title('Running time')

#%%
# Plot time complexity for counting sort for different array size
def plot_time_complexity_count_sort():    
    time_lists = list()
    # change m from 10 to 100000 with steps of 10000
    for m in range(10,100000,10000):
        time_ = list()
        # repeat timing 10 times and the the average to get robust results
        for i in range(10):
            # generate random ordinals
            ordinals = np.random.randint(ord('A'), ord('z')+1, m)
            start_time = time.time()
            sorted_words_list = counting_sort(ordinals)
            end_time = time.time()
            time_.append(end_time - start_time)
        time_lists.append(sum(time_)/10)
    #PLOT
    fig = plt.figure(figsize=(16,4))
    ax1 = fig.add_subplot(1,1,1)
    plt.plot(range(10,100000,10000),time_lists)
    plt.xlabel('word lenght')
    plt.ylabel('Average running time (secs)')
    plt.title('Running time for counting sort')