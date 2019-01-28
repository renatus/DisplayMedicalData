# Function to draw Matplotlib window
def draw(np, plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100, dfMedicationStartStop, dfCycle, dfTSH, dfTgAb, dfLevothyroxine):
    # Open window with a given name
    plt.figure("Thyroid Line Plot")
    # Create subplots and put them to appropriate places of the program-opened window
    # Arguments in first parentheses are setting grid for sublots; first one - for vertical dimension, second - for horizontal one.
    # Arguments in a second parentheses are setting subplot location within this aformentioned grid.
    # Arguments in a second parentheses can't be greater than (or equal to) those in first parentheses.
    # Otherwise you'll get an error: IndexError: invalid index
    # "colspan" argument sets horizontal length of a subplot.
    # "rowspan" argument sets vertical height of a subplot.
    # "sharex" argument sets subplot current subplot has to share X axis with.
    # In this case, when you'll zoom into one plot, another will be zoomed accordingly.
    axBTempDay = plt.subplot2grid((6, 4), (0, 0), colspan=4, rowspan=2)
    axMALongTrend = plt.subplot2grid((6, 4), (2, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axLevothyroxine = plt.subplot2grid((6, 4), (3, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axTSH = plt.subplot2grid((6, 4), (4, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axTgAb = plt.subplot2grid((6, 4), (5, 0), colspan=4, rowspan=1, sharex=axBTempDay)

    # Plot Temperature mean, min and max (per day) line graphs
    axBTempDay.plot(temperatureByDayMean.index, temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
    axBTempDay.plot(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], label='MAX Temperature')
    axBTempDay.plot(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], label='MIN Temperature')

    # Add Moving Average Line plot (for 100 days) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBTemp Line plot
    axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken']) - len(temperatureMA100):], temperatureMA100,
                       label='Temperature Moving Average 100')

    # # Plot Levothyroxine intake line graph
    axLevothyroxine.plot(dfLevothyroxine['dateTimeTaken'], dfLevothyroxine['value'], label='Levothyroxine intake, mcg')

    # Plot TSH concentration line graph
    axTSH.plot(dfTSH['dateTimeTaken'], dfTSH['value'], label='TSH, mcIU/mL')

    # Plot TgAb concentration line graphs
    axTgAb.plot(dfTgAb['dateTimeTaken'], dfTgAb['value'], label='TgAb, IU/mL')

    # Fills

    # axBTempDay subplot
    # Fill space under virtual line @ Y axis  = 36.9 for Body Temperature MIN line graph
    # Use dfDataframe.index instead of dfDataframe['dateTimeTaken'] for fillings, otherwise there would be an error
    axBTempDay.fill_between(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], 36.9,
                            where=(36.9 > temperatureByDayMin['bdTemperature']), alpha=0.2, color='green',
                            interpolate=True)
    # Fill space above virtual line @ Y axis  = 37.5 for Body Temperature MAX line graph
    # Use dfDataframe.index instead of dfDataframe['dateTimeTaken'] for fillings, otherwise there would be an error
    axBTempDay.fill_between(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], 37.5,
                            where=(37.5 < temperatureByDayMax['bdTemperature']), alpha=0.2, color='orange',
                            interpolate=True)

    # axTSH subplot
    # Fill space above virtual line @ Y axis  = 0.1 for TSH line graph
    # Use dfDataframe.index instead of dfDataframe['dateTimeTaken'] for fillings, otherwise there would be an error
    axTSH.fill_between(dfTSH.index, dfTSH['value'], 0.1,
                            where=(0.1 < dfTSH['value']), alpha=0.2, color='red',
                            interpolate=True)

    # Subplot properties

    # Add grid to subplots
    axBTempDay.grid(True)
    axMALongTrend.grid(True)
    axLevothyroxine.grid(True)
    axTSH.grid(True)
    axTgAb.grid(True)

    # Set displayable name for subplot
    # May use multiple lines with \n
    axBTempDay.set_title("Thyroid hormones")

    # Add legend to subplots
    axBTempDay.legend()
    axMALongTrend.legend()
    axLevothyroxine.legend()
    axTSH.legend()
    axTgAb.legend()

    # Set X axis label to subplot
    axMALongTrend.set_xlabel(
        'Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

    # Set Y axis label to subplot
    axBTempDay.set_ylabel('DAILY Temperature')
    axMALongTrend.set_ylabel('MA-100')
    axLevothyroxine.set_ylabel('Levothyroxine')
    axTSH.set_ylabel('TSH')
    axTgAb.set_ylabel('TgAb')

    # Rotate X axis labels for subplot
    plt.setp(axTgAb.get_xticklabels(), rotation=45)

    # Add vertical lines to subplot

    # Iterate through Menstrual Cycle dataframe entries
    for row in dfCycle.itertuples():
        # Menstrual cycle start datetime
        cycleStartDatetime = row.value
        # Add vertical line to subplot
        axBTempDay.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.6)
        # Add inscriptions to our vertical lines
        # First argument equals to X value of respective line
        # Second argument sets Y value of our inscription
        # Third argument sets text of inscription
        # rotation=90 will make inscription vertical
        # alpha=0.4 will make inscription semitransparent
        axBTempDay.text(cycleStartDatetime, 37.7, "Cycle start", fontsize='smaller', rotation=90, verticalalignment='center', color="r",
                        alpha=0.4)

    # Iterate through Medicament intake dataframe entries
    for row in dfMedicationStartStop.itertuples():
        # Medicament intake datetime
        medicationDatetime = row.value
        # Add vertical line to subplot
        axBTempDay.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        # Add inscriptions to our vertical lines
        # First argument equals to X value of respective line
        # Second argument sets Y value of our inscription
        # Third argument sets text of inscription
        # rotation=90 will make inscription vertical
        # alpha=0.4 will make inscription semitransparent
        axBTempDay.text(medicationDatetime, 37.3, row.text, fontsize='smaller', rotation=90, verticalalignment='center', color="black",
                     alpha=0.4)

    # Remove free space between subplots
    plt.subplots_adjust(hspace=0)

    # Modify axes Tick Labels for all subplots, except one at the bottom
    for ax in [axBTempDay, axMALongTrend, axLevothyroxine, axTSH]:
        # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
        plt.setp(ax.get_xticklabels(), visible=False)