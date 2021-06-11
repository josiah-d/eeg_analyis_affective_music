# imports
import sys
sys.path.insert(0, '..')

import mne
import pandas as pd

from src import load_subjs, plot_eeg


class Subj:
    """A class to represent a research subject.

    Attributes
    ----------
    subj_id : str
        subject's uuid
    subj_filepath : str
        file path the to subject's data folder

    Methods
    -------
    add_trialpath
        Creates a path to the desired trial
    create_epoch_df
        Builds a pandas dataframe of the data during the interventions
    create_post_epoch_df
        Builds a pandas dataframe of the data immediately following the interventions
    define_epoch
        Established the start of each intervention
    edf_dataframe
        Converts the .edf to a pandas dataframe
    read_channels
        Obtains the channel, e.g. the electrodes, that were used in the experiment from the metadata
    read_edf
        Loads the raw data into memory
    read_eeg_meta
        Obtains the eeg metadata
    read_events
        Loads the interventions data
    read_events_meta
        Obtains the eeg metadata
    """

    def __init__(self, subj_id):
        """This creates a research subject object from a .edf file.

        Parameters
        ----------
        subj_id : str
            subject's uuid
        subj_filepath : str
            file path the to subject's data folder
        """
        self.subj_id = subj_id
        self.subj_filepath = f'data/ds002721-download/{subj_id}'
        
    def add_trialpath(self, trial_id):
        """Creates a path to the desired trial.

        Parameters
        ----------
        trial_id : str
            trial's id

        Returns
        -------
        None
        """
        self.trial_id = trial_id
        self.trial_filepath = f'{self.subj_filepath}/eeg/{self.subj_id}_{self.trial_id}'
        
    def read_edf(self):
        """Loads the raw data into memory.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.data =  mne.io.read_raw_edf(f'../{self.trial_filepath}_eeg.edf', preload=True)
        
    def read_channels(self):
        """Obtains the channel, e.g. the electrodes, that were used in the experiment from the metadata.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.channel_meta = pd.read_csv(f'../{self.trial_filepath}_channels.tsv', delimiter='\t')
    
    def read_eeg_meta(self):
        """Obtains the eeg metadata.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.eeg_meta = pd.read_json(f'../{self.trial_filepath}_eeg.json', typ='series')

    def read_events(self):
        """Loads the interventions data.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.events = pd.read_csv(f'../{self.trial_filepath}_events.tsv', delimiter='\t')
    
    def read_events_meta(self):
        """Obtains the eeg metadata.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.events_meta = pd.read_json(f'../{self.trial_filepath}_events.json').T

    def edf_dataframe(self):
        """Converts the .edf to a pandas dataframe.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        channels = self.data.ch_names
        data = self.data.get_data()
        df = pd.DataFrame(data).T
        df.columns = channels
        self.data_df = df[::10]
    
    def define_epoch(self):
        """Established the start of each intervention.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        df = self.events[self.events['trial_type'] == 788]
        self.epochs = df['onset'].to_numpy() * 1000
    
    def create_epoch_df(self):
        """Builds a pandas dataframe of the data during the interventions.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        df = self.data_df
        epoch_df = pd.DataFrame()
        for epoch in self.epochs:
            temp_df = pd.DataFrame(df.iloc[int(epoch): int(epoch + 2000)])
            epoch_df = pd.concat([epoch_df, temp_df], axis=0)
        self.epochs_df = epoch_df
    
    def create_post_epoch_df(self):
        """Builds a pandas dataframe of the data immediately following the interventions.

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        df = self.data_df
        post_epoch_df = pd.DataFrame()
        for epoch in self.epochs:
            temp_df = pd.DataFrame(df.iloc[int(epoch + 2000): int(epoch + 4000)])
            post_epoch_df = pd.concat([post_epoch_df, temp_df], axis=0)
        self.post_epochs_df = post_epoch_df
