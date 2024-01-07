// ** Custom Components
import Avatar from '@components/avatar'

// ** Third Party Components
import axios from 'axios'
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
// ** Get initial Data
axios.get('/victim/').then(response => {
  data = response.data
}, [])


// ** Table Zero Config Column
export const basicColumns = [
 

  {
    name: 'Target Ip',
    selector: 'target_ip',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: 'Target Mac Address',
    selector: 'target_mac_address',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: 'No Of Times Attacked',
    selector: 'no_of_times_attacked',
    sortable: true,
    minWidth: '150px'
  }

]

// export const Ip = [
 

//   {
//     name: 'Attacker IP',
//     selector: 'attacker_iP',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Attacker Mac Address',
//     selector: 'attacker_mac',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'No Of Times Attacked',
//     selector: 'attack_timestamp',
//     sortable: true,
//     minWidth: '150px'
//   }

// ]

// export const Fastest = [
 

//   {
//     name: 'Attacker IP',
//     selector: 'attacker_iP',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Attacker Mac Address',
//     selector: 'attacker_mac',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Attack Timestamp',
//     selector: 'attack_timestamp',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'No Of Times Attacked',
//     selector: 'no_of_times_attacked',
//     sortable: true,
//     minWidth: '150px'
//   }

// ]
// export const Geo = [
 

//   {
//     name: 'Attacker IP',
//     selector: 'attacker_iP',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Attacker Mac Address',
//     selector: 'attacker_mac',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Attack Timestamp',
//     selector: 'attack_timestamp',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Attacker City',
//     selector: ' attacker_city',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'No Of Times Attacked',
//     selector: 'no_of_times_attacked',
//     sortable: true,
//     minWidth: '150px'
//   }

// ]
// export const Tcp = [
 

//   {
//     name: 'Attacker IP',
//     selector: 'target_iP',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Attacker Mac Address',
//     selector: 'target_mac',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Tcp Port',
//     selector: ' tcp_port',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'No Of Times Attacked',
//     selector: 'attack_timestamp',
//     sortable: true,
//     minWidth: '150px'
//   }

// ]
// export const Udp = [
 
//   {
//     name: 'Target IP',
//     selector: 'target_iP',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Target Mac Address',
//     selector: 'target_mac',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'udp Port',
//     selector: 'udp_port',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'No Of Times Attacked',
//     selector: 'attack_timestamp',
//     sortable: true,
//     minWidth: '150px'
//   }

// ]
// export const Top = [
 
//   {
//     name: 'Target IP',
//     selector: 'target_iP',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Target Mac Address',
//     selector: 'target_mac',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Threat Type',
//     selector: 'type_of_threat',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'No Of Times Attacked',
//     selector: 'attack_timestamp',
//     sortable: true,
//     minWidth: '150px'
//   }

// ]
// export const Attacker = [
 
//   {
//     name: 'Target IP',
//     selector: 'attacker_iP',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Target Mac Address',
//     selector: 'attacker_mac',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'Threat Type',
//     selector: 'type_of_threat',
//     sortable: true,
//     minWidth: '150px'
//   },
//   {
//     name: 'No Of Times Attacked',
//     selector: 'attack_timestamp',
//     sortable: true,
//     minWidth: '150px'
//   }

// ]
 
//** Expandable table component
const ExpandableTable = ({ data }) => {
  return (
    <div className='expandable-content p-2'>
      <p>
        <span className='font-weight-bold'>City:</span> {data.city}
      </p>
      <p>
        <span className='font-weight-bold'>Experience:</span> {data.experience}
      </p>
      <p className='m-0'>
        <span className='font-weight-bold'>Post:</span> {data.post}
      </p>
    </div>
  )
}

export default ExpandableTable
