# Import packages
# Package for data analysis
import pandas as pd
#To fix ImportError: No module named '_tkinter' during matplotlib import use
#sudo apt-get install python3-tk
# For graph plotting
import matplotlib.pyplot as plt
# For plotting functionality like advanced fills with "where" argument
import numpy as np
# We need Seaborn for beautiful corellation matrixes out of the box
import seaborn as sns



# Function to calculate Moving Average
# "values" argument takes List or Numpy Array of values to calculate Moving Average
# "window" argument takes Integer to set number of values to calculate average from
def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma



# Load JSON file and convert it to Pandas DataFrame
# If you've an error in JSON syntax, like trailing comma, you'll see an error:
# ValueError: Unexpected character found when decoding array value (1)
# Body temperature measurements with date and time
dfBTemp = pd.read_json('body_temperature.json')
# Menstrual cycle start dates
dfCycle = pd.read_json('menstrual_cycle_start.json')
# Medicament intake with date and time
dfMedication = pd.read_json('medication_reports.json')
# Blood test results
dfBlood = pd.read_json('blood_test.json')
# Blood pressure results
dfBloodPressure = pd.read_json('blood_pressure.json')

# Rename columns in DataFrame
dfBTemp = dfBTemp.rename({'bd-temperature':'bdTemperature', 'dateTaken':'dateTaken'}, axis='columns')
# Show information about DataFrame
#dfBTemp.info()

# Body temperature Dataframe
# Convert objects to datetime
dfBTemp.dateTaken = pd.to_datetime(dfBTemp.dateTaken)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfBTemp.set_index('dateTaken', drop=False, inplace=True)

# Menstrual cycle Dataframe
# Convert objects to datetime
dfCycle.value = pd.to_datetime(dfCycle.value)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfCycle.set_index('value', drop=False, inplace=True)

# Medicament intake Dataframe
# Convert objects to datetime
dfMedication.value = pd.to_datetime(dfMedication.value)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfMedication.set_index('value', drop=False, inplace=True)

# Blood test results Dataframe
# Convert objects to datetime
dfBlood.dateTaken = pd.to_datetime(dfBlood.dateTaken)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfBlood.set_index('dateTaken', drop=False, inplace=True)

# Blood Pressure results Dataframe
# Rename columns in DataFrame
dfBloodPressure = dfBloodPressure.rename({'dateTimeTaken':'dateTaken', 'bt-blood_pressure_max':'bloodPressureSystolic', 'bt-blood_pressure_min':'bloodPressureDiastolic', 'bt-pulse_BPM':'pulseBPM'}, axis='columns')
# Convert objects to datetime
dfBloodPressure.dateTaken = pd.to_datetime(dfBloodPressure.dateTaken)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfBloodPressure.set_index('dateTaken', drop=False, inplace=True)

# Count number of measurements with given temperature value (like 37.1 - 120, 37.2 - 93)
#https://stackoverflow.com/questions/10373660/converting-a-pandas-groupby-object-to-dataframe
temperatureValuesOccurrenceDf = dfBTemp.groupby(['bdTemperature']).count()
# Array of floats like 37.2
temperatureValues = np.asarray(temperatureValuesOccurrenceDf.index)
# Array of integers like 93
temperatureValuesOccurrence = np.asarray(temperatureValuesOccurrenceDf.dateTaken)

# Get Moving Averages
# Get list of all temperature values
temperatureValuesList = dfBTemp['bdTemperature'].astype(float).values.tolist()
# If you'll pass values of a wrong type (say, text instead of floats), you'll get an error:
# Cannot cast array data from dtype('float64') to dtype('<U32') according to the rule 'safe'
# Moving Average for 5 measurements
temperatureMA5 = movingaverage(temperatureValuesList, 5)
# Moving Average for 15 measurements
temperatureMA15 = movingaverage(temperatureValuesList, 15)
# Moving Average for 100 measurements
temperatureMA100 = movingaverage(temperatureValuesList, 100)
# Convert Moving Average Lists to Numpy Arrays, since we need them for fillings with WHERE statement
temperatureMA5 = np.asarray(temperatureMA5)
temperatureMA15 = np.asarray(temperatureMA15)
temperatureMA100 = np.asarray(temperatureMA100)
# Array of all datetime moments, corresponding to individual temperature measurements
datetimesNparr = np.asarray(dfBTemp['dateTaken'])

# Calculate mean temperature for a given hour of measurement - say, 17.00 - 37.2
# Group the data by the index's hour value, then aggregate by the average
temperatureByHour = dfBTemp.groupby(dfBTemp.index.hour).mean()
# Array of hours like 1, 2, 3, 4...
temperatureByHourIndex = np.asarray(temperatureByHour.index)
# Array of corresponding mean temperature values, like 36.8, 37, 37.2, 37...
temperatureByHourValues = np.asarray(temperatureByHour['bdTemperature'])

# Calculate number of measurements taken through a given hour - say, 17.00 - 138
temperatureMeasurementsByHour = dfBTemp.groupby(dfBTemp.index.hour).count()
# Array of hours like 1, 2, 3, 4...
temperatureMeasurementsByHourIndex = np.asarray(temperatureMeasurementsByHour.index)
# Array of corresponding number of temperature measurements, like 138, 45, 15, 3...
temperatureMeasurementsByHourValues = np.asarray(temperatureMeasurementsByHour['bdTemperature'])

