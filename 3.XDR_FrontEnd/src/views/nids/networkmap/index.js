// ================================================================================================
//  File Name: index.js
//  Description: Details of the Network Map.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import React, { useState, useEffect } from 'react'
import {
  TabContent,
  TabPane,
  Nav,
  NavItem,
  NavLink,
  Card,
  CardBody,
  Spinner
} from 'reactstrap'
import { useSelector } from "react-redux"
import axios from '@axios'
import { token } from '@utils'
import Breadcrumbs from '@components/breadcrumbs/bread'
import AwsMap from './awsMap'
import PreLoader from './preLoader'
import NotAuthorizedInner from '@src/views/notAuthorizedInner'

const NetworkMap = () => {
  const pagePermissionStore = useSelector((store) => store.pagesPermissions)
  const [active, setActive] = useState('')

  const [apiMapData, setApiMapData] = useState({
    aws: false,
    azure: false,
    onpremise: false,
    awsData: [],
    azureData: [],
    onpremiseData: [],
    apiLoader: false,
    apiErrMsg: ""
  })

  const toggle = tab => {
    setActive(tab)
  }

  const getApi = () => {

    setApiMapData(pre => ({ ...pre, apiLoader: true, apiErrMsg: "" }))

    axios.get('/dynamic-network-map',
      { headers: { Authorization: token() } }).then(res => {
        setApiMapData(pre => ({ ...pre, apiLoader: false }))

        if (res.data.message_type === "success") {

          setApiMapData(pre => ({
            ...pre,
            aws: res.data.aws,
            azure: res.data.azure,
            onpremise: res.data.onpremise,
            awsData: res.data.data.aws,
            azureData: res.data.data.azure,
            onpremiseData: res.data.data.onpremise
          }))

          let checkTabAcive = ""
          if (res.data.aws) {
            checkTabAcive = 'aws'
          }

          if (res.data.azure) {
            checkTabAcive = 'azure'
          }

          if (res.data.onpremise) {
            checkTabAcive = 'onpremise'
          }

          setActive(checkTabAcive)

        }

      })
      .catch(err => {
        setApiMapData(pre => ({ ...pre, apiLoader: false, apiErrMsg: err.message }))
      })
  }

  useEffect(() => {
    getApi()
  }, [])

  if (pagePermissionStore.loading === false) {
    return (
      <div className="text-center mt-5 pt-5"><Spinner md={5} color="primary" /></div>
    )
  } else {
    if (pagePermissionStore.env_nids === false) {
      return <NotAuthorizedInner />
    }
  }

  return (
    <React.Fragment>
      <Breadcrumbs breadCrumbTitle='Network Map' />
      <Card>
        <CardBody>
          <Nav pills className='mb-0'>
            {
              apiMapData.aws ? <NavItem>
                <NavLink
                  active={active === 'aws'}
                  onClick={() => {
                    toggle('aws')
                  }}
                >
                  AWS
                </NavLink>
              </NavItem> : null
            }

            {
              apiMapData.onpremise ? <NavItem>
                <NavLink
                  active={active === 'onpremise'}
                  onClick={() => {
                    toggle('onpremise')
                  }}
                >
                  Onpremise
                </NavLink>
              </NavItem> : null
            }

            {
              apiMapData.azure ? <NavItem>
                <NavLink
                  active={active === 'azure'}
                  onClick={() => {
                    toggle('azure')
                  }}
                >
                  Azure
                </NavLink>
              </NavItem> : null
            }

          </Nav>
        </CardBody>
      </Card>

      <Card>
        <CardBody>
          <TabContent className='py-50' activeTab={active}>
            <TabPane tabId='aws'>
              <AwsMap awsData={apiMapData.awsData} />
            </TabPane>
            <TabPane tabId='azure'>
              <AwsMap awsData={apiMapData.azureData} />
            </TabPane>
            <TabPane tabId='onpremise'>
              <AwsMap awsData={apiMapData.onpremiseData} />
            </TabPane>
          </TabContent>

          {apiMapData.apiErrMsg ? <p className='text-center'>{apiMapData.apiErrMsg}</p> : null}

        </CardBody>
        {apiMapData.apiLoader ? <PreLoader /> : null}
      </Card>
    </React.Fragment>
  )
}
export default NetworkMap