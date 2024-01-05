// ================================================================================================
//  File Name: data.js
//  Description: Details of the NIDS Incidents ( Attacked Host Details )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==========================================================================================
// ** Custom Components
import Avatar from '@components/avatar'

// ** Third Party Components
import axios from 'axios'
import { MoreVertical, Edit, FileText, Archive, Trash } from 'react-feather'
import { Badge, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap'

// ** Vars
const states = ['success', 'danger', 'warning', 'info', 'dark', 'primary', 'secondary']

const status = {
  1: { title: 'Current', color: 'light-primary' },
  2: { title: 'Professional', color: 'light-success' },
  3: { title: 'Rejected', color: 'light-danger' },
  4: { title: 'Resigned', color: 'light-warning' },
  5: { title: 'Applied', color: 'light-info' }
}


// ** Table Common Column
export const columns = [
  {
    name: 'Email',
    selector: 'target_ip',
    icon : <Trash size={15} />,
    sortable: true,
    minWidth: '250px'
  },
  {
    name: 'Date',
    selector: 'target_ip_count',
    sortable: true,
    minWidth: '150px'
  },

  {
    name: 'Salary',
    selector: 'target_mac',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: 'Age',
    selector: 'type_of_threat',
    sortable: true,
    minWidth: '100px'
  }
]


export default columns