# Calculate mean, max and min temperature for each day
temperatureByDayMean = dfBTemp.groupby([pd.Grouper(freq='D')]).mean()
temperatureByDayMin = dfBTemp.groupby([pd.Grouper(freq='D')]).min()
temperatureByDayMax = dfBTemp.groupby([pd.Grouper(freq='D')]).max()



# Calculate mean, max and min Blood Pressure value for each day
# Contains mean, min or max values for all DataFrame properties like systolic and diastolic blood pressure, as well as pulse

bloodPressureByDayMean = dfBloodPressure.groupby([pd.Grouper(freq='D')]).mean()
# pd.Grouper(freq='D') will give you full set of days
# Even if there were no measurements during particular day, it will be in the dataframe
# We've to delete such empty days, otherwise only continuos day series will pe displayed by Matplotlib
# Isolated days will not be shown
# Iterate through dataframe
i = 0
for row in bloodPressureByDayMean.itertuples():
    # if property value is not a number
    if np.isnan(row.bloodPressureSystolic):
        # Delete current row
        # row.Index will give you current row index, datetime object in this case
        bloodPressureByDayMean = bloodPressureByDayMean.drop([row.Index])

bloodPressureByDayMin = dfBloodPressure.groupby([pd.Grouper(freq='D')]).min()
# pd.Grouper(freq='D') will give you full set of days
# Even if there were no measurements during particular day, it will be in the dataframe
# We've to delete such empty days, otherwise only continuos day series will pe displayed by Matplotlib
# Isolated days will not be shown
# Iterate through dataframe
i = 0
for row in bloodPressureByDayMin.itertuples():
    # if property value is not a number
    if np.isnan(row.bloodPressureSystolic):
        # Delete current row
        # row.Index will give you current row index, datetime object in this case
        bloodPressureByDayMin = bloodPressureByDayMin.drop([row.Index])

bloodPressureByDayMax = dfBloodPressure.groupby([pd.Grouper(freq='D')]).max()
# pd.Grouper(freq='D') will give you full set of days
# Even if there were no measurements during particular day, it will be in the dataframe
# We've to delete such empty days, otherwise only continuos day series will pe displayed by Matplotlib
# Isolated days will not be shown
# Iterate through dataframe
i = 0
for row in bloodPressureByDayMax.itertuples():
    # if property value is not a number
    if np.isnan(row.bloodPressureSystolic):
        # Delete current row
        # row.Index will give you current row index, datetime object in this case
        bloodPressureByDayMax = bloodPressureByDayMax.drop([row.Index])

# Get Moving Averages
# Get list of all Systolic Pressure values
pressureSystolicValuesList = dfBloodPressure['bloodPressureSystolic'].astype(float).values.tolist()
# If you'll pass values of a wrong type (say, text instead of floats), you'll get an error:
# Cannot cast array data from dtype('float64') to dtype('<U32') according to the rule 'safe'
# Moving Average for 30 measurements
pressureSystolicMA30 = movingaverage(pressureSystolicValuesList, 30)
# Convert Moving Average Lists to Numpy Arrays, since we need them for fillings with WHERE statement
pressureSystolicMA30 = np.asarray(pressureSystolicMA30)











dfCyclePeriods = pd.DataFrame(columns=['startDate', 'endDate', 'tempValuesThroughCycle'])
# Iterate through Menstrual Cycle dataframe entries
i = 0
for row in dfCycle.itertuples():
    # Menstrual cycle start datetime
    cycleStartDatetime = row.value
    if i==0:
        prevDatetime = cycleStartDatetime
    elif i < len(dfCycle.value):
        # Like dfBTemp.loc['2018-04-11':'2018-05-07']
        dfTempThroughCycle = dfBTemp.loc[prevDatetime:cycleStartDatetime]
        tempValuesThroughCycle = dfTempThroughCycle['bdTemperature']
        dfCyclePeriods = dfCyclePeriods.append({'startDate': prevDatetime,
                                                'endDate': cycleStartDatetime,
                                                'tempValuesThroughCycle': tempValuesThroughCycle}, ignore_index=True)

        # print(str(prevDatetime) + "-" + str(cycleStartDatetime))
        prevDatetime = cycleStartDatetime
    i += 1
# print(str(prevDatetime) + "-" + str(pd.to_datetime('today')))
dfCyclePeriods = dfCyclePeriods.append({'startDate': prevDatetime, 'endDate': pd.to_datetime('today')}, ignore_index=True)
dfTempThroughCycle = dfBTemp.loc[prevDatetime:pd.to_datetime('today')]
tempValuesThroughCycle = dfTempThroughCycle['bdTemperature']
dfCyclePeriods = dfCyclePeriods.append({'startDate': prevDatetime,
                                        'endDate': pd.to_datetime('today'),
                                        'tempValuesThroughCycle': tempValuesThroughCycle}, ignore_index=True)

tempValuesThroughCycle = dfCyclePeriods['tempValuesThroughCycle'].iloc[0]
#print(tempValuesThroughCycle[2])
#print(tempValuesThroughCycle)









#print(dfCyclePeriods.info())
# Print first row of Pandas DataFrame column 'endDate'
#print(dfCyclePeriods['endDate'].iloc[0])
















