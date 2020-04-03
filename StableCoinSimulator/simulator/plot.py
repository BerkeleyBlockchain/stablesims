import numpy as np
import matplotlib.pyplot as plt

def bin_data(data, bin_size):
    valid_length = (data.shape[0] // bin_size) * bin_size
    data = data[:valid_length]
    N = data.shape[0]
    binned = np.zeros(N // bin_size)
    for k in range(0, N, bin_size):
        binned[k // bin_size] = data[k : k + bin_size].mean()
    return binned

def compute_metrics(data, ideal): 
    diff = data - ideal
    l1 = float(np.mean(np.abs(diff)))
    l2 = float(np.mean(np.square(diff)))
    linf = float(np.max(np.abs(diff)))

    print ('L-1 Dev: %.5f' % l1)
    print ('L-2 Dev: %.5f' % l2)
    print ('L-inf Dev: %.5f' % linf)

def plot_prices(market, price_func, bin_size=50, warmup=100, ideal_dev=0.1, title=''): 
    data = np.array(market.prices[price_func])[warmup:]
    binned = bin_data(data, bin_size)
    
    ideal = np.ones(binned.shape)

    compute_metrics(binned, ideal)

    plt.plot(ideal, 'r', label='1 USD')
    plt.plot(ideal - ideal_dev, 'g--', label='Lower Threshold')
    plt.plot(ideal + ideal_dev, 'g--', label='Upper Threshold')
    plt.plot(binned, 'b', label='BAS vs USD')
#     plt.plot(market.prices['MAday'], 'y')
    plt.ylim(1.0 - ideal_dev * 5, 1.0 + ideal_dev * 5)
    plt.title(title)
    plt.ylabel('USD price')
    plt.legend()