// ================================================================================================
//  File Name: TableZeroConfig.js
//  Description: Details of the Dashboard ( Agent ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard.
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Table Columns
import { useState, useEffect } from 'react'
import { data, basicColumns } from './data'
import axios from '@axios'
import { token } from '@utils'
import "../../administration/user/Loader.css"
// ** Third Party Components
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle, Spinner } from 'reactstrap'
import { useParams } from 'react-router-dom'

const DataTablesBasic = () => {
  const { org_location } = useParams()
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(null)

  useEffect(() => {
    axios.get(`/allagent/?location_id=${org_location}`, { headers: { Authorization: token() } }).then((res) => {
      if (res.data.message_type === 'success') {
        setData(res.data.data)
        setLoading(true)
      }
    })
  }, [])
 
  // useEffect(() => {
  //   axios.get('/allagent/').then(response => {
  //   setData(response.data)
  //   setLoading(true)
  //   })
  // }, [])
  
  return (
    <Card>
      <CardHeader>
        <CardTitle tag='h4'>Agents Details</CardTitle>
      </CardHeader>
      {loading ? loading : <div className='d-flex justify-content-center align-items-center' style={{ height: '210px' }}> <div class="tri-color-ripple-spinner">
            <div class="ripple ripple1"></div>
            <div class="ripple ripple2"></div>
          </div> </div>}
      <DataTable
        noHeader
        pagination
        data={data}
        columns={basicColumns}
        className='react-dataTable'
        sortIcon={<ChevronDown size={10} />}
        paginationRowsPerPageOptions={[10, 25, 50, 100]}
      />
    </Card>
  )
}

export default DataTablesBasic
