#pragma once

#include <stdint.h>
#include <iostream>

#define FLASH_MEM_SIZE (500 * 1024 * 1024) // 500 MB
extern char StateMachineByteArray[FLASH_MEM_SIZE];

typedef struct ParamStructure {
	/*generic parameter information*/
	uint32_t   ParamMainType : 2;          /*!< 2 (Offset 0+0) bits for main type (none, scalar, table, 3dtable) @values: eHEADParamMainValueType_t @unit:none|scalar|table*/
	uint32_t   ParamMainValueType : 1;          /*!< 1 (Offset 0+2) bit  for (value, factor) - defines the type of the parameter @unit:val|fac|bool*/
	uint32_t   ParamOperator : 1;          /*!< 1 (Offset 0+3) bit for the operator (</>) @unit:less|greater*/
	/*head specific parameter information*/
	uint32_t   ParamOutType : 7;          /*!< 7 (Offset 0+4) bits for OutType (128 different types like TTC, ModuleConditionEgoVel...) */
	uint32_t   Padding1 : 6;          /*!< 6 (Offset 0+11) bits */
	uint32_t   ParameterMode : 4;          /*!< 4 (Offset 0+17) bits - one BIT for every driver preference setting (early, middle, late, acc) @unit:Early|Middle|Late|ACC*/
	uint32_t   ParameterOrGroup : 3;          /*!< 3 (Offset 0+21) bits - or group - OR(AND(all Group 0 parameters), AND(all Group 1 parameters),...),@unit:0-8*/
	uint32_t   ParamObjectClass : 4;          /*!< 4 (Offset 0+24) bits for object class (Veh, Ped, Cycl, Obst) */
	uint32_t   ParamDynProp : 2;          /*!< 2 (Offset 0+28) bits for object dynamic property (Moving/Stat) */
	uint32_t   Padding2 : 2;          /*!< 2 (Offset 0+30) bits */
	uint32_t   ParameterHypSubType : 32;         /*!< 32(Offset 1+0)  bits - one BIT for every Hypothesis (HEADParameterHypothesisBit(xxx)|...|...) @unit:hyptype*/
	uint32_t   ParamSensorSource : 8;          /*!< 8 (Offset 2+0)  bits -  8 bits for each sensor type */
	uint32_t   ParamObjMovDir : 3;          /*!< 3 (Offset 2+8)  bits for object movement direction @unit DoT|Crossing|Oncoming|None */
	uint32_t   Padding3 : 21;         /*!< 21(Offset 2+11) bits */
}HEADParamStructure_t;


typedef struct Module
{
	/*!@publicsection*/
	uint8_t      strModuleName[24u + 1u];   /*!< module name*/
	uint8_t      uiNumOrGroups;                              /*!< defines the number of orGroups for this module @range @ref HEAD_MAX_OR_GROUPS*/
	uint16_t     uiHypInOrGroup[8];         /*!< orGroup array with corresponding hypotheses*/
	uint8_t      eSMState;                                   /*!< global state machine state @values @ref eHEADSMState_t*/
	uint8_t      eSMLastState;                               /*!< global state machine last state @values @ref eHEADSMState_t*/
	uint8_t      eQoS;                                       /*!< defines the states of the QoS for a module @values @ref eHEADModuleQoS_t*/
	uint8_t      eReportedError;                             /*!< defines the reported error for a module @values @ref eHEADModuleRepError_t*/
	float        fStateTimer[4];               /*!< counts the seconds how long the module is in the current state*/
	float        fNotInStateTimer[4];          /*!< counts the seconds how long the module is not in the current state*/
	/*!@privatesection*/
	const void   *pInternal;                  /*!< pointer to internal state information @ ref HEADModuleInternalInterface_t*/
	const void   *pOutput;                    /*!< pointer to output interface @ref HEADModuleOutputInterface_t*/
	const void                           *pOutputParams;              /*!< pointer to a output parameter structure (is used by the function defined in pOutput)*/
}Module_t; /* typedef already forward declared */
//


void write_DGSM_byte_mem();
void read_DGSM_byte_mem();
