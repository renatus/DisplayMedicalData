# Function to draw Matplotlib window
def draw(plt, pd, dfBlood):
    # Open window with a given name
    plt.figure("Blood Tests - Corellation Matrix")
    # print(dfBlood.describe())
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
    axBloodCorr = plt.subplot2grid((6, 6), (0, 0), colspan=5, rowspan=5)

    # corr = dfBlood.corr()
    # sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, annot=True, linewidths=.5, ax=axBloodCorr)

    d = {'dateTaken': pd.date_range(start='2018.03.17', end='2018.06.12', freq='1D'),
         'dailyDose': 100,
         'cumulativeDose': 100}
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
    # sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, annot=True, linewidths=.5, ax=axBloodCorr)
    # print(corr)

    # print(dfIronSuppl.loc['2018-04-11':'2018-05-07'])