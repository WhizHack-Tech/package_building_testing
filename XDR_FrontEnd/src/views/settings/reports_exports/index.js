// ================================================================================================
//  File Name: index.js
//  Description: Details of the Dynamic Report ( Pages ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useEffect } from "react"
import { Row, Col } from "reactstrap"
import Breadcrumbs from '@components/breadcrumbs/nids_charts'
import TableViews from "./tablesView"
import SideBar from "./Sidebar"
import { useDispatch } from "react-redux"
import { getDefaultData } from "./store/actions"
import { useTranslation } from 'react-i18next'
import HeaderFilter from "./header_filter"
const ReportExports = () => {
  const { t } = useTranslation()
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(getDefaultData('last_1_hour'))
  }, [])

  return (
    <Fragment>
      <Breadcrumbs breadCrumbTitle={t('Dynamic Reports')} />
      <Row className="match-height">
        <Col md="12">
          <HeaderFilter />
        </Col>
        <Col md='3'>
          <SideBar />
        </Col>
        <Col md='9'>
          <TableViews />
        </Col>
      </Row>
    </Fragment>
  )
}

export default ReportExports