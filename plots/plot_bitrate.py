import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

## File name with Data Columns
datafile_str="data/bitrate_results.txt"
datafile_col_x="Payload Size (in bits)"
datafile_col_y1="Bits-Per-Second (bps)"
datafile_col_y3="Bit-Rate (KB/s)"
datafile_col_y2="Bit-Error-Rate (%)"
datafile_col_y4="BER 1->0 (%)"
datafile_col_y5="BER 0->1 (%)"
datafile_col_y6="BER 1-bit (%)"
datafile_col_y7="BER multi-bit (%)"


def save_figure(data, file_name):
    sns.set_context("notebook",rc={"lines.linewidth": 2,"lines.markersize": 9})
    plt.rcParams.update({'font.family': 'serif'})
    plt.rcParams.update({'font.size': 25})

    #--Plot
    sns_plot = sns.lineplot(x=datafile_col_x,y=datafile_col_y3,
                            marker='*',markersize=14,color="blue",label="Bit-Rate (KB/s)",
                            data=data)


    ax1 = sns_plot.axes
    ax2 = sns_plot.axes.twinx()
    sns_plot = sns.lineplot(x=datafile_col_x,y=datafile_col_y2, ax=ax2,
                            marker='^', markersize=10,color="red", label="Bit-Error-Rate (%)",
                            data=data)

    #sns_plot = sns.lineplot(x=datafile_col_x,y=datafile_col_y3,
    #                        ax=ax2, 
    #                        marker='*',color="red",label="bit-rate (KB/s)",
    #                        data=data)
    #
    #--Add semilog plot
    # import pdb;pdb.set_trace()
    sns_plot.set(xscale="log")
    sns_plot.set_xlim(5*10**4,5*10**9)
    #--Set range

    #--Other axis
    ax1.set_ylim([1500, 2700])
    ax1.legend(loc='best',prop={'size': 10.5})

    #sns_plot.axes.set_xlim(10)
    ax2.grid(False)
    ax2.set_ylim(0,50)
    ax2.legend(loc='best',prop={'size': 10.5})


    #--Set ticks location
    #sns_plot.axes.xaxis.set_major_locator(ticker.MultipleLocator(10))

    #--Show Plot
    # plt.show()
    #--Save Figure
    fig = sns_plot.get_figure()
    fig.set_size_inches(6,3.5)
    plt.tight_layout()
    fig.savefig(file_name, bbox_inches="tight")
    plt.close()


#Read Data File using Pandas
data=pd.read_csv(datafile_str,sep="\s+")
data.columns=[datafile_col_x,datafile_col_y1,datafile_col_y2,datafile_col_y4,datafile_col_y5,datafile_col_y6,datafile_col_y7]
data[datafile_col_y3] = data[datafile_col_y1].div(8*1024)

#Make percentages to floats:
data[datafile_col_y2] = data[datafile_col_y2].str.rstrip('%').astype('float') 
data1 = data.groupby(by=[datafile_col_x])[datafile_col_y2, datafile_col_y3].agg('min').reset_index()
data2 = data.groupby(by=[datafile_col_x])[datafile_col_y2, datafile_col_y3].agg('mean').reset_index()

save_figure(data1, 'Image Data/bitrate_min.jpg')
save_figure(data2, 'Image Data/bitrate_avg.jpg')