# WINDOW
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
axBTemp = plt.subplot2grid((6,4), (0,0), colspan=4, rowspan=2)
axBTempDay = plt.subplot2grid((6,4), (2,0), colspan=4, rowspan=2, sharex=axBTemp)
axMAvsMA2 = plt.subplot2grid((6,4), (4,0), colspan=4, rowspan=1, sharex=axBTemp)
axMALongTrend = plt.subplot2grid((6,4), (5,0), colspan=4, rowspan=1, sharex=axBTemp)

# Plot Temperature line graph
axBTemp.plot(dfBTemp['dateTaken'],dfBTemp['bdTemperature'], label='Body Temperature')

# Plot Temperature mean, min and max (per day) line graphs
axBTempDay.plot(temperatureByDayMean.index,temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
axBTempDay.plot(temperatureByDayMax.index,temperatureByDayMax['bdTemperature'], label='MAX Temperature')
axBTempDay.plot(temperatureByDayMin.index,temperatureByDayMin['bdTemperature'], label='MIN Temperature')

# Add 2 Moving Average Line plots (for 5 and for 15 days) to subplot
# Moving Averages are being calculated based on data for axBTemp Line plot
axMAvsMA2.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken'])-len(temperatureMA5):],temperatureMA5, label='Temperature Moving Average 5')
axMAvsMA2.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken'])-len(temperatureMA15):],temperatureMA15, label='Temperature Moving Average 15')

# Add Moving Average Line plot (for 100 days) to subplot - shows long trends
# Moving Averages are being calculated based on data for axBTemp Line plot
axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken'])-len(temperatureMA100):],temperatureMA100, label='Temperature Moving Average 100')

# Fills

# axBTempDay subplot
# Fill space under virtual line @ Y axis  = 36.9 for Body Temperature MIN line graph
axBTempDay.fill_between(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], 36.9, where=(36.9 > temperatureByDayMin['bdTemperature']), alpha = 0.2, color='green', interpolate=True)
# Fill space above virtual line @ Y axis  = 37.5 for Body Temperature MAX line graph
axBTempDay.fill_between(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], 37.5, where=(37.5 < temperatureByDayMax['bdTemperature']), alpha = 0.2, color='orange', interpolate=True)

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
axMALongTrend.set_xlabel('Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

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
    axBTemp.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha = 0.6)
    axBTempDay.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha = 0.6)
    axMAvsMA2.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha = 0.6)
    # Add inscriptions to our vertical lines
    # First argument equals to X value of respective line
    # Second argument sets Y value of our inscription
    # Third argument sets text of inscription
    # rotation=90 will make inscription vertical
    axBTempDay.text(cycleStartDatetime, 37.9, "Cycle start", rotation=90, verticalalignment='center', color="r", alpha = 0.4)

# Iterate through Medicament intake dataframe entries
for row in dfMedication.itertuples():
    # Medicament intake datetime
    medicationDatetime = row.value
    # Add vertical line to subplot
    axBTemp.axvline(x=medicationDatetime, label="Medication", color="black", alpha = 0.6)
    axBTempDay.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
    axMAvsMA2.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
    axMALongTrend.axvline(x=medicationDatetime, label="Medication", color="black", alpha=0.1)
    # Add inscriptions to our vertical lines
    # First argument equals to X value of respective line
    # Second argument sets Y value of our inscription
    # Third argument sets text of inscription
    # rotation=90 will make inscription vertical
    axBTemp.text(medicationDatetime, 37.3, row.text, rotation=90, verticalalignment='center', color="black", alpha = 0.4)

# Remove free space between subplots
plt.subplots_adjust(hspace=0)

# Modify axes Tick Labels for subplots
for ax in [axBTemp, axBTempDay, axMAvsMA2]:
    # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
    plt.setp(ax.get_xticklabels(), visible=False)














#print(dfBlood['bt-hemoglobin-Hb'])





# WINDOW
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
axBTempDay = plt.subplot2grid((12,4), (0,0), colspan=4, rowspan=3)
axMALongTrend = plt.subplot2grid((12,4), (3,0), colspan=4, rowspan=1, sharex=axBTempDay)
axErythrocytes = plt.subplot2grid((12,4), (4,0), colspan=4, rowspan=1, sharex=axBTempDay)
axHemoglobin = plt.subplot2grid((12,4), (5,0), colspan=4, rowspan=1, sharex=axBTempDay)
axHematocrit = plt.subplot2grid((12,4), (6,0), colspan=4, rowspan=1, sharex=axBTempDay)
axMCV = plt.subplot2grid((12,4), (7,0), colspan=4, rowspan=1, sharex=axBTempDay)
axMCH = plt.subplot2grid((12,4), (8,0), colspan=4, rowspan=1, sharex=axBTempDay)
axMCHC = plt.subplot2grid((12,4), (9,0), colspan=4, rowspan=1, sharex=axBTempDay)
axRDW = plt.subplot2grid((12,4), (10,0), colspan=4, rowspan=1, sharex=axBTempDay)
axESR = plt.subplot2grid((12,4), (11,0), colspan=4, rowspan=1, sharex=axBTempDay)

