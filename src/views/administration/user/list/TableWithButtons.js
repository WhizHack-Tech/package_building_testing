// ================================================================================================
//  File Name: TableWithButton.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
// ** React Imports
import { Fragment, useState, forwardRef, useContext, useEffect } from 'react'
import { Link } from 'react-router-dom'
// ** Table Data & Columns
import { columns } from './data'
import { AbilityContext } from '@src/utility/context/Can'
// ** Add New Modal Component
// import AddNewModal from './AddNewModal'
// import Location from './Location'
import { getAllData } from '../store/action'
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
import "../Loader.css"

import { useDispatch, useSelector } from 'react-redux'

// ** Bootstrap Checkbox Component
const BootstrapCheckbox = forwardRef(({ onClick, ...rest }, ref) => (
  <div className='custom-control custom-checkbox'>
    <input type='checkbox' className='custom-control-input' ref={ref} {...rest} />
    <label className='custom-control-label' onClick={onClick} />
  </div>
))

const TableWithButtons = () => {
  const ability = useContext(AbilityContext)

  const dispatch = useDispatch()
  const store = useSelector(state => state.users)

  const [currentPage, setCurrentPage] = useState(0)
  const [searchValue, setSearchValue] = useState('')
  const [filteredData, setFilteredData] = useState([])


  useEffect(() => {
    if (store.data.length === 0) {
      dispatch(getAllData())
    }
  }, [])
  // ** Function to handle filter
  const handleFilter = e => {
    const value = e.target.value.trim()
    let updatedData = []
    setSearchValue(value)


    if (value.length) {
      updatedData = store.data.filter(item => {
        const startsWith =
          item.organization_name.toLowerCase().startsWith(value.toLowerCase()) ||
          item.email.toLowerCase().startsWith(value.toLowerCase()) ||
          item.city.toLowerCase().startsWith(value.toLowerCase()) ||
          item.phone_number.toLowerCase().startsWith(value.toLowerCase()) ||
          item.branchcode.toLowerCase().startsWith(value.toLowerCase()) ||
          item.city.toLowerCase().startsWith(value.toLowerCase())
        const includes =
          item.organization_name.toLowerCase().includes(value.toLowerCase()) ||
          item.email.toLowerCase().includes(value.toLowerCase()) ||
          item.city.toLowerCase().includes(value.toLowerCase()) ||
          item.phone_number.toLowerCase().startsWith(value.toLowerCase()) ||
          item.branchcode.toLowerCase().startsWith(value.toLowerCase()) ||
          item.city.toLowerCase().includes(value.toLowerCase())
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
      pageCount={searchValue.length ? filteredData.length / 7 : store.data.length / 7 || 1}
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
          <CardTitle tag='h4'>Organization Settings</CardTitle>
          <div className='d-flex mt-md-0 mt-1'>
            {ability.can('read', 'all') ? (
              <>
                {/* <div className='d-flex align-items-center mb-sm-0 mb-1 mr-2'>
                  <Button.Ripple color='primary' onClick={handleModal}>
                    Attach Sensor
                  </Button.Ripple>
                </div> */}
                <div className='d-flex align-items-center mb-sm-0 mb-1 mr-2'>
                  <Button.Ripple color='primary'
                    tag={Link}
                    to={`/addlocation`}
                    className='w-100'
                  >
                    Attach Location
                  </Button.Ripple>
                </div>
                <Button.Ripple color='primary'
                  tag={Link}
                  to={`/administration/account-settings/`}
                  className='w-100'
                >
                  Add New Org
                </Button.Ripple>
              </>
            ) : null}
          </div>
        </CardHeader>
        <Row className='justify-content-end mx-0'>
          <Col className='d-flex align-items-center justify-content-end mt-1' md='3' sm='6'>
            <Label className='mr-1' for='search-input'>
              Search
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
        {(store.loading === false) ? <div className='d-flex justify-content-center align-items-center' style={{ height: '210px' }}> <div class="tri-color-ripple-spinner">
            <div class="ripple ripple1"></div>
            <div class="ripple ripple2"></div>
          </div> </div> : ""}
        <DataTable
          noHeader
          pagination
          columns={columns}
          paginationPerPage={10}
          className='react-dataTable'
          paginationDefaultPage={currentPage + 1}
          // paginationComponent={CustomPagination}
          data={searchValue.length ? filteredData : store.data}
          selectableRowsComponent={BootstrapCheckbox}
        />
      </Card>
      {/* <AddNewModal open={modal} handleModal={handleModal} /> */}
      {/* <Location open={modal1} handleModal1={handleModal1} /> */}
    </Fragment>
  )
}

export default TableWithButtons
