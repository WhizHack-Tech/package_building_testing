// ==============================================================================================
//  File Name: bread.js
//  Description: header Breadcrumb component
// ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { Link } from 'react-router-dom'
import { addDays, format } from "date-fns"
import { useState, useEffect, useMemo } from "react"
import { DateRangePicker } from "react-date-range"
import "react-date-range/dist/styles.css" // main style file
import "react-date-range/dist/theme/default.css" // theme css file
import { dashboar_charts } from "../../../redux/actions/charts/dashboard_charts"
import { useDispatch, useSelector } from "react-redux"
// ** Third Party Components
import Proptypes from 'prop-types'
import { Grid, CheckSquare, MessageSquare, Mail, Calendar } from 'react-feather'
import {
  Breadcrumb,
  BreadcrumbItem,
  UncontrolledButtonDropdown,
  DropdownMenu,
  DropdownItem,
  DropdownToggle,
  ButtonGroup,
  Button,
  Col,
  Spinner
} from 'reactstrap'

const BreadCrumbs = props => {
  const [state, setState] = useState([])
  const [btnToggle, setBtnToggle] = useState(false)
 
  // ** Props
  const { breadCrumbTitle, breadCrumbParent, breadCrumbParent2, breadCrumbParent3, breadCrumbActive } = props
 
 return (
    <div className='content-header row'>
      <div className='content-header-left col-md-9 col-12 mb-1'>
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