# Plot Temperature mean, min and max (per day) line graphs
axBTempDay.plot(temperatureByDayMean.index,temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
axBTempDay.plot(temperatureByDayMax.index,temperatureByDayMax['bdTemperature'], label='MAX Temperature')
axBTempDay.plot(temperatureByDayMin.index,temperatureByDayMin['bdTemperature'], label='MIN Temperature')

# Add Moving Average Line plot (for 100 days) to subplot - shows long trends
# Moving Averages are being calculated based on data for axBTemp Line plot
axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken'])-len(temperatureMA100):],temperatureMA100, label='Temperature Moving Average 100')

# There will be a gap in case data is missing for particular date
axHemoglobin.plot(dfBlood.index,dfBlood['bt-hemoglobin-Hb'], label='Hemoglobin-Hb, g/L')
axErythrocytes.plot(dfBlood.index,dfBlood['bt-erythrocytes-RBC'], label='Erythrocytes-RBC, 10^12/L')
axHematocrit.plot(dfBlood.index,dfBlood['bt-hematocrit-Hct'], label='Hematocrit-Hct, %')
axMCV.plot(dfBlood.index,dfBlood['bt-meanErythrocyteVolume-MCV'], label='Mean Erythrocyte Volume-MCV, fL')
axMCH.plot(dfBlood.index,dfBlood['bt-meanCellHemoglobin-MCH'], label='Mean Cell Hemoglobin-MCH, pg')
axMCHC.plot(dfBlood.index,dfBlood['bt-meanCellHemoglobinConcentration-MCHC'], label='Mean Cell Hemoglobin Concentration-MCHC, g/dL')
axRDW.plot(dfBlood.index,dfBlood['bt-redCellDistributionWidth-RDW'], label='Red Cell Distribution Width-RDW, %')
axESR.plot(dfBlood.index,dfBlood['bt-erythrocyteSedimentationRate-ESR'], label='Erythrocyte Sedimentation Rate-ESR, mm/hr')

# Fills

# axBTempDay subplot
# Fill space under virtual line @ Y axis  = 36.9 for Body Temperature MIN line graph
axBTempDay.fill_between(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], 36.9, where=(36.9 > temperatureByDayMin['bdTemperature']), alpha = 0.2, color='green', interpolate=True)
# Fill space above virtual line @ Y axis  = 37.5 for Body Temperature MAX line graph
axBTempDay.fill_between(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], 37.5, where=(37.5 < temperatureByDayMax['bdTemperature']), alpha = 0.2, color='orange', interpolate=True)

