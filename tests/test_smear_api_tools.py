import smear_api_tools as sapi
import pytest
import pandas as pd
import numpy as np

# valid dates
dt1_valid=pd.to_datetime('2010-07-01')
dt2_valid=pd.to_datetime('2010-07-05')
dtstr1_valid='2010-07-01'
dtstr2_valid='2010-07-10'
dt_range_valid=pd.date_range(start='2010-07-01',end='2010-07-05')
dtstr_range_valid=["2010-07-01","2010-07-02","2010-07-03"]

# impossible but valid dates
dt1_impossible=pd.to_datetime('2030-07-01')
dt2_impossible=pd.to_datetime('2030-07-05')
dtstr1_impossible='2030-07-01'
dtstr2_impossible='2030-07-05'
dt_range_impossible=pd.date_range(start='2030-07-01',end='2030-07-05')
dtstr_range_impossible=["2030-07-01","2030-07-02","2030-07-03"]

#bad dates
dt_bad = 123
dtstr_bad_parse="asd"
dtstr_bad_value="111"

# variable names
var_valid="HYY_META.Pamb0"
var_list_valid=["HYY_META.Pamb0","HYY_META.T04icos"]
var_impossible='fake_variable'
var_list_impossible=['fake_variable1','fake_variable2']
var_bad=1
var_list_bad=[1,2,3]

# search terms
search_term_valid = "pressure"
search_term_impossible = "augndeytfgkd"
search_term_bad = 123

# diameter values
d1_valid=3e-9
d2_valid=100e-9
d1_bad=[1,2,3]
d2_bad="asd"
d1_outside=1e-9
d2_outside=2000e-9
d3_outside=3000e-9



# getVariableMetadata

@pytest.mark.parametrize("arg",[var_bad,var_list_bad])
def test_getVariableMetadata1(arg):
    with pytest.raises(Exception):
        sapi.getVariableMetadata(arg)

@pytest.mark.parametrize("arg,output",[
    (var_impossible,[]),
    (var_list_impossible,[])])      
def test_getVariableMetadata2(arg,output):
    assert len(sapi.getVariableMetadata(arg))==output

@pytest.mark.parametrize("arg,output",[
    (var_valid,[]),
    (var_list_valid,[])])      
def test_getVariableMetadata2(arg,output):
    assert len(sapi.getVariableMetadata(arg))!=output


# getData

# Bad inputs
@pytest.mark.parametrize("arg1,arg2,arg3,arg4,arg5",[
    (var_valid,None,None,None,Exception),         # no dates
    (var_bad,dt1_valid,None,None,Exception),       # bad var
    (var_list_bad,dt1_valid,None,None,Exception),  # bad var list
    (var_valid,dt_bad,None,None,Exception),        # bad date (dt)
    (var_valid,dtstr_bad_value,None,None,ValueError),    # bad date (dtstr)       
    (var_valid,None,dt_bad,dt2_valid,Exception),   # bad start (dt)
    (var_valid,None,dtstr_bad_value,dtstr2_valid,ValueError) # bad start (dtstr)
    ])      
def test_getData_bad(arg1,arg2,arg3,arg4,arg5):
    with pytest.raises(arg5):
        sapi.getData(arg1,dates=arg2,start=arg3,end=arg4)
   
# Empty output
@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    (var_valid,dt1_impossible,None,None),          # impossible date
    (var_valid,dt_range_impossible,None,None),     # impossible dates
    (var_valid,dtstr1_impossible,None,None),          # impossible datestr 
    (var_valid,dtstr_range_impossible,None,None),     # impossible datestrs
    (var_impossible,dt1_valid,None,None),          # impossible var
    (var_list_impossible,dt1_valid,None,None),     # impossible var list
    (var_valid,None,dtstr1_impossible,dtstr2_impossible), # impossible start and end (dtstr)     
    (var_valid,None,dt1_impossible,dt2_impossible)   # impossible start and end (dt)
    ])      
def test_getData_impossible(arg1,arg2,arg3,arg4):
    assert len(sapi.getData(arg1,dates=arg2,start=arg3,end=arg4))==0

# Nonempty output
@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    (var_valid,dt1_valid,None,None),         
    (var_valid,dt_range_valid,None,None),    
    (var_valid,dtstr1_valid,None,None),      
    (var_valid,dtstr_range_valid,None,None), 
    (var_list_valid,dt1_valid,None,None),           
    (var_valid,None,dtstr1_valid,dtstr2_valid),    
    (var_valid,None,dt1_valid,dt2_valid)       
    ])      
def test_getData_valid(arg1,arg2,arg3,arg4):
    assert len(sapi.getData(arg1,dates=arg2,start=arg3,end=arg4))>0


# listAllData

@pytest.mark.parametrize("arg1,arg2",[
    (None,False),
    (search_term_valid,False),
    (search_term_valid,True)])
def test_listAllData_valid(arg1,arg2):   
    assert len(sapi.listAllData(search_term=arg1,verbose=arg2))>0

@pytest.mark.parametrize("arg1,arg2",[
    (search_term_impossible,False)])
def test_listAllData_empty(arg1,arg2):   
    assert len(sapi.listAllData(search_term=arg1,verbose=arg2))==0

