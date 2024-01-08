// ==============================================================================================
//  File Name: useJwt.js
//  Description: Details of the useJwt component.
//  ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** JWT Service Import
import JwtService from './jwtService'

// ** Export Service as useJwt
export default function useJwt(jwtOverrideConfig) {
  const jwt = new JwtService(jwtOverrideConfig)

  return {
    jwt
  }
}
