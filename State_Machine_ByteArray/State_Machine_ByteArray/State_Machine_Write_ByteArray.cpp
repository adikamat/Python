// State_Machine_ByteArray.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include "pch.h"
#include <vector>
#include "DataTypes.h"

char StateMachineByteArray[FLASH_MEM_SIZE];

//uint32_t add_packet(void *data, char *pDestByteArray)
//{
//	// Read first 4 bytes to get the size of packet
//	uint32_t bytes_count;
//	memcpy(&bytes_count, data, sizeof(uint32_t));
//}

uint32_t write_transition_packet(std::vector<ParamStructure_t> param_list, char *pDestByteArray)
{
	char *memPtr = pDestByteArray;
	uint32_t bytes_written = 0;

	// Add bytes count to memory
	uint32_t bytes_count = sizeof(ParamStructure_t);
	memcpy(memPtr, &bytes_count, sizeof(uint32_t));
	memPtr += sizeof(uint32_t);

	// Copy Conditions to memory
	for (auto param : param_list)
	{
		memcpy(memPtr, &param, sizeof(ParamStructure_t));
		memPtr += sizeof(ParamStructure_t);
		bytes_written += sizeof(ParamStructure_t);
	}

	// Add bytes count to memory
	memcpy(pDestByteArray, &bytes_written, sizeof(uint32_t));

	// Calculate total bytes written to memory including size 
	bytes_written += sizeof(uint32_t);

	return bytes_written;
}

uint32_t write_condition_group_packet(std::vector<ParamStructure_t> param_list, char *pDestByteArray)
{
	char *memPtr = pDestByteArray;
	uint32_t bytes_written = 0;

	// Add bytes count to memory
	uint32_t bytes_count = sizeof(ParamStructure_t);
	memcpy(memPtr, &bytes_count, sizeof(uint32_t));
	memPtr += sizeof(uint32_t);

	// Copy Conditions to memory
	for (auto param : param_list)
	{
		memcpy(memPtr, &param, sizeof(ParamStructure_t));
		memPtr += sizeof(ParamStructure_t);
		bytes_written += sizeof(ParamStructure_t);
	}
	
	// Add bytes count to memory
	memcpy(pDestByteArray, &bytes_written, sizeof(uint32_t));

	// Calculate total bytes written to memory including size 
	bytes_written += sizeof(uint32_t);

	return bytes_written;
}

uint32_t write_condition_packet(ParamStructure_t *param, char *pDestByteArray)
{
	char *memPtr = pDestByteArray;
	uint32_t bytes_written;
	
	// Add bytes count to memory
	uint32_t bytes_count = sizeof(ParamStructure_t);
	memcpy(memPtr, &bytes_count, sizeof(uint32_t));
	memPtr += sizeof(uint32_t);

	// Copy Condition to memory
	memcpy(memPtr, param, sizeof(ParamStructure_t));

	// Calculate bytes written to memory
	bytes_written = sizeof(uint32_t) + sizeof(ParamStructure_t);

	return bytes_written;
}

void write_DGSM_byte_mem()
{
	uint32_t NUM_MODULES = 1;
	uint32_t NUM_STATES = 2;
	uint32_t NUM_TRANS = 2;
	uint32_t NUM_CG = 1;
	uint32_t NUM_CONDS = 2;
	uint32_t module_count, state_count, trans_count, cg_count, cond_count;
	uint32_t bytes_written, cond_bytes_count, cg_byte_count, trans_byte_count, state_byte_count, module_byte_count;

	ParamStructure_t param1 = { 1, 1, 0, 25, 0, 3 };
	ParamStructure_t param2 = { 1, 1, 0, 15, 0, 7 };

	ParamStructure_t *param_array[] = {&param1, &param2};

	char *module_size_ptr;
	char *state_size_ptr;
	char *trans_size_ptr;
	char *cg_size_ptr;
	char *cond_size_ptr;

	char *curr_mem_ptr = StateMachineByteArray + sizeof(uint32_t);
	module_byte_count = 0;
	for (module_count = 0; module_count < NUM_MODULES; ++module_count)
	{
		module_size_ptr = curr_mem_ptr;
		curr_mem_ptr += sizeof(uint32_t);
		state_byte_count = 0; 

		for (state_count = 0; state_count < NUM_STATES; ++state_count)
		{
			// Store pointer to fill state bytes size
			state_size_ptr = curr_mem_ptr;
			curr_mem_ptr += sizeof(uint32_t);
			trans_byte_count = 0;

			// Fill Transition data to memory
			for (trans_count = 0; trans_count < NUM_TRANS; ++trans_count)
			{
				// Store pointer to fill transition bytes size
				trans_size_ptr = curr_mem_ptr;
				curr_mem_ptr += sizeof(uint32_t);
				cg_byte_count = 0;

				// Fill CG data to memory
				for (cg_count = 0; cg_count < NUM_CG; ++cg_count)
				{
					// Store pointer to fill CG bytes size
					cg_size_ptr = curr_mem_ptr;
					curr_mem_ptr += sizeof(uint32_t);
					cond_bytes_count = 0;
					
					// Fill conditions data to buffer
					for (cond_count = 0; cond_count < NUM_CONDS; ++cond_count)
					{
						bytes_written = write_condition_packet(param_array[cond_count], curr_mem_ptr);
						curr_mem_ptr += bytes_written;
						cond_bytes_count += bytes_written;
					}
					
					// Fill the size of CG packet
					memcpy(cg_size_ptr, &cond_bytes_count, sizeof(uint32_t));
					
					// CG Bytes Count = Num of Cond bytes + 4 bytes for writing the size of CG packet
					cg_byte_count += cond_bytes_count + sizeof(uint32_t);
				}

				// Fill the size of transition packet
				memcpy(trans_size_ptr, &cg_byte_count, sizeof(uint32_t));

				// Trans Bytes Count = Size of CG Bytes count + 4 bytes for size
				trans_byte_count += cg_byte_count + sizeof(uint32_t);
			}

			// Fill the size of state packet
			memcpy(state_size_ptr, &trans_byte_count, sizeof(uint32_t));

			// Trans Bytes Count = Size of CG Bytes count + 4 bytes for size
			state_byte_count += trans_byte_count + sizeof(uint32_t);
		}

		// Fill the size of module packet
		memcpy(module_size_ptr, &state_byte_count, sizeof(uint32_t));

		// Trans Bytes Count = Size of CG Bytes count + 4 bytes for size
		module_byte_count += state_byte_count + sizeof(uint32_t);
	}
	// Fill the size of module packet
	memcpy(StateMachineByteArray, &module_byte_count, sizeof(uint32_t));

    std::cout << "Hello World!\n"; 
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
