def get_sheets(file):
    if 'pd' not in locals():
        import pandas as pd
    all_sheets = list(pd.read_excel(file, engine='odf', sheet_name=None, header=10).keys())
    list_tables = pd.read_excel(file, engine='odf',header=10)
    list_tables = list_tables[~list_tables['Subject'].isna()].set_index('Subject')
    list_tables.columns = [x.strip() for x in list_tables.columns]
    table_lookup = list_tables['Table No.'].to_dict()
    available_sheets = {k:v for k,v in table_lookup.items() if v in all_sheets}

    return available_sheets

def get_clean_stats(file, period='year', sheet:str='A1'):
    """Attempts to extract the trended data from the .odf 'live tables' file
    returning the sheetname you specify
    """
    if 'pd' not in locals():
        import pandas as pd
    try:
        tmp = pd.read_excel(file, engine='odf', sheet_name=sheet, header=[1,2,3,4,5])
    except:
        sheets = pd.read_excel(file, engine='odf', sheet_name=None, nrows=1).keys()
        try:
            sheetname = [x for x in sheets if sheet in x][0]
            tmp = pd.read_excel(file, engine='odf', sheet_name=sheetname, header=[1,2,3,4,5])
        except:
            raise NameError(f"Error: sheet '{sheet}' not found, please check the spreadsheet\nAvailable sheets: \n{sheets}")

    tmp.columns = ['|'.join([y for y in x if not y.startswith('Unnamed:')]) for x in tmp.columns]
    tmp.columns = ['date', 'quarter', 'real_or_predicted'] + list(tmp.columns[3:])

    notes_start = tmp[tmp['date'].astype(str).str.startswith('Notes')].index[0]
    tmp = tmp.loc[:notes_start]

    # remove first and last rows if they are all null values
    if tmp.shape[1] == tmp.iloc[0].isnull().sum():
        tmp = tmp.iloc[1:]
    if tmp.shape[1] == tmp.iloc[-1].isnull().sum():
        tmp = tmp.iloc[:-1]
    # reset index for future .iloc statements to be accurate
    tmp.reset_index().drop(columns='index', inplace=True)

    tmp.dropna(how='all',inplace=True)

    tmp = tmp[tmp['real_or_predicted'] == 'R'].copy()

    tmp['date'] = tmp['date'].ffill().astype(str)

    yrs_ix = tmp[tmp['date'].str.contains('/')].index
    quarters_ix = tmp[~tmp['date'].str.contains('/')].index

    years = tmp.loc[yrs_ix].copy()
    years['period'] = years['date'].astype(str).str.replace('/','-20',regex=False)
    years['period_type'] = 'year'

    quarters = tmp.loc[quarters_ix].dropna(how='all').copy()
    quarters['period'] = quarters['date'].astype(str) + ' ' + quarters['quarter']
    quarters['period_type'] = 'quarter'

    data = pd.concat([years, quarters],ignore_index=True
                    ).drop(columns=['date','quarter','real_or_predicted']).dropna(how='all', axis=1)

    data = pd.concat([data.iloc[:,-2:], data.iloc[:,:-2]],axis=1)
    
    if period in ['year','quarter']:
        return data.query(f"period_type == '{period}'").set_index('period').drop(columns='period_type')
    
    return data

def plot_reasons(file, period='quarter', sheet='A1', savefig_file=None):
    """NOTE: this is in beta. 
    
    The graph displays % share by each criteria, calculating as a fraction of the first field which may not always be the total
    ""reasons_lost_home_pct""
    """
    if 'plt' not in locals():
        import matplotlib.pyplot as plt
        
    fig = plt.figure(figsize=(12,12))
    ax1 = fig.add_subplot()

    reasons_lost_home = get_clean_stats(file, period=period, sheet=sheet)
    reasons_lost_home_pct = reasons_lost_home.T.iloc[1:].copy() / reasons_lost_home.T.iloc[0].copy()

    # add data to plot
    reasons_lost_home_pct.sort_values(reasons_lost_home_pct.columns[-1]).T.plot(kind='area',stacked=True, ax=ax1)
    
    # add legend
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=[1,0.5])

    # add title
    sheet_desr = [k for k,v in get_sheets(file).items() if v == sheet][0]
    fig.suptitle(sheet_desr)
    
    if savefig_file != None:
        from pathlib import Path
        fig.savefig(Path(savefig_file,'.png'), dpi=150)
        
    fig.show()
    return fig, ax1

def plot_ethnicity(file, period='quarter', sheet='Ethnicity of main applicant'):
    if 'plt' not in locals():
        import matplotlib.pyplot as plt
        
    # lookup correct spreadsheet
    lkp_sheets = get_sheets(file)
    if sheet in lkp_sheets.values():
        sheetname = sheet
    elif sheet in lkp_sheets.keys():
        sheetname = lkp_sheets.get(sheet)
    else:
        raise NameError(f"Error: sheet {sheet} not found in spreadsheet")
    
    ttest = get_clean_stats(file, period=period, sheet=sheetname)
    
    # do the subtotal fields only:
    ttest = ttest[[x for x in ttest if '|Total' in x]].T.drop_duplicates()

    raw_figs = ttest[ttest>1].dropna()
    pct_figs = ttest[ttest<=1].dropna()

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot()
    raw_figs.T.plot(kind='area',stacked=True, ax=ax)
    
    # setup title and legend
    ax.set_title('Ethnicity : Total Applicants')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=[1,0.5])
    
    fig.show()
    return fig, ax