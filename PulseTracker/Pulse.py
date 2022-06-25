import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class PulseTracker():
    """
    Pulse tracker will give you the points where the change in slopes are maximum.

    example:
            dt = 0.1
            t = np.arange(0,4,dt)
            f_clean = np.sin(2*np.pi*440*t) + np.sin(2*np.pi*587*t)  # high pitch beep
            f = f_clean + 2*np.random.randn(len(t))

            # Creating an instance of the class
            tracker = PulseTracker(t[:100],f[:100])

            # show the slopes
            tracker.show_slopes()

            # set the threshold
            tracker.set_threshold(value=50)

            """
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.s_x = []
        self.s_y = []
        self.check = False
    def get_slope(self):
        """
        """
        x1_list, x2_list, y1_list, y2_list, slopes = [[] for i in range(5)]
        # the length of both the x and y data must be same.
        for i in range(1,len(self.x)):

            x1 = self.x[i-1]
            x2 = self.x[i]
            y1 = self.y[i-1]
            y2 = self.y[i]
            slope = (y2-y1)/(x2-x1)

            # saves values:
            slopes.append(slope)
            x1_list.append(x1)
            x2_list.append(x2)
            y1_list.append(y1)
            y2_list.append(y2)
        slopes = np.where(np.isnan(np.array(slopes)),0,np.array(slopes))
        return slopes,np.array(x1_list),np.array(x2_list),np.array(y1_list),np.array(y2_list)

    def show_slopes(self):
        """
        shows the slopes along with the Data
        """
        fig, ax = plt.subplots(2,1,figsize=(10,6))
        ax[0].set_title("Data (y v/s x)")
        ax[1].set_title("Slope v/s x")
        ax[0].plot(self.x,self.y, label='Data (y v/s x)')
        ax[1].plot(self.get_slope()[1],self.get_slope()[0],label="Slope v/s x", color='red')
        ax[0].legend()
        ax[1].legend()
        plt.show()

    def get_points(self, approach='both'):
        """
        Returns two lists of the points where slopes change (depending on the threshold)

        approach := 'up' : will calculate upper points for you.
                    'down' : will calculate lower points for you.
                    'both': will calculate upper and lower points for you.
        """
        self.check = True
        try:
            # These lists are to get the edges of the pulses
            selective_x = []
            selective_y = []

            # we can then append the lists and plot these points.
            # NOTE: Try setting the slope_threshold based on the above graph to different values.
            for i in range(1,len(self.get_slope()[0])):

                if approach.lower() == 'both':
                    if (self.get_slope()[0][i]-self.get_slope()[0][i-1])>self.threshold:
                        selective_x.append(self.get_slope()[1][i])
                        selective_y.append(self.get_slope()[3][i])
                    elif (self.get_slope()[0][i]-self.get_slope()[0][i-1])<-self.threshold:
                        selective_x.append(self.get_slope()[1][i])
                        selective_y.append(self.get_slope()[3][i])

                elif approach.lower() == 'up':
                    if (self.get_slope()[0][i]-self.get_slope()[0][i-1])<-self.threshold:
                        selective_x.append(self.get_slope()[1][i])
                        selective_y.append(self.get_slope()[3][i])

                elif approach.lower() == 'down':
                    if (self.get_slope()[0][i]-self.get_slope()[0][i-1])>self.threshold:
                        selective_x.append(self.get_slope()[1][i])
                        selective_y.append(self.get_slope()[3][i])
            # Plot the points(edges):
            self.s_x = selective_x
            self.s_y = selective_y
            return selective_x, selective_y
        except:
            raise(ThresholdValueError)

    def find_interval(self):
        """
        Returns : Average interval between two edge points,
                  All intervals"""
        # Get the final time intervals:
        intervals = []

        for i in range(1,len(self.s_x)):
            diff = self.s_x[i]-self.s_x[i-1]
            intervals.append(diff)

        intervals = np.array(intervals)
        return intervals.mean(), intervals

    def set_threshold(self,value, plot=True):
        """
        Set threshold value for slope."""
        self.threshold = value
        if plot:
            plt.plot(self.get_slope()[1],self.get_slope()[0], label='Data')
            plt.plot(self.get_slope()[1],np.repeat(self.threshold,len(self.get_slope()[1])),'r--',label='Threshold')
            plt.legend()
            plt.show()

    def points(self):
        return s_x,s_y

    def show_points(self,figsize=(7,5)):
        """
        Plot coordinates with slopes > threshold """
        if self.check == False:
            self.s_x, self.s_y = self.get_points()
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(self.x,self.y, label='Data')
        ax.scatter(self.s_x,self.s_y,color='red', label='Coordinates with slopes above threshold')
        ax.legend()
