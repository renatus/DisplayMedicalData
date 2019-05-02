# Import packages
# Package for data analysis
import pandas as pd
#To fix ImportError: No module named '_tkinter' during matplotlib import use
#sudo apt-get install python3-tk
# For graph plotting
import matplotlib.pyplot as plt
# For plotting functionality like advanced fills with "where" argument
import numpy as np
# SYS module provides access to some variables used or maintained by the interpreter and to functions that interact closely with the interpreter.
import sys
# We need Seaborn for beautiful corellation matrixes out of the box

# Add path to custom package with modules to draw individual Matplotlib windows
sys.path.append("windows")



# Load JSON file and convert it to Pandas DataFrame
# If you've an error in JSON syntax, like trailing comma, you'll see an error:
# ValueError: Unexpected character found when decoding array value (1)
# Body temperature measurements with date and time
dfBTemp = pd.read_json('body_temperature.json')
# Menstrual cycle start dates
dfCycle = pd.read_json('menstrual_cycle_start.json')
# Medicament intake with date and time
dfMedicationStartStop = pd.read_json('medication_start_stop.json')
# Blood test results
dfBlood = pd.read_json('blood_test.json')
# Blood pressure measurements with date and time
dfBloodPressure = pd.read_json('blood_pressure.json')
# Misc data about patient's body condition
dfWellbeing = pd.read_json('wellbeing.json')
# # Thyroid hormones level Dataframe
# dfThyroid = pd.read_json('thyroid.json')
# TSH hormone level Dataframe
dfTSH = pd.read_json('tsh.json')
# TgAb antibodies level Dataframe
dfTgAb = pd.read_json('tgab.json')
# Levothyroxine hormone intake Dataframe
dfLevothyroxine = pd.read_json('levothyroxine_start_stop.json')
# T3 hormone level Dataframe
dfT3 = pd.read_json('t3.json')
# T4 hormone level Dataframe
dfT4 = pd.read_json('t4.json')

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
dfMedicationStartStop.value = pd.to_datetime(dfMedicationStartStop.value)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfMedicationStartStop.set_index('value', drop=False, inplace=True)

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

# Misc data about patient's body Dataframe
# Rename columns in DataFrame
dfWellbeing = dfWellbeing.rename({'dateTimeTaken':'dateTimeTaken'}, axis='columns')
# Convert objects to datetime
dfWellbeing.dateTimeTaken = pd.to_datetime(dfWellbeing.dateTimeTaken)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfWellbeing.set_index('dateTimeTaken', drop=False, inplace=True)

# # Thyroid hormones level Dataframe
# # Rename columns in DataFrame
# dfThyroid = dfThyroid.rename({'dateTimeTaken':'dateTimeTaken'}, axis='columns')
# # Convert objects to datetime
# dfThyroid.dateTimeTaken = pd.to_datetime(dfThyroid.dateTimeTaken)
# # Set Dataframe's index
# # We need "drop=False" argument to save original 'dateTaken' column
# dfThyroid.set_index('dateTimeTaken', drop=False, inplace=True)

# TSH hormone level Dataframe
# Rename columns in DataFrame
dfTSH = dfTSH.rename({'dateTimeTaken':'dateTimeTaken'}, axis='columns')
# Convert objects to datetime
dfTSH.dateTimeTaken = pd.to_datetime(dfTSH.dateTimeTaken)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfTSH.set_index('dateTimeTaken', drop=False, inplace=True)

# TgAb antibodies level Dataframe
# Rename columns in DataFrame
dfTgAb = dfTgAb.rename({'dateTimeTaken':'dateTimeTaken'}, axis='columns')
# Convert objects to datetime
dfTgAb.dateTimeTaken = pd.to_datetime(dfTgAb.dateTimeTaken)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfTgAb.set_index('dateTimeTaken', drop=False, inplace=True)

# Levothyroxine hormone intake Dataframe
# Rename columns in DataFrame
dfLevothyroxine = dfLevothyroxine.rename({'dateTimeTaken':'dateTimeTaken', 'dosage':'value'}, axis='columns')
# Convert objects to datetime
dfLevothyroxine.dateTimeTaken = pd.to_datetime(dfLevothyroxine.dateTimeTaken)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfLevothyroxine.set_index('dateTimeTaken', drop=False, inplace=True)

# T3 hormone level Dataframe
# Rename columns in DataFrame
dfT3 = dfT3.rename({'dateTimeTaken':'dateTimeTaken'}, axis='columns')
# Convert objects to datetime
dfT3.dateTimeTaken = pd.to_datetime(dfT3.dateTimeTaken)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfT3.set_index('dateTimeTaken', drop=False, inplace=True)

# T4 hormone level Dataframe
# Rename columns in DataFrame
dfT4 = dfT4.rename({'dateTimeTaken':'dateTimeTaken'}, axis='columns')
# Convert objects to datetime
dfT4.dateTimeTaken = pd.to_datetime(dfT4.dateTimeTaken)
# Set Dataframe's index
# We need "drop=False" argument to save original 'dateTaken' column
dfT4.set_index('dateTimeTaken', drop=False, inplace=True)



# Count number of measurements with given temperature value (like 37.1 - 120, 37.2 - 93)
#https://stackoverflow.com/questions/10373660/converting-a-pandas-groupby-object-to-dataframe
dfTemperatureValuesOccurrence = dfBTemp.groupby(['bdTemperature']).count()
# Array of floats like 37.2
temperatureValues = np.asarray(dfTemperatureValuesOccurrence.index)
# Array of integers like 93
temperatureValuesOccurrence = np.asarray(dfTemperatureValuesOccurrence.dateTaken)

