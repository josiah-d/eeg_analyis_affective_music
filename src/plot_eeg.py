import matplotlib.pyplot as plt

plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12

def plot_epoch(ax, start, stop, label='_nolegend_'):
    return ax.axvspan(start, stop, facecolor='#990000', alpha=0.1, label=label)

def all_leads(subj):
    fig, ax = plt.subplots(19, sharex='all', figsize=(16, 9))
    fig.suptitle(f'EEG Data\nSubject: {subj.subj_id}\nTrial: {subj.trial_id}')
    
    for i, col in enumerate(subj.data_df.columns):
        if i == 0:
            plot_epoch(ax[i], 75000, 80000, label='music')
        else:
            plot_epoch(ax[i], 75000, 80000)
        plot_epoch(ax[i], 175000, 200000)

        ax[i].plot(subj.data_df[col], linewidth=0.3)
        ax[i].set_ylabel(col)
        ax[i].set_yticks([])
    
    ax[-1].set_xlabel('Time (ms)')

    fig.legend(loc='center right')
    plt.savefig('../img/delme.jpg')
