// =============================================================================================
//  File Name: Can.js
//  Description: Details of the canUtility component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Imports createContext function
import { createContext } from 'react'

// ** Imports createContextualCan function
import { createContextualCan } from '@casl/react'

// ** Create Context
export const AbilityContext = createContext()

// ** Init Can Context
export const Can = createContextualCan(AbilityContext.Consumer)
