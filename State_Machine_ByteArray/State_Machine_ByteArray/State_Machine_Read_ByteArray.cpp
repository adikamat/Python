#include "pch.h"
#include "DataTypes.h"

Module_t Module[1];
//HEADConditionGrp_t myCG1;

uint32_t parse_condition_packet(ParamStructure_t *param, char *pDestByteArray)
{
	char *memPtr = pDestByteArray;
	uint32_t bytes_read;

	// Read bytes count 
	uint32_t bytes_count;
	memcpy(&bytes_count, memPtr, sizeof(uint32_t));
	std::cout << "Cond bytes count = " << bytes_count << std::endl;
	memPtr = memPtr + sizeof(uint32_t);	

	// Copy Condition from memory
	memcpy(param, memPtr, sizeof(ParamStructure_t));
	std::cout << "Param Data: " << param->ParamMainType << param->ParamMainValueType << param->ParamOutType << param->ParameterMode << std::endl;

	// Calculate bytes written to memory
	bytes_read = sizeof(uint32_t) + bytes_count;

	return bytes_read;
}

void read_DGSM_byte_mem()
{
	char *baseAddr = StateMachineByteArray;
	uint32_t DGSM_bytes_count;
	uint32_t module_index = 0, state_index = 0, trans_index = 0, cg_index = 0, cond_index = 0;

	// Read size of State Machine data
	memcpy(&DGSM_bytes_count, baseAddr, sizeof(uint32_t));
	std::cout << "DGSM bytes count = " << DGSM_bytes_count << std::endl;

	char *module_curr_ptr;
	char *state_curr_ptr;
	char *trans_curr_ptr;
	char *cg_curr_ptr;
	char *cond_curr_ptr;

	module_curr_ptr = baseAddr + sizeof(uint32_t);
	// Parse Module Packets
	while (module_curr_ptr < (baseAddr + DGSM_bytes_count))
	{
		// Read a single module packet
		uint32_t module_bytes_count;
		memcpy(&module_bytes_count, module_curr_ptr, sizeof(uint32_t));
		std::cout << "Module " << (module_index + 1) << " bytes count = " << module_bytes_count << std::endl;

		// Parse State Packets
		state_curr_ptr = module_curr_ptr + sizeof(uint32_t);
		while (state_curr_ptr < (module_curr_ptr + module_bytes_count))
		{
			// Read a single state packet
			uint32_t state_bytes_count;
			memcpy(&state_bytes_count, state_curr_ptr, sizeof(uint32_t));
			std::cout << "State " << (state_index + 1) << " bytes count = " << state_bytes_count << std::endl;

			// Parse Transition Packets
			trans_curr_ptr = state_curr_ptr + sizeof(uint32_t);
			while (trans_curr_ptr < (state_curr_ptr + state_bytes_count))
			{
				// Read a single transition packet
				uint32_t trans_bytes_count;
				memcpy(&trans_bytes_count, trans_curr_ptr, sizeof(uint32_t));
				std::cout << "Transition " << (trans_index + 1) << " bytes count = " << trans_bytes_count << std::endl;

				// Parse CG packets
				cg_curr_ptr = trans_curr_ptr + sizeof(uint32_t);
				while (cg_curr_ptr < (trans_curr_ptr + trans_bytes_count))
				{
					// Read a single CG packet
					uint32_t cg_bytes_count;
					memcpy(&cg_bytes_count, cg_curr_ptr, sizeof(uint32_t));
					std::cout << "CG " << (cg_index + 1) << " bytes count = " << cg_bytes_count << std::endl;

					// Parse condition packets
					cond_curr_ptr = cg_curr_ptr + sizeof(uint32_t);
					while (cond_curr_ptr < (cg_curr_ptr + cg_bytes_count))
					{
						HEADParamStructure_t param;
						// Read a single condition packet
						uint32_t cond_bytes_count = parse_condition_packet(&param, cond_curr_ptr);

						// Move to next condition packet
						cond_curr_ptr += cond_bytes_count;
					}

					// Move to next CG packet
					cg_curr_ptr += cg_bytes_count + sizeof(uint32_t);
					++cg_index;
				}

				// Move to next transition
				trans_curr_ptr += trans_bytes_count + sizeof(uint32_t);
				++trans_index;
			}

			// Move to next state
			state_curr_ptr += state_bytes_count + sizeof(uint32_t);
			++state_index;
		}

		// Move to next module
		module_curr_ptr += module_bytes_count + sizeof(uint32_t);
		++module_index;
	}
}