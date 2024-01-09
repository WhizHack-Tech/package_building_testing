// ================================================================================================
//  File Name: index.js
//  Description: Details of the Setting ( Application ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { Fragment } from 'react'
import BreadCrumbs from '@components/breadcrumbs'

// ** Third Party Components
import { Row, Col } from 'reactstrap'

// ** Tables

import TableWithButtons from './TableWithButtons'

// ** Styles
import '@styles/react/libs/tables/react-dataTable-component.scss'

const Tables = () => {
  return (
    <Fragment>
       <BreadCrumbs breadCrumbTitle='Application Details'/>
      <Row>
        <Col sm='12'>
          <TableWithButtons />
        </Col>
      
      </Row>
    </Fragment>
  )
}

export default Tables
