import smear_api_tools as sapi
import pytest
import pandas as pd
import numpy as np

# valid dates
dt1_valid=pd.to_datetime('2010-07-01')
dt2_valid=pd.to_datetime('2010-07-05')
dtstr1_valid='2010-07-01'
dtstr2_valid='2010-07-05'
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

# Station names
station_valid='KUM'
station_bad='ASD'



# getVariableMetadata

@pytest.mark.parametrize("arg",[var_bad,var_list_bad])
def test_getVariableMetadata_bad(arg):
    with pytest.raises(Exception):
        sapi.getVariableMetadata(arg)

@pytest.mark.parametrize("arg",[
    (var_impossible),
    (var_list_impossible)
    ])      
def test_getVariableMetadata_empty(arg):
    assert len(sapi.getVariableMetadata(arg))==0

@pytest.mark.parametrize("arg",[
    (var_valid),
    (var_list_valid)
    ])      
def test_getVariableMetadata_valid(arg):
    assert len(sapi.getVariableMetadata(arg))>0


# getData

# Bad inputs
@pytest.mark.parametrize("arg1,arg2,arg3,arg4,arg5",[
    (var_valid,None,None,None,Exception),         
    (var_bad,dt1_valid,None,None,Exception),      
    (var_list_bad,dt1_valid,None,None,Exception),  
    (var_valid,dt_bad,None,None,Exception),        
    (var_valid,dtstr_bad_value,None,None,ValueError),           
    (var_valid,None,dt_bad,dt2_valid,Exception),   
    (var_valid,None,dtstr_bad_value,dtstr2_valid,ValueError) 
    ])      
def test_getData_bad(arg1,arg2,arg3,arg4,arg5):
    with pytest.raises(arg5):
        sapi.getData(arg1,dates=arg2,start=arg3,end=arg4)
   
# Empty output
@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    (var_valid,dt1_impossible,None,None),          
    (var_valid,dtstr1_impossible,None,None),    
    (var_impossible,dt1_valid,None,None),         
    (var_list_impossible,dt1_valid,None,None),    
    (var_valid,None,dtstr1_impossible,dtstr2_impossible),      
    (var_valid,None,dt1_impossible,dt2_impossible)   
    ])      
def test_getData_empty(arg1,arg2,arg3,arg4):
    assert sapi.getData(arg1,dates=arg2,start=arg3,end=arg4).empty==True

# List of empty outputs
@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    (var_valid,dt_range_impossible,None,None),
    (var_valid,dtstr_range_impossible,None,None)
    ])      
def test_getData_list_empty(arg1,arg2,arg3,arg4):
    df=sapi.getData(arg1,dates=arg2,start=arg3,end=arg4)
    assert all([x.empty for x in df])==True

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
    (station_valid,None,None,None),
    (station_bad,dt1_valid,None,None),
    (station_valid,dt_bad,None,None),
    (station_valid,dtstr_bad_value,None,None),
    (station_valid,None,dt_bad,dt2_valid),
    (station_valid,None,dtstr_bad_value,dtstr2_valid)
    ])
def test_getDmpsData_bad(arg1,arg2,arg3,arg4):
    with pytest.raises(Exception):
        sapi.getDmpsData(station=arg1,dates=arg2,start=arg3,end=arg4)
   
@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    (station_valid,dt1_impossible,None,None),
    (station_valid,None,dt1_impossible,dt2_impossible),
    (station_valid,None,dtstr1_impossible,dtstr2_impossible)
    ])
def test_getDmpsData_empty(arg1,arg2,arg3,arg4):
    assert sapi.getDmpsData(station=arg1,dates=arg2,start=arg3,end=arg4).empty==True
 
@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    (station_valid,dt_range_impossible,None,None),
    (station_valid,dtstr_range_impossible,None,None)
    ])
def test_getDmpsData_list_empty(arg1,arg2,arg3,arg4):
    df=sapi.getDmpsData(station=arg1,dates=arg2,start=arg3,end=arg4)
    assert all([x.empty for x in df])==True

@pytest.mark.parametrize("arg1,arg2,arg3,arg4",[
    (station_valid,dt1_valid,None,None),
    (station_valid,dt_range_valid,None,None),
    (station_valid,dtstr_range_valid,None,None),
    (station_valid,None,dt1_valid,dt2_valid),
    (station_valid,None,dtstr1_valid,dtstr2_valid)
    ])
def test_getDmpsData_valid(arg1,arg2,arg3,arg4):
    assert len(sapi.getDmpsData(station=arg1,dates=arg2,start=arg3,end=arg4))>0
