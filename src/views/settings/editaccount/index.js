// ================================================================================================
//  File Name: index.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useState, useEffect, useContext } from 'react'
import Tabs from './Tabs'
import axios from '@axios'
import Config from './Config'
import InfoTabContent from './InfoTabContent'
import GeneralTabContent from './GeneralTabContent'
import PasswordTabContent from './PasswordTabContent'
import NotificationsTabContent from './NotificationsTabContent'
import { Row, Col, TabContent, TabPane, Card, CardBody, Spinner } from 'reactstrap'
import { token } from '@utils'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/pages/page-account-settings.scss'
import Breadcrumbs from '@components/breadcrumbs/bread'
import { useTranslation } from 'react-i18next'
import { AbilityContext } from '@src/utility/context/Can'
import WhiteLists from './MultipleTabs'

const AccountSettings = () => {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState('1'),
    [data, setData] = useState(null)

  const ability = useContext(AbilityContext)

  const toggleTab = tab => {
    setActiveTab(tab)
  }

  useEffect(() => {
    axios.get('/account-manage-detail', { headers: { Authorization: token() } }).then(response => {
      setData(response.data)
    })
  }, [])

  return (
    <Fragment>
      <Breadcrumbs breadCrumbTitle={t('Account Setting')} />
      {data !== null ? (
        <Row>
          <Col className='mb-2 mb-md-0' md='3'>
            <Tabs activeTab={activeTab} toggleTab={toggleTab} />
          </Col>
          <Col md='9'>
            <Card>
              <CardBody>
                <TabContent activeTab={activeTab}>
                  <TabPane tabId='1'>
                    <GeneralTabContent data={data} />
                  </TabPane>
                  <TabPane tabId='2'>
                    <PasswordTabContent />
                  </TabPane>
                  <TabPane tabId='3'>
                    <NotificationsTabContent data={data} />
                  </TabPane>
                  <TabPane tabId='4'>
                    <InfoTabContent data={data} />
                  </TabPane>
                  {ability.can('read', 'all') ? (
                    <TabPane tabId='5'>
                      <Config data={data} />
                    </TabPane>
                  ) : null}

                  <TabPane tabId='6'>
                    <WhiteLists />
                  </TabPane>

                </TabContent>
              </CardBody>
            </Card>
          </Col>
        </Row>
      ) : <div className='d-flex justify-content-center'><Spinner color='primary' type='grow' /></div>}
    </Fragment>
  )
}

export default AccountSettings
