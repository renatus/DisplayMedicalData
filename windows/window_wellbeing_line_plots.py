# Function to draw Matplotlib window
def draw(np, plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA5, temperatureMA15, temperatureMA100, datetimesNparr, dfMedication, dfCycle, dfWellbeing):
    # Open window with a given name
    plt.figure("Wellbeing Line Plot")
    # Create subplots and put them to appropriate places of the program-opened window
    # Arguments in first parentheses are setting grid for sublots; first one - for vertical dimension, second - for horizontal one.
    # Arguments in a second parentheses are setting subplot location within this aformentioned grid.
    # Arguments in a second parentheses can't be greater than (or equal to) those in first parentheses.
    # Otherwise you'll get an error: IndexError: invalid index
    # "colspan" argument sets horizontal length of a subplot.
    # "rowspan" argument sets vertical height of a subplot.
    # "sharex" argument sets subplot current subplot has to share X axis with.
    # In this case, when you'll zoom into one plot, another will be zoomed accordingly.
    axBTemp = plt.subplot2grid((8, 4), (0, 0), colspan=4, rowspan=2)
    axBTempDay = plt.subplot2grid((8, 4), (2, 0), colspan=4, rowspan=2, sharex=axBTemp)
    axMALongTrend = plt.subplot2grid((8, 4), (4, 0), colspan=4, rowspan=1, sharex=axBTemp)
    axVaginalBleeding = plt.subplot2grid((8, 4), (5, 0), colspan=4, rowspan=1, sharex=axBTemp)
    axWellbeing = plt.subplot2grid((8, 4), (6, 0), colspan=4, rowspan=1, sharex=axBTemp)
    axWellbeingMA = plt.subplot2grid((8, 4), (7, 0), colspan=4, rowspan=1, sharex=axBTemp)

    # Plot Temperature line graph
    axBTemp.plot(dfBTemp['dateTaken'], dfBTemp['bdTemperature'], label='Body Temperature')

    # Plot Temperature mean, min and max (per day) line graphs
    axBTempDay.plot(temperatureByDayMean.index, temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
    axBTempDay.plot(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], label='MAX Temperature')
    axBTempDay.plot(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], label='MIN Temperature')

    # Add Moving Average Line plot (for 100 days) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBTemp Line plot
    axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken']) - len(temperatureMA100):], temperatureMA100,
                       label='Temperature Moving Average 100')

    # Plot Vaginal Bleeding intensity line graph
    axVaginalBleeding.plot(dfWellbeing['dateTimeTaken'], dfWellbeing['vaginalBleeding'], label='Vaginal Bleeding, ml', color='r')

    # Plot Overall Wellbeing and Headache Intensity line graphs
    axWellbeing.plot(dfWellbeing['dateTimeTaken'], dfWellbeing['perceivedWellBeing'], label='Percieved Wellbeing, higher is better')
    axWellbeing.plot(dfWellbeing['dateTimeTaken'], dfWellbeing['headacheIntensity'], label='Headache Intensity, lower is better')

    # Plot Overall Wellbeing and Headache Intensity Moving Average line graphs

    # Get Overall Wellbeing Moving Average for 10 measurements (working with Pandas DataFrames and with Pandas-provided tools)
    perceivedWellBeingMA10 = dfWellbeing['perceivedWellBeing'].rolling(10).mean()
    # Convert Moving Average Lists to Numpy Arrays, since we need them for fillings with WHERE statement
    perceivedWellBeingMA10 = np.asarray(perceivedWellBeingMA10)
    axWellbeingMA.plot(dfWellbeing['dateTimeTaken'], perceivedWellBeingMA10, label='Percieved Wellbeing MA10, higher is better')

    # Get Headache Intensity Moving Average for 10 measurements (working with Pandas DataFrames and with Pandas-provided tools)
    headacheIntensityMA10 = dfWellbeing['headacheIntensity'].rolling(10).mean()
    # Convert Moving Average Lists to Numpy Arrays, since we need them for fillings with WHERE statement
    headacheIntensityMA10 = np.asarray(headacheIntensityMA10)
    axWellbeingMA.plot(dfWellbeing['dateTimeTaken'], headacheIntensityMA10, label='Headache Intensity MA10, lower is better')



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

    # Subplot properties

    # Add grid to subplots
    axBTemp.grid(True)
    axBTempDay.grid(True)
    axMALongTrend.grid(True)
    axVaginalBleeding.grid(True)
    axWellbeing.grid(True)
    axWellbeingMA.grid(True)

    # Set displayable name for subplot
    # May use multiple lines with \n
    axBTemp.set_title("Overall Wellbeing")

    # Add legend to subplots
    axBTemp.legend()
    axBTempDay.legend()
    axMALongTrend.legend()
    axVaginalBleeding.legend()
    axWellbeing.legend()
    axWellbeingMA.legend()

    # Set X axis label to subplot
    axMALongTrend.set_xlabel(
        'Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

    # Set Y axis label to subplot
    axBTemp.set_ylabel('Temperature')
    axBTempDay.set_ylabel('DAILY Temperature')
    axMALongTrend.set_ylabel('MA-100')
    axVaginalBleeding.set_ylabel('Mences')
    axWellbeing.set_ylabel('Wellbeing')
    axWellbeingMA.set_ylabel('Wellbeing MA')

    # Rotate X axis labels for subplot
    plt.setp(axWellbeingMA.get_xticklabels(), rotation=45)

    # Add vertical lines to subplot

    # Iterate through Menstrual Cycle dataframe entries
    for row in dfCycle.itertuples():
        # Menstrual cycle start datetime
        cycleStartDatetime = row.value
        # Add vertical line to subplot
        axBTemp.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.6)
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
    for row in dfMedication.itertuples():
        # Medicament intake datetime
        medicationDatetime = row.value
        # Add vertical line to subplot
        axBTemp.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.6)
        axBTempDay.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        # Add inscriptions to our vertical lines
        # First argument equals to X value of respective line
        # Second argument sets Y value of our inscription
        # Third argument sets text of inscription
        # rotation=90 will make inscription vertical
        # alpha=0.4 will make inscription semitransparent
        axBTemp.text(medicationDatetime, 37.3, row.text, fontsize='smaller', rotation=90, verticalalignment='center', color="black",
                     alpha=0.4)

    # Remove free space between subplots
    plt.subplots_adjust(hspace=0)

    # Modify axes Tick Labels for all subplots, except one at the bottom
    for ax in [axBTemp, axBTempDay, axMALongTrend, axVaginalBleeding, axWellbeing]:
        # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
        plt.setp(ax.get_xticklabels(), visible=False)