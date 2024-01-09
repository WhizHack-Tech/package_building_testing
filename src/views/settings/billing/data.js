// ================================================================================================
//  File Name: data.js
//  Description: Details of the Setting ( Reducer ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** Custom Components
import Avatar from '@components/avatar'
import { Link } from 'react-router-dom'
// ** Third Party Components
import { Eye } from 'react-feather'

// ** Renders Client Columns
const renderClient = row => {
  const stateNum = Math.floor(Math.random() * 6),
    states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
    color = states[stateNum]

  if (row.billing_image) {
    return <Avatar className='mr-1' img={row.billing_image} width='32' height='32' />
  } else {
    return <Avatar color={color || 'primary'} className='mr-1' content={row.billing_types || 'John Doe'} initials />
  }
}

// ** Table Common Column
export const columns = [
  {
    name: 'Billing Cycle Type',
    selector: 'billing_types',
    sortable: true,
    minWidth: '150px',
    cell: row => (
      <div className='d-flex justify-content-left align-items-center'>
        {renderClient(row)}
        <div className='d-flex flex-column'>
            <span className='font-weight-bold'>{row.billing_types}</span>
        </div>
      </div>
    )
  },
  {
    name: 'Description',
    selector: 'billing_descriptions',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: 'Descriptions',
    selector: 'billing_descriptions',
    sortable: true,
    minWidth: '250px'
  },
  {
    name: 'Actions',
    minWidth: '100px',
    sortable: true,
    cell: row => (
      <div className='column-action d-flex align-items-center'>
        <Link to={`/settings/billingedit/${row.id}`} id={`pw-tooltip-${row.id}`}>
          <Eye size={17} className='mx-1' />
        </Link>
      </div>
    )
  }
]

export default columns
