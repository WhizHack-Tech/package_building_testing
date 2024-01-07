   // ================================================================================================
//  File Name:  Table.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
// ** React Imports
import { Fragment, useState, forwardRef, useEffect } from 'react'

// ** Table Data & Columns
import { columns } from './data'

// ** Add New Modal Component
import AddNewModal from './AddNewModal'
import { useTranslation } from 'react-i18next'
// ** Third Party Components
import ReactPaginate from 'react-paginate'
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
  Spinner
} from 'reactstrap'
// ** axios base url
import axios from '@axios'
// ** Authorization token  
import { token } from '@utils'

// ** Bootstrap Checkbox Component
const BootstrapCheckbox = forwardRef(({ onClick, ...rest }, ref) => (
  <div className='custom-control custom-checkbox'>
    <input type='checkbox' className='custom-control-input' ref={ref} {...rest} />
    <label className='custom-control-label' onClick={onClick} />
  </div>
))

const DataTableWithButtons = () => {
  // ** States
  const {t} = useTranslation()
  const [modal, setModal] = useState(false)
  const [currentPage, setCurrentPage] = useState(0)
  const [searchValue, setSearchValue] = useState('')
  const [filteredData, setFilteredData] = useState([])
  const [data, setData] = useState([])
  const [loadingData, setLoadingData] = useState(false)
// **  axios api of get ("User list" of particular Organization data )
  useEffect(() => {
    axios.post('/sub-clients', {}, { headers: { Authorization: token() } }).then(res => {
      setData(res.data)
      setLoadingData(true)
    })
  }, [])

  // ** Function to handle Modal toggle
  const handleModal = () => setModal(!modal)

  // ** Function to handle filter
  const handleFilter = (e) => {
    const value = e.target.value.trim() // Trim the input value
    let updatedData = []
    setSearchValue(value)
  
    const status = {
      1: { title: 'Current', color: 'light-primary' },
      2: { title: 'Professional', color: 'light-success' },
      3: { title: 'Rejected', color: 'light-danger' },
      4: { title: 'Resigned', color: 'light-warning' },
      5: { title: 'Applied', color: 'light-info' }
    }
    
    // Function to search and handle filter
    if (value.length) {
      updatedData = data.filter((item) => {
        const startsWith =
          item.first_name.toLowerCase().startsWith(value.toLowerCase()) ||
          item.last_name.toLowerCase().startsWith(value.toLowerCase()) ||
          item.email.toLowerCase().startsWith(value.toLowerCase()) ||
          item.contact_number.toLowerCase().startsWith(value.toLowerCase())
  
        const includes =
          item.first_name.toLowerCase().includes(value.toLowerCase()) ||
          item.last_name.toLowerCase().includes(value.toLowerCase()) ||
          item.email.toLowerCase().includes(value.toLowerCase()) ||
          item.contact_number.toLowerCase().includes(value.toLowerCase())
  
        if (startsWith) {
          return startsWith
        } else if (!startsWith && includes) {
          return includes
        } else return null
      })
      setFilteredData(updatedData)
      setSearchValue(value)
    }
  }
  

  // ** Function to handle Pagination
  const handlePagination = page => {
    setCurrentPage(page.selected)
  }

  // ** Custom Pagination
  const CustomPagination = () => (
    <ReactPaginate
      previousLabel=''
      nextLabel=''
      forcePage={currentPage}
      onPageChange={page => handlePagination(page)}
      pageCount={searchValue.length ? filteredData.length / 7 : data.length / 7 || 1}
      breakLabel='...'
      pageRangeDisplayed={2}
      marginPagesDisplayed={2}
      activeClassName='active'
      pageClassName='page-item'
      breakClassName='page-item'
      breakLinkClassName='page-link'
      nextLinkClassName='page-link'
      nextClassName='page-item next'
      previousClassName='page-item prev'
      previousLinkClassName='page-link'
      pageLinkClassName='page-link'
      containerClassName='pagination react-paginate separated-pagination pagination-sm justify-content-end pr-1 mt-1'
    />
  )

  return (
    <Fragment>
      <Card>
        <CardHeader className='flex-md-row flex-column align-md-items-center align-items-start border-bottom'>
          <CardTitle tag='h2'>{t('Users List')}</CardTitle>
          <div className='d-flex mt-md-0 mt-1'>
            <div className='d-flex align-items-center mb-sm-0 mb-1 mr-2'>
              <Button.Ripple color='primary' onClick={handleModal}>
                {t('Add User')}
              </Button.Ripple>
            </div>
          </div>
        </CardHeader>
        <Row className='justify-content-end mx-0'>
          <Col className='d-flex align-items-center justify-content-end mt-1' md='3' sm='6'>
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
        </Row>
        { loadingData ? <DataTable
          noHeader
          pagination
          columns={columns({t})}
          paginationPerPage={10}
          className='react-dataTable'
          paginationDefaultPage={currentPage + 1}
          // paginationComponent={CustomPagination}
          data={searchValue.length ? filteredData : data}
          selectableRowsComponent={BootstrapCheckbox}
        /> :  <div className='text-center m-5'><Spinner color='primary' type='grow' /></div> }
      </Card>
      <AddNewModal open={modal} handleModal={handleModal} />
    </Fragment>
  )
}

export default DataTableWithButtons
