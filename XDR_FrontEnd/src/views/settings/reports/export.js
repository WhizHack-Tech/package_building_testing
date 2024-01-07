// ================================================================================================
//  File Name: export.js
//  Description: Details of the Static Report Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useState, useRef, useEffect } from 'react'
import XLSX from 'xlsx'
import {
  Row,
  Col,
  Card,
  Table,
  CardHeader,
  CardTitle,
  UncontrolledButtonDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem
} from 'reactstrap'
import jsPDF from 'jspdf'
import 'jspdf-autotable'
import { Share, FileText, Grid } from 'react-feather'
import { useTranslation } from 'react-i18next'

const Export = ({ data }) => {
  const { t } = useTranslation()
  const tableRef = useRef()

  const [colNames, setColNames] = useState({
    title: [],
    key: []
  })

  function convertKeysToTitleCase(obj) {
    const colName = {
      title: [],
      key: []
    }

    Object.keys(obj).map((key, index) => {

      const words = key.split("_")
      const titleCaseWords = words.map(
        (word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
      )

      colName.title[index] = titleCaseWords.join(" ")
      colName.key[index] = key
    })

    return colName
  }

  useEffect(() => {

    if (data.length > 0) {
      setColNames(convertKeysToTitleCase(data[0]))
    }

  }, [data.length])

  // ** Converts table to CSV
  function convertArrayOfObjectsToCSV(array) {
    let result

    const columnDelimiter = ','
    const lineDelimiter = '\n'
    const keys = Object.keys(data[0])

    result = ''
    result += keys.join(columnDelimiter)
    result += lineDelimiter

    array.forEach(item => {
      let ctr = 0
      keys.forEach(key => {
        if (ctr > 0) result += columnDelimiter

        result += item[key]

        ctr++
      })
      result += lineDelimiter
    })

    return result
  }

  // ** Downloads CSV
  function downloadCSV(array) {
    const link = document.createElement('a')
    let csv = convertArrayOfObjectsToCSV(array)
    if (csv === null) return

    const filename = 'XDR Report.csv'

    if (!csv.match(/^data:text\/csv/i)) {
      csv = `data:text/csv;charset=utf-8,${csv}`
    }

    link.setAttribute('href', encodeURI(csv))
    link.setAttribute('download', filename)
    link.click()
  }

  // ** download PDF
  const downloadPdf = () => {

    let dataArr = []

    dataArr = data.map((row, index) => {
      return colNames.key.map((colName, i) => {
        return row[colName]
      })
    }
    )

    const doc = new jsPDF({
      orientation: 'l'
    })

    doc.text("XDR Report", 14, 10)
    doc.autoTable({
      theme: "striped",
      // data: data.map(data => ({ ...data, ObjectKey: data.columns })),
      head: [[...colNames.title]],
      body: dataArr
    })

    doc.save('XDR Report.pdf')
  }

  // ** download xlsx
  const downloadExcel = () => {
    const workSheet = XLSX.utils.json_to_sheet(data)
    const workBook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workBook, workSheet, "table")
    //Buffer
    XLSX.write(workBook, { bookType: "xlsx", type: "buffer" })
    //Binary string
    XLSX.write(workBook, { bookType: "xlsx", type: "binary" })
    //Download
    XLSX.writeFile(workBook, "XDR Report.xlsx")
  }

  return (
    <Fragment>
      <Row className='export-component'>
        <Col sm='12'>
          <Card>
            <CardHeader>
              <CardTitle tag='h2'>{t('Filter Data')}</CardTitle>
              <div className='d-flex justify-content-end flex-wrap flex-sm-row flex-column'>
                <UncontrolledButtonDropdown>
                  <DropdownToggle color='secondary' caret outline>
                    <Share size={15} />
                    <span className='align-middle ml-50'>{t('Export')}</span>
                  </DropdownToggle>
                  <DropdownMenu right>
                    <DropdownItem className='w-100' onClick={() => downloadCSV(data)}>
                      <FileText size={15} />
                      <span className='align-middle ml-50'>{t('CSV')}</span>
                    </DropdownItem>
                    <DropdownItem className='w-100' onClick={() => downloadExcel(data)}>
                      <Grid size={15} />
                      <span className='align-middle ml-50'>{t('Excel')}</span>
                    </DropdownItem>
                    <DropdownItem className='w-100' onClick={() => downloadPdf(data)}>
                      <Grid size={15} />
                      <span className='align-middle ml-50'>{t('PDF')}</span>
                    </DropdownItem>
                  </DropdownMenu>
                </UncontrolledButtonDropdown>
              </div>
            </CardHeader>
            <Table innerRef={tableRef} className='table-hover-animation ml-1' responsive>
              <thead>
                <tr>
                  {colNames.title.length > 0 && colNames.title.map((row, index) => (
                    <td key={index}>{row.toUpperCase()}</td>
                  ))}
                </tr>
              </thead>
              <tbody>
                {
                  data.map((row, index) => (
                    <tr key={index}>
                      {colNames.key.map((colName, i) => (
                        <td key={i}>
                          {row[colName]}
                        </td>
                      ))}
                    </tr>
                  ))
                }
              </tbody>
            </Table>
          </Card>
        </Col>
      </Row>
    </Fragment>
  )
}

export default Export