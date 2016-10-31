import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.gridspec as gridspec

OFFENSE_COL_IND = 6
DISTRICT_COL_IND = 11

VEHICLE_OFFENSE_IND = 51
ASSUALT_OFFENSE_IND = 1


def plot_sorted_counts_by_col(col, ax, num_items=0):
    '''Calculates number of entries in the table grouped by column col,
    and plots the values sorted in descending order using bar graph on ax. 
    Maximum number of itemsis defined by the optional argument num_items'''
    count_by_col = df_merged_nonan.groupby(col).size()
    count_by_col_list = list(count_by_col)
    if num_items == 0:
        num_items = len(count_by_col.keys())

    ax.barh(range(num_items),np.sort(count_by_col_list)[-num_items:])
    sorted_labels = [count_by_col.keys()[i] for i in np.argsort(count_by_col_list)] 
    ax.set_yticks([x+0.5 for x in range(num_items)])
    ax.set_yticklabels(sorted_labels[-num_items:])
    return ax


def get_response_time_by_col(col_ind, types_vec):
    '''Returns array with the length of types_vec, where each entry is an array
    of response time for specific value of types_vec. The index in the results matrix 
    containing the types defined in types_vec is col_ind'''
    data_vec = [[] for y in range(len(types_vec))]
    for i in range(len(data_arr)):
        if data_arr[i,col_ind] in types_vec:
            ind = np.where(types_vec == data_arr[i,col_ind])[0][0]
            data_vec[ind].append(data_arr[i,-1])
    
    return data_vec


def scatter_with_least_squares(x, y, ax):
    '''Plots a scatters plot of x vs. y on ax and adds least squares line'''
    ax.scatter(x, y, label='Districts')
    m, b = np.polyfit(x, y, 1)
    X = np.linspace(np.min(x), np.max(x), 20)
    ax.plot(X, X*m + b)
    return ax


# read files
df1 = pd.read_csv(r'Seattle_Police_Department_Police_Report_Incident.csv')
df2 = pd.read_csv(r'Seattle_Police_Department_911_Incident_Response.csv')

# clean data
df1_fixed = df1.drop_duplicates(['General Offense Number']);
df2_fixed = df2.drop_duplicates(['General Offense Number']);

# merge two datasets according to offense ID, remove rows with nan
df_merged = pd.merge(df1_fixed , df2_fixed, on='General Offense Number')
df_merged_nonan = df_merged.dropna(subset=['At Scene Time', 'Date Reported','District/Sector_x', 'Summarized Offense Description'])


# calculate time of report and arrival to scence, and difference between them (response time)
dt_reported_list = []
dt_atscene_list = []
dt_diff = []

mat_len = df_merged_nonan.shape[0];
for i in range(mat_len):
    dt_reported = datetime.strptime(df_merged_nonan['Date Reported'].iloc[i],'%m/%d/%Y %I:%M:%S %p')
    dt_atscene = datetime.strptime(df_merged_nonan['At Scene Time'].iloc[i],'%m/%d/%Y %I:%M:%S %p')
    
    dt_reported_list.append(dt_reported)
    dt_atscene_list.append(dt_atscene)
    dt_diff.append((dt_atscene - dt_reported).total_seconds() / 60)
    
df_merged_nonan.loc[:,'reported_dt'] = pd.Series(dt_reported_list, index=df_merged_nonan.index)
df_merged_nonan.loc[:,'atscene_dt'] = pd.Series(dt_atscene_list, index=df_merged_nonan.index)
df_merged_nonan.loc[:,'reported_atscene_diff'] = pd.Series(dt_diff, index=df_merged_nonan.index)


# numpy representation of data
data_arr = df_merged_nonan.values

offense_types = np.unique(data_arr[:,6])
districts = np.unique([x for x in data_arr[:,11] if x != 'nan' and x != '99'])


##########
# Plot 1 #
##########
# Initial exploration of data - offense count and response time distribution
fig = plt.figure(figsize=(12,8))
gs = gridspec.GridSpec(2, 6)
gs.update( wspace=0.7, hspace=0.45)

# Number of offenses of each type, top 12, sorted
ax1 = plot_sorted_counts_by_col('Summarized Offense Description', plt.subplot(gs[0, :3]), 12)
ax1.set_title('Number of offenses by type (top 12 out of %s)' % len(offense_types))
ax1.set_xlabel('# of visited offenses')
ax1.set_xticks(ax1.get_xticks()[range(0,len(ax1.get_xticks()),2)])

# Number of offenses in each districts, sorted
ax2 = plot_sorted_counts_by_col('District/Sector_x', plt.subplot(gs[0, 3:]),17)
ax2.set_title('Number of offenses by district')
ax2.set_xlabel('# of visited offenses')


# Ploting the response time
# how many are below -300 and above 300
print(np.sum(np.logical_or((data_arr[:,-1] > 300) , (data_arr[:,-1] < -300))) / len(data_arr[:,-1]))
# only ~2% of offenses have response time bigger than 300 minutes or smaller than -300 minutes


