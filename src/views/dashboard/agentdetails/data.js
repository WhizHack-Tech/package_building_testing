// ================================================================================================
//  File Name: data.js
//  Description: Details of the Dashboard ( Agent ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Third Party Components
import { Badge, UncontrolledTooltip, Button } from 'reactstrap'
import { format } from 'date-fns'
import { Link } from 'react-router-dom'
import { Download } from 'react-feather'
import { jsPDF } from 'jspdf'
import 'jspdf-autotable'
import "./pdfStyles.css"

// ** Vars
const states = ['success', 'danger', 'warning', 'info', 'dark', 'primary', 'secondary']

const status = {
  1: { title: 'Restarting', color: 'light-primary' },
  2: { title: 'Running', color: 'light-success' },
  3: { title: 'Stopped', color: 'light-danger' },
  4: { title: 'Resigned', color: 'light-warning' },
  5: { title: '', color: 'light-info' }
}

const handleDownloadPDF = (rowData) => {
  if (!rowData) {
    console.log('rowData is null or undefined:', rowData)
    return
  }

  console.log('rowData:', rowData)

  const doc = new jsPDF()

  const {
    organization_name,
    creation_timestamp,
    attach_agent_key,
    attach_agent_network,
    attach_agent_group,
    trace_attach_agent,
    trace_alert_agent,
    trace_event_agent,
    trace_global_agent,
    trace_incident_agent,
    trace_dpi_agent,
    hids_assets_agent,
    hids_event_agent,
    hids_incident_agent,
    hids_alert_agent,
    nids_alert_agent,
    nids_assets_agent,
    nids_event_agent,
    nids_global_agent,
    nids_incident_agent,
    nids_nmap_agent,
    soar_agent,
    tps_agent,
    ess_agent,
    sbs_agent,
    tptf_agent,
    mm_agent,
    hc_agent
  } = rowData

  doc.setFont('helvetica', 'bold')
  doc.setFontSize(16)
  const headingText = 'Agent Details'
  const textWidth = (doc.getStringUnitWidth(headingText) * doc.internal.getFontSize()) / doc.internal.scaleFactor
  const textOffset = (doc.internal.pageSize.width - textWidth) / 2

  doc.text(headingText, textOffset, 20)
  doc.setFont('Arial', 'normal')
  doc.setFontSize(11)
  doc.setTextColor(255, 0, 0)
  doc.text('Organization Name :', 10, 40)
  doc.text('Creation Timestamp :', 10, 50)
  doc.text('Attach Agent Key :', 10, 60)
  doc.text('Attach Agent Network :', 10, 70)
  doc.text('Attach Agent Group :', 10, 80)
  doc.text('TRACE Attach Agent :', 10, 90)
  doc.text('TRACE Alert Agent :', 10, 100)
  doc.text('TRACE Event Agent :', 10, 110)
  doc.text('TRACE Global Agent :', 10, 120)
  doc.text('TRACE Incident Agent :', 10, 130)
  doc.text('TRACE DPI Agent :', 10, 140)
  doc.text('HIDS Assets Agent :', 10, 150)
  doc.text('HIDS Event Agent :', 10, 160)
  doc.text('HIDS Incident Agent :', 10, 170)
  doc.text('HIDS Alert Agent :', 10, 180)
  doc.text('NIDS Alert Agent :', 10, 190)
  doc.text('NIDS Assets Agent :', 10, 200)
  doc.text('NIDS Event Agent :', 10, 210)
  doc.text('NIDS Global Agent :', 10, 220)
  doc.text('NIDS Incident Agent :', 10, 230)
  doc.text('NIDS NMAP Agent :', 10, 240)
  doc.text('SOAR Agent :', 10, 250)
  doc.text('TPS Agent :', 10, 260)
  doc.text('ESS Agent :', 10, 270)
  doc.text('SBS Agent :', 10, 280)
  doc.text('TPTF Agent :', 10, 290)
  doc.text('MM Agent :', 10, 300)
  doc.text('HC Agent :', 10, 310)


  // Add null checks for other properties before accessing them
  doc.setTextColor(0)
  doc.text(organization_name !== undefined && organization_name !== null ? organization_name.toString() : '', 50, 40)
  doc.text(creation_timestamp !== undefined && creation_timestamp !== null ? creation_timestamp.toString() : '', 50, 50)
  doc.text(attach_agent_key !== undefined && attach_agent_key !== null ? attach_agent_key.toString() : '', 50, 60)
  doc.text(attach_agent_network !== undefined && attach_agent_network !== null ? attach_agent_network.toString() : '', 50, 70)
  doc.text(attach_agent_group !== undefined && attach_agent_group !== null ? attach_agent_group.toString() : '', 50, 80)
  doc.text(trace_attach_agent !== undefined && trace_attach_agent !== null ? trace_attach_agent.toString() : '', 50, 90)
  doc.text(trace_alert_agent !== undefined && trace_alert_agent !== null ? trace_alert_agent.toString() : '', 50, 100)
  doc.text(trace_event_agent !== undefined && trace_event_agent !== null ? trace_event_agent.toString() : '', 50, 110)
  doc.text(trace_global_agent !== undefined && trace_global_agent !== null ? trace_global_agent.toString() : '', 50, 120)
  doc.text(trace_incident_agent !== undefined && trace_incident_agent !== null ? trace_incident_agent.toString() : '', 50, 130)
  doc.text(trace_dpi_agent !== undefined && trace_dpi_agent !== null ? trace_dpi_agent.toString() : '', 50, 140)
  doc.text(hids_assets_agent !== undefined && hids_assets_agent !== null ? hids_assets_agent.toString() : '', 50, 150)
  doc.text(hids_event_agent !== undefined && hids_event_agent !== null ? hids_event_agent.toString() : '', 50, 160)
  doc.text(hids_incident_agent !== undefined && hids_incident_agent !== null ? hids_incident_agent.toString() : '', 50, 170)
  doc.text(hids_alert_agent !== undefined && hids_alert_agent !== null ? hids_alert_agent.toString() : '', 50, 180)
  doc.text(nids_alert_agent !== undefined && nids_alert_agent !== null ? nids_alert_agent.toString() : '', 50, 190)
  doc.text(nids_assets_agent !== undefined && nids_assets_agent !== null ? nids_assets_agent.toString() : '', 50, 200)
  doc.text(nids_event_agent !== undefined && nids_event_agent !== null ? nids_event_agent.toString() : '', 50, 210)
  doc.text(nids_global_agent !== undefined && nids_global_agent !== null ? nids_global_agent.toString() : '', 50, 220)
  doc.text(nids_incident_agent !== undefined && nids_incident_agent !== null ? nids_incident_agent.toString() : '', 50, 230)
  doc.text(nids_nmap_agent !== undefined && nids_nmap_agent !== null ? nids_nmap_agent.toString() : '', 50, 240)
  doc.text(soar_agent !== undefined && soar_agent !== null ? soar_agent.toString() : '', 50, 250)
  doc.text(tps_agent !== undefined && tps_agent !== null ? tps_agent.toString() : '', 50, 260)
  doc.text(ess_agent !== undefined && ess_agent !== null ? ess_agent.toString() : '', 50, 270)
  doc.text(sbs_agent !== undefined && sbs_agent !== null ? sbs_agent.toString() : '', 50, 280)
  doc.text(tptf_agent !== undefined && tptf_agent !== null ? tptf_agent.toString() : '', 50, 290)
  doc.text(mm_agent !== undefined && mm_agent !== null ? mm_agent.toString() : '', 50, 300)
  doc.text(hc_agent !== undefined && hc_agent !== null ? hc_agent.toString() : '', 50, 310)

  doc.save('Indices.pdf')
}

  const CustomDownloadButton = ({ data }) => (
    <Button.Ripple color='flat-primary' size='sm' className="btn btn-sm" onClick={() => handleDownloadPDF(data)}>
      <Download size={16} />
    </Button.Ripple>
  )

