# Function to draw Matplotlib window
def draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100, dfMedication, dfCycle, dfBlood):
    # Open window with a given name
    plt.figure("Erythrocytes-related Line Plots")
    # Create subplots and put them to appropriate places of the program-opened window
    # Arguments in first parentheses are setting grid for sublots; first one - for vertical dimension, second - for horizontal one.
    # Arguments in a second parentheses are setting subplot location within this aformentioned grid.
    # Arguments in a second parentheses can't be greater than (or equal to) those in first parentheses.
    # Otherwise you'll get an error: IndexError: invalid index
    # "colspan" argument sets horizontal length of a subplot.
    # "rowspan" argument sets vertical height of a subplot.
    # "sharex" argument sets subplot current subplot has to share X axis with.
    # In this case, when you'll zoom into one plot, another will be zoomed accordingly.
    axBTempDay = plt.subplot2grid((12, 4), (0, 0), colspan=4, rowspan=3)
    axMALongTrend = plt.subplot2grid((12, 4), (3, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axErythrocytes = plt.subplot2grid((12, 4), (4, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axHemoglobin = plt.subplot2grid((12, 4), (5, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axHematocrit = plt.subplot2grid((12, 4), (6, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axMCV = plt.subplot2grid((12, 4), (7, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axMCH = plt.subplot2grid((12, 4), (8, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axMCHC = plt.subplot2grid((12, 4), (9, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axRDW = plt.subplot2grid((12, 4), (10, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axESR = plt.subplot2grid((12, 4), (11, 0), colspan=4, rowspan=1, sharex=axBTempDay)

    # Plot Temperature mean, min and max (per day) line graphs
    axBTempDay.plot(temperatureByDayMean.index, temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
    axBTempDay.plot(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], label='MAX Temperature')
    axBTempDay.plot(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], label='MIN Temperature')

    # Add Moving Average Line plot (for 100 days) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBTemp Line plot
    axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken']) - len(temperatureMA100):], temperatureMA100,
                       label='Temperature Moving Average 100')

    # There will be a gap in case data is missing for particular date
    axHemoglobin.plot(dfBlood.index, dfBlood['bt-hemoglobin-Hb'], label='Hemoglobin-Hb, g/L')
    axErythrocytes.plot(dfBlood.index, dfBlood['bt-erythrocytes-RBC'], label='Erythrocytes-RBC, 10^12/L')
    axHematocrit.plot(dfBlood.index, dfBlood['bt-hematocrit-Hct'], label='Hematocrit-Hct, %')
    axMCV.plot(dfBlood.index, dfBlood['bt-meanErythrocyteVolume-MCV'], label='Mean Erythrocyte Volume-MCV, fL')
    axMCH.plot(dfBlood.index, dfBlood['bt-meanCellHemoglobin-MCH'], label='Mean Cell Hemoglobin-MCH, pg')
    axMCHC.plot(dfBlood.index, dfBlood['bt-meanCellHemoglobinConcentration-MCHC'],
                label='Mean Cell Hemoglobin Concentration-MCHC, g/dL')
    axRDW.plot(dfBlood.index, dfBlood['bt-redCellDistributionWidth-RDW'], label='Red Cell Distribution Width-RDW, %')
    axESR.plot(dfBlood.index, dfBlood['bt-erythrocyteSedimentationRate-ESR'],
               label='Erythrocyte Sedimentation Rate-ESR, mm/hr')

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

    # axHemoglobin subplot
    # Fill space under virtual line @ Y axis  = 110 up to line graph
    axHemoglobin.fill_between(dfBlood.index, dfBlood['bt-hemoglobin-Hb'], 110,
                              where=(110 > dfBlood['bt-hemoglobin-Hb']), alpha=0.2, color='red', interpolate=True)
    # Fill space above virtual line @ Y axis  = 140 up to line graph
    axHemoglobin.fill_between(dfBlood.index, dfBlood['bt-hemoglobin-Hb'], 140,
                              where=(140 < dfBlood['bt-hemoglobin-Hb']), alpha=0.2, color='red', interpolate=True)

    # axErythrocytes subplot
    # Fill space under virtual line @ Y axis  = 4.1 up to line graph
    axErythrocytes.fill_between(dfBlood.index, dfBlood['bt-erythrocytes-RBC'], 4.1,
                                where=(4.1 > dfBlood['bt-erythrocytes-RBC']), alpha=0.2, color='red', interpolate=True)
    # Fill space above virtual line @ Y axis  = 5.1 up to line graph
    axErythrocytes.fill_between(dfBlood.index, dfBlood['bt-erythrocytes-RBC'], 5.1,
                                where=(5.1 < dfBlood['bt-erythrocytes-RBC']), alpha=0.2, color='red', interpolate=True)

    # axHematocrit subplot
    # Fill space under virtual line @ Y axis  = 35 up to line graph
    axHematocrit.fill_between(dfBlood.index, dfBlood['bt-hematocrit-Hct'], 35,
                              where=(35 > dfBlood['bt-hematocrit-Hct']), alpha=0.2, color='red', interpolate=True)
    # Fill space above virtual line @ Y axis  = 47 up to line graph
    axHematocrit.fill_between(dfBlood.index, dfBlood['bt-hematocrit-Hct'], 47,
                              where=(47 < dfBlood['bt-hematocrit-Hct']), alpha=0.2, color='red', interpolate=True)

    # axMCV subplot
    # Fill space under virtual line @ Y axis  = 75 up to line graph
    axMCV.fill_between(dfBlood.index, dfBlood['bt-meanErythrocyteVolume-MCV'], 75,
                       where=(75 > dfBlood['bt-meanErythrocyteVolume-MCV']), alpha=0.2, color='red', interpolate=True)
    # Fill space above virtual line @ Y axis  = 95 up to line graph
    axMCV.fill_between(dfBlood.index, dfBlood['bt-meanErythrocyteVolume-MCV'], 95,
                       where=(95 < dfBlood['bt-meanErythrocyteVolume-MCV']), alpha=0.2, color='red', interpolate=True)

    # axMCH subplot
    # Fill space under virtual line @ Y axis  = 26 up to line graph
    axMCH.fill_between(dfBlood.index, dfBlood['bt-meanCellHemoglobin-MCH'], 26,
                       where=(26 > dfBlood['bt-meanCellHemoglobin-MCH']), alpha=0.2, color='red', interpolate=True)
    # Fill space above virtual line @ Y axis  = 34 up to line graph
    axMCH.fill_between(dfBlood.index, dfBlood['bt-meanCellHemoglobin-MCH'], 34,
                       where=(34 < dfBlood['bt-meanCellHemoglobin-MCH']), alpha=0.2, color='red', interpolate=True)

    # axMCHC subplot
    # Fill space under virtual line @ Y axis  = 30 up to line graph
    axMCHC.fill_between(dfBlood.index, dfBlood['bt-meanCellHemoglobinConcentration-MCHC'], 30,
                        where=(30 > dfBlood['bt-meanCellHemoglobinConcentration-MCHC']), alpha=0.2, color='red',
                        interpolate=True)
    # Fill space above virtual line @ Y axis  = 38 up to line graph
    axMCHC.fill_between(dfBlood.index, dfBlood['bt-meanCellHemoglobinConcentration-MCHC'], 38,
                        where=(38 < dfBlood['bt-meanCellHemoglobinConcentration-MCHC']), alpha=0.2, color='red',
                        interpolate=True)

    # axRDW subplot
    # Fill space under virtual line @ Y axis  = 11.5 up to line graph
    axRDW.fill_between(dfBlood.index, dfBlood['bt-redCellDistributionWidth-RDW'], 11.5,
                       where=(11.5 > dfBlood['bt-redCellDistributionWidth-RDW']), alpha=0.2, color='red',
                       interpolate=True)
    # Fill space above virtual line @ Y axis  = 14.5 up to line graph
    axRDW.fill_between(dfBlood.index, dfBlood['bt-redCellDistributionWidth-RDW'], 14.5,
                       where=(14.5 < dfBlood['bt-redCellDistributionWidth-RDW']), alpha=0.2, color='red',
                       interpolate=True)

    # axESR subplot
    # Fill space under virtual line @ Y axis  = 2 up to line graph
    axESR.fill_between(dfBlood.index, dfBlood['bt-erythrocyteSedimentationRate-ESR'], 2,
                       where=(2 > dfBlood['bt-erythrocyteSedimentationRate-ESR']), alpha=0.2, color='red',
                       interpolate=True)
    # Fill space above virtual line @ Y axis  = 15 up to line graph
    axESR.fill_between(dfBlood.index, dfBlood['bt-erythrocyteSedimentationRate-ESR'], 15,
                       where=(15 < dfBlood['bt-erythrocyteSedimentationRate-ESR']), alpha=0.2, color='red',
                       interpolate=True)

    # Subplot properties

    # Add grid to subplots
    axBTempDay.grid(True)
    axMALongTrend.grid(True)
    axHemoglobin.grid(True)
    axErythrocytes.grid(True)
    axHematocrit.grid(True)
    axMCV.grid(True)
    axMCH.grid(True)
    axMCHC.grid(True)
    axRDW.grid(True)
    axESR.grid(True)

    # Set displayable name for subplot
    # May use multiple lines with \n
    axBTempDay.set_title("Blood Test - Erythrocytes")

    # Add legend to subplots
    axBTempDay.legend()
    axMALongTrend.legend()
    axHemoglobin.legend()
    axErythrocytes.legend()
    axHematocrit.legend()
    axMCV.legend()
    axMCH.legend()
    axMCHC.legend()
    axRDW.legend()
    axESR.legend()

    # Set X axis label to subplot
    axMALongTrend.set_xlabel(
        'Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

    # Set Y axis label to subplot
    axBTempDay.set_ylabel('DAILY Temperature')
    axMALongTrend.set_ylabel('MA-100')
    axHemoglobin.set_ylabel('Hb')
    axErythrocytes.set_ylabel('RBC')
    axHematocrit.set_ylabel('Hct')
    axMCV.set_ylabel('MCV')
    axMCH.set_ylabel('MCH')
    axMCHC.set_ylabel('MCHC')
    axRDW.set_ylabel('RDW')
    axESR.set_ylabel('ESR')

    # Rotate X axis labels for subplot
    plt.setp(axMALongTrend.get_xticklabels(), rotation=45)

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
        axBTempDay.text(cycleStartDatetime, 37.8, "Cycle start", rotation=90, verticalalignment='center', color="r",
                        alpha=0.4)

    # Iterate through Medicament intake dataframe entries
    for row in dfMedication.itertuples():
        # Medicament intake datetime
        medicationDatetime = row.value
        # Add vertical line to subplot
        axBTempDay.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axHemoglobin.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axErythrocytes.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axHematocrit.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMCV.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMCH.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMCHC.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axRDW.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axESR.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        # Add inscriptions to our vertical lines
        # First argument equals to X value of respective line
        # Second argument sets Y value of our inscription
        # Third argument sets text of inscription
        # rotation=90 will make inscription vertical
        axBTempDay.text(medicationDatetime, 37.3, row.text, fontsize='smaller', rotation=90, verticalalignment='center',
                        color="black", alpha=0.4)

    # Remove free space between subplots
    plt.subplots_adjust(hspace=0)

    # Modify axes Tick Labels for all subplots, except latest one
    for ax in [axBTempDay, axMALongTrend, axHemoglobin, axErythrocytes, axHematocrit, axMCV, axMCH, axMCHC, axRDW]:
        # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
        plt.setp(ax.get_xticklabels(), visible=False)