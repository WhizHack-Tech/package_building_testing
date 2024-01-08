// ================================================================================================
//  File Name: data.js
//  Description: Details of the Dashboard ( Agent ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Third Party Components
import { Badge, UncontrolledTooltip } from 'reactstrap'
import { format } from 'date-fns'
import { Link } from 'react-router-dom'
import { Eye } from 'react-feather'

// ** Vars
const states = ['success', 'danger', 'warning', 'info', 'dark', 'primary', 'secondary']

const status = {
  1: { title: 'Restarting', color: 'light-primary' },
  2: { title: 'Running', color: 'light-success' },
  3: { title: 'Stopped', color: 'light-danger' },
  4: { title: 'Resigned', color: 'light-warning' },
  5: { title: '', color: 'light-info' }
}

// ** Table Zero Config Column
export const basicColumns = [
  {
    name: 'Organization Name',
    selector: 'organization_name',
    sortable: true,
    minWidth: '100px'
  },
    {
    name: 'Agent Group',
    selector: 'attach_agent_group',
    sortable: true,
    minWidth: '100px',
    cell: row => {
      return (
        <div>
          <Badge color='info'>{row.attach_agent_group}</Badge>
        </div>
      )
    }
  },
  {
    name: 'Agent Key',
    selector: 'attach_agent_key',
    sortable: true,
    minWidth: '100px',
    cell: row => {
      return (
        <div>
          <Badge color='warning'>{row.attach_agent_key}</Badge>
        </div>
      )
    }
  },
  {
    name: 'Date',
    selector: 'creation_timestamp',
    sortable: true,
    minWidth: '100px',
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Badge color='light-primary'>
            <span className='font-weight-bold text-uppercase'>{format(new Date(row.creation_timestamp), "yyyy-MM-dd, h:mm:ss a")}</span>
          </Badge>
        </div>
      )
    }
  },
  {
    name: 'Actions',
    minWidth: '100px',
    selector: 'fullName',
    sortable: true,
    cell: row => (
      <div className='column-action d-flex align-items-center'>
        <Link to={`/dashboard/agentdetails/${row.org_location}`} id={`pw-tooltip-${row.org_location}`}>
          <Eye size={17} className='mx-1' />
        </Link>
        <UncontrolledTooltip placement='top' target={`pw-tooltip-${row.org_location}`}>
          View Agents Detais
        </UncontrolledTooltip>
      </div>
    )
  }
]


export default basicColumns
