
// ================================================================================================
//  File Name: index.js
//  Description: Index page for the Logs Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
import { Fragment } from 'react'
import { Link } from 'react-router-dom'
import { Row, Col } from 'reactstrap'
import BasicTimeline from './BasicTimeline'
import Breadcrumbs from '@components/breadcrumbs/bread'
import { useTranslation } from 'react-i18next'

const Timeline = () => {
  const { t } = useTranslation()
  return (
    <Fragment>
      <Breadcrumbs breadCrumbTitle={t('Logs')} />
      <Row>
        <Col lg='12'>
          <BasicTimeline />
        </Col>
      </Row>
    </Fragment>
  )
}

export default Timeline
