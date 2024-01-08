// ==============================================================================================
//  File Name: navbar/index.js
//  Description: Details of the navbar component.
//  ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { Fragment } from 'react'

// ** Custom Components
import NavbarUser from './NavbarUser'

const ThemeNavbar = props => {
  // ** Props
  const { skin, setSkin, setMenuVisibility } = props

  return (
    <Fragment>
      <NavbarUser skin={skin} setSkin={setSkin} setMenuVisibility={setMenuVisibility} />
    </Fragment>
  )
}

export default ThemeNavbar
