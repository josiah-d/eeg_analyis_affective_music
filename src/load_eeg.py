# imports
import sys
sys.path.insert(0, '..')

import mne
import pandas as pd

from src import load_subjs, plot_eeg


class Subj:
    """
    Loads a subject's EEG data.
    """

    def __init__(self, subj_id):
        self.subj_id = subj_id
        self.subj_filepath = f'data/ds002721-download/{subj_id}'
        self.trial_filepath = None
        self.data = None
        self.data_df = None
        self.channel_meta = None
        self.eeg_meta = None
        self.events = None
        self.events_meta = None
        self.epochs = None
        self.epochs_df = None
        self.post_epochs_df = None
        
    def add_trialpath(self, trial_id):
        self.trial_id = trial_id
        self.trial_filepath = f'{self.subj_filepath}/eeg/{self.subj_id}_{self.trial_id}'
        
    def read_edf(self):
        self.data =  mne.io.read_raw_edf(f'../{self.trial_filepath}_eeg.edf', preload=True)
        
    def read_channels(self):
        self.channel_meta = pd.read_csv(f'../{self.trial_filepath}_channels.tsv', delimiter='\t')
    
    def read_eeg_meta(self):
        self.eeg_meta = pd.read_json(f'../{self.trial_filepath}_eeg.json', typ='series')

    def read_events(self):
        self.events = pd.read_csv(f'../{self.trial_filepath}_events.tsv', delimiter='\t')
    
    def read_events_meta(self):
        self.events_meta = pd.read_json(f'../{self.trial_filepath}_events.json').T

    def edf_dataframe(self):
        channels = self.data.ch_names
        data = self.data.get_data()
        df = pd.DataFrame(data).T
        df.columns = channels
        self.data_df = df
    
    def define_epoch(self):
        df = self.events[self.events['trial_type'] == 788]
        self.epochs = df['onset'].to_numpy() * 1000
    
    def create_epoch_df(self):
        df = self.data_df
        epoch_df = pd.DataFrame()
        for epoch in self.epochs:
            temp_df = pd.DataFrame(df.iloc[int(epoch): int(epoch + 20000)])
            epoch_df = pd.concat([epoch_df, temp_df], axis=0)
        self.epochs_df = epoch_df
    
    def create_post_epoch_df(self):
        df = self.data_df
        post_epoch_df = pd.DataFrame()
        for epoch in self.epochs:
            temp_df = pd.DataFrame(df.iloc[int(epoch + 20000): int(epoch + 40000)])
            post_epoch_df = pd.concat([post_epoch_df, temp_df], axis=0)
        self.post_epochs_df = post_epoch_df
