# Function to draw Matplotlib window
def draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100,
         bloodPressureByDayMean, bloodPressureByDayMax, bloodPressureByDayMin,
         pressureSystolicMA30, pressureSystolicMA13d, pressureDiastolicMA30, pressureDiastolicMA13d, pulseMA30, pulseMA13d,
         dfMedication, dfCycle, dfBloodPressure):
    # Open window with a given name
    plt.figure("Blood Pressure Line Plots - Part 2")
    # Create subplots and put them to appropriate places of the program-opened window
    # Arguments in first parentheses are setting grid for sublots; first one - for vertical dimension, second - for horizontal one.
    # Arguments in a second parentheses are setting subplot location within this aformentioned grid.
    # Arguments in a second parentheses can't be greater than (or equal to) those in first parentheses.
    # Otherwise you'll get an error: IndexError: invalid index
    # "colspan" argument sets horizontal length of a subplot.
    # "rowspan" argument sets vertical height of a subplot.
    # "sharex" argument sets subplot current subplot has to share X axis with.
    # In this case, when you'll zoom into one plot, another will be zoomed accordingly.
    axBTempDay = plt.subplot2grid((11, 4), (0, 0), colspan=4, rowspan=3)
    axBloodPressure = plt.subplot2grid((11, 4), (3, 0), colspan=4, rowspan=2, sharex=axBTempDay)
    axBloodPressureSystolicMALongTrend = plt.subplot2grid((11, 4), (5, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axBloodPressureSystolicMALongTrendPeriod = plt.subplot2grid((11, 4), (6, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axBloodPressureDiastolicMALongTrend = plt.subplot2grid((11, 4), (7, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axBloodPressureDiastolicMALongTrendPeriod = plt.subplot2grid((11, 4), (8, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axPulseMALongTrend = plt.subplot2grid((11, 4), (9, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axPulseMALongTrendPeriod = plt.subplot2grid((11, 4), (10, 0), colspan=4, rowspan=1, sharex=axBTempDay)

    # Plot Temperature mean, min and max (per day) line graphs
    axBTempDay.plot(temperatureByDayMean.index, temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
    axBTempDay.plot(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], label='MAX Temperature')
    axBTempDay.plot(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], label='MIN Temperature')

    # Plot Systolic and Diastolic Blood Pressure, as well as pulse
    # There will be a gap in case data is missing for particular date
    axBloodPressure.plot(bloodPressureByDayMean.index, bloodPressureByDayMean['bloodPressureSystolic'],
                                 label='MEAN Systolic Pressure, mmHg')
    axBloodPressure.plot(bloodPressureByDayMax.index, bloodPressureByDayMean['bloodPressureDiastolic'],
                                 label='MEAN Diastolic Pressure, mmHg')
    axBloodPressure.plot(bloodPressureByDayMin.index, bloodPressureByDayMean['pulseBPM'],
                                 label='MEAN Pulse, bpm')

    # Add Systolic Pressure Moving Average Line plot (for 30 measurements) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBloodPressureSystolic Line plot
    axBloodPressureSystolicMALongTrend.plot(
        dfBloodPressure['dateTaken'][len(dfBloodPressure['dateTaken']) - len(pressureSystolicMA30):],
        pressureSystolicMA30, label='Systolic Pressure Moving Average 30')

    # Add Systolic Pressure Moving Average Line plot (for 13 days) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBloodPressureSystolic Line plot
    axBloodPressureSystolicMALongTrendPeriod.plot(
        dfBloodPressure['dateTaken'][len(dfBloodPressure['dateTaken']) - len(pressureSystolicMA13d):],
        pressureSystolicMA13d, label='Systolic Pressure Moving Average 13 days')

    # Add Diastolic Pressure Moving Average Line plot (for 30 measurements) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBloodPressureDiastolic Line plot
    axBloodPressureDiastolicMALongTrend.plot(
        dfBloodPressure['dateTaken'][len(dfBloodPressure['dateTaken']) - len(pressureDiastolicMA30):],
        pressureDiastolicMA30, label='Diastolic Pressure Moving Average 30')

    # Add Diastolic Pressure Moving Average Line plot (for 13 days) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBloodPressureDiastolic Line plot
    axBloodPressureDiastolicMALongTrendPeriod.plot(
        dfBloodPressure['dateTaken'][len(dfBloodPressure['dateTaken']) - len(pressureDiastolicMA13d):],
        pressureDiastolicMA13d, label='Diastolic Pressure Moving Average 13 days')

    # Add Pulse Moving Average Line plot (for 30 measurements) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axPulse Line plot
    axPulseMALongTrend.plot(
        dfBloodPressure['dateTaken'][len(dfBloodPressure['dateTaken']) - len(pulseMA30):],
        pulseMA30, label='Pulse Moving Average 30')

    # Add Pulse Moving Average Line plot (for 13 days) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axPulse Line plot
    axPulseMALongTrendPeriod.plot(
        dfBloodPressure['dateTaken'][len(dfBloodPressure['dateTaken']) - len(pulseMA13d):],
        pulseMA13d, label='Pulse Moving Average 13 days')



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
    axBTempDay.grid(True)
    axBloodPressure.grid(True)
    axBloodPressureSystolicMALongTrend.grid(True)
    axBloodPressureSystolicMALongTrendPeriod.grid(True)
    axBloodPressureDiastolicMALongTrend.grid(True)
    axBloodPressureDiastolicMALongTrendPeriod.grid(True)
    axPulseMALongTrend.grid(True)
    axPulseMALongTrendPeriod.grid(True)

    # Set displayable name for subplot
    # May use multiple lines with \n
    axBTempDay.set_title("Blood Pressure and Pulse - Part 2")

    # Add legend to subplots
    axBTempDay.legend()
    axBloodPressure.legend()
    axBloodPressureSystolicMALongTrend.legend()
    axBloodPressureSystolicMALongTrendPeriod.legend()
    axBloodPressureDiastolicMALongTrend.legend()
    axBloodPressureDiastolicMALongTrendPeriod.legend()
    axPulseMALongTrend.legend()
    axPulseMALongTrendPeriod.legend()

    # Set Y axis label to subplot
    axBTempDay.set_ylabel('DAILY Temperature')
    axBloodPressure.set_ylabel('DAILY Pressure, Pulse')
    axBloodPressureSystolicMALongTrend.set_ylabel('Systolic')
    axBloodPressureDiastolicMALongTrend.set_ylabel('Diastolic')
    axPulseMALongTrend.set_ylabel('Pulse')

    # Add vertical lines to subplot

    # Iterate through Menstrual Cycle dataframe entries
    for row in dfCycle.itertuples():
        # Menstrual cycle start datetime
        cycleStartDatetime = row.value
        # Add vertical line to subplot
        axBTempDay.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.4)
        axBloodPressure.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.1)
        axBloodPressureSystolicMALongTrend.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.1)
        axBloodPressureSystolicMALongTrendPeriod.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.1)
        axBloodPressureDiastolicMALongTrend.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.1)
        axBloodPressureDiastolicMALongTrendPeriod.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.1)
        axPulseMALongTrend.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.1)
        axPulseMALongTrendPeriod.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.1)
        # Add inscriptions to our vertical lines
        # First argument equals to X value of respective line
        # Second argument sets Y value of our inscription
        # Third argument sets text of inscription
        # rotation=90 will make inscription vertical
        # alpha=0.4 will make inscription semitransparent
        axBTempDay.text(cycleStartDatetime, 37.8, "Cycle start", rotation=90, verticalalignment='center', color="r",
                        alpha=0.4)

    # Iterate through Medicament intake dataframe entries
    for row in dfMedication.itertuples():
        # Medicament intake datetime
        medicationDatetime = row.value
        # Add vertical line to subplot
        axBTempDay.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axBloodPressure.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axBloodPressureSystolicMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axBloodPressureSystolicMALongTrendPeriod.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axBloodPressureDiastolicMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axBloodPressureDiastolicMALongTrendPeriod.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axPulseMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axPulseMALongTrendPeriod.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        # Add inscriptions to our vertical lines
        # First argument equals to X value of respective line
        # Second argument sets Y value of our inscription
        # Third argument sets text of inscription
        # rotation=90 will make inscription vertical
        # alpha=0.4 will make inscription semitransparent
        axBTempDay.text(medicationDatetime, 37.3, row.text, fontsize='smaller', rotation=90, verticalalignment='center',
                        color="black", alpha=0.4)

    # Remove free space between subplots
    plt.subplots_adjust(hspace=0)

    # Modify axes Tick Labels for all subplots, except one at the bottom
    for ax in [axBTempDay, axBloodPressure, axBloodPressureSystolicMALongTrend, axBloodPressureSystolicMALongTrendPeriod, axBloodPressureDiastolicMALongTrend, axBloodPressureDiastolicMALongTrendPeriod, axPulseMALongTrend]:
        # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
        plt.setp(ax.get_xticklabels(), visible=False)