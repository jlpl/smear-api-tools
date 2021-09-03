import pandas as pd
import urllib.request, json
from collections import Iterable
from datetime import datetime, timedelta

def isStr(obj):
    return isinstance(obj,str)

def isStrIterable(obj):
    result=False
    if (isinstance(obj,Iterable) & ~isinstance(obj,str)):
        if all(isinstance(elem,str) for elem in obj):
            result=True
    return result

def isDatetime(obj):
    return isinstance(obj,datetime)

def isDatetimeIterable(obj):
    result=False
    if isinstance(obj,Iterable):
        if all(isinstance(elem,datetime) for elem in obj):
            result=True
    return result

def parse(year, month, day, hour, minute, second):
    return year+ '-' +month+ '-' +day+ ' ' +hour+ ':' +minute+ ':' +second

def getData(variables,dates=None,start=None,end=None,quality='ANY',averaging='1',avg_type='NONE'):
    """ Get timeseries of variables using Smart SMEAR API 
    
    Parameters
    ----------

    variables: string or array of strings
        name of a measured quantity in the database
        (tablevariable)

    dates: datetime object or array of datetime objects
        the date(s) for which measurements are downloaded

    start: datetime object
        begin of measurement

    end: datetime object
        end of measurement
    
    quality: string
        "ANY"
    
    averaging: string
        "1" (no averaging) or "30" (30 min) or "60" (60 min)
    
    avg_type: string
        "NONE" or "ARITHMETIC" or "MEDIAN" or "MIN" or "MAX"

    Returns
    -------
    
    pandas DataFrame or list of DataFrames
        downloaded data, list is given for array of date objects

        In the dataframes:
        index   : time
        columns : variables
        values  : data

    """

    if isStrIterable(variables):
        col_names = [x for x in variables]
        tablevariables = ['&tablevariable='+x for x in variables]
        variable_string = ''.join(list(tablevariables))

    elif isStr(variables):
        col_names = [variables]
        variable_string = '&tablevariable='+variables
    else:
        raise Exception('"variables" must be string or array of strings')

    if ((start is not None) and (end is not None)):
   
        if (isDatetime(start) & isDatetime(end)):
            pass
        else:
            raise Exception('"start" and "end" must be datetime objects')

        st=start.strftime("%Y-%m-%dT%H:%M:%S")
        et=end.strftime("%Y-%m-%dT%H:%M:%S")

        try:
 
            url_string = 'https://smear-backend.rahtiapp.fi/search/timeseries/csv?'\
                            +variable_string\
                            +'&from='+st.replace(':','%3A')\
                            +'&to='+et.replace(':','%3A')\
                            +'&quality='+quality\
                            +'&interval='+averaging\
                            +'&aggregation='+avg_type

            data = pd.read_csv(url_string, parse_dates = [[0,1,2,3,4,5]], date_parser = parse) 

        except:
            return pd.DataFrame([])            
       
        if data.empty:
            return pd.DataFrame([])
        else:
            data.set_index('Year_Month_Day_Hour_Minute_Second',drop=True,inplace=True)
            data.index.names=['time']
            data = data.reindex(col_names, axis=1)
            data.columns = col_names
            return data

    elif dates is not None:
        
        if isDatetimeIterable(dates):
            is_date_list=True
        elif isDatetime(dates):
            dates = [dates]
            is_date_list=False
        else:
            raise Exception('"dates" must be datetime object or array of datetime objects')

        datas = []
        for t in dates:
            st=t.strftime("%Y-%m-%dT%H:%M:%S")
            et=(t+timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")

            try:

                url_string = 'https://smear-backend.rahtiapp.fi/search/timeseries/csv?'\
                            +variable_string\
                            +'&from='+st.replace(':','%3A')\
                            +'&to='+et.replace(':','%3A')\
                            +'&quality='+quality\
                            +'&interval='+averaging\
                            +'&aggregation='+avg_type

                data = pd.read_csv(url_string, parse_dates = [[0,1,2,3,4,5]], date_parser = parse) 

            except:
                continue

            if data.empty:
                continue

            data.set_index('Year_Month_Day_Hour_Minute_Second',drop=True,inplace=True)
            data.index.names=['time']
            data = data.reindex(col_names, axis=1)
            data.columns = col_names
            datas.append(data)

        if ((datas==[]) & (is_date_list==True)):
            return []
        elif ((datas==[]) & (is_date_list==False)):
            return pd.DataFrame([])
        elif ((datas!=[]) & (is_date_list==False)):
            return datas[0]
        else:
            return datas

    else:
        raise Exception('Missing "start" and "end" or "dates"')

def listAllData():
    """ List and describe all variables in the SMEAR database """

    variable_meta_url="https://smear-backend.rahtiapp.fi/search/variable"

    # Variable metadata
    with urllib.request.urlopen(variable_meta_url) as url:
        variablemetadata = json.loads(url.read().decode())

    # Create dataframe with description and variable name
    df = pd.DataFrame(columns=['description','tablevariable','source'])
    for x in variablemetadata:

        df2 = pd.DataFrame([[x['description'],
                           x['tableName']+'.'+x['name'],
                           x['source']]],columns=['description','tablevariable','source'])
        df=df.append(df2,ignore_index=True)

    return df


def getVariableMetadata(variables):
    """ Get variable metadata using Smart SMEAR API 
    
    Parameters
    ----------

    variables: string or array of strings
        name (tablevariable) of a measured quantity in the database

    Returns
    -------

    dict or list of dicts
        metadata for given tablevariables
        
    """

    if isStrIterable(variables):
        col_names = [x for x in variables]
        tablevariables = ['&tablevariable='+x for x in variables]
        variable_string = ''.join(list(tablevariables))
    elif isStr(variables):
        col_names = [variables]
        variable_string = '&tablevariable='+variables
    else:
        raise Exception('"variables" must be string or array of strings')

    meta_url = 'https://smear-backend.rahtiapp.fi/search/variable?'+variable_string

    try:
        with urllib.request.urlopen(meta_url) as url:
            metadata = json.loads(url.read().decode())
    except:
        metadata = []
           
    return metadata

def getDmpsData(station='HYY',start=None,end=None,dates=None,quality='ANY',averaging='1',avg_type='NONE'):
    """ Get DMPS data using Smart SMEAR API 
    
    Parameters
    ----------

    station: string
        "HYY", "KUM" or "VAR"

    dates: datetime object or array of datetime objects
        the days for which data is are downloaded

    start: datetime object
        begin time for data

    end: datetime object
        end time for data
    
    quality: string
        "ANY"
    
    averaging: string
        "1" (no averaging) or "30" (30 minutes) or "60" (60 minutes)
    
    avg_type: str
        "NONE" or "ARITHMETIC" or "MEDIAN" or "MIN" or "MAX"

    Returns
    -------
    
    pandas DataFrame or list of DataFrames
        downloaded data, list is given when dates is array    
     
        index   : time
        columns : bin geometric mean diameters
        values  : dN/dlogDp

    """

    variables = ['d100e1',
    'd112e1',
    'd126e1',
    'd141e1',
    'd158e1',
    'd178e1',
    'd200e1',
    'd224e1',
    'd251e1',
    'd282e1',
    'd316e1',
    'd355e1',
    'd398e1',
    'd447e1',
    'd501e1',
    'd562e1',
    'd631e1',
    'd708e1',
    'd794e1',
    'd891e1',
    'd100e2',
    'd112e2',
    'd126e2',
    'd141e2',
    'd158e2',
    'd178e2',
    'd200e2',
    'd224e2',
    'd251e2',
    'd282e2',
    'd316e2',
    'd355e2',
    'd398e2',
    'd447e2',
    'd501e2',
    'd562e2',
    'd631e2',
    'd708e2',
    'd794e2',
    'd891e2',
    'd100e3',
    'd112e3',
    'd126e3',
    'd141e3',
    'd158e3',
    'd178e3',
    'd200e3',
    'd224e3',
    'd251e3',
    'd282e3',
    'd316e3',
    'd355e3',
    'd398e3',
    'd447e3',
    'd501e3',
    'd562e3',
    'd631e3',
    'd708e3',
    'd794e3',
    'd891e3',
    'd100e4']

    if ((station=='HYY') | (station=='KUM') | (station=='VAR')):
        col_names = [station + '_DMPS.'+x for x in variables]
        tablevariables = ['&tablevariable='+station + '_DMPS.'+x for x in variables]
        x = ''.join(list(tablevariables))
        dp = [float(x[1:])*0.001*1e-9 for x in variables]
    else:
        raise Exception('"station" must be "HYY", "KUM" or "VAR"')

    if ((start is not None) and (end is not None)):
        
        if (isDatetime(start) & isDatetime(end)):
            pass
        else:
            raise Exception('"start" and "end" must to be datetime objects')

        st=start.strftime("%Y-%m-%dT%H:%M:%S")
        et=end.strftime("%Y-%m-%dT%H:%M:%S")

        url_string = 'https://smear-backend.rahtiapp.fi/search/timeseries/csv?'\
                            +x\
                            +'&from='+st.replace(':','%3A')\
                            +'&to='+et.replace(':','%3A')\
                            +'&quality='+quality\
                            +'&interval='+averaging\
                            +'&aggregation='+avg_type

        
        try:
            data = pd.read_csv(url_string, parse_dates = [[0,1,2,3,4,5]], date_parser=parse)
        except:
            return pd.DataFrame([])

        if data.empty:
            return pd.DataFrame([])
        else:
            data.set_index('Year_Month_Day_Hour_Minute_Second',drop=True,inplace=True)
            data.index.names=['time']
            data = data.reindex(col_names, axis=1)
            data.columns = dp
            return data

    elif dates is not None:

        if isDatetimeIterable(dates):
            is_date_list=True
        elif isDatetime(dates):
            dates = [dates]
            is_date_list=False
        else:
            raise Exception('"dates" must be datetime object or array of datetime objects')

        datas = []
        for t in dates:
            st=t.strftime("%Y-%m-%dT%H:%M:%S")
            et=(t+timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")

            html_string = 'https://smear-backend.rahtiapp.fi/search/timeseries/csv?'\
                                +x\
                                +'&from='+st.replace(':','%3A')\
                                +'&to='+et.replace(':','%3A')\
                                +'&quality='+quality\
                                +'&interval='+averaging\
                                +'&aggregation='+avg_type
     
            try:
                data = pd.read_csv(html_string, parse_dates = [[0,1,2,3,4,5]], date_parser=parse)
            except:
                continue

            if data.empty:
                continue

            data.set_index('Year_Month_Day_Hour_Minute_Second',drop=True,inplace=True)
            data.index.names=['time']
            data = data.reindex(col_names, axis=1)
            data.columns = dp
            datas.append(data)

        if ((datas==[]) & (is_date_list==True)):
            return []
        elif ((datas==[]) & (is_date_list==False)):
            return pd.DataFrame([])
        elif ((datas!=[]) & (is_date_list==False)):
            return datas[0]
        else:
            return datas

    else:
        raise Exception('Missing "start" and "end" or "dates"')
