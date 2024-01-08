// ================================================================================================
//  File Name: PlanCard.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================

import React from 'react'
import { Card, CardHeader, CardBody, Badge, Button } from 'reactstrap'
import jsPDF from 'jspdf'
import 'jspdf-autotable'
import { ChevronDown, Download } from 'react-feather'
import "./Loader.css"
const PlanCard = ({ selectedUser }) => {

  if (selectedUser.message_type === null) {
    return (
      <Card>
        <CardBody className='d-flex justify-content-center align-items-center' style={{ height: '210px' }}>
          <div class="tri-color-ripple-spinner">
            <div class="ripple ripple1"></div>
            <div class="ripple ripple2"></div>
          </div>
        </CardBody>
      </Card>
    )
  }

  const downloadAsPDF = () => {
    const doc = new jsPDF()
  
    // Add content to the PDF
    const title = 'Current Plan'
    const titleWidth = doc.getStringUnitWidth(title) * doc.internal.getFontSize() / doc.internal.scaleFactor
    const pageWidth = doc.internal.pageSize.width
  
    // Calculate the X-coordinate to center the title
    const titleX = (pageWidth - titleWidth) / 2
  
    doc.text(title, titleX, 10) // Title
  
    // Example: Add your card content as text
    const cardContent = `
      Plan Name: ${selectedUser.message_type === 'data_found' ? selectedUser.data.plan_name : ''}
      
      Billing Name: ${selectedUser.message_type === 'data_found' ? selectedUser.data.billing_types : ''}

      TRACE: ${selectedUser.message_type === 'data_found' ? selectedUser.data.trace_sensor_key : ''}

      HIDS: ${selectedUser.message_type === 'data_found' ? selectedUser.data.hids_sensor_key : ''}

      NIDS: ${selectedUser.message_type === 'data_found' ? selectedUser.data.nids_sensor_key : ''}

      SOAR: ${selectedUser.message_type === 'data_found' ? selectedUser.data.soar_sensor_key : ''}

      Account Status: ${selectedUser.message_type === 'data_found' ? (selectedUser.data.is_active ? 'Active' : 'Deactive') : ''}

    `
  
    doc.text(cardContent, 10, 20)
  
    // Save the PDF with a file name
    doc.save('plan_card.pdf')
  }
  

  return (
    <Card>
      <div>
      <div style={{ height: '300px' }}>
        <CardHeader className='d-flex justify-content-between align-items-center pt-75 pb-1'>
          <h5 className='mb-0'>Current Plan</h5>
          <Badge id='plan-expiry-date' color='light-primary'>
            {selectedUser.message_type === 'data_found' ? new Date(selectedUser.data.created_at).toDateString() : ''}
            </Badge>
            <Button.Ripple color='flat-primary' size='sm' className="btn btn-sm" onClick={downloadAsPDF}>
              <Download size={16} />
            </Button.Ripple>
        </CardHeader>
        <CardBody>
          <ul className='list-unstyled mt-1'>
            <li>
              <span className='align-middle'><b>Plan Name </b><Badge color='light-success'>{selectedUser.message_type === "data_found" ? selectedUser.data.plan_name : ''}</Badge></span>
            </li>
            <li className='mt-1'>
              <span className='align-middle'><b>Billing Name </b><Badge color='light-warning'>{selectedUser.message_type === "data_found" ? selectedUser.data.billing_types : ''}</Badge></span>
            </li>
            <li className='mt-1 mb-0'>
              <span className='align-middle'><b>Account Status </b>
                {selectedUser.message_type === "data_found" ? <Badge color='light-info'>{selectedUser.data.is_active ? 'Active' : 'Deactive'}</Badge> : ""}
              </span>
            </li>
            <li className='mt-1 mb-0'>
              <span className='align-middle'><b>TRACE </b>
                {selectedUser.message_type === "data_found" ? <Badge color='light-info'>{selectedUser.message_type === "data_found" ? selectedUser.data.trace_sensor_key : ''}</Badge> : ""}
              </span>
            </li>
            <li className='mt-1 mb-0'>
              <span className='align-middle'><b>HIDS </b>
                {selectedUser.message_type === "data_found" ? <Badge color='light-info'>{selectedUser.message_type === "data_found" ? selectedUser.data.hids_sensor_key : ''}</Badge> : ""}
              </span>
            </li>
            <li className='mt-1 mb-0'>
              <span className='align-middle'><b>NIDS </b>
                {selectedUser.message_type === "data_found" ? <Badge color='light-info'>{selectedUser.message_type === "data_found" ? selectedUser.data.nids_sensor_key : ''}</Badge> : ""}
              </span>
            </li>
            <li className='mt-1 mb-0'>
              <span className='align-middle'><b>SOAR </b>
                {selectedUser.message_type === "data_found" ? <Badge color='light-info'>{selectedUser.message_type === "data_found" ? selectedUser.data.soar_sensor_key : ''}</Badge> : ""}
              </span>
            </li>
          </ul>
        </CardBody>
      </div>
      </div>
    </Card>
  )
}

export default PlanCard
