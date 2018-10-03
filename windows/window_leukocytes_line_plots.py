# Function to draw Matplotlib window
def draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100, dfMedication, dfCycle, dfBlood):
    # Open window with a given name
    plt.figure("Leukocytes-related Line Plots")
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
    axWBC = plt.subplot2grid((11, 4), (4, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axNeutrophilicBandForms = plt.subplot2grid((11, 4), (5, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axNeutrophilGranulocytes = plt.subplot2grid((11, 4), (6, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axEosinophilGranulocytes = plt.subplot2grid((11, 4), (7, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axBasophilGranulocytes = plt.subplot2grid((11, 4), (8, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axLymphocytes = plt.subplot2grid((11, 4), (9, 0), colspan=4, rowspan=1, sharex=axBTempDay)
    axMonocytes = plt.subplot2grid((11, 4), (10, 0), colspan=4, rowspan=1, sharex=axBTempDay)

    # Plot Temperature mean, min and max (per day) line graphs
    axBTempDay.plot(temperatureByDayMean.index, temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
    axBTempDay.plot(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], label='MAX Temperature')
    axBTempDay.plot(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], label='MIN Temperature')

    # Add Moving Average Line plot (for 100 days) to subplot - shows long trends
    # Moving Averages are being calculated based on data for axBTemp Line plot
    axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken']) - len(temperatureMA100):], temperatureMA100,
                       label='Temperature Moving Average 100')

    # There will be a gap in case data is missing for particular date
    axWBC.plot(dfBlood.index, dfBlood['bt-whiteBloodCells-WBC'], label='White Blood Cells-WBC, 10^9/L')
    axNeutrophilicBandForms.plot(dfBlood.index, dfBlood['bt-neutrophilicBandForms'], label='Neutrophilic Band Forms, %')
    axNeutrophilGranulocytes.plot(dfBlood.index, dfBlood['bt-neutrophilGranulocytes-PMNs'],
                                  label='Neutrophil Granulocytes-PMNs, %')
    axEosinophilGranulocytes.plot(dfBlood.index, dfBlood['bt-eosinophilGranulocytes'],
                                  label='Eosinophil Granulocytes, %')
    axBasophilGranulocytes.plot(dfBlood.index, dfBlood['bt-basophilGranulocytes'], label='Basophil Granulocytes, %')
    axLymphocytes.plot(dfBlood.index, dfBlood['bt-lymphocytes'], label='Lymphocytes, %')
    axMonocytes.plot(dfBlood.index, dfBlood['bt-monocytes'], label='Monocytes, %')

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

    # axWBC subplot
    # Fill space under virtual line @ Y axis  = 4 up to line graph
    axWBC.fill_between(dfBlood.index, dfBlood['bt-whiteBloodCells-WBC'], 4,
                       where=(4 > dfBlood['bt-whiteBloodCells-WBC']), alpha=0.2, color='red', interpolate=True)
    # Fill space above virtual line @ Y axis  = 9 up to line graph
    axWBC.fill_between(dfBlood.index, dfBlood['bt-whiteBloodCells-WBC'], 9,
                       where=(9 < dfBlood['bt-whiteBloodCells-WBC']), alpha=0.2, color='red', interpolate=True)

    # axNeutrophilicBandForms subplot
    # Fill space under virtual line @ Y axis  = 1 up to line graph
    axNeutrophilicBandForms.fill_between(dfBlood.index, dfBlood['bt-neutrophilicBandForms'], 1,
                                         where=(1 > dfBlood['bt-neutrophilicBandForms']), alpha=0.2, color='red',
                                         interpolate=True)
    # Fill space above virtual line @ Y axis  = 6 up to line graph
    axNeutrophilicBandForms.fill_between(dfBlood.index, dfBlood['bt-neutrophilicBandForms'], 6,
                                         where=(6 < dfBlood['bt-neutrophilicBandForms']), alpha=0.2, color='red',
                                         interpolate=True)

    # axNeutrophilGranulocytes subplot
    # Fill space under virtual line @ Y axis  = 47 up to line graph
    axNeutrophilGranulocytes.fill_between(dfBlood.index, dfBlood['bt-neutrophilGranulocytes-PMNs'], 47,
                                          where=(47 > dfBlood['bt-neutrophilGranulocytes-PMNs']), alpha=0.2,
                                          color='red', interpolate=True)
    # Fill space above virtual line @ Y axis  = 72 up to line graph
    axNeutrophilGranulocytes.fill_between(dfBlood.index, dfBlood['bt-neutrophilGranulocytes-PMNs'], 72,
                                          where=(72 < dfBlood['bt-neutrophilGranulocytes-PMNs']), alpha=0.2,
                                          color='red', interpolate=True)

    # axEosinophilGranulocytes subplot
    # Fill space under virtual line @ Y axis  = 1 up to line graph
    axEosinophilGranulocytes.fill_between(dfBlood.index, dfBlood['bt-eosinophilGranulocytes'], 1,
                                          where=(1 > dfBlood['bt-eosinophilGranulocytes']), alpha=0.2, color='red',
                                          interpolate=True)
    # Fill space above virtual line @ Y axis  = 5 up to line graph
    axEosinophilGranulocytes.fill_between(dfBlood.index, dfBlood['bt-eosinophilGranulocytes'], 5,
                                          where=(5 < dfBlood['bt-eosinophilGranulocytes']), alpha=0.2, color='red',
                                          interpolate=True)

    # axBasophilGranulocytes subplot
    # Fill space under virtual line @ Y axis  = 0 up to line graph
    axBasophilGranulocytes.fill_between(dfBlood.index, dfBlood['bt-basophilGranulocytes'], 0,
                                        where=(0 > dfBlood['bt-basophilGranulocytes']), alpha=0.2, color='red',
                                        interpolate=True)
    # Fill space above virtual line @ Y axis  = 1 up to line graph
    axBasophilGranulocytes.fill_between(dfBlood.index, dfBlood['bt-basophilGranulocytes'], 1,
                                        where=(1 < dfBlood['bt-basophilGranulocytes']), alpha=0.2, color='red',
                                        interpolate=True)

    # axLymphocytes subplot
    # Fill space under virtual line @ Y axis  = 19 up to line graph
    axLymphocytes.fill_between(dfBlood.index, dfBlood['bt-lymphocytes'], 19, where=(19 > dfBlood['bt-lymphocytes']),
                               alpha=0.2, color='red', interpolate=True)
    # Fill space above virtual line @ Y axis  = 37 up to line graph
    axLymphocytes.fill_between(dfBlood.index, dfBlood['bt-lymphocytes'], 37, where=(37 < dfBlood['bt-lymphocytes']),
                               alpha=0.2, color='red', interpolate=True)

    # axMonocytes subplot
    # Fill space under virtual line @ Y axis  = 3 up to line graph
    axMonocytes.fill_between(dfBlood.index, dfBlood['bt-monocytes'], 3, where=(3 > dfBlood['bt-monocytes']), alpha=0.2,
                             color='red', interpolate=True)
    # Fill space above virtual line @ Y axis  = 11 up to line graph
    axMonocytes.fill_between(dfBlood.index, dfBlood['bt-monocytes'], 11, where=(11 < dfBlood['bt-monocytes']),
                             alpha=0.2, color='red', interpolate=True)

    # Subplot properties

    # Add grid to subplots
    axBTempDay.grid(True)
    axMALongTrend.grid(True)
    axWBC.grid(True)
    axNeutrophilicBandForms.grid(True)
    axNeutrophilGranulocytes.grid(True)
    axEosinophilGranulocytes.grid(True)
    axBasophilGranulocytes.grid(True)
    axLymphocytes.grid(True)
    axMonocytes.grid(True)

    # Set displayable name for subplot
    # May use multiple lines with \n
    axBTempDay.set_title("Blood Test - Leukocytes")

    # Add legend to subplots
    axBTempDay.legend()
    axMALongTrend.legend()
    axWBC.legend()
    axNeutrophilicBandForms.legend()
    axNeutrophilGranulocytes.legend()
    axEosinophilGranulocytes.legend()
    axBasophilGranulocytes.legend()
    axLymphocytes.legend()
    axMonocytes.legend()

    # Set X axis label to subplot
    axMALongTrend.set_xlabel(
        'Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

    # Set Y axis label to subplot
    axBTempDay.set_ylabel('DAILY Temperature')
    axMALongTrend.set_ylabel('MA-100')
    axWBC.set_ylabel('WBC')
    # axNeutrophilicBandForms.set_ylabel('')
    # axNeutrophilGranulocytes.set_ylabel('')
    # axEosinophilGranulocytes.set_ylabel('')
    # axBasophilGranulocytes.set_ylabel('')
    # axLymphocytes.set_ylabel('')
    # axMonocytes.set_ylabel('')

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
        axWBC.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axNeutrophilicBandForms.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axNeutrophilGranulocytes.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axEosinophilGranulocytes.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axBasophilGranulocytes.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axLymphocytes.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
        axMonocytes.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
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
    for ax in [axBTempDay, axMALongTrend, axWBC, axNeutrophilicBandForms, axNeutrophilGranulocytes,
               axEosinophilGranulocytes, axBasophilGranulocytes, axLymphocytes]:
        # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
        plt.setp(ax.get_xticklabels(), visible=False)