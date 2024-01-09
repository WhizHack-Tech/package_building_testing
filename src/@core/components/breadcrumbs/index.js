// ==============================================================================================
//  File Name: breadcrumbs/index.js
//  Description: Details of the breadcrumbs component.
//  ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Third Party Components
import Proptypes from 'prop-types'

const BreadCrumbs = props => { 
  // ** Props
  const { breadCrumbTitle } = props
 
 return (
    <div className='content-header row'>
      <div className='content-header-left col-md-9 col-12 mb-2'>
        <div className='row breadcrumbs-top'>
          <div className='col-12'>
            {breadCrumbTitle ? <h4>{breadCrumbTitle}</h4> : ''}
          </div>
        </div>
      </div>
    </div>
  )
}
export default BreadCrumbs

// ** PropTypes
BreadCrumbs.propTypes = {
  breadCrumbTitle: Proptypes.string.isRequired
}