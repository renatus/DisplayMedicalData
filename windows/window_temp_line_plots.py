# Function to draw Matplotlib window
def draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA5, temperatureMA15, temperatureMA100, datetimesNparr, dfMedicationStartStop, dfCycle):
    # Open window with a given name
    plt.figure("Body Temperature Line Plot")
    # Create subplots and put them to appropriate places of the program-opened window
    # Arguments in first parentheses are setting grid for sublots; first one - for vertical dimension, second - for horizontal one.
    # Arguments in a second parentheses are setting subplot location within this aformentioned grid.
    # Arguments in a second parentheses can't be greater than (or equal to) those in first parentheses.
    # Otherwise you'll get an error: IndexError: invalid index
    # "colspan" argument sets horizontal length of a subplot.
    # "rowspan" argument sets vertical height of a subplot.
    # "sharex" argument sets subplot current subplot has to share X axis with.
    # In this case, when you'll zoom into one plot, another will be zoomed accordingly.
    axBTemp = plt.subplot2grid((6, 4), (0, 0), colspan=4, rowspan=2)
    axBTempDay = plt.subplot2grid((6, 4), (2, 0), colspan=4, rowspan=2, sharex=axBTemp)
    axMAvsMA2 = plt.subplot2grid((6, 4), (4, 0), colspan=4, rowspan=1, sharex=axBTemp)
    axMALongTrend = plt.subplot2grid((6, 4), (5, 0), colspan=4, rowspan=1, sharex=axBTemp)

    # Plot Temperature line graph
    axBTemp.plot(dfBTemp['dateTaken'], dfBTemp['bdTemperature'], label='Body Temperature')

    # Plot Temperature mean, min and max (per day) line graphs
    axBTempDay.plot(temperatureByDayMean.index, temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
    axBTempDay.plot(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], label='MAX Temperature')
    axBTempDay.plot(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], label='MIN Temperature')

    # Add 2 Moving Average Line plots (for 5 and for 15 days) to subplot
    # Moving Averages are being calculated based on data for axBTemp Line plot
    axMAvsMA2.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken']) - len(temperatureMA5):], temperatureMA5,
                   label='Temperature Moving Average 5')
    axMAvsMA2.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken']) - len(temperatureMA15):], temperatureMA15,
                   label='Temperature Moving Average 15')

    # Add Moving Average Line plot (for 100 days) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBTemp Line plot
    axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken']) - len(temperatureMA100):], temperatureMA100,
                       label='Temperature Moving Average 100')

    # Fills

    # axBTempDay subplot
    # Fill space under virtual line @ Y axis  = 36.9 for Body Temperature MIN line graph
    axBTempDay.fill_between(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], 36.9,
                            where=(36.9 > temperatureByDayMin['bdTemperature']), alpha=0.2, color='green',
                            interpolate=True)
    # Fill space above virtual line @ Y axis  = 37.5 for Body Temperature MAX line graph
    axBTempDay.fill_between(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], 37.5,
                            where=(37.5 < temperatureByDayMax['bdTemperature']), alpha=0.2, color='orange',
                            interpolate=True)

    # axMAvsMA2 subplot
    # Red filling means rising body temperature, green filling - lowering body temperature
    # Calculate start moment for our fill
    # We need 15 values for our "longest" Moving Average, so we need to get rid of the first 15 values of our datetime array (indexes 0-14)
    # Constructions like "nparr_x[10 - 1:]" and "nparr_x[-startMoment:]" are examples of Python slice notation. You can get subset of values with it.
    # https://stackoverflow.com/questions/509211/understanding-pythons-slice-notation
    startMoment = len(datetimesNparr[15 - 1:])
    # Fill space between two Moving Average Line plots, WHERE "longer" Moving Average value is greater than "shorter"
    # It means, that we've DOWNWARD trend at our axBTemp Line plot
    # We need "interpolate=True" to get rid of small uncolored spaces near lines crossings
    axMAvsMA2.fill_between(datetimesNparr[-startMoment:], temperatureMA15[-startMoment:], temperatureMA5[-startMoment:],
                           where=(temperatureMA5[-startMoment:] < temperatureMA15[-startMoment:]),
                           facecolor='green', edgecolor='green', alpha=0.5, interpolate=True)
    # Fill space between two Moving Average Line plots, WHERE "longer" Moving Average value is smaller than "shorter"
    # It means, that we've UPWARD trend at our axBTemp Line plot
    axMAvsMA2.fill_between(datetimesNparr[-startMoment:], temperatureMA15[-startMoment:], temperatureMA5[-startMoment:],
                           where=(temperatureMA5[-startMoment:] >= temperatureMA15[-startMoment:]),
                           facecolor='red', edgecolor='red', alpha=0.5, interpolate=True)

    # Subplot properties

    # Add grid to subplots
    axBTemp.grid(True)
    axBTempDay.grid(True)
    axMAvsMA2.grid(True)
    axMALongTrend.grid(True)

    # Set displayable name for subplot
    # May use multiple lines with \n
    axBTemp.set_title("Progesterone-dependent low grade fever, measured in an axillary position")

    # Add legend to subplots
    axBTemp.legend()
    axBTempDay.legend()
    axMALongTrend.legend()

    # Set X axis label to subplot
    axMALongTrend.set_xlabel(
        'Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

    # Set Y axis label to subplot
    axBTemp.set_ylabel('Temperature')
    axBTempDay.set_ylabel('DAILY Temperature')
    axMAvsMA2.set_ylabel('MA-5 vs MA-15')
    axMALongTrend.set_ylabel('MA-100')

    # Rotate X axis labels for subplot
    plt.setp(axMALongTrend.get_xticklabels(), rotation=45)

    # Add vertical lines to subplot

    # Iterate through Menstrual Cycle dataframe entries
    for row in dfCycle.itertuples():
        # Menstrual cycle start datetime
        cycleStartDatetime = row.value
        # Add vertical line to subplot
        axBTemp.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.6)
        axBTempDay.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.6)
        axMAvsMA2.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.6)
        # Add inscriptions to our vertical lines
        # First argument equals to X value of respective line
        # Second argument sets Y value of our inscription
        # Third argument sets text of inscription
        # rotation=90 will make inscription vertical
        # alpha=0.4 will make inscription semitransparent
        axBTempDay.text(cycleStartDatetime, 37.9, "Cycle start", rotation=90, verticalalignment='center', color="r",
                        alpha=0.4)

    # Iterate through Medicament intake dataframe entries
    for row in dfMedicationStartStop.itertuples():
        # Medicament intake datetime
        medicationDatetime = row.value
        # Add vertical line to subplot
        axBTemp.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.6)
        axBTempDay.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMAvsMA2.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        # Add inscriptions to our vertical lines
        # First argument equals to X value of respective line
        # Second argument sets Y value of our inscription
        # Third argument sets text of inscription
        # rotation=90 will make inscription vertical
        # alpha=0.4 will make inscription semitransparent
        axBTemp.text(medicationDatetime, 37.3, row.text, rotation=90, verticalalignment='center', color="black",
                     alpha=0.4)

    # Remove free space between subplots
    plt.subplots_adjust(hspace=0)

    # Modify axes Tick Labels for all subplots, except one at the bottom
    for ax in [axBTemp, axBTempDay, axMAvsMA2]:
        # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
        plt.setp(ax.get_xticklabels(), visible=False)