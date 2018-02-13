# Author: Oliver Chalkley
# Created: 05/12/2017
# Affiliation: Complexity sciences (BCCS) and the Minimal Genome Group (MGG)

import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
class Visualise():
    """This class takes the path to a pickle of a pandas dataframe from the Whole-Cell model (Karr 2012 et. al.). It automatically loads the pandas dataframe ready for use. The rest of the functions are to analyse/visualise the data."""
    def __init__(self, input_, from_pickle = True):
        if from_pickle == True:
            pickle_file = input_
            self.pickle_file = pickle_file
            self.data_frame = pd.io.pickle.read_pickle(self.pickle_file)
        else:
            self.data_frame = input_

#    @static
    def comparisonOverview(pandas_series):
        """Takes a pandas series (name must be the offical name used by the whole-cell modelling suite) and overlays it onto 200 equivalent WT time series."""
        pass
#@static
    def comparisonStatistics(pandas_series, amount_of_timesteps_to_condense = 1, statistic_for_series = 'mean()'):
        """Takes a pandas series (name must be the official name used by the whole-cell modelling suite) and marks the series point onto box plots representing the equiavlent WT points."""
        pass

    def dataOverview(self, save_name = None, no_of_lines_in_plot = 5, order_of_magnitude_change_limit = 0.5):
        """This prints all the data in the data frame but organises it so that time series that of a similar order of magnitude are on the same plot but also so there's not too many time series on one plot. Basically view all the data in as fewer plots as possible."""
        # the order of magnitude of timeseries can vary greatly and so time series should be grouped with other times of a similar order of magnitude. I found means, maxs or mins to give misleading results and found that STD did a reasonable job.
        # reorder dataframe columns so that those with the largest STD are first and the smallest last
        data_ordered = self.data_frame.reindex_axis(self.data_frame.apply(lambda x: x.std()).sort_values(ascending = False).index, axis=1)

        # make split into managable amounts of figures
        figure_counter = 1
        series_counter = 1
        next_series_counter = series_counter + 2
        stop_flag = False
        while stop_flag == False:
            tmp_difference = abs((math.log10(data_ordered.iloc[:, series_counter].std()) - math.log10(data_ordered.iloc[:, next_series_counter].std())))
            print("tmp_difference = ", tmp_difference)
            if (tmp_difference > order_of_magnitude_change_limit or abs(next_series_counter - series_counter) > no_of_lines_in_plot):
                data_ordered.iloc[:, series_counter:(next_series_counter - 1)].plot() 
                if save_name != None:
                    plt.savefig(save_name + str(figure_counter) + '.pdf')
                    plt.close()
                else:
                    plt.show()
                series_counter = next_series_counter
                next_series_counter += 2
                figure_counter += 1
            else:
                next_series_counter += 1

            if (series_counter == len(data_ordered.columns) -1 or next_series_counter == len(data_ordered.columns) - 1):
                stop_flag = True