// ** Table Zero Config Column
export const basicColumns = [
  {
    name: 'Download',
    selector: null,
    sortable: true,
    Width: '150px',
    cell: row => <CustomDownloadButton data={row} />
  },
  {
    name: 'Trace Attach Agent',
    selector: 'trace_attach_agent',
    sortable: true,
    minWidth: '250px'
  },
  {
    name: 'Trace Alert',
    selector: 'trace_alert_agent',
    sortable: true,
    minWidth: '300px'
  },
    {
    name: 'Trace Event',
    selector: 'trace_event_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'Trace Incident',
    selector: 'trace_global_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'Trace Global',
    selector: 'trace_global_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'Trace DPI',
    selector: 'trace_dpi_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'Hids Assets',
    selector: 'hids_assets_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'Hids Alert',
    selector: 'hids_alert_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'Hids Event',
    selector: 'hids_event_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'Hids Incident',
    selector: 'hids_incident_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'NIDS Alert',
    selector: 'nids_alert_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'NIDS Event',
    selector: 'nids_event_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'NIDS Incident',
    selector: 'nids_incident_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'NIDS Assets',
    selector: 'nids_assets_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'NIDS Golbal',
    selector: 'nids_global_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'NIDS Map',
    selector: 'nids_nmap_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'Agent Network',
    selector: 'attach_agent_network',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'Soar Agent',
    selector: 'soar_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'TPS Agent',
    selector: 'tps_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'ESS Agent',
    selector: 'ess_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'SBS Agent',
    selector: 'sbs_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'TPTF Agent',
    selector: 'tptf_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'MM Agent',
    selector: 'mm_agent',
    sortable: true,
    minWidth: '300px'
  },
  {
    name: 'HC Agent',
    selector: 'hc_agent',
    sortable: true,
    minWidth: '300px'
  }
]


export default basicColumns