# Get Temperature Moving Averages with Pandas
# Moving Average for 5 measurements
temperatureMA5 = dfBTemp['bdTemperature'].rolling(5).mean()
# Moving Average for 15 measurements
temperatureMA15 = dfBTemp['bdTemperature'].rolling(15).mean()
# Moving Average for 100 measurements
temperatureMA100 = dfBTemp['bdTemperature'].rolling(100).mean()
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
# We've to delete such empty days, otherwise only continuous day series will pe displayed by Matplotlib
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

# Get Moving Averages (working with Pandas DataFrames and with Pandas-provided tools)

# Systolic Pressure Moving Average for 30 measurements
pressureSystolicMA30 = dfBloodPressure['bloodPressureSystolic'].rolling(30).mean()
# Systolic Pressure Moving Average for 13 days
pressureSystolicMA13d = dfBloodPressure['bloodPressureSystolic'].rolling('13d').mean()
# Convert Moving Average Lists to Numpy Arrays, since we need them for fillings with WHERE statement
pressureSystolicMA30 = np.asarray(pressureSystolicMA30)
pressureSystolicMA13d = np.asarray(pressureSystolicMA13d)

# Diastolic Pressure Moving Average for 30 measurements
pressureDiastolicMA30 = dfBloodPressure['bloodPressureDiastolic'].rolling(30).mean()
# Diastolic Pressure Moving Average for 13 days
pressureDiastolicMA13d = dfBloodPressure['bloodPressureDiastolic'].rolling('13d').mean()
# Convert Moving Average Lists to Numpy Arrays, since we need them for fillings with WHERE statement
pressureDiastolicMA30 = np.asarray(pressureDiastolicMA30)
pressureDiastolicMA13d= np.asarray(pressureDiastolicMA13d)

# Pulse Moving Average for 30 measurements
pulseMA30 = dfBloodPressure['pulseBPM'].rolling(30).mean()
# Pulse Moving Average for 13 days
pulseMA13d = dfBloodPressure['pulseBPM'].rolling(13).mean()
# Convert Moving Average Lists to Numpy Arrays, since we need them for fillings with WHERE statement
pulseMA30 = np.asarray(pulseMA30)
pulseMA13d = np.asarray(pulseMA13d)



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



# Debugging

# print(dfCyclePeriods.info())
# Print first row of Pandas DataFrame column 'endDate'
# print(dfCyclePeriods['endDate'].iloc[0])

# print(bloodPressureByDayMax.describe())
# print(bloodPressureByDayMax['bloodPressureSystolic'])



# Draw WINDOW
# Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
from windows import window_temp_line_plots as windTempLPlots
windTempLPlots.draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA5, temperatureMA15, temperatureMA100, datetimesNparr, dfMedicationStartStop, dfCycle)

# Draw WINDOW
# Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
from windows import window_erythrocytes_line_plots as windTempLPlots
windTempLPlots.draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100, dfMedicationStartStop, dfCycle, dfBlood)

# Draw WINDOW
# Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
from windows import window_leukocytes_line_plots as windTempLPlots
windTempLPlots.draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100, dfMedicationStartStop, dfCycle, dfBlood)

# Draw WINDOW
# Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
from windows import window_thyroid_line_plots as windThyroidLPlots
windThyroidLPlots.draw(np, plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100, dfMedicationStartStop, dfCycle, dfTSH, dfTgAb, dfLevothyroxine)

# Draw WINDOW
# Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
from windows import window_thyroid_line_plots_2 as windThyroidLPlots2
windThyroidLPlots2.draw(np, plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100, dfMedicationStartStop, dfCycle, dfT4, dfT3, dfLevothyroxine)

# Draw WINDOW
# Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
from windows import window_pressure_line_plots as windTempLPlots
windTempLPlots.draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100,
                    bloodPressureByDayMean, bloodPressureByDayMax, bloodPressureByDayMin, pressureSystolicMA30,
                    dfMedicationStartStop, dfCycle, dfBloodPressure)

# Draw WINDOW
# Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
from windows import window_pressure_line_plots_2 as windTempLPlots2
windTempLPlots2.draw(plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA100,
                     bloodPressureByDayMean, bloodPressureByDayMax, bloodPressureByDayMin,
                     pressureSystolicMA30, pressureSystolicMA13d, pressureDiastolicMA30, pressureDiastolicMA13d, pulseMA30, pulseMA13d,
                     dfMedicationStartStop, dfCycle, dfBloodPressure)

# Draw WINDOW
# Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
from windows import window_wellbeing_line_plots as windWellbeingLPlots
windWellbeingLPlots.draw(np, plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA5, temperatureMA15, temperatureMA100, datetimesNparr, dfMedicationStartStop, dfCycle, dfWellbeing)

# Draw WINDOW
# Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
from windows import window_wellbeing_line_plots_2 as windWellbeingLPlots2
windWellbeingLPlots2.draw(np, plt, dfBTemp, temperatureByDayMean, temperatureByDayMax, temperatureByDayMin, temperatureMA5, temperatureMA15, temperatureMA100, datetimesNparr, dfMedicationStartStop, dfCycle, dfWellbeing)


# # Draw WINDOW
# # Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
# from windows import window_temp_frequency as windTempFreq
# windTempFreq.draw(plt, temperatureValues, temperatureValuesOccurrence, temperatureMeasurementsByHourIndex, temperatureMeasurementsByHourValues, temperatureByHourIndex, temperatureByHourValues)

# # Draw WINDOW
# # Don't forget to append sys.path with "windows" custom package path - sys.path.append("windows")
# from windows import window_blood_corellation_matrix as windTempLPlots
# windTempLPlots.draw(plt, pd, dfBlood)



# Show plot
plt.show()