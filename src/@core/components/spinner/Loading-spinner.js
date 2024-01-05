// =============================================================================================
//  File Name: spinner/index.js
//  Description: Details of the spinner loader component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

const ComponentSpinner = () => {
  return (
    <div className='fallback-spinner'>
      <div className='loading component-loader'>
        <div className='effect-1 effects'></div>
        <div className='effect-2 effects'></div>
        <div className='effect-3 effects'></div>
      </div>
    </div>
  )
}

export default ComponentSpinner
