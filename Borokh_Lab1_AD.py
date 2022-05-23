import pandas as pd
import urllib.request
from datetime import datetime


def region_year_vhi(index, year):
    """
        Function which show a VHI range for the region per year and search for extremes (min and max).
    """
    year = str(year)
    current_data = vhi_data.loc[(vhi_data.Region == index) & (vhi_data.Year == year)]
    min_vhi = current_data['VHI'].min()
    max_vhi = current_data['VHI'].max()
    print(f"Min VHI for {index} region in {year} year:", min_vhi)
    print(f"Max VHI for {index} region in {year} year:", max_vhi)
    return


def region_vhi(index):
    """
        Function which show a number of VHI for all years for the area, identify years with extreme
        droughts that affected more than the specified percentage of the region.
    """
    current_data = vhi_data.loc[vhi_data.Region == index]
    extreme_drought = current_data[(current_data.VHI <= 15) & (current_data.VHI != -1)]
    drought = current_data[(current_data.VHI <= 35) & (current_data.VHI > 15)]
    extreme_drought_years = set(extreme_drought["Year"].tolist())
    drought_years = set(drought["Year"].tolist())
    for year in extreme_drought_years:
        print(f"Extreme draught was in {year}.")
    for year in drought_years:
        print(f"Draught was in {year}.")
    return


def index_replace(data_to_replace):
    """
        Function than replace indexes of regions in data.
    """
    data_to_replace['Region'].replace(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
        [22, 24, 23, 25, 3, 4, 8, 19, 20, 21, 9, 9, 10, 11, 12, 13, 14, 15, 16, 25, 17, 18, 6, 1, 2, 7, 5],
        inplace=True)
    return


if __name__ == '__main__':
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
    dfs = []
    for i in range(1, 28):
        url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1" \
              f"=2000&year2=2022&type=Mean "
        vhi_url = urllib.request.urlopen(url)
        out = open(f'vhi_id_{i}_{datetime.now().date()}.csv', 'wb')
        out.write(vhi_url.read())
        out.close()
        print(f"VHI for {i} region is downloaded...")
        file = f'vhi_id_{i}_{datetime.now().date()}.csv'
        dfs.append(pd.read_csv(file, names=headers, header=1, index_col=False))
    data = pd.concat(dfs, ignore_index=True)
    data = data.drop(data.loc[data['VHI'] == -1].index)
    data = data.replace(to_replace='<tt><pre>', value='', regex=True)
    data = data.replace(to_replace='</pre></tt>', value='', regex=True)
    data = data.dropna()
    vhi_data = data.reset_index(drop=True)
    previous = 0
    region = 1
    for i in range(0, len(vhi_data)-1):
        if (vhi_data.iloc[i, 0] == '2022') and (vhi_data.iloc[i + 1, 0] == '2000'):
            for j in range(previous, i+1):
                vhi_data.loc[j, 'Region'] = region
            previous = i + 1
            region += 1
        elif (vhi_data.iloc[i, 0] == '2022') and i == len(vhi_data)-2:
            j = 0
            for j in range(previous, i):
                vhi_data.loc[j, 'Region'] = region
            vhi_data.loc[j+1, 'Region'] = region
            vhi_data.loc[j+2, 'Region'] = region
    print(vhi_data)
    index_replace(vhi_data)
    region_year_vhi(1, 2020)
    region_vhi(1)
