import mne
import pandas as pd


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
        self.epochs = self.events[self.events['trial_type'] == 788]