import pandas as pd
import numpy as np
import urllib.request, json
from collections.abc import Iterable
from datetime import datetime, timedelta

__pdoc__ = {
    'isStr': False,
    'isStrIterable': False,
    'isDatetime': False,
    'isDatetimeIterable': False,
    'isNumeric': False,
    'isNumericIterable': False,
    'parse': False,
}


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

def isNumeric(obj):
    try:
        float(obj)
        return True
    except:
        return False

def isNumericIterable(obj):
    result=False
    if isinstance(obj,Iterable):
        if all(isNumeric(elem) for elem in obj):
            result=True
    return result

def parse(year, month, day, hour, minute, second):
    return year+ '-' +month+ '-' +day+ ' ' +hour+ ':' +minute+ ':' +second

def getData(variables,dates=None,start=None,end=None,quality='ANY',averaging='1',avg_type='NONE'):
    """ Get timeseries of variables using Smart SMEAR API 
    
    Parameters
    ----------

    variables : string or array of strings
        name of a measured quantity in the database (tablevariable)

    dates : datetime object or string or array of datetime objects or strings
        the date(s) for which measurements are downloaded

    start : datetime object or string
        begin of measurement

    end : datetime object or string
        end of measurement
    
    quality : string
        `"ANY"`
    
    averaging : string
        `"1"` (no averaging), `"30"` (30 min) or `"60"` (60 min)
    
    avg_type : string
        `"NONE"`, `"ARITHMETIC"`, `"MEDIAN"`, `"MIN"` or `"MAX"`

    Returns
    -------
    
    pandas DataFrame or list of DataFrames
        downloaded data, list is given for array of date objects

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

    if ((start is not None) and (end is not None) and (dates is not None)):
        raise Exception('Give either "start" and "end" or "dates"')
    
    if ((start is not None) and (end is not None)):
        
        if (isDatetime(start) & isDatetime(end)):
            pass
        elif (isStr(start) & isStr(end)):
            start=pd.to_datetime(start)
            end=pd.to_datetime(end)    
        else:
            raise Exception('"start" and "end" must be datetime objects or strings')

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
        elif isStrIterable(dates):
            dates = pd.to_datetime(dates)
            is_date_list=True
        elif isStr(dates):
            dates = [pd.to_datetime(dates)]
            is_date_list=False
        else:
            raise Exception('"dates" must be datetime object or string or array of datetime objects or strings')

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
                datas.append(pd.DataFrame([]))
                continue

            if data.empty:
                datas.append(pd.DataFrame([]))
                continue

            data.set_index('Year_Month_Day_Hour_Minute_Second',drop=True,inplace=True)
            data.index.names=['time']
            data = data.reindex(col_names, axis=1)
            data.columns = col_names
            datas.append(data)

        if (is_date_list==False):
            return datas[0]
        else:
            return datas

    else:
        raise Exception('Missing "start" and "end" or "dates"')

def listAllData(search_term=None,verbose=False):
    """ List and describe variables in the SMEAR database 

    Parameters
    ----------
    
    search_term : string
        search term for searching the database, if `None`
        all results are returned.

    verbose : boolean
        verbose or not verbose output

    Returns
    -------

    pandas DataFrame

    """

    # Find variables that contain the search_term in their title
    if search_term is not None:
        if isStr(search_term):
            pass
        else:
            raise Exception('"search_term" should be a string')

    if isinstance(verbose,bool):
        pass
    else:
        raise Exception('"verbose" should be True or False')

    variable_meta_url="https://smear-backend.rahtiapp.fi/search/variable"

    nums = list("0123456789x") 
    numssub = list("₀₁₂₃₄₅₆₇₈₉ₓ")

    # Variable metadata
    with urllib.request.urlopen(variable_meta_url) as url:
        variablemetadata = json.loads(url.read().decode())

    # Create dataframe with description and variable name
    df_verb = pd.DataFrame(columns=['title','tablevariable','description','source'])
    df_short = pd.DataFrame(columns=['title','tablevariable'])

    for x in variablemetadata:

        if verbose:

            title = str(x['title'])
            tablevariable = x['tableName']+'.'+x['name']
            description = str(x['description'])
            source = str(x['source'])

            # Replace subscripted numbers with normal numbers in the names
            if isStr(title):
                for i in range(len(nums)):
                    title = title.replace(numssub[i], nums[i])
    
            if isStr(description):
                for i in range(len(nums)):
                    description = description.replace(numssub[i], nums[i])
    
            if isStr(source):
                for i in range(len(nums)):
                    source = source.replace(numssub[i], nums[i])
    
            df2 = pd.DataFrame([[
                title, 
                tablevariable,
                description,
                source]],
                columns=['title','tablevariable','description','source'])

            df_verb = df_verb.append(df2,ignore_index=True)
 
        else:

            title = str(x['title'])
            tablevariable = x['tableName']+'.'+x['name']

            # Replace subscripted numbers with normal numbers in the names
            if isStr(title):
                for i in range(len(nums)):
                    title = title.replace(numssub[i], nums[i])
    
            df2 = pd.DataFrame([[
                title, 
                tablevariable]],
                columns=['title','tablevariable'])

            df_short = df_short.append(df2,ignore_index=True)

    if verbose:
        df = df_verb
    else:
        df = df_short    

    # Find variables that contain the search_term in their title
    if search_term is not None:
        df = df.loc[df['title'].str.lower().str.find(search_term.lower())!=-1.0,:]

    return df

def getVariableMetadata(variables):
    """ Get variable metadata using Smart SMEAR API 
    
    Parameters
    ----------

    variables : string or array of strings
        name (tablevariable) of a measured quantity in the database

    Returns
    -------

    dictionary or list of dictionaries
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

    station : string
        `"HYY"`, `"KUM"` or `"VAR"`

    dates : datetime object or string or array of datetime objects or strings
        the days for which data is are downloaded

    start : datetime object or string
        begin time for data

    end : datetime object or string
        end time for data
    
    quality : string
        `"ANY"`
    
    averaging : string
        `"1"` (no averaging), `"30"` (30 minutes) or `"60"` (60 minutes)
    
    avg_type : str
        `"NONE"`, `"ARITHMETIC"`, `"MEDIAN"`, `"MIN"` or `"MAX"`

    Returns
    -------
    
    pandas DataFrame or list of DataFrames
        downloaded data, list is given when dates is array 
        
        index = time (utc+2)  
        columns = bin geometric mean diameters (m)  
        values = dN/dlogDp (cm-3)

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
        elif (isStr(start) & isStr(end)):
            start=pd.to_datetime(start)
            end=pd.to_datetime(end)    
        else:
            raise Exception('"start" and "end" must be datetime objects or strings')

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
        elif isStrIterable(dates):
            dates = pd.to_datetime(dates)
            is_date_list=True
        elif isStr(dates):
            dates = [pd.to_datetime(dates)]
            is_date_list=False
        else:
            raise Exception('"dates" must be datetime object or string or array of datetime objects or strings')

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
                datas.append(pd.DataFrame([]))
                continue

            if data.empty:
                datas.append(pd.DataFrame([]))
                continue

            data.set_index('Year_Month_Day_Hour_Minute_Second',drop=True,inplace=True)
            data.index.names=['time']
            data = data.reindex(col_names, axis=1)
            data.columns = dp
            datas.append(data)

        if (is_date_list==False):
            return datas[0]
        else:
            return datas

    else:
        raise Exception('Missing "start" and "end" or "dates"')
