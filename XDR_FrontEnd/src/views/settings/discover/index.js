// ================================================================================================
//  File Name: index.js
//  Description: Details of the Discover Data.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment } from 'react'
import { Row, Col } from 'reactstrap'
import Breadcrumbs from '@components/breadcrumbs/bread'
import ColumnForm from './ColumnForm'
import { useTranslation } from 'react-i18next'

const FormLayouts = () => {
  const {t} = useTranslation()
  return (
    <Fragment>
     <Breadcrumbs breadCrumbTitle={t('Discover')} />
      <Row>
        <Col sm='12'>
          <ColumnForm />
        </Col>
      </Row>
    </Fragment>
  )
}
export default FormLayouts
