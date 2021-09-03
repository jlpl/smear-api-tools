import smear_api_tools as sapi
import pytest
import pandas as pd

# valid date ranges
t1=pd.to_datetime('2010-07-01')
t2=pd.to_datetime('2010-07-05')
tr=pd.date_range(start='2010-07-01',end='2010-07-05')

# impossible but valid date ranges
t1_i=pd.to_datetime('2030-07-01')
t2_i=pd.to_datetime('2030-07-05')
tr_i=pd.date_range(start='2030-07-01',end='2030-07-05')

# valid variable names
var="HYY_META.Pamb0"
var_list=["HYY_META.Pamb0","HYY_META.T04icos"]

# valid but nonexistent variable names
var_i='fake_variable'
var_list_i=['fake_variable1','fake_variable2']

# erroneous values
b=1
b_list=[1,2,3]

# getVariableMetadata

def test_getVariableMetadata_err1():
    with pytest.raises(Exception):
        sapi.getVariableMetadata(b)
def test_getVariableMetadata_err2():
    with pytest.raises(Exception):
        sapi.getVariableMetadata(b_list)
def test_getVariableMetadata_imm1():
    assert sapi.getVariableMetadata(var_i)==[]
def test_getVariableMetadata_imm2():
    assert sapi.getVariableMetadata(var_list_i)==[]
def test_getVariableMetadata_val1():
    assert sapi.getVariableMetadata(var)!=[]
def test_getVariableMetadata_val2():
    assert sapi.getVariableMetadata(var_list)!=[]


# getData

# Erroneous values
def test_getData_err1():
     with pytest.raises(Exception):
        sapi.getData(var)
def test_getData_err2():
     with pytest.raises(Exception):
        sapi.getData(b,dates=t1)
def test_getData_err3():
     with pytest.raises(Exception):
        sapi.getData(b_list,dates=t1)
def test_getData_err4():
     with pytest.raises(Exception):
        sapi.getData(var,dates=b)
def test_getData_err5():
     with pytest.raises(Exception):
        sapi.getData(var,dates=b_list)
def test_getData_err6():
     with pytest.raises(Exception):
        sapi.getData(var,start=b,end=t2)
def test_getData_err7():
     with pytest.raises(Exception):
        sapi.getData(var,start=t1,end=b)

# Valid but impossible values
def test_getData_imm1():
    assert sapi.getData(var,dates=t1_i).empty==True
def test_getData_imm2():
    assert sapi.getData(var,dates=tr_i)==[]
def test_getData_imm3():
    assert sapi.getData(var_i,dates=t1).empty==True
def test_getData_imm4():
    assert sapi.getData(var_list_i,dates=t1).empty==True
def test_getData_imm5():
    assert sapi.getData(var,start=t1_i,end=t2_i).empty==True

# Valid values
def test_getData_val1():
    assert sapi.getData(var,dates=t1).empty==False
def test_getData_val2():
    assert sapi.getData(var,dates=tr)!=[]
def test_getData_val3():
    assert sapi.getData(var,start=t1,end=t2).empty==False
def test_getData_val4():
    assert sapi.getData(var_list,dates=t1).empty==False


# listAllData

def test_listAllData():
    assert sapi.listAllData().empty==False


# getDmpsData

# Erroneous values
def test_getDmpsData_err1():
     with pytest.raises(Exception):
        sapi.getDmpsData()
def test_getDmpsData_err2():
     with pytest.raises(Exception):
        sapi.getDmpsData(station=b)
def test_getDmpsData_err3():
     with pytest.raises(Exception):
        sapi.getDmpsData(dates=b)
def test_getDmpsData_err4():
     with pytest.raises(Exception):
        sapi.getDmpsData(dates=b_list)
def test_getDmpsData_err5():
     with pytest.raises(Exception):
        sapi.getDmpsData(start=b,end=t2)
def test_getDmpsData_err6():
     with pytest.raises(Exception):
        sapi.getDmpsData(start=t1,end=b)

# Valid but impossible values
def test_getDmpsData_imm1():
    assert sapi.getDmpsData(dates=t1_i).empty==True
def test_getDmpsData_imm2():
    assert sapi.getDmpsData(dates=tr_i)==[]
def test_getDmpsData_imm3():
    assert sapi.getDmpsData(start=t1_i,end=t2_i).empty==True

# Valid values
def test_getDmpsData_val1():
    assert sapi.getDmpsData(dates=t1).empty==False
def test_getDmpsData_val2():
    assert sapi.getDmpsData(dates=tr)!=[]
def test_getDmpsData_val3():
    assert sapi.getDmpsData(start=t1,end=t2).empty==False

