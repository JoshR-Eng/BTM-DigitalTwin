# Enabling CAN on MicroAutoBox III & SCALEXIO

### Requirements
- MAB III or SCALEXIO
- Simulink
- dSPACE Liscenses
    - ConfigurationDesk
    - ControlDesk
    - ConfigurationDesk: Bus Manager
- \*A .dbc file containing the structure of CAN messages in dSPACE applicable format

### Communication Matrix (.dbc file)
CAN communication is enabled via the Bus Manager, this service takes a 'Communication Matrix' as a template and allows assignment of a CAN bus at given ports on a Simulink model. The Communication Matrix must be imported by a user defined .dbc file (or a couple other file types)

An example...
```dbc
VERSION ""

NS_ :
    NS_DESC_
    CM_
    BA_DEF_
    BA_
    VAL_
    CAT_DEF_
    CAT_
    FILTER
    BA_DEF_DEF_
    EV_DATA_
    ENVVAR_DATA_
    SGTYPE_
    SGTYPE_VAL_
    BA_DEF_SGTYPE_
    BA_SGTYPE_
    SIG_TYPE_REF_
    VAL_TABLE_
    SIG_GROUP_
    SIG_VALTYPE_
    SIGTYPE_VALTYPE_
    BO_TX_BU_
    BA_DEF_REL_
    BA_REL_
    BA_DEF_DEF_REL_
    BU_SG_REL_
    BU_EV_REL_
    BU_BO_REL_
    SG_MUL_VAL_

BS_:

BU_: dSPACE Pi

BO_ 500 BTM_Status: 2 dSPACE
 SG_ Temperature : 0|16@1- (0.1, 0) [0|500] "K" Pi

BO_ 501 Control_Command: 2 Pi
 SG_ CoolingPower : 0|16@1- (1,0) [0|5000] "W" dSPACE
```
