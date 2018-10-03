# Function to draw Matplotlib window
def draw(plt, temperatureValues, temperatureValuesOccurrence, temperatureMeasurementsByHourIndex, temperatureMeasurementsByHourValues, temperatureByHourIndex, temperatureByHourValues):
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
    axTempOccurence = plt.subplot2grid((6, 4), (0, 0), colspan=4, rowspan=2)
    axMeasurementsPerHour = plt.subplot2grid((6, 4), (2, 0), colspan=2, rowspan=2)
    axTempPerHour = plt.subplot2grid((6, 4), (2, 2), colspan=2, rowspan=2)

    # Set starting and ending points for Y axis (so it'll start from 36.7 rather than from 0)
    axTempPerHour.set_ylim(ymin=36.7, ymax=37.7)

    # Prevent Bar chart columns from overlapping by setting their width
    axTempOccurenceBarWidth = 0.04
    axMeasurementsPerHourBarWidth = 0.5
    axTempPerHourBarWidth = 0.5

    # Set column opacity
    bar_opacity = 0.4
    error_config = {'ecolor': '0.3'}
    # Add Bar charts to respective subplots
    # First argument is for X axis, second - for Y axis. Third sets column width.
    axTempOccurence.bar(temperatureValues, temperatureValuesOccurrence, axTempOccurenceBarWidth, alpha=bar_opacity,
                        color='b', error_kw=error_config, label='Body Temperature')
    axMeasurementsPerHour.bar(temperatureMeasurementsByHourIndex, temperatureMeasurementsByHourValues,
                              axMeasurementsPerHourBarWidth, alpha=bar_opacity, color='b', error_kw=error_config,
                              label='Body Temperature')
    axTempPerHour.bar(temperatureByHourIndex, temperatureByHourValues, axTempPerHourBarWidth, alpha=bar_opacity,
                      color='b', error_kw=error_config, label='Body Temperature')

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