#axHemoglobin subplot
# Fill space under virtual line @ Y axis  = 110 up to line graph
axHemoglobin.fill_between(dfBlood.index,dfBlood['bt-hemoglobin-Hb'], 110, where=(110 > dfBlood['bt-hemoglobin-Hb']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 140 up to line graph
axHemoglobin.fill_between(dfBlood.index,dfBlood['bt-hemoglobin-Hb'], 140, where=(140 < dfBlood['bt-hemoglobin-Hb']), alpha = 0.2, color='red', interpolate=True)

#axErythrocytes subplot
# Fill space under virtual line @ Y axis  = 4.1 up to line graph
axErythrocytes.fill_between(dfBlood.index,dfBlood['bt-erythrocytes-RBC'], 4.1, where=(4.1 > dfBlood['bt-erythrocytes-RBC']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 5.1 up to line graph
axErythrocytes.fill_between(dfBlood.index,dfBlood['bt-erythrocytes-RBC'], 5.1, where=(5.1 < dfBlood['bt-erythrocytes-RBC']), alpha = 0.2, color='red', interpolate=True)

#axHematocrit subplot
# Fill space under virtual line @ Y axis  = 35 up to line graph
axHematocrit.fill_between(dfBlood.index,dfBlood['bt-hematocrit-Hct'], 35, where=(35 > dfBlood['bt-hematocrit-Hct']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 47 up to line graph
axHematocrit.fill_between(dfBlood.index,dfBlood['bt-hematocrit-Hct'], 47, where=(47 < dfBlood['bt-hematocrit-Hct']), alpha = 0.2, color='red', interpolate=True)

#axMCV subplot
# Fill space under virtual line @ Y axis  = 75 up to line graph
axMCV.fill_between(dfBlood.index,dfBlood['bt-meanErythrocyteVolume-MCV'], 75, where=(75 > dfBlood['bt-meanErythrocyteVolume-MCV']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 95 up to line graph
axMCV.fill_between(dfBlood.index,dfBlood['bt-meanErythrocyteVolume-MCV'], 95, where=(95 < dfBlood['bt-meanErythrocyteVolume-MCV']), alpha = 0.2, color='red', interpolate=True)

#axMCH subplot
# Fill space under virtual line @ Y axis  = 26 up to line graph
axMCH.fill_between(dfBlood.index,dfBlood['bt-meanCellHemoglobin-MCH'], 26, where=(26 > dfBlood['bt-meanCellHemoglobin-MCH']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 34 up to line graph
axMCH.fill_between(dfBlood.index,dfBlood['bt-meanCellHemoglobin-MCH'], 34, where=(34 < dfBlood['bt-meanCellHemoglobin-MCH']), alpha = 0.2, color='red', interpolate=True)

#axMCHC subplot
# Fill space under virtual line @ Y axis  = 30 up to line graph
axMCHC.fill_between(dfBlood.index,dfBlood['bt-meanCellHemoglobinConcentration-MCHC'], 30, where=(30 > dfBlood['bt-meanCellHemoglobinConcentration-MCHC']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 38 up to line graph
axMCHC.fill_between(dfBlood.index,dfBlood['bt-meanCellHemoglobinConcentration-MCHC'], 38, where=(38 < dfBlood['bt-meanCellHemoglobinConcentration-MCHC']), alpha = 0.2, color='red', interpolate=True)

#axRDW subplot
# Fill space under virtual line @ Y axis  = 11.5 up to line graph
axRDW.fill_between(dfBlood.index,dfBlood['bt-redCellDistributionWidth-RDW'], 11.5, where=(11.5 > dfBlood['bt-redCellDistributionWidth-RDW']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 14.5 up to line graph
axRDW.fill_between(dfBlood.index,dfBlood['bt-redCellDistributionWidth-RDW'], 14.5, where=(14.5 < dfBlood['bt-redCellDistributionWidth-RDW']), alpha = 0.2, color='red', interpolate=True)

#axESR subplot
# Fill space under virtual line @ Y axis  = 2 up to line graph
axESR.fill_between(dfBlood.index,dfBlood['bt-erythrocyteSedimentationRate-ESR'], 2, where=(2 > dfBlood['bt-erythrocyteSedimentationRate-ESR']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 15 up to line graph
axESR.fill_between(dfBlood.index,dfBlood['bt-erythrocyteSedimentationRate-ESR'], 15, where=(15 < dfBlood['bt-erythrocyteSedimentationRate-ESR']), alpha = 0.2, color='red', interpolate=True)

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
axMALongTrend.set_xlabel('Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

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
    axBTempDay.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha = 0.6)
    # Add inscriptions to our vertical lines
    # First argument equals to X value of respective line
    # Second argument sets Y value of our inscription
    # Third argument sets text of inscription
    # rotation=90 will make inscription vertical
    axBTempDay.text(cycleStartDatetime, 37.8, "Cycle start", rotation=90, verticalalignment='center', color="r", alpha = 0.4)

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
    axBTempDay.text(medicationDatetime, 37.3, row.text, fontsize='smaller', rotation=90, verticalalignment='center', color="black", alpha=0.4)

# Remove free space between subplots
plt.subplots_adjust(hspace=0)

# Modify axes Tick Labels for all subplots, except latest one
for ax in [axBTempDay, axMALongTrend, axHemoglobin, axErythrocytes, axHematocrit, axMCV, axMCH, axMCHC, axRDW]:
    # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
    plt.setp(ax.get_xticklabels(), visible=False)


















# WINDOW
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
axBTempDay = plt.subplot2grid((11,4), (0,0), colspan=4, rowspan=3)
axMALongTrend = plt.subplot2grid((11,4), (3,0), colspan=4, rowspan=1, sharex=axBTempDay)
axWBC = plt.subplot2grid((11,4), (4,0), colspan=4, rowspan=1, sharex=axBTempDay)
axNeutrophilicBandForms = plt.subplot2grid((11,4), (5,0), colspan=4, rowspan=1, sharex=axBTempDay)
axNeutrophilGranulocytes = plt.subplot2grid((11,4), (6,0), colspan=4, rowspan=1, sharex=axBTempDay)
axEosinophilGranulocytes = plt.subplot2grid((11,4), (7,0), colspan=4, rowspan=1, sharex=axBTempDay)
axBasophilGranulocytes = plt.subplot2grid((11,4), (8,0), colspan=4, rowspan=1, sharex=axBTempDay)
axLymphocytes = plt.subplot2grid((11,4), (9,0), colspan=4, rowspan=1, sharex=axBTempDay)
axMonocytes = plt.subplot2grid((11,4), (10,0), colspan=4, rowspan=1, sharex=axBTempDay)

# Plot Temperature mean, min and max (per day) line graphs
axBTempDay.plot(temperatureByDayMean.index,temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
axBTempDay.plot(temperatureByDayMax.index,temperatureByDayMax['bdTemperature'], label='MAX Temperature')
axBTempDay.plot(temperatureByDayMin.index,temperatureByDayMin['bdTemperature'], label='MIN Temperature')

# Add Moving Average Line plot (for 100 days) to subplot - shows long trends
# Moving Averages are being calculated based on data for axBTemp Line plot
axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken'])-len(temperatureMA100):],temperatureMA100, label='Temperature Moving Average 100')

# There will be a gap in case data is missing for particular date
axWBC.plot(dfBlood.index,dfBlood['bt-whiteBloodCells-WBC'], label='White Blood Cells-WBC, 10^9/L')
axNeutrophilicBandForms.plot(dfBlood.index,dfBlood['bt-neutrophilicBandForms'], label='Neutrophilic Band Forms, %')
axNeutrophilGranulocytes.plot(dfBlood.index,dfBlood['bt-neutrophilGranulocytes-PMNs'], label='Neutrophil Granulocytes-PMNs, %')
axEosinophilGranulocytes.plot(dfBlood.index,dfBlood['bt-eosinophilGranulocytes'], label='Eosinophil Granulocytes, %')
axBasophilGranulocytes.plot(dfBlood.index,dfBlood['bt-basophilGranulocytes'], label='Basophil Granulocytes, %')
axLymphocytes.plot(dfBlood.index,dfBlood['bt-lymphocytes'], label='Lymphocytes, %')
axMonocytes.plot(dfBlood.index,dfBlood['bt-monocytes'], label='Monocytes, %')

# Fills

# axBTempDay subplot
# Fill space under virtual line @ Y axis  = 36.9 for Body Temperature MIN line graph
axBTempDay.fill_between(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], 36.9, where=(36.9 > temperatureByDayMin['bdTemperature']), alpha = 0.2, color='green', interpolate=True)
# Fill space above virtual line @ Y axis  = 37.5 for Body Temperature MAX line graph
axBTempDay.fill_between(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], 37.5, where=(37.5 < temperatureByDayMax['bdTemperature']), alpha = 0.2, color='orange', interpolate=True)

#axWBC subplot
# Fill space under virtual line @ Y axis  = 4 up to line graph
axWBC.fill_between(dfBlood.index,dfBlood['bt-whiteBloodCells-WBC'], 4, where=(4 > dfBlood['bt-whiteBloodCells-WBC']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 9 up to line graph
axWBC.fill_between(dfBlood.index,dfBlood['bt-whiteBloodCells-WBC'], 9, where=(9 < dfBlood['bt-whiteBloodCells-WBC']), alpha = 0.2, color='red', interpolate=True)

#axNeutrophilicBandForms subplot
# Fill space under virtual line @ Y axis  = 1 up to line graph
axNeutrophilicBandForms.fill_between(dfBlood.index,dfBlood['bt-neutrophilicBandForms'], 1, where=(1 > dfBlood['bt-neutrophilicBandForms']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 6 up to line graph
axNeutrophilicBandForms.fill_between(dfBlood.index,dfBlood['bt-neutrophilicBandForms'], 6, where=(6 < dfBlood['bt-neutrophilicBandForms']), alpha = 0.2, color='red', interpolate=True)

#axNeutrophilGranulocytes subplot
# Fill space under virtual line @ Y axis  = 47 up to line graph
axNeutrophilGranulocytes.fill_between(dfBlood.index,dfBlood['bt-neutrophilGranulocytes-PMNs'], 47, where=(47 > dfBlood['bt-neutrophilGranulocytes-PMNs']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 72 up to line graph
axNeutrophilGranulocytes.fill_between(dfBlood.index,dfBlood['bt-neutrophilGranulocytes-PMNs'], 72, where=(72 < dfBlood['bt-neutrophilGranulocytes-PMNs']), alpha = 0.2, color='red', interpolate=True)

#axEosinophilGranulocytes subplot
# Fill space under virtual line @ Y axis  = 1 up to line graph
axEosinophilGranulocytes.fill_between(dfBlood.index,dfBlood['bt-eosinophilGranulocytes'], 1, where=(1 > dfBlood['bt-eosinophilGranulocytes']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 5 up to line graph
axEosinophilGranulocytes.fill_between(dfBlood.index,dfBlood['bt-eosinophilGranulocytes'], 5, where=(5 < dfBlood['bt-eosinophilGranulocytes']), alpha = 0.2, color='red', interpolate=True)

#axBasophilGranulocytes subplot
# Fill space under virtual line @ Y axis  = 0 up to line graph
axBasophilGranulocytes.fill_between(dfBlood.index,dfBlood['bt-basophilGranulocytes'], 0, where=(0 > dfBlood['bt-basophilGranulocytes']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 1 up to line graph
axBasophilGranulocytes.fill_between(dfBlood.index,dfBlood['bt-basophilGranulocytes'], 1, where=(1 < dfBlood['bt-basophilGranulocytes']), alpha = 0.2, color='red', interpolate=True)

#axLymphocytes subplot
# Fill space under virtual line @ Y axis  = 19 up to line graph
axLymphocytes.fill_between(dfBlood.index,dfBlood['bt-lymphocytes'], 19, where=(19 > dfBlood['bt-lymphocytes']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 37 up to line graph
axLymphocytes.fill_between(dfBlood.index,dfBlood['bt-lymphocytes'], 37, where=(37 < dfBlood['bt-lymphocytes']), alpha = 0.2, color='red', interpolate=True)

#axMonocytes subplot
# Fill space under virtual line @ Y axis  = 3 up to line graph
axMonocytes.fill_between(dfBlood.index,dfBlood['bt-monocytes'], 3, where=(3 > dfBlood['bt-monocytes']), alpha = 0.2, color='red', interpolate=True)
# Fill space above virtual line @ Y axis  = 11 up to line graph
axMonocytes.fill_between(dfBlood.index,dfBlood['bt-monocytes'], 11, where=(11 < dfBlood['bt-monocytes']), alpha = 0.2, color='red', interpolate=True)

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
axMALongTrend.set_xlabel('Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

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
    axBTempDay.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha = 0.6)
    # Add inscriptions to our vertical lines
    # First argument equals to X value of respective line
    # Second argument sets Y value of our inscription
    # Third argument sets text of inscription
    # rotation=90 will make inscription vertical
    axBTempDay.text(cycleStartDatetime, 37.8, "Cycle start", rotation=90, verticalalignment='center', color="r", alpha = 0.4)

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
    axBTempDay.text(medicationDatetime, 37.3, row.text, fontsize='smaller', rotation=90, verticalalignment='center', color="black", alpha=0.4)

# Remove free space between subplots
plt.subplots_adjust(hspace=0)

# Modify axes Tick Labels for all subplots, except latest one
for ax in [axBTempDay, axMALongTrend, axWBC, axNeutrophilicBandForms, axNeutrophilGranulocytes, axEosinophilGranulocytes, axBasophilGranulocytes, axLymphocytes]:
    # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
    plt.setp(ax.get_xticklabels(), visible=False)





















print(bloodPressureByDayMax.describe())
print(bloodPressureByDayMax['bloodPressureSystolic'])




# WINDOW
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
axBTempDay = plt.subplot2grid((11,4), (0,0), colspan=4, rowspan=3)
axMALongTrend = plt.subplot2grid((11,4), (3,0), colspan=4, rowspan=1, sharex=axBTempDay)
axBloodPressureSystolic = plt.subplot2grid((11,4), (4,0), colspan=4, rowspan=2, sharex=axBTempDay)
axBloodPressureDiastolic = plt.subplot2grid((11,4), (6,0), colspan=4, rowspan=2, sharex=axBTempDay)
axPulse = plt.subplot2grid((11,4), (8,0), colspan=4, rowspan=2, sharex=axBTempDay)
axBloodPressureSystolicMALongTrend = plt.subplot2grid((11,4), (10,0), colspan=4, rowspan=1, sharex=axBTempDay)


# Plot Temperature mean, min and max (per day) line graphs
axBTempDay.plot(temperatureByDayMean.index,temperatureByDayMean['bdTemperature'], label='MEAN Temperature')
axBTempDay.plot(temperatureByDayMax.index,temperatureByDayMax['bdTemperature'], label='MAX Temperature')
axBTempDay.plot(temperatureByDayMin.index,temperatureByDayMin['bdTemperature'], label='MIN Temperature')

# Add Moving Average Line plot (for 100 days) to subplot - shows long trends
# Moving Averages are being calculated based on data for axBTemp Line plot
axMALongTrend.plot(dfBTemp['dateTaken'][len(dfBTemp['dateTaken'])-len(temperatureMA100):],temperatureMA100, label='Temperature Moving Average 100')

# Plot Systolic Blood Pressure mean, min and max (per day) line graphs
# There will be a gap in case data is missing for particular date
axBloodPressureSystolic.plot(bloodPressureByDayMean.index, bloodPressureByDayMean['bloodPressureSystolic'], label='MEAN Systolic Pressure, mmHg')
axBloodPressureSystolic.plot(bloodPressureByDayMax.index, bloodPressureByDayMax['bloodPressureSystolic'], label='MAX Systolic Pressure, mmHg')
axBloodPressureSystolic.plot(bloodPressureByDayMin.index, bloodPressureByDayMin['bloodPressureSystolic'], label='MIN Systolic Pressure, mmHg')

# Plot Diastolic Blood Pressure mean, min and max (per day) line graphs
# There will be a gap in case data is missing for particular date
axBloodPressureDiastolic.plot(bloodPressureByDayMean.index, bloodPressureByDayMean['bloodPressureDiastolic'], label='MEAN Diastolic Pressure, mmHg')
axBloodPressureDiastolic.plot(bloodPressureByDayMax.index, bloodPressureByDayMax['bloodPressureDiastolic'], label='MAX Diastolic Pressure, mmHg')
axBloodPressureDiastolic.plot(bloodPressureByDayMin.index, bloodPressureByDayMin['bloodPressureDiastolic'], label='MIN Diastolic Pressure, mmHg')

# Plot Pulse mean, min and max (per day) line graphs
# There will be a gap in case data is missing for particular date
axPulse.plot(bloodPressureByDayMean.index, bloodPressureByDayMean['pulseBPM'], label='MEAN Pulse, BPM')
axPulse.plot(bloodPressureByDayMax.index, bloodPressureByDayMax['pulseBPM'], label='MAX Pulse, BPM')
axPulse.plot(bloodPressureByDayMin.index, bloodPressureByDayMin['pulseBPM'], label='MIN Pulse, BPM')

# Add Systolic Pressure Moving Average Line plot (for 30 days) to subplot - shows long trends
# Moving Averages are being calculated based on data for axBloodPressureSystolic Line plot
axBloodPressureSystolicMALongTrend.plot(dfBloodPressure['dateTaken'][len(dfBloodPressure['dateTaken'])-len(pressureSystolicMA30):],pressureSystolicMA30, label='Systolic Pressure Moving Average 30')

# Fills

# axBTempDay subplot
# Fill space under virtual line @ Y axis  = 36.9 for Body Temperature MIN line graph
axBTempDay.fill_between(temperatureByDayMin.index, temperatureByDayMin['bdTemperature'], 36.9, where=(36.9 > temperatureByDayMin['bdTemperature']), alpha = 0.2, color='green', interpolate=True)
# Fill space above virtual line @ Y axis  = 37.5 for Body Temperature MAX line graph
axBTempDay.fill_between(temperatureByDayMax.index, temperatureByDayMax['bdTemperature'], 37.5, where=(37.5 < temperatureByDayMax['bdTemperature']), alpha = 0.2, color='orange', interpolate=True)

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
axMALongTrend.set_xlabel('Red filling at MA-5 vs MA-15 plot means rising body temperature, green filling - lowering body temperature')

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
    axBTempDay.axvline(x=cycleStartDatetime, label="Menstrual cycle START", color="red", alpha = 0.4)
    # Add inscriptions to our vertical lines
    # First argument equals to X value of respective line
    # Second argument sets Y value of our inscription
    # Third argument sets text of inscription
    # rotation=90 will make inscription vertical
    axBTempDay.text(cycleStartDatetime, 37.8, "Cycle start", rotation=90, verticalalignment='center', color="r", alpha = 0.4)

# Iterate through Medicament intake dataframe entries
for row in dfMedication.itertuples():
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
    axBTempDay.text(medicationDatetime, 37.3, row.text, fontsize='smaller', rotation=90, verticalalignment='center', color="black", alpha = 0.4)

# Remove free space between subplots
plt.subplots_adjust(hspace=0)

# Modify axes Tick Labels for subplots
for ax in [axBTempDay, axMALongTrend, axHemoglobin, axErythrocytes, axHematocrit, axMCV, axMCH, axMCHC, axRDW]:
    # Remove X axis Tick Labels (are not visible anyway, if there are no free space between sublots)
    plt.setp(ax.get_xticklabels(), visible=False)










# WINDOW
# Open window with a given name
plt.figure("Blood Tests - Corellation Matrix")
#print(dfBlood.describe())
# print(dfBlood.corr())

# Create subplots and put them to appropriate places of the program-opened window
# Arguments in first parentheses are setting grid for sublots; first one - for vertical dimension, second - for horizontal one.
# Arguments in a second parentheses are setting subplot location within this aformentioned grid.
# Arguments in a second parentheses can't be greater than (or equal to) those in first parentheses.
# Otherwise you'll get an error: IndexError: invalid index
# "colspan" argument sets horizontal length of a subplot.
# "rowspan" argument sets vertical height of a subplot.
# "sharex" argument sets subplot current subplot has to share X axis with.
# In this case, when you'll zoom into one plot, another will be zoomed accordingly.
axBloodCorr = plt.subplot2grid((6,6), (0,0), colspan=5, rowspan=5)


# corr = dfBlood.corr()
# sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, annot=True, linewidths=.5, ax=axBloodCorr)






d = {'dateTaken' : pd.date_range(start='2018.03.17', end='2018.06.12', freq='1D'),
     'dailyDose':100,
     'cumulativeDose':100}
i = 0
cumulativeDose = 100;
dailyDoseList = []
cumulativeDoseList = []

print(len(d['dateTaken']))
for x in d['dateTaken']:
    # d['dailyDose'][i] = 100
    # d['cumulativeDose'][i] = cumulativeDose
    dailyDoseList.append(100)
    cumulativeDoseList.append(cumulativeDose)
    cumulativeDose += 100
    i += 1
    # print(x)

d = {'dateTaken': pd.to_datetime(d['dateTaken']),
     'dailyDose': dailyDoseList,
     'cumulativeDose': cumulativeDoseList}

print(len(d['dailyDose']))
# print(d)
dfIronSuppl = pd.DataFrame(d)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfIronSuppl.set_index('dateTaken', drop=False, inplace=True)

corr = dfBlood.corrwith(dfIronSuppl)
#sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, annot=True, linewidths=.5, ax=axBloodCorr)
#print(corr)

#print(dfIronSuppl.loc['2018-04-11':'2018-05-07'])













# WINDOW
# Open window with a given name
plt.figure("Body Temperature - Frequency")
# Create subplots and put them to appropriate places of the program-opened window
# Arguments in first parentheses are setting grid for sublots; first one - for vertical dimension, second - for horizontal one.
# Arguments in a second parentheses are setting subplot location within this aformentioned grid.
# Arguments in a second parentheses can't be greater than (or equal to) those in first parentheses.
# Otherwise you'll get an error: IndexError: invalid index
# "colspan" argument sets horizontal length of a subplot.
# "rowspan" argument sets vertical height of a subplot.
# "sharex" argument sets subplot current subplot has to share X axis with.
# In this case, when you'll zoom into one plot, another will be zoomed accordingly.
axTempOccurence = plt.subplot2grid((6,4), (0,0), colspan=4, rowspan=2)
axMeasurementsPerHour = plt.subplot2grid((6,4), (2,0), colspan=2, rowspan=2)
axTempPerHour = plt.subplot2grid((6,4), (2,2), colspan=2, rowspan=2)

# Set starting and ending points for Y axis (so it'll start from 36.7 rather than from 0)
axTempPerHour.set_ylim(ymin= 36.7, ymax=37.7)

# Prevent Bar chart columns from overlapping by setting their width
axTempOccurenceBarWidth = 0.04
axMeasurementsPerHourBarWidth = 0.5
axTempPerHourBarWidth = 0.5

# Set column opacity
bar_opacity = 0.4
error_config = {'ecolor': '0.3'}
# Add Bar charts to respective subplots
# First argument is for X axis, second - for Y axis. Third sets column width.
axTempOccurence.bar(temperatureValues, temperatureValuesOccurrence, axTempOccurenceBarWidth, alpha=bar_opacity, color='b', error_kw=error_config, label='Body Temperature')
axMeasurementsPerHour.bar(temperatureMeasurementsByHourIndex, temperatureMeasurementsByHourValues, axMeasurementsPerHourBarWidth, alpha=bar_opacity, color='b', error_kw=error_config, label='Body Temperature')
axTempPerHour.bar(temperatureByHourIndex, temperatureByHourValues, axTempPerHourBarWidth, alpha=bar_opacity, color='b', error_kw=error_config, label='Body Temperature')

# Set displayable name for subplot
# May use multiple lines with \n
axTempOccurence.set_title("Number of measurements per given temperature value")

# Set X axis label to subplot
axMeasurementsPerHour.set_xlabel('Hour of the day')
axTempPerHour.set_xlabel('Hour of the day')

# Set Y axis label to subplot
axTempOccurence.set_ylabel('Number of measurements')
axMeasurementsPerHour.set_ylabel('Number of measurements')
axTempPerHour.set_ylabel('Temperature')



# Show plot
plt.show()