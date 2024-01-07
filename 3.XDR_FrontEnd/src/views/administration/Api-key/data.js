// ================================================================================================
//  File Name: data.js
//  Description: Row Fields.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================

import { Eye } from 'react-feather'
import { Badge, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap'
import { toast } from 'react-toastify'
import { format } from 'date-fns'

const api_key_status = {
  true: { title: 'Active', color: 'light-success' },
  false: { title: 'Deactive', color: 'light-danger' }
}

export const Columns = ({ t }) => {
  const copyApiKey = event => {
    let copyCodeText = event.target.innerText
    navigator.clipboard.writeText(copyCodeText).then(function () {
      toast.success("Key Name Copied")
    }, function (err) {
      console.error('Async: Could not copy text: ', err.message)
    })
  }

  return [
    {
      name: t('Product Type'),
      sortable: true,
      selector: row => row.product_name,
      minWidth: '50px'
    },
    {
      name: t('Api Type'),
      sortable: true,
      selector: row => row.api_type,
      minWidth: '80px'
    },
    {
      name: t('Product Log'),
      sortable: true,
      selector: row => row.product_logs_name,
      minWidth: '250px'
    },
    {
      name: t('Key'),
      allowOverflow: true,
      minWidth: '80px',
      cell: row => {
        return (
          <div className='d-flex'>
            <UncontrolledDropdown>
              <DropdownToggle className='pr-1' tag='span'>
                <Eye size={15} />
              </DropdownToggle>
              <DropdownMenu down>
                <DropdownItem tag='span' className='w-100'>
                  <span className='align-middle ml-50' onClick={copyApiKey}>{row.api_key}</span>
                </DropdownItem>
              </DropdownMenu>
            </UncontrolledDropdown>
          </div>
        )
      }
    },
    {
      name: t('Date'),
      selector: row => row.created_at,
      sortable: true,
      cell: row => {
        return (
          <div className='d-flex justify-content-left align-items-center'>
            <span className='font-weight-bold text-uppercase'>{format(new Date(row.created_at), "yyyy-MM-dd, h:mm:ss a")}</span>
          </div>
        )
      }
    },
    {
      name: t('Status'),
      selector: row => row.api_key_status,
      sortable: true,
      cell: row => {
        return (
          <Badge color={api_key_status[row.api_key_status].color} pill>
            {api_key_status[row.api_key_status].title}
          </Badge>
        )
      }
    }
  ]
}
export default Columns