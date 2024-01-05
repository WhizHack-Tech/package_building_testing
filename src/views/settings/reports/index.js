// ================================================================================================
//  File Name: index.js
//  Description: Details of the Static Report Index Page.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment } from 'react'
import { Row, Col } from 'reactstrap'
import Breadcrumbs from '@components/breadcrumbs/bread'
import MultipleColumnForm from './MultipleColumnForm'
import { useTranslation } from 'react-i18next'
// import TableZeroConfig from './TableZeroConfig'

const FormLayouts = () => {
  const {t} = useTranslation()
  return (
    <Fragment>
     <Breadcrumbs breadCrumbTitle={t('Report')} />
      <Row>
        <Col sm='12'>
          <MultipleColumnForm />
        </Col>
        {/* <Col sm='12'>
          <TableZeroConfig />
        </Col> */}
      </Row>
    </Fragment>
  )
}
export default FormLayouts
