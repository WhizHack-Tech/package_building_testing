// ================================================================================================
//  File Name: ApiTable.js
//  Description: Show the Api key Details in Table.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================

// ** React Imports
import { Fragment, useState, forwardRef, useEffect } from 'react'
import { Eye, Copy, Globe} from 'react-feather'
// ** Table Data & Columns
import axios from '@axios'
import { token } from '@utils'
// ** Add New Modal Component
import AddApikey from './AddApikey'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
// ** Third Party Components
import ReactPaginate from 'react-paginate'
import { toast } from 'react-toastify'
import DataTable from 'react-data-table-component'
import {
  Card,
  CardHeader,
  CardTitle,
  Button,
  Input,
  Label,
  Row,
  Col,
  Spinner,
  Badge, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem
} from 'reactstrap'

const DataTableWithButtons = () => {
  const { t } = useTranslation()
  const [tableData, setTableData] = useState([])
  const [loading, setLoading] = useState(false)
  const [apiStatus, setApiStatus] = useState(false)
  // ** States
  const [modal, setModal] = useState(false)
  // ** Function to handle Modal toggle
  const handleModal = () => setModal(!modal)

  useEffect(() => {
    axios.get('/display-third-party-api-key', { headers: { Authorization: token() } }).then(res => {
      if (res.data.message_type === 'data_found') {
      setTableData(res.data.data)
      setLoading(true)
      }
    })
  }, [])

  const api_key_status = {
    true: { title: 'Active', color: 'light-success' },
    false: { title: 'Deactive', color: 'light-danger' }
  }
  const api_type = {
    1: { name: 'GET' },
    2: { name: 'POST' },
    default: { name: 'Unknown' }
  }

  const copyApiKey = (row) => {
    const apiKey = row.api_key
    if (apiKey) {
      navigator.clipboard.writeText(apiKey).then(
        function () {
          toast.success("Key Name Copied")
        },
        function (err) {
          console.error('Async: Could not copy text: ', err.message)
        }
      )
    }
  }

  const columnsName = [
    {
      name: t('Api Type'),
      sortable: true,
      selector: row => row.api_type,
      minWidth: '100px',
      cell: row => {
        // Check if the api_type[row.api_type] exists, if not, use the default value
        const apiTypeTitle = api_type[row.api_type]?.name || api_type.default.name
        return (
          <div>
            {apiTypeTitle}
          </div>
        )
      }
    },
    // {
    //   name: t('Product Name'),
    //   sortable: true,
    //   selector: row => row.product_name,
    //   minWidth: '100px'
    // },
    {
      name: t('Product Name'),
      sortable: true,
      selector: row => row.product_name,
      minWidth: '100px',
      cell: row => {
        return (
          <div>
            {row.product_name.map((log, index) => (
              <div key={index}>{log}</div>
            ))}
          </div>
        )
      }
    },
    {
      name: t('Product Logs'),
      sortable: true,
      selector: row => row.product_logs_name,
      minWidth: '100px',
      cell: row => {
        return (
          <div>
            {row.product_logs_name.map((log, index) => (
              <div key={index}>{log}</div>
            ))}
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
    },
    {
      name: t('Date'),
      selector: row => row.created_at,
      sortable: true,
      minWidth: '100px',
      cell: row => {
        return (
          <div className='d-flex justify-content-left align-items-center'>
            <span className='font-weight-bold text-uppercase'>{format(new Date(row.created_at), "yyyy-MM-dd, h:mm:ss a")}</span>
          </div>
        )
      }
    },
    {
      name: t('URL'),
      sortable: true,
      selector: row => row.url,
      minWidth: '450px',
      cell: row => {
        return (
          <div className='d-flex justify-content-left align-items-center'>
            <Globe size={15} className='mb-0' />&nbsp;
            <span className='font-weight-bold'>{row.url}</span>
          </div>
        )
      }
    },
    {
      name: t('Key'),
      sortable: true,
      selector: row => row,
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
                  <span className='align-middle ml-50' onClick={() => copyApiKey(row)}>
                    <Copy size={15}/> {row.api_key}
                  </span>
                </DropdownItem>
              </DropdownMenu>
            </UncontrolledDropdown>
          </div>
        )
      }
    }
    
  ]

  return (
    <Fragment>
      <Card>
        <CardHeader className='flex-md-row flex-column align-md-items-center align-items-start border-bottom'>
          <CardTitle tag='h2'>{t('Applications')}</CardTitle>
          <div className='d-flex mt-md-0 mt-1'>
            <Button className='ml-2' color='primary' onClick={handleModal}>
              <span className='align-middle ml-50'>{t('Create Api key')}</span>
            </Button>
          </div>
        </CardHeader>
        {/* <Row className='justify-content-end mx-0'>
          <Col className='d-flex align-items-center justify-content-end mt-1' md='6' sm='12'>
            <Label className='mr-1' for='search-input'>
              {t('Search')}
            </Label>
            <Input
              className='dataTable-filter mb-50'
              type='text'
              bsSize='sm'
              id='search-input'
              value={searchValue}
              onChange={handleFilter}
            />
          </Col>
        </Row> */}
        {loading ? loading : <div className='d-flex justify-content-center'><Spinner color='primary' type='grow' className="mt-5" /></div>}
        <DataTable
          noHeader
          pagination
          columns={columnsName}
          data={tableData}
          paginationPerPage={10}
          className='react-dataTable'
          paginationRowsPerPageOptions={[10, 25, 50, 100]}
        />
      </Card>
      <AddApikey open={modal} handleModal={handleModal} />
    </Fragment>
  )
}

export default DataTableWithButtons