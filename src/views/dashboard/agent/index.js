// ================================================================================================
//  File Name: index.js
//  Description: Details of the Dashboard ( Agent ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** React Imports
import { Fragment } from 'react'
import Breadcrumbs from '@components/breadcrumbs'
// ** Third Party Components
import { Row, Col, Breadcrumb, BreadcrumbItem } from 'reactstrap'

// ** Tables
import TableZeroConfig from './TableZeroConfig'

// ** Styles
import '@styles/react/libs/tables/react-dataTable-component.scss'

const Tables = () => {
  return (
    <Fragment>
      <Breadcrumbs breadCrumbTitle='Agent Details'/>
      <Row>
        <Col sm='12'>
          <TableZeroConfig />
        </Col>
      </Row>
    </Fragment>
  )
}

export default Tables
