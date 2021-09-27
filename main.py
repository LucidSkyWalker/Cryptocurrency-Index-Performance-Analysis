# %%
import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, plot
import pandas
import numpy as np

def load_dict(filename):
    return json.load(open(filename))


def gainz_of_TopX_coins(year, TopX=10):
    """Gainz in % of TopX Coins. Each entry of return list is describing the gainz of 
        a coin in the chosen year.

            Args:
                year (int): year for input of coin-data [2016-2022] NOTE: 2022 describes 2021-08 for simplicity.
                TopX (int, optional): What range of Top Tier coins should be returned. Defaults to 10.

            Returns:
                List: Gainz in % for the Top Tier Coins, starting with Rank 1 to Rank X"""    
    coins_year = load_dict(r'coin-data\\{}.json'.format(year))['cryptocurrency']['listingHistorical']['data']
    coins_year_later = load_dict(r'coin-data\\{}.json'.format(year+1))['cryptocurrency']['listingHistorical']['data']
    change_of_coins = []
    for coin in coins_year[:TopX]: #Top10    
        name = coin['name']
        price_coin = coin['quote']['USD']['price']
        price_coin_yl = None
        for data in coins_year_later:
            if data['name'] == name:
                price_coin_yl = data['quote']['USD']['price']
                break
        if price_coin_yl == None:
            return print("No fitting data found for: {}".format(name))    
        change_in_percent = round(((price_coin_yl-price_coin)/price_coin),4)
        change_of_coins.append(change_in_percent)
    return change_of_coins

def specific_coin_gain_of_year(year, coin_name):
    """Gainz of a specific coin within one year.

        Args:
            year (int): available range [2016-2022] NOTE: 2022 describes 2021-08.
            coin_name (string): Name of coin. e.g. 'Bitcoin'.

        Returns:
            [double]: gainz in % of the chosen coin."""    
    coins_year = load_dict(r'coin-data\\{}.json'.format(year))['cryptocurrency']['listingHistorical']['data']
    coins_year_later = load_dict(r'coin-data\\{}.json'.format(year+1))['cryptocurrency']['listingHistorical']['data']
    for coin in coins_year:
        name = coin['name']
        if not name == coin_name:
            continue
        price_coin = coin['quote']['USD']['price']
        for data in coins_year_later:
            if data['name'] == name:
                price_coin_yl = data['quote']['USD']['price']
                change_in_percent = round(((price_coin_yl-price_coin)/price_coin),4)
                return change_in_percent

def coin_mc_distribution(year, TopX=10):
    """Distribution of Market Captialization of TopX ranked coins in a specific year.

        Args:            
            year (int): year for input of coin-data [2016-2022] NOTE: 2022 describes 2021-08 for simplicity.
            TopX (int, optional): What range of Top Tier coins should be returned. Defaults to 10.


        Returns:
            [type]: [description]"""    
    coins_year = load_dict(r'coin-data\\{}.json'.format(year))['cryptocurrency']['listingHistorical']['data']
    mc_distribution_of_coins = []
    for coin in coins_year[:TopX]:
        mc = coin['quote']['USD']['market_cap']
        mc_distribution_of_coins.append(mc)
    sum_of_mcs = sum(mc_distribution_of_coins)
    return [x/sum_of_mcs for x in mc_distribution_of_coins]

def gainz_of_specific_coin(coin_name):
    """Gainz of a specific coin from 2016 until 2021-08.

            Args:
                coin_name (string): Name of coin. eg. 'Bitcoin'.

            Returns:
                list: Gainz (in %) per year of a specific coin."""    
    result_list = []
    for year in range(2016,2022): #Note: 2022 is used for simplicity to describe 2021-08
        result = specific_coin_gain_of_year(year, coin_name)
        result_list.append(result)
    return result_list

def weighted_gainz_of_Top10():
    """Weighting gainz of Top10 with the corresponding market cap at the beginning of the year.

        Returns:
            list: Gainz per year"""    
    result_list = []
    for year in range(2016,2022):
        result = gainz_of_TopX_coins(year)
        mc_dist = coin_mc_distribution(year)
        weighted = sum([a * b for a, b in zip(result, mc_dist)])
        result_list.append(weighted)
    return result_list

def non_weighted_gainz_of_Top10():
    """Equally weighted gainz of coins

            Returns:
                list: Gainz per year"""    
    result_list = []
    for year in range(2016,2022):
        result = gainz_of_TopX_coins(year)
        non_weighted = sum(result)/10
        result_list.append(non_weighted)
    return result_list

def cummulative_if_one_dollar_invested(gainz):
    """Dollars gained per year until 2021-08 if 1 Dollar was invested in 2016.

            Args:
                gainz (list): Gainz in % for the different years [2016-2022].
                NOTE: 2022 describes gaines so far in 2021 (until september). 
                Naming was chosen for simplicity in code generics. 
            Returns:
                List: Value of dollars in each year"""    
    result = []
    value = 1 # 1 Dollar invested
    for i in gainz:
        if i is None:
            result.append(0)
        else:
            value = value + value*i
            result.append(value)  
    return result

def plot_results(btc_list, weighted_list, non_weighted_list, y_scale_log=False, cumm=False):
    x = np.arange(6)
    if not cumm:
        df = pandas.DataFrame({
            'Factor': x,
            'BTC': [round(x, 2)*100 for x in btc_list],
            'Weighted' : [round(x, 2)*100 for x in weighted_list],
            'Non-Weighted': [round(x, 2)*100 for x in non_weighted_list]
        })
    else:
        df = pandas.DataFrame({
            'Factor': x,
            'BTC': [round(x) for x in btc_list],
            'Weighted' : [round(x) for x in weighted_list],
            'Non-Weighted': [round(x) for x in non_weighted_list]
        })
    width = 0.2
    fig, ax = plt.subplots(figsize=(16, 8))
    rect1 = ax.bar(x-width, df["BTC"], width,color='burlywood', label='BTC')
    rect2 = ax.bar(x, df["Weighted"], width, color='green', label='Top 10 (Weighted)')
    rect3 = ax.bar(x+width, df["Non-Weighted"], width, color='black', label='Top 10 (Not Weighted)')
    ax.bar_label(rect1, padding=3)
    ax.bar_label(rect2, padding=3)
    ax.bar_label(rect3, padding=3)
    ax.legend()
    plt.xticks(x, ['2017', '2018', '2019', '2020', '2021', '2021-09'])
    if y_scale_log:
        plt.yscale('log')
    plt.title('Performance Comparison')
    if not cumm:
        plt.ylabel('Gainz in each year [in %]')        
    else:    
        plt.ylabel('Cummulative Gainz [in $] (if one dollar was invested in 2016)')
    fig.tight_layout()
    #plt.show()
    if not cumm:
        plt.savefig('percent.png')
    else:
        plt.savefig('cumm.png')
        
        
# %% Main
if __name__ == "__main__":
    weighted = weighted_gainz_of_Top10()
    non_weighted = non_weighted_gainz_of_Top10()
    btc = gainz_of_specific_coin('Bitcoin')
    cumm_weighted = cummulative_if_one_dollar_invested(weighted)
    cumm_non_weighted = cummulative_if_one_dollar_invested(non_weighted)
    cumm_btc = cummulative_if_one_dollar_invested(btc)
    plot_results(btc, weighted, non_weighted, cumm=False)
    plot_results(cumm_btc,  cumm_weighted, cumm_non_weighted, cumm=True)

