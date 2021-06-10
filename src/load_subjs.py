# imports
import sys
sys.path.insert(0, '..')

import pandas as pd

from src import load_eeg, plot_eeg


def load_all_subjs_epochs(subj_id, trial_id, plot=False):
    subj_trial = load_eeg.Subj(subj_id)
    subj_trial.add_trialpath(trial_id)
    subj_trial.read_events()
    subj_trial.read_events_meta()
    subj_trial.define_epoch()
    subj_trial.read_edf()
    subj_trial.edf_dataframe()
    subj_trial.create_epoch_df()
    subj_trial.create_post_epoch_df()

    if plot:
        plot_eeg.all_leads(subj_trial, epochs=subj_trial.epochs)

    return subj_trial


def combine_subj_data(subjs, save=False):
    trials = ['task-run1', 'task-run2', 'task-run3', 'task-run4', 'task-run5', 'task-run6']
    
    control_df = pd.DataFrame()
    epochs_df = pd.DataFrame()
    post_epochs_df = pd.DataFrame()
    
    for subj in subjs:
        for i, trial in enumerate(trials):
            try:
                subj_trial = load_all_subjs_epochs(subj, trial)
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

    if save:
        control_df.to_csv('../data/control_all.csv')
        epochs_df.to_csv('../data/epochs_all.csv')
        post_epochs_df.to_csv('../data/post_epochs_all.csv')

    return control_df, epochs_df, post_epochs_df