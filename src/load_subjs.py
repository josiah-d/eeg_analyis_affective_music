# imports
import sys
sys.path.insert(0, '..')

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