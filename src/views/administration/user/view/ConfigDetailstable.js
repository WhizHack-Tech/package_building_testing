// ================================================================================================
//  File Name: ConfigDetails.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
// ** Table Columns
import ExpandableTable, { columns } from './data'

// ** Third Party Components
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle } from 'reactstrap'
import { useState, useEffect } from 'react'
import axios from '@axios'
import { token } from '@utils'
import { useParams } from "react-router-dom"
const DataTablesBasic = () => {
  const { id } = useParams()
  const [data, setData] = useState([])
  const [stepdata, setStepdata] = useState([])
  const [loading, setLoading] = useState(null)
 
  useEffect(() => {
    axios.get(`/get-location-details-org_id?org_id=${id}`, { headers: { Authorization: token()} }).then(response => {
    setData(response.data)
    console.log(response.data)
    setLoading(true)
    })
  }, [])
  //  useEffect(() => {
  //   axios.get(`http://localhost:3009/location`).then(response => {
  //     setData(response.data)
  //     setStepdata(response.data.location)
  //   console.log(response.data.location)
  //   })
  // }, [])

  return (
    <Card>
      <DataTable
        noHeader
        pagination
        expandableRows
        expandOnRowClicked
        data={data}
        paginationPerPage={5}
        columns={columns}
        className='react-dataTable'
        expandableRowsComponent={<ExpandableTable />}
        sortIcon={<ChevronDown size={10} />}
        paginationRowsPerPageOptions={[10, 25, 50, 100]}
      />
    </Card>
  )
}

export default DataTablesBasic