# Distribution of response time - all offenses
ax3 = plt.subplot(gs[1, :2])
ax3.hist(df_merged_nonan['reported_atscene_diff'],range(-300,300,10),normed=True)
ax3.set_title('Response time distribution,\nALL OFFENSES, n=%s' % \
              len(df_merged_nonan['reported_atscene_diff']))
ax3.set_xlabel('Response time (min.)')
ax3.set_ylabel('Probability')
ax3.set_ylim([0, 0.045])

offense_data_vec = get_response_time_by_col(OFFENSE_COL_IND, offense_types)
offense_sum_vec = [len(x) for x in offense_data_vec]

# Distribution of response time - vehicle offense example
ax4 = plt.subplot(gs[1, 2:4])
ax4.hist(offense_data_vec[VEHICLE_OFFENSE_IND],range(-300,300,10),normed=True)
ax4.set_title('Response time distribution,\n%s, n=%s' % \
              (offense_types[VEHICLE_OFFENSE_IND],offense_sum_vec[VEHICLE_OFFENSE_IND]))
ax4.set_xlabel('Response time (min.)')
ax4.set_ylim([0, 0.045])

# Distribution of response time - assault example
ax5 = plt.subplot(gs[1, 4:])
ax5.hist(offense_data_vec[ASSUALT_OFFENSE_IND],range(-300,300,10),normed=True)
ax5.set_title('Response time distribution,\n%s, n=%s' % \
              (offense_types[ASSUALT_OFFENSE_IND],offense_sum_vec[ASSUALT_OFFENSE_IND]))
ax5.set_xlabel('Response time (min.)')
ax5.set_ylim([0, 0.045])

fig.savefig('Plot1.png')



##########
# Plot 2 #
##########
# Correlation between number of offenses and response time
max_response_time = 300
min_response_time = 1

# get matrix of response time arrays. 
# vec_arr[i,j] contains response times of offenses of type i occoured in district j
count_mat = np.zeros([len(offense_types), len(districts)])
vec_arr = [[[] for x in range(len(districts))] for y in range(len(offense_types))]

for i in range(len(data_arr)):
    if (data_arr[i,11] == '99') or (data_arr[i,-1] > max_response_time) or (data_arr[i,-1] < min_response_time):
        continue
    indx = np.where(offense_types == data_arr[i,OFFENSE_COL_IND])[0][0]
    indy = np.where(districts == data_arr[i,DISTRICT_COL_IND])[0][0]
    
    count_mat[indx,indy] = count_mat[indx,indy] + 1
    vec_arr[indx][indy].append(data_arr[i,-1])
    
median_arr = [[np.median(y) for y in x] for x in vec_arr]
mean_arr = [[np.mean(y) for y in x] for x in vec_arr]
cnt_arr = [[len(y) for y in x] for x in vec_arr]

# response time in each district (not taking into account type of offense)
district_data_vec = get_response_time_by_col(DISTRICT_COL_IND, districts)
district_data_vec = [[y for y in x if (y>=min_response_time and y<=max_response_time)] for x in district_data_vec]
district_cnt = [len(x) for x in district_data_vec]
district_mean_response_time = [np.mean(x) for x in district_data_vec]


fig = plt.figure(figsize=(10,8))
gs = gridspec.GridSpec(2, 4)
gs.update( wspace=0.4, hspace=0.4)

# Number of offenses in a district vs. the mean response time in a district
ax1 = scatter_with_least_squares(district_cnt,district_mean_response_time,plt.subplot(gs[0, 1:3]))
ax1.set_title("Districts number of offenses vs. mean response time, \n ALL OFFENSES R=%.3f" %  \
              np.corrcoef(district_cnt, district_mean_response_time)[0][1])        
ax1.legend(loc='upper left')
ax1.set_xlabel('Number of offenses')
ax1.set_ylabel('Mean response time')

# Number of offenses in a district of type "vehicle offense" vs. their mean response time in the district
ax2 = scatter_with_least_squares(cnt_arr[VEHICLE_OFFENSE_IND],mean_arr[VEHICLE_OFFENSE_IND],plt.subplot(gs[1, :2]))
ax2.set_title("Districts offense count vs. mean response time,\n%s, R=%.3f" %  \
              (offense_types[VEHICLE_OFFENSE_IND],np.corrcoef(cnt_arr[VEHICLE_OFFENSE_IND], \
                                                              mean_arr[VEHICLE_OFFENSE_IND])[0][1]))        
ax2.set_xlabel('Number of offenses')
ax2.set_ylabel('Mean response time')
ax2.legend(loc='upper left')

# Number of offenses in a district of type "assault" vs. their mean response time in the district
ax3 = scatter_with_least_squares(cnt_arr[ASSUALT_OFFENSE_IND],mean_arr[ASSUALT_OFFENSE_IND],plt.subplot(gs[1, 2:]))
ax3.set_title("Districts offense count vs. mean response time,\n%s, R=%.3f" %  \
              (offense_types[ASSUALT_OFFENSE_IND],np.corrcoef(cnt_arr[ASSUALT_OFFENSE_IND], \ 
                                                              mean_arr[ASSUALT_OFFENSE_IND])[0][1]))        
ax3.set_xlabel('Number of offenses')
ax3.set_ylabel('Mean response time')
ax3.legend(loc='upper right')

fig.savefig('Plot2.png')
