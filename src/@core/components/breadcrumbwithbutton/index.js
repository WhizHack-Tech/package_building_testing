// ==============================================================================================
//  File Name: breadcrumbwithbutton/index.js
//  Description: Details of the breadcrumbwithbutton component.
//  ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { Link } from 'react-router-dom'
import { addDays } from "date-fns"
import { useState, useEffect } from "react"
import { DateRangePicker } from "react-date-range"
import "react-date-range/dist/styles.css" // main style file
import "react-date-range/dist/theme/default.css" // theme css file

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
  Col
} from 'reactstrap'

const BreadCrumbs = props => {
  const [state, setState] = useState([])

  useEffect(() => {
    if (state.length === 0) {
      setState([
        {
          startDate: new Date(),
          endDate: addDays(new Date(), 7),
          key: "selection"
        }
      ])
    }
  }, [state, setState])
  // ** Props
  const { breadCrumbTitle, breadCrumbParent, breadCrumbParent2, breadCrumbParent3, breadCrumbActive } = props

  return (
    <div className='content-header row'>
      <div className='content-header-left col-md-9 col-12 mb-2'>
        <div className='row breadcrumbs-top'>
          <div className='col-12'>
            {breadCrumbTitle ? <h2 className='content-header-title float-left mb-0'>{breadCrumbTitle}</h2> : ''}
            <div className='breadcrumb-wrapper vs-breadcrumbs d-sm-block d-none col-12'>
              <Breadcrumb>
                <BreadcrumbItem tag='li'>
                  <Link to='/'>Home</Link>
                </BreadcrumbItem>
                <BreadcrumbItem tag='li' className='text-primary'>
                  {breadCrumbParent}
                </BreadcrumbItem>
                {breadCrumbParent2 ? (
                  <BreadcrumbItem tag='li' className='text-primary'>
                    {breadCrumbParent2}
                  </BreadcrumbItem>
                ) : (
                  ''
                )}
                {breadCrumbParent3 ? (
                  <BreadcrumbItem tag='li' className='text-primary'>
                    {breadCrumbParent3}
                  </BreadcrumbItem>
                ) : (
                  ''
                )}
                <BreadcrumbItem tag='li' active>
                  {breadCrumbActive}
                </BreadcrumbItem>
              </Breadcrumb>
            </div>
          </div>
        </div>
      </div>
      <div className='content-header-right text-md-right col-md-3 col-12 d-md-block d-none'>
        <div className='form-group breadcrum-right dropdown'>
          <UncontrolledButtonDropdown>
            <DropdownToggle color='primary' size='sm' className='btn-icon btn-round dropdown-toggle'>
              <Calendar size={14} />
            </DropdownToggle>
            <DropdownMenu tag='ul' right>
            <div key={JSON.stringify(state)}>
      <DateRangePicker
        onChange={(item) => setState([item.selection])}
        showSelectionPreview={true}
        moveRangeOnFirstSelection={false}
        months={2}
        ranges={state}
        direction="horizontal"
      />
      <Col sm={12}>
                  <hr />
                </Col>
       <div style={{float: 'right'}}>
        <Button size="small" color="primary">
          Apply
        </Button>
        <Button size="small" color="white">
          Cancel
        </Button>
      </div>
    </div>
            </DropdownMenu>
          </UncontrolledButtonDropdown>
        </div>
      </div>
    </div>
  )
}
export default BreadCrumbs

// ** PropTypes
BreadCrumbs.propTypes = {
  breadCrumbTitle: Proptypes.string.isRequired,
  breadCrumbActive: Proptypes.string.isRequired
}
