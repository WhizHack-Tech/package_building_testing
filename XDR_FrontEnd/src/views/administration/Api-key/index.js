// ================================================================================================
//  File Name: index.js
//  Description: Index for the Api Folder.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
// ** React Imports
import { Fragment } from 'react'
import { useTranslation } from 'react-i18next'
// ** Custom Components
import Breadcrumbs from '@components/breadcrumbs/bread'

// ** Third Party Components
import { Row, Col } from 'reactstrap'

// ** Tables

import ApiTable from './ApiTable'

// ** Styles
import '@styles/react/libs/tables/react-dataTable-component.scss'

const Tables = () => {
  const { t } = useTranslation()
  return (
    <Fragment>
      <Breadcrumbs breadCrumbTitle={t('Key Management')} />
      <Row>
        <Col sm='12'>
          <ApiTable />
        </Col>
      </Row>
    </Fragment>
  )
}

export default Tables
