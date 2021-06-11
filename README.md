# EEG Analysis of Affective Music Experiences

Josiah Duhaime

---

## Background

Electroencephalography (EEG) is a non-invasive means of measuring elctrical activity, e.g. excitatory postsynaptic potential and inhibitory postsynaptic potentials, on the scalp which represents the macro electrical activity of the cerebral cortex. More simply, EEGs measure depolarizations and hyperpolarizations across a brain region and between electrodes.

Each electrode used during an EEG has a particular naming convention. Here is a simplified version of the rules:

* Even electrodes are on the right
* Odd electrodes are on the left
* z is used to denote a mid sagittal electrode
* A letter code denotes the region of the brain
    * Pre-frontal: Fp
    * Frontal: F
    * Temporal: T
    * Parietal: P
    * Occipital: O
    * Central: C

There are several standards for collecting EEG data. One such is called the Standard 10-20. This montage can be expanded or restricted by adding or removing electrodes to allow for greater or lesser granularity.

![Standard 10/20 Montage](img/montage.png)

---

## Goals

* Increase competency in exploratory data analysis
* Gain familiarity with EEG data
    * Potential future projects regarding brain computer interfaces

---

## Data

The [data](https://openneuro.org/datasets/ds002721/versions/1.0.0) obtained from the work of Nicoletta Nicolaou (creator), Ian Daly (creator), Slawomir Nasuto (principle investigator) and others which can be obtained through [brainlife](https://brainlife.io/).

There were 31 subjects (18 female, 13 male; mean age of 39.13 ± 14.48; age range 18-66) who were involved in this study to provide EEG data. Each subject conducted six EEGs, less subject 6 who was unable to perform the sixth EEG due to a non-disclosed reason. 

The first and sixth EEGs were used as controls while the second to fifth had interventions. The intervention was an exposure to the a selection of affective music. The music was obtained from the work of [Eerola and Vuoskoski](https://journals.sagepub.com/doi/10.1177/0305735610362821). During trials 2-5, the subject listened to 10, 20 second blocks of affective music and were asked varied questions regarding their emotional reaction to the music. 

* 31 Subjects
* 6 EEGs
* 300 - 600 secs
* Sampling rate: 1000 Hz
* 19 electrodes
* ~1,750,000,000 data points

The data was mainly in a European Data Format (EDF) which is a common file format for the exchange and storage of medical time series data. In addition, there was JavaScript Object Notation (JSON) and Comma-Separated Values (CSV) files that contained metadata and definitions of the codes used in the metadata.

---

## Data Visualization

Initially, each subjects' data was plotted to assess the quality and shape of the sensor data. In Figure 1, the EEG data is plotted for each sensor. Figure 2 is comparable; however, there are red bars overlayed during the epochs where affective music was played for the subject.

![Subj 1, Trial 1](img/all_leads/all_leads_sub-01_task-run1.jpg)

**Figure 1: EEG Data, Subject: sub-01, Trial: task-run1**

![Subj 1, Trial 2](img/all_leads/all_leads_sub-01_task-run2.jpg)

**Figure 2: EEG Data, Subject: sub-01, Trial: task-run2**

There were no significant holes or perturbations noted in the data.

Note: All subject and trial EEG plots are in `img/all_leads`.

The data was then parsed to three bins. The `control` data was all of the EEG data from trials 1 and 6. Similarly, `epochs` is the data from each of the red shaded regions and `post_epochs` is the 20 sec segment immediately following the affective music intervention. The `post_epochs` data was parse to assess for a lingering effect of the affective music. 

Then, correlation heat maps were used to assess the interactions between each of the sensors for each group.

![Subj All, Trial All](img/correlations/correlations_all.jpg)

**Figure 3: Correlation of EEG Data, Subject: All, Trial: All**

The `control` data is labeled `Without Music`. This plot was used as the baseline. The `epochs` data is labeled `During Music (20s)` and shows a marked loss of correlation across sensor `T3` and lesser so across `Cz`. This seemed to persist in the data from `post_epochs` labels `Immediately Following Music (20s)`.

In the aggregated data, there were no negatively correlated regions. However, there were sensors in the individual data that were strongly negatively correlated. For instance, subject 29 had a marked loss of correlation numerous sensors and a gain in correlation in others which seems to be persistent.

![Subj 29, Trial All](img/correlations/correlations_sub-29.jpg)

**Figure 4: Correlation of EEG Data, Subject: 29, Trial: All**

Note: All subject and trial correlation EEG plots are in `img/correlations`.

Lastly, histograms for each category, e.g. `control`, `epochs`, `post_epochs`, were plotted as a stacked histogram with the mean noted. The `control` data has a more central tendency while the `epochs` data is shifted negatively. The `post_epochs` data is still shifted negatively but seems to be beginning to normalize. Additionally, the plots suggest that there is a positive skew.

![EEG Voltage](img/histograms/grouped_eeg_voltages.jpg)

**Figure 5: Histogram of EEG Sensors, Subject: All, Trial: All**

Note: All sensor plots are in `img/histograms`.

---

## Statistics

The null hypothesis, H<sub>0</sub>, states that there is no discernible difference between the `control` and `epochs` data. 

H<sub>0</sub> = `control` == `epochs`

A significance level of 0.01 was used to assess the p-values; however, since 19 hypothesis tests would be computed, a Bonferroni correction was used which established &alpha; as 0.0005. 

A T Test was conducted on all sensors from the `control` data against the `epochs` data. All of the p-values were greatly less than &alpha;=0.0005 with most being zero during to the memory limitations of python. The power of each of these tests was 1.0 and both the absolute effect size and the relative effect size were calculated. 

**Table 1: Hypothesis Testing Results**

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>t</th>
      <th>p</th>
      <th>sig</th>
      <th>power</th>
      <th>abs_effect_size</th>
      <th>relev_effect_size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>FP1</th>
      <td>62.358931</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000013</td>
      <td>-0.440880</td>
    </tr>
    <tr>
      <th>FP2</th>
      <td>132.347907</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000025</td>
      <td>-1.677738</td>
    </tr>
    <tr>
      <th>F7</th>
      <td>62.930092</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000008</td>
      <td>2.582388</td>
    </tr>
    <tr>
      <th>F3</th>
      <td>24.890371</td>
      <td>1.169934e-136</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000002</td>
      <td>-0.060947</td>
    </tr>
    <tr>
      <th>Fz</th>
      <td>-61.355396</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>-0.000005</td>
      <td>0.175469</td>
    </tr>
    <tr>
      <th>F4</th>
      <td>139.590200</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000013</td>
      <td>-0.829454</td>
    </tr>
    <tr>
      <th>F8</th>
      <td>146.449168</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000017</td>
      <td>13.290460</td>
    </tr>
    <tr>
      <th>T3</th>
      <td>-22.446353</td>
      <td>1.776391e-111</td>
      <td>True</td>
      <td>1.0</td>
      <td>-0.000011</td>
      <td>-0.579437</td>
    </tr>
    <tr>
      <th>C3</th>
      <td>51.283345</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000004</td>
      <td>-0.186249</td>
    </tr>
    <tr>
      <th>Cz</th>
      <td>-52.205131</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>-0.000004</td>
      <td>0.200423</td>
    </tr>
    <tr>
      <th>C4</th>
      <td>70.062581</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000005</td>
      <td>-0.959366</td>
    </tr>
    <tr>
      <th>T4</th>
      <td>137.077588</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000013</td>
      <td>-1.724223</td>
    </tr>
    <tr>
      <th>T5</th>
      <td>46.478751</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000005</td>
      <td>-0.523513</td>
    </tr>
    <tr>
      <th>P3</th>
      <td>125.714777</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000010</td>
      <td>-0.767292</td>
    </tr>
    <tr>
      <th>Pz</th>
      <td>38.873714</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000003</td>
      <td>2.703736</td>
    </tr>
    <tr>
      <th>P4</th>
      <td>42.286457</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000004</td>
      <td>-0.271190</td>
    </tr>
    <tr>
      <th>T6</th>
      <td>168.623868</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000014</td>
      <td>1.299559</td>
    </tr>
    <tr>
      <th>O1</th>
      <td>116.846661</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000012</td>
      <td>0.876514</td>
    </tr>
    <tr>
      <th>O2</th>
      <td>48.706708</td>
      <td>0.000000e+00</td>
      <td>True</td>
      <td>1.0</td>
      <td>0.000005</td>
      <td>0.413585</td>
    </tr>
  </tbody>
</table>

![Relative Effect & T Statistics](img/relev_effect_size_t_stat.jpg)

**Figure 5: Relative Effect Size & T Statistics**

The relative effect size is most notable on electrodes `F7`, `F8`, and `Pz`.

---

## Conclusions

The null hypothesis can be rejected indicating that when affective music is played it causes brain wave changes that are detectible by an EEG. 

---

## Next Steps

* Analyze by the type of music
* Analyze by stated response to music
* Separate by sex
* Normalize data
* Explore sentiment analysis & emotional response to music
* EDA of STD, rate of change, skew, cartesian distance

---

## References

1. [Daly, I., Hallowell, J., Hwang, F., Kirke, A., Malik, A., Roesch, E., Weaver, J., Williams, D., Miranda, E., & Nasuto, S. (2014). Changes in music tempo entrain movement related brain activity. *2014 36th Annual International Conference of the IEEE Engineering in Medicine and Biology Society,* 4595-4598. doi: 10.1109/EMBC.2014.6944647](https://ieeexplore.ieee.org/document/6944647)
1. [Daly, I., Malik, A., Hwang, F., Roesch, E., Weaver, J., Kirke, A., Williams, D., Miranda, E., & Nasuto, S. (2014). Neural correlates of emotional responses to music: An EEG study. *Neuroscience Letters, 573*, 52-57. doi: 10.1016/j.neulet.2014.05.003](https://www.sciencedirect.com/science/article/abs/pii/S030439401400367X)
1. [Daly, Ian., Williams, D., Hallowell, J., Hwang, F., Kirke, A., Malike, A., Weaver, J,. Miranda, E., & Nasuto, S. (2015). Music-induced emotions can be predicted from a combination of brain activity and acoustic features. *Brain and Cognition, 101*, 1-11. doi: 10.1016/j.bandc.2015.08.003](https://www.sciencedirect.com/science/article/abs/pii/S0278262615300142)
1. [Daly, I., Nicolaou, N., Williams, D., Hwang, F., Kirke, A., Miranda, E., & Nasuto, S. (2020). Neural and physiological data from participants listening to afective music. *Scientific Data, 7*(177). doi: 10.6084/m9.figshare.12326519](https://www.nature.com/articles/s41597-020-0507-6)
