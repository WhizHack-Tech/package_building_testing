// ** React Imports
import { Fragment } from 'react'
import Breadcrumbs from '@components/breadcrumbs'

// ** Third Party Components
import { Row, Col } from 'reactstrap'

// ** Tables

import TableWithButtons from './TableWithButtons'

// ** Styles
import '@styles/react/libs/tables/react-dataTable-component.scss'

const Tables = () => {
  return (
    <Fragment>
      <Breadcrumbs breadCrumbTitle='Email'/>
      <Row>
        <Col sm='12'>
          <TableWithButtons />
        </Col>  
      </Row>
    </Fragment>
  )
}

export default Tables
