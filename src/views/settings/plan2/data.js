// ================================================================================================
//  File Name: data.js
//  Description: Details of the Setting ( Plan ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** Custom Components
import Avatar from '@components/avatar'
import { Link } from 'react-router-dom'

// ** Third Party Components
import { Columns, Eye } from 'react-feather'

// ** Renders Client Columns
const renderClient = row => {
  const stateNum = Math.floor(Math.random() * 6),
    states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
    color = states[stateNum]

  if (row.avatar) {
    return <Avatar className='mr-1' img={row.avatar} width='32' height='32' />
  } else {
    return <Avatar color={color || 'primary'} className='mr-1' content={row.plan_name || 'John Doe'} initials />
  }
}

// ** Table Common Column
export const columns = [
  {
    name: 'Plan Name',
    selector: 'plan_name',
    sortable: true,
    minWidth: '150px',
    cell: row => (
      <div className='d-flex justify-content-left align-items-center'>
        {renderClient(row)}
        <div className='d-flex flex-column'>
            <span className='font-weight-bold'>{row.plan_name}</span>
        </div>
      </div>
    )
  },
  {
    name: 'Start Date',
    selector: 'plan_start_date',
    sortable: true,
    minWidth: '350px'
  },
  {
    name: 'End Date',
    selector: 'plan_end_date',
    sortable: true,
    minWidth: '250px'
  },
  {
    name: 'Description',
    selector: 'plan_descriptions',
    sortable: true,
    minWidth: '250px'
  },
  {
    name: 'Actions',
    minWidth: '150px',
    sortable: true,
    cell: row => (
      <div className='column-action d-flex align-items-center'>
        <Link to={`/settings/planedit/${row.id}`} id={`pw-tooltip-${row.id}`}>
          <Eye size={17} className='mx-1' />
        </Link>
      </div>
    )
  }
]

export default Columns
