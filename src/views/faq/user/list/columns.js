// ** React Imports
import { Link } from 'react-router-dom'

// ** Custom Components
import Avatar from '@components/avatar'

// ** Store & Actions
import { getUser, deleteUser } from '../store/action'
import { store } from '@store/storeConfig/store'

// ** Third Party Components
import { Badge, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap'
import { Slack, User, Settings, Database, Edit2, MoreVertical, FileText, Trash2, Archive } from 'react-feather'

// ** Renders Client Columns
const renderClient = row => {
  const stateNum = Math.floor(Math.random() * 6),
    states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
    color = states[stateNum]

  if (row.avatar.length) {
    return <Avatar className='mr-1' img={row.avatar} width='32' height='32' />
  } else {
    return <Avatar color={color || 'primary'} className='mr-1' content={row.fullName || 'John Doe'} initials />
  }
}

// ** Renders Role Columns
const renderRole = row => {
  const roleObj = {
    subscriber: {
      class: 'text-primary',
      icon: User
    },
    maintainer: {
      class: 'text-success',
      icon: Database
    },
    editor: {
      class: 'text-info',
      icon: Edit2
    },
    author: {
      class: 'text-warning',
      icon: Settings
    },
    admin: {
      class: 'text-danger',
      icon: Slack
    }
  }

  const Icon = roleObj[row.role] ? roleObj[row.role].icon : Edit2

  return (
    <span className='text-truncate text-capitalize align-middle'>
      <Icon size={18} className={`${roleObj[row.role] ? roleObj[row.role].class : ''} mr-50`} />
      {row.role}
    </span>
  )
}

const statusObj = {
  pending: 'light-warning',
  active: 'light-success',
  inactive: 'light-secondary'
}

export const columns = [
  {
    name: 'ID',
    minWidth: '320px',
    selector: 'organization_id',
    sortable: true,
    cell: row => row.organization_id
  },
  {
    name: 'User',
    minWidth: '297px',
    selector: 'organization_name',
    sortable: true
    // cell: row => (
    //   <div className='d-flex justify-content-left align-items-center'>
    //     {renderClient(row)}
    //     <div className='d-flex flex-column'>
    //       <Link
    //         to={`/faq/user/view/${row.id}`}
    //         className='user-name text-truncate mb-0'
    //         onClick={() => store.dispatch(getUser(row.id))}
    //       >
    //         <span className='font-weight-bold'>{row.fullName}</span>
    //       </Link>
    //       <small className='text-truncate text-muted mb-0'>@{row.username}</small>
    //     </div>
    //   </div>
    // )
  },
  {
    name: 'Email',
    minWidth: '320px',
    selector: 'organization_primary_email_id',
    sortable: true,
    cell: row => row.organization_primary_email_id
  },
  {
    name: 'Role',
    minWidth: '172px',
    selector: 'organization_name',
    sortable: true
    // cell: row => renderRole(row)
  },
  {
    name: 'Plan',
    minWidth: '138px',
    selector: 'organization_name',
    sortable: true,
    cell: row => <span className='text-capitalize'>{row.organization_name}</span>
  },
  // {
  //   name: 'Status',
  //   minWidth: '138px',
  //   selector: 'status',
  //   sortable: true,
  //   cell: row => (
  //     <Badge className='text-capitalize' color={statusObj[row.status]} pill>
  //       {row.status}
  //     </Badge>
  //   )
  // },
  {
    name: 'Actions',
    minWidth: '100px',
    cell: row => (
      <UncontrolledDropdown>
        <DropdownToggle tag='div' className='btn btn-sm'>
          <MoreVertical size={14} className='cursor-pointer' />
        </DropdownToggle>
        <DropdownMenu right>
          <DropdownItem
            tag={Link}
            to={`/faq/user/view/${row.organization_id}`}
            className='w-100'
            onClick={() => store.dispatch(getUser(row.organization_id))}
          >
            <FileText size={14} className='mr-50' />
            <span className='align-middle'>Details</span>
          </DropdownItem>
          <DropdownItem
            tag={Link}
            to={`/faq/user/edit/${row.organization_id}`}
            className='w-100'
            onClick={() => store.dispatch(getUser(row.organization_id))}
          >
            <Archive size={14} className='mr-50' />
            <span className='align-middle'>Edit</span>
          </DropdownItem>
          <DropdownItem className='w-100' onClick={() => store.dispatch(deleteUser(row.organization_id))}>
            <Trash2 size={14} className='mr-50' />
            <span className='align-middle'>Delete</span>
          </DropdownItem>
        </DropdownMenu>
      </UncontrolledDropdown>
    )
  }
]