@pytest.mark.parametrize("arg1,arg2,arg3",[
    (search_term_bad,False,Exception),
    (search_term_valid,123,Exception)])
def test_listAllData_bad(arg1,arg2,arg3):   
    with pytest.raises(arg3):
        sapi.listAllData(search_term=arg1,verbose=arg2)


## getDmpsData

@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    ('KUM',None,None,None),
    ('ASD',dt1_valid,None,None),
    ('KUM',dt_bad,None,None),
    ('KUM',dtstr_bad_value,None,None),
    ('KUM',None,dt_bad,dt2_valid),
    ('KUM',None,dtstr_bad_value,dtstr2_valid)
    ])
def test_getDmpsData_bad(arg1,arg2,arg3,arg4):
    with pytest.raises(Exception):
        sapi.getDmpsData(station=arg1,dates=arg2,start=arg3,end=arg4)
   

@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    ('KUM',dt1_impossible,None,None),
    ('KUM',dt_range_impossible,None,None),
    ('KUM',dtstr_range_impossible,None,None),
    ('KUM',None,dt1_impossible,dt2_impossible),
    ('KUM',None,dtstr1_impossible,dtstr2_impossible)
    ])
def test_getDmpsData_empty(arg1,arg2,arg3,arg4):
    assert len(sapi.getDmpsData(station=arg1,dates=arg2,start=arg3,end=arg4))==0
 
@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    ('HYY',dt1_valid,None,None),
    ('HYY',dt_range_valid,None,None),
    ('HYY',dtstr_range_valid,None,None),
    ('HYY',None,dt1_valid,dt2_valid),
    ('HYY',None,dtstr1_valid,dtstr2_valid)
    ])
def test_getDmpsData_valid(arg1,arg2,arg3,arg4):
    assert len(sapi.getDmpsData(station=arg1,dates=arg2,start=arg3,end=arg4))>0
 



## getConcData

@pytest.mark.parametrize("arg1,arg2,arg3,arg4,arg5,arg6",[
    ('KUM',d1_valid,d2_valid,None,None,None),
    ('ASD',d1_valid,d2_valid,dt1_valid,None,None),
    ('KUM',d1_valid,d2_valid,dt_bad,None,None),
    ('KUM',d1_valid,d2_valid,dtstr_bad_value,None,None),
    ('KUM',d1_valid,d2_valid,None,dt_bad,dt2_valid),
    ('KUM',d1_valid,d2_valid,None,dtstr_bad_value,dtstr2_valid),
    ('KUM',d1_bad,d2_valid,dt1_valid,None,None),
    ('KUM',d1_valid,d2_bad,dt1_valid,None,None),
    ('KUM',d2_valid,d1_valid,dt1_valid,None,None)
])
def test_getConcData_bad(arg1,arg2,arg3,arg4,arg5,arg6):
    with pytest.raises(Exception):
        sapi.getConcData(station=arg1,dp1=arg2,dp2=arg3,dates=arg4,start=arg5,end=arg6)
   
@pytest.mark.parametrize("arg1,arg2,arg3,arg4,arg5,arg6",[
    ('KUM',d1_valid,d2_valid,dt1_impossible,None,None),
    ('KUM',d1_valid,d2_valid,dt_range_impossible,None,None),
    ('KUM',d1_valid,d2_valid,dtstr_range_impossible,None,None),
    ('KUM',d1_valid,d2_valid,None,dt1_impossible,dt2_impossible),
    ('KUM',d1_valid,d2_valid,None,dtstr1_impossible,dtstr2_impossible)
])
def test_getConcData_empty(arg1,arg2,arg3,arg4,arg5,arg6):
    assert len(sapi.getConcData(station=arg1,dp1=arg2,dp2=arg3,dates=arg4,start=arg5,end=arg6))==0
 
@pytest.mark.parametrize("arg1,arg2,arg3,arg4,arg5,arg6",[
    ('KUM',d1_valid,d2_valid,dt1_valid,None,None),
    ('KUM',d1_valid,d2_valid,dt_range_valid,None,None),
    ('KUM',d1_valid,d2_valid,dtstr_range_valid,None,None),
    ('KUM',d1_valid,d2_valid,None,dt1_valid,dt2_valid),
    ('KUM',d1_valid,d2_valid,None,dtstr1_valid,dtstr2_valid)
    ])
def test_getConcData_valid(arg1,arg2,arg3,arg4,arg5,arg6):
    assert len(sapi.getConcData(station=arg1,dp1=arg2,dp2=arg3,dates=arg4,start=arg5,end=arg6))>0
    assert np.all(np.isnan(sapi.getConcData(station=arg1,dp1=arg2,dp2=arg3,dates=arg4,start=arg5,end=arg6)))==False

@pytest.mark.parametrize("arg1,arg2,arg3,arg4,arg5,arg6",[
    ('KUM',d1_outside,d1_valid,dt1_valid,None,None),
    ('KUM',d2_outside,d3_outside,dt1_valid,None,None)
    ])
def test_getConcData_nans(arg1,arg2,arg3,arg4,arg5,arg6):
    assert np.all(np.isnan(sapi.getConcData(station=arg1,dp1=arg2,dp2=arg3,dates=arg4,start=arg5,end=arg6)))==True
