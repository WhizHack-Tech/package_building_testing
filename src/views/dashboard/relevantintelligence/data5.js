// ** Custom Components
import Avatar from '@components/avatar'

// ** Third Party Components
import axios from 'axios'
import { FormattedMessage } from 'react-intl'
import { MoreVertical, Edit, FileText, Archive, Trash } from 'react-feather'
import { Badge, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap'

// ** Vars
//const states = ['success', 'danger', 'warning', 'info', 'dark', 'primary', 'secondary']

const data_source_id = {
  3: { title: 'Offline', color: 'light-primary' },
  2: { title: 'Active', color: 'light-success' },
  0: { title: 'IDS', color: 'light-warning' },
  1: { title: 'USML', color: 'light-danger' },
  5: { title: 'Vulnerable', color: 'light-info' }
}
const attack_threat_severity = {
  0: { title: 'Milt', color: 'light-primary' },
  1: { title: 'Moderate', color: 'light-info' },
  2: { title: 'Severe', color: 'light-warning' },
  3: { title: 'Critical', color: 'light-danger' },
  4: { title: 'Normal', color: 'light-success' }
}

export let data

export const Udp = [
  {
    name: <FormattedMessage id='Target IP' />,
    selector: 'target_ip',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: <FormattedMessage id='Target Mac Address' />,
    selector: 'target_mac_address',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: <FormattedMessage id='UDP Port' />,
    selector: 'udp_port',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: <FormattedMessage id='No Of Times Attacked' />,
    selector: 'count(target_ip)',
    sortable: true,
    minWidth: '150px'
  }
]

export default Udp
