import { Fragment, useState, useEffect } from 'react'
import Tabs from './Tabs'
import Onprim from './Onprim'
import Breadcrumbs from '@components/breadcrumbs/bread'
import Newgraph from './Newgraph'
import { useTranslation } from 'react-i18next'
import { Row, Col, TabContent, TabPane, Card, CardBody } from 'reactstrap'

const AccountSettings = () => {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState('1')

  const toggleTab = tab => {
    setActiveTab(tab)
  }
  
  return (
    <Fragment>
      <Breadcrumbs breadCrumbTitle={t("Network Map")} />
      <Col>
        <Tabs activeTab={activeTab} toggleTab={toggleTab} />
      </Col>
      <Row>
        <Col md='12'>
          <Card>
            <CardBody>
              <TabContent activeTab={activeTab}>
                <TabPane tabId='3'>
                  < Newgraph />
                </TabPane>
                <TabPane tabId='1'>
                  <Onprim />
                </TabPane>
              </TabContent>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Fragment>
  )
}

export default AccountSettings
