// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( Log Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment } from 'react'
import { Row, Col } from 'reactstrap'
import ClientLogs from './clientLogs'
import MasterLogs from './masterLogs'
import BreadCrumbs from '@components/breadcrumbs'

const Timeline = () => {
  return (
    <Fragment>
    <BreadCrumbs breadCrumbTitle='Logs Details'/>
      <Row>
        <Col lg='6'>
          <ClientLogs />
        </Col>
        <Col lg='6'>
          <MasterLogs />
        </Col>
      </Row>
    </Fragment>
  )
}

export default Timeline
