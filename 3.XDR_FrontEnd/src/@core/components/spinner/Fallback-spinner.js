// =============================================================================================
//  File Name: spinner/index.js
//  Description: Details of the fallback spinner loader component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import logo from '@src/assets/images/logo/logo.png'

const SpinnerComponent = () => {
  return (
    <div className='fallback-spinner vh-100'>
      <img className='fallback-logo' src={logo} alt='logo' />
      <div className='loading'>
        <div className='effect-1 effects'></div>
        <div className='effect-2 effects'></div>
        <div className='effect-3 effects'></div>
      </div>
    </div>
  )
}

export default SpinnerComponent
