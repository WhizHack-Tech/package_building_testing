// =============================================================================================
//  File Name: ability.js
//  Description: Details of the ability component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Ability } from '@casl/ability'
import { initialAbility } from './initialAbility'

//  Read ability from localStorage
// * Handles auto fetching previous abilities if already logged in user
// ? You can update this if you store user abilities to more secure place
// ! Anyone can update localStorage so be careful and please update this
const userData = JSON.parse(localStorage.getItem('clientData'))
const existingAbility = userData ? userData.ability : null

export default new Ability(existingAbility || initialAbility)
