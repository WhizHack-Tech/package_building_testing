// ================================================================================================
//  File Name: index.js
//  Description: Details of the Notification.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment } from 'react'
import { Row, Col } from 'reactstrap'
import Notifications from './Notifications'
import Breadcrumbs from '@components/breadcrumbs/bread'
import { useTranslation } from 'react-i18next'

const Timeline = () => {
  const {t} = useTranslation()
  return (
    <Fragment>
      <Breadcrumbs breadCrumbTitle={t('Notifications')}/>
      <Row>
        <Col sm='12'>
          <Notifications />
        </Col>
      </Row>
    </Fragment>
  )
}

export default Timeline
