# imports
import sys
sys.path.insert(0, '..')

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

from src import load_eeg, load_subjs

# set plot style
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
    """Plots a red bar over the intervention.

    Parameters
    ----------
    ax : matplotlib.axes._subplots.AxesSubplot
        subplot to be plotted on
    start : int
        x value to begin the bar
    stop : int
        x value to end the bar
    label : str
        text label for the legend

    Returns
    -------
    epoch plot : method
        a red, translucent bar spanning the entire y axis and between the start, stop values on the x axis
        """
    return ax.axvspan(start, stop, facecolor='#990000', alpha=0.1, label=label)


def all_leads(subj, epochs=[]):
    """Stacked line plot of all electrodes.

    Parameters
    ----------
    subj : load_eeg.Subj
        class instance of the load_eeg.Subj with all attributes added
    epochs : list
        array of the start of each intervention

    Returns
    -------
    None
    """

    fig, ax = plt.subplots(19, sharex='all', figsize=(16, 9))
    fig.suptitle(f'EEG Data\nSubject: {subj.subj_id}\nTrial: {subj.trial_id}')
    
    for i, col in enumerate(subj.data_df.columns):
        for j, epoch in enumerate(epochs):
            if j == 0 and i == 0:
                plot_epoch(ax[i], epoch, epoch+20000, label='music')
            else:
                plot_epoch(ax[i], epoch, epoch+20000)

        ax[i].plot(subj.data_df[col], linewidth=0.3)
        ax[i].set_ylabel(col)
        ax[i].set_yticks([])
    
    ax[-1].set_xlabel('Time (ms)')

    if len(epochs) > 0:
        fig.legend(loc='center right')
    plt.savefig(f'../img/all_leads_{subj.subj_id}_{subj.trial_id}.jpg')


def plot_corrs(subj_id):
    """Correlation heatmap of an individual.

    Parameters
    ----------
    subj_id : str
        subject's uuid

    Returns
    -------
    None
    """
    trials = ['task-run1', 'task-run2', 'task-run3', 'task-run4', 'task-run5', 'task-run6']
    control_df = pd.DataFrame()
    epochs_df = pd.DataFrame()
    post_epochs_df = pd.DataFrame()
    
    for i, trial in enumerate(trials):
        try:
            subj_trial = load_subjs.load_all_subjs_epochs(subj_id, trial)
            if i == 0 or i == 5:
                if control_df.shape == (0, 0):
                    control_df = subj_trial.data_df
                else:
                    control_df = pd.concat([control_df, subj_trial.data_df], axis=0)
            else:
                if epochs_df.shape == (0, 0):
                    epochs_df = subj_trial.epochs_df
                else:
                    epochs_df = pd.concat([epochs_df, subj_trial.epochs_df], axis=0)
                if post_epochs_df.shape == (0, 0):
                    post_epochs_df = subj_trial.post_epochs_df
                else:
                    post_epochs_df = pd.concat([post_epochs_df, subj_trial.post_epochs_df], axis=0)
        except FileNotFoundError:
            pass
    
    fig, ax = plt.subplots(3, figsize=(5,15))

    sn.heatmap(control_df.corr(), center=0, annot=False, ax=ax[0], vmin=-1, vmax=1)
    ax[0].set_title('Without Music')
    sn.heatmap(epochs_df.corr(), center=0, annot=False, ax=ax[1], vmin=-1, vmax=1)
    ax[1].set_title('During Music (20s)')
    sn.heatmap(post_epochs_df.corr(), center=0, annot=False, ax=ax[2], vmin=-1, vmax=1)
    ax[2].set_title('Immediately Following Music (20s)')
    
    fig.suptitle(f'Correlation of EEG Data\nSubject: {subj_id}\nTrial: All')
    plt.savefig(f'../img/correlations_{subj_id}.jpg')


def plot_corrs_all(subjs):
    """Correlation heatmap of all subjects.

    Parameters
    ----------
    subjs : list
        all of the subjects' uuids to be combined

    Returns
    -------
    None
    """
    control_df, epochs_df, post_epochs_df = load_subjs.combine_subj_data(subjs)
    
    fig, ax = plt.subplots(3, figsize=(5,15))

    sn.heatmap(control_df.corr(), center=0, annot=False, ax=ax[0], vmin=-1, vmax=1)
    ax[0].set_title('Without Music')
    sn.heatmap(epochs_df.corr(), center=0, annot=False, ax=ax[1], vmin=-1, vmax=1)
    ax[1].set_title('During Music (20s)')
    sn.heatmap(post_epochs_df.corr(), center=0, annot=False, ax=ax[2], vmin=-1, vmax=1)
    ax[2].set_title('Immediately Following Music (20s)')
    
    fig.suptitle(f'Correlation of EEG Data\nSubject: All\nTrial: All')
    plt.savefig('../img/correlations_all.jpg')


def eeg_hist(ax, data, x_min, x_max, y_lab, title, label=None, line_label=None):
    """Histogram of an electrode voltages.

    Parameters
    ----------
    ax : matplotlib.axes._subplots.AxesSubplot
        subplot to be plotted on
    data : array
        Must be array-like object, e.g. list, numpy.array, pandas.Series
    x_min : float
        set minimum value for the plot's x axis
    x_max : float
        set maximum value for the plot's x axis
    y_lab : str
        text label for the legend
    title : str
        title of the subplot
    label : str
        text label for the legend
    line_label : str
        text label for the legend

    Returns
    -------
    None
    """
    ax.hist(data, bins=500, stacked=True, label=label)
    ax.axvline(data.mean(), ymin=0, ymax=1, color='black', label=line_label)
    ax.set_xlim(x_min, x_max)
    ax.set_ylabel(y_lab)
    ax.ticklabel_format(useOffset=False, style='plain')
    ax.set_title(title)
