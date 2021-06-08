# import nme
# import pandas as pd


class LoadSubj:
    """
    Loads a subject's EEG data.
    """

    def __init__(self, subj_id, trial_id=None):
        self.subj_id = subj_id
        self.trial_id = trial_id

        #self.subj_filepath = f'data/ds002721-download/{subj_id}'
        #self.trial_filepath = f'{self.subj_filepath}/eeg/{self.subj_id}_{self.trial_id}_eeg.edf'
    
    def read_edf(self):
        pass


#raw = mne.io.read_raw_edf('data/ds002721-download/sub-01/eeg/sub-01_task-run2_eeg.edf', preload=True)


subj_1 = LoadSubj(subj_id='sub-01', trial_id='task-run2')













subj_id = 1234

print('folder/folder/{}'.format(subj_id))
print(f'folder/folder/{subj_id}')

