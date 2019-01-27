# Function to draw Matplotlib window
def draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100,
         bloodPressureByDayMean, bloodPressureByDayMax, bloodPressureByDayMin, pressureSystolicMA30,
         dfMedicationStartStop, dfCycle, dfBloodPressure):
    # Open window with a given name
    plt.figure("Blood Pressure Line Plots")
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
    axMALongTrend = plt.subplot2grid((11, 4), (3, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axBloodPressureSystolic = plt.subplot2grid((11, 4), (4, 0), colspan=4, rowspan=2, sharex=axBTempDay)
    axBloodPressureDiastolic = plt.subplot2grid((11, 4), (6, 0), colspan=4, rowspan=2, sharex=axBTempDay)
    axPulse = plt.subplot2grid((11, 4), (8, 0), colspan=4, rowspan=2, sharex=axBTempDay)
    axBloodPressureSystolicMALongTrend = plt.subplot2grid((11, 4), (10, 0), colspan=4, rowspan=1, sharex=axBTempDay)

    # Plot Temperature mean, min and max (per day) line graphs
    axBTempDay.plot(temperatureByDayMean.index, temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
    axBTempDay.plot(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], label='MAX Temperature')
    axBTempDay.plot(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], label='MIN Temperature')

    # Add Moving Average Line plot (for 100 days) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBTemp Line plot
    axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken']) - len(temperatureMA100):], temperatureMA100,
                       label='Temperature Moving Average 100')

    # Plot Systolic Blood Pressure mean, min and max (per day) line graphs
    # There will be a gap in case data is missing for particular date
    axBloodPressureSystolic.plot(bloodPressureByDayMean.index, bloodPressureByDayMean['bloodPressureSystolic'],
                                 label='MEAN Systolic Pressure, mmHg')
    axBloodPressureSystolic.plot(bloodPressureByDayMax.index, bloodPressureByDayMax['bloodPressureSystolic'],
                                 label='MAX Systolic Pressure, mmHg')
    axBloodPressureSystolic.plot(bloodPressureByDayMin.index, bloodPressureByDayMin['bloodPressureSystolic'],
                                 label='MIN Systolic Pressure, mmHg')

    # Plot Diastolic Blood Pressure mean, min and max (per day) line graphs
    # There will be a gap in case data is missing for particular date
    axBloodPressureDiastolic.plot(bloodPressureByDayMean.index, bloodPressureByDayMean['bloodPressureDiastolic'],
                                  label='MEAN Diastolic Pressure, mmHg')
    axBloodPressureDiastolic.plot(bloodPressureByDayMax.index, bloodPressureByDayMax['bloodPressureDiastolic'],
                                  label='MAX Diastolic Pressure, mmHg')
    axBloodPressureDiastolic.plot(bloodPressureByDayMin.index, bloodPressureByDayMin['bloodPressureDiastolic'],
                                  label='MIN Diastolic Pressure, mmHg')

    # Plot Pulse mean, min and max (per day) line graphs
    # There will be a gap in case data is missing for particular date
    axPulse.plot(bloodPressureByDayMean.index, bloodPressureByDayMean['pulseBPM'], label='MEAN Pulse, BPM')
    axPulse.plot(bloodPressureByDayMax.index, bloodPressureByDayMax['pulseBPM'], label='MAX Pulse, BPM')
    axPulse.plot(bloodPressureByDayMin.index, bloodPressureByDayMin['pulseBPM'], label='MIN Pulse, BPM')

    # Add Systolic Pressure Moving Average Line plot (for 30 measurements) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBloodPressureSystolic Line plot
    axBloodPressureSystolicMALongTrend.plot(
        dfBloodPressure['dateTaken'][len(dfBloodPressure['dateTaken']) - len(pressureSystolicMA30):],
        pressureSystolicMA30, label='Systolic Pressure Moving Average 30')

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
    axMALongTrend.grid(True)
    axBloodPressureSystolic.grid(True)
    axBloodPressureDiastolic.grid(True)
    axPulse.grid(True)
    axBloodPressureSystolicMALongTrend.grid(True)

    # Set displayable name for subplot
    # May use multiple lines with \n
    axBTempDay.set_title("Blood Pressure and Pulse")

    # Add legend to subplots
    axBTempDay.legend()
    axMALongTrend.legend()
    axBloodPressureSystolic.legend()
    axBloodPressureDiastolic.legend()
    axPulse.legend()
    axBloodPressureSystolicMALongTrend.legend()

    # Set X axis label to subplot
    axMALongTrend.set_xlabel(
        'Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

    # Set Y axis label to subplot
    axBTempDay.set_ylabel('DAILY Temperature')
    axMALongTrend.set_ylabel('MA-100')
    axBloodPressureSystolic.set_ylabel('Systolic')
    axBloodPressureDiastolic.set_ylabel('Diastolic')
    axPulse.set_ylabel('Pulse')
    axBloodPressureSystolicMALongTrend.set_ylabel('MA-30')

    # Rotate X axis labels for subplot
    plt.setp(axMALongTrend.get_xticklabels(), rotation=45)

    # Add vertical lines to subplot

    # Iterate through Menstrual Cycle dataframe entries
    for row in dfCycle.itertuples():
        # Menstrual cycle start datetime
        cycleStartDatetime = row.value
        # Add vertical line to subplot
        axBTempDay.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha=0.4)
        # Add inscriptions to our vertical lines
        # First argument equals to X value of respective line
        # Second argument sets Y value of our inscription
        # Third argument sets text of inscription
        # rotation=90 will make inscription vertical
        # alpha=0.4 will make inscription semitransparent
        axBTempDay.text(cycleStartDatetime, 37.8, "Cycle start", rotation=90, verticalalignment='center', color="r",
                        alpha=0.4)

    # Iterate through Medicament intake dataframe entries
    for row in dfMedicationStartStop.itertuples():
        # Medicament intake datetime
        medicationDatetime = row.value
        # Add vertical line to subplot
        axBTempDay.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axBloodPressureSystolic.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axBloodPressureDiastolic.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axPulse.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axBloodPressureSystolicMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
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
    for ax in [axBTempDay, axMALongTrend, axBloodPressureSystolic, axBloodPressureDiastolic, axPulse]:
        # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
        plt.setp(ax.get_xticklabels(), visible=False)