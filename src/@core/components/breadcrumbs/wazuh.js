// ==============================================================================================
//  File Name: wazuh.js
//  Description: Details of the Network-Map filter by date component.
// ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { addDays, format } from "date-fns"
import { useState, useEffect } from "react"
import Flatpickr from 'react-flatpickr'
import { useTranslation } from 'react-i18next'
import 'flatpickr/dist/flatpickr.css'
import "react-date-range/dist/styles.css"
import "react-date-range/dist/theme/default.css"
import Proptypes, { object } from 'prop-types'
import { Filter, ChevronsRight, RefreshCw } from 'react-feather'
import {
  Button,
  Col,
  Spinner,
  FormGroup,
  Label,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Row,
  Badge
} from 'reactstrap'
import { data } from "jquery"
const MultipleBadge = ({ filterData, color }) => {
  if (typeof filterData === "object") {
    return filterData.map((v, key) => {
      return <Badge key={key} color={color} className="ml-1">{v}</Badge>
    })
  } else {
    return <Badge key={key} color={color}>{filterData}</Badge>
  }
}

const BreadCrumbs = props => {
    const [picker, setPicker] = useState(new Date())
  const {t} = useTranslation()
  const [startDatePicker, setStartDatePicker] = useState(0)
  const [endDatePicker, setEndDatePicker] = useState(0)
  const [basicModal, setBasicModal] = useState(false)
   // ** Props
   const { breadCrumbTitle, breadCrumbParent, breadCrumbParent2, breadCrumbParent3, breadCrumbActive } = props
  return (
    <div className='content-header row'>
      <div className='content-header-left col-md-2 col-12 mb-2'>
        <div className='row breadcrumbs-top'>
          <div className='col-12'>
            {breadCrumbTitle ? <h4>{breadCrumbTitle}</h4> : ''}
          </div>
        </div>
      </div>

      <div className='content-header-right text-md-right col-md-10 col-12 d-md-block d-none'>
        <div className='form-group breadcrum-right dropdown'>
        <div className="d-inline-block text-primary">
        <Badge color='light-success'>{t('Start Date')}</Badge> <ChevronsRight /> <Badge color='dark'>2023-11-01</Badge> | <Badge color='light-success'>{t('End Date')}</Badge> <ChevronsRight /> <Badge color='dark'>2023-13-01</Badge>
          </div>
          <Button.Ripple color='primary' size='sm' onClick={() => setBasicModal(!basicModal)} className='ml-1'>
            {t('Filter')}
          </Button.Ripple>
          <Modal isOpen={basicModal} toggle={() => setBasicModal(!basicModal)} modalClassName="modal-primary">
            <ModalHeader toggle={() => setBasicModal(!basicModal)}>{t('Filter')}</ModalHeader>
            <ModalBody>
              <Row>
                <Col sm='6' md="6">
                  <FormGroup>
                    <Label for='range-picker-start'>{t('Start Date')}</Label>
                    <Flatpickr
                      id='range-picker-start'
                      className='form-control'
                      value={picker} 
                      onChange={date => setPicker(date)}
                      options={{
                        mode: "single",
                        allowInput: false,
                        dateFormat: "Y-m-d",
                        disable: [
                          {
                            from: addDays(new Date(), +0),
                            to: "9999-01-01"
                          }
                        ]
                      }}
                      autocomplete="off"
                      style={{ background: "white", color: "black" }}
                    />
                  </FormGroup>
                </Col>
                <Col sm='6' md="6">
                  <FormGroup>
                    <Label for='range-picker-end'>{t('End Date')}</Label>
                    <Flatpickr
                      id='range-picker-end'
                      className='form-control'
                      value={picker} 
                      onChange={date => setPicker(date)}
                      options={{
                        mode: "single",
                        allowInput: false,
                        dateFormat: "Y-m-d",
                        disable: [
                          {
                            from: addDays(new Date(), +0),
                            to: "9999-01-01"
                          }
                        ]
                      }}
                      autocomplete="off"
                      style={{ background: "white", color: "black" }}
                    />
                  </FormGroup>
                </Col>
              </Row>
            </ModalBody>
            <ModalFooter>
              <div style={{ float: 'right' }}>
                <Button size="small" color="danger" onClick={() => setBasicModal(!basicModal)} >
                  {t('Close')}
                </Button>
                <Button size="small" color="primary" className="ml-1" onClick={() => setBasicModal(!basicModal)}>
                  {t('Submit')}
                </Button>
              </div>
            </ModalFooter>
          </Modal>
        </div>
      </div>
    </div>
  )
}
export default BreadCrumbs

BreadCrumbs.propTypes = {
  breadCrumbTitle: Proptypes.string.isRequired
}