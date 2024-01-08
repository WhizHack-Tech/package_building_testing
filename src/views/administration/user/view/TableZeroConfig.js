// ================================================================================================
//  File Name: TableZeroConfig.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
// ** Table Columns
import { data, basicColumns } from './data'

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
  const [loading, setLoading] = useState(null)
 
  useEffect(() => {
    axios.get(`/show-user-org-count?location_id=${id}`, { headers: { Authorization: token()} }).then(response => {
    setData(response.data)
    setLoading(true)
    })
  }, [])
  return (
    <Card>
      <DataTable
        noHeader
        pagination
        data={data}
        paginationPerPage={5}
        columns={basicColumns}
        className='react-dataTable'
        sortIcon={<ChevronDown size={10} />}
        paginationRowsPerPageOptions={[10, 25, 50, 100]}
      />
    </Card>
  )
}

export default DataTablesBasic
