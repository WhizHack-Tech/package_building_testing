#  ==================================================================================================
#  File Name: auto_pass_generator.py
#  Description: This file contains code to generate random string sequence.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

import random
import string
	
def rand_pass(size):
	generate_pass = ''.join([random.choice( string.ascii_uppercase +
											string.ascii_lowercase +
											string.digits)
											for n in range(size)])
							
	return generate_pass
	
# Driver Code
# password = rand_pass(10)
# print(password)
