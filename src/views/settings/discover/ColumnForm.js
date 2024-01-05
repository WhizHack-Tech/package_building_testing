// ================================================================================================
//  File Name: ColumnFrom.js
//  Description: Details of the Discover Data.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Card, CardHeader, CardTitle, CardBody, FormGroup, Input, CustomInput, Label, Row, Col, Button, InputGroup, InputGroupAddon, InputGroupText, Form, Spinner } from 'reactstrap'
import SearchTable from "./searchTable"
import { toast } from 'react-toastify'
import { useState, Fragment, usestate, useEffect } from 'react'
import * as Icons from 'react-feather'
import axios from "@axios"
import { useTranslation } from 'react-i18next'
import { token, selectThemeColors } from '@utils'
import { splitWord } from '../../../utility/helpers'
import Select from 'react-select'

const ColumnForm = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [tableLoading, setTableLoading] = useState(false)
  const [tableData, setTableData] = useState([])
  const [searchVal, setSearchVal] = useState({ search_val: null, col_name: null, index_name: null })
  const [indexName, setIndexName] = useState([])

  useEffect(() => {
    axios.get(`/innovative-search-get-indices-name`, { headers: { Authorization: token() } })
      .then((res) => {
        if (res.data.message_type === "success") {
          setIndexName(res.data.data.indices)
          console.log(res.data.data.indices)
        }
      })
  }, [])

  const formSubmit = (event) => {
    event.preventDefault()

    let search_val = event.target.search_val.value
    let col_name = event.target.col_name.value
    let index_name = event.target.index_name.value

    setSearchVal({
      search_val: event.target.search_val.value,
      col_name: event.target.col_name.value,
      index_name: event.target.index_name.value
    })

    setLoading(true)
    setTableLoading(false)

    axios.get(`/innovative-search-api?search_val=${search_val}&index_name=${index_name}&col_name=${col_name}&limit=${20}`, { headers: { Authorization: token() } })
      .then(res => {

        if (res.data.message_type === "data_ok") {
          setTableLoading(true)
          setTableData(res.data.data)
        }

        if (res.data.message_type === "data_not_found") {
          toast.warn(t('Data Not Found'), {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined
          })
        }

        if (res.data.message_type === "s_is_wrong") {
          if (res.data.search_val !== undefined) {
            toast.warn(t('Search value is empty'), {
              position: "top-right",
              autoClose: 5000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true,
              progress: undefined
            })
          }
        }

        setLoading(false)
      })
      .catch(err => {
        setLoading(true)
      })
  }

  return (
    <Fragment>
      <Card>
        <CardHeader>
          <CardTitle tag='h4'>{t('Discover Data')}</CardTitle>
        </CardHeader>
        <CardBody>
          <Form onSubmit={formSubmit}>
            <Row>
              <Col md={4}>
                <FormGroup>
                  <Label for='index_name'>{t('Select Index')}</Label>
                  <Select
                    id="index_name"
                    isClearable={false}
                    theme={selectThemeColors}
                    name='index_name'
                    options={
                      Array.isArray(indexName) ? (
                        indexName.map((list) => ({
                          value: list,
                          label: splitWord(list),
                          color: '#00B8D9',
                          isFixed: true
                        }))
                      ) : (
                        [] // or handle the case when indexName is not an array
                      )
                    }
                    className='react-select'
                    classNamePrefix='select'
                  />
                </FormGroup>
              </Col>
              <Col md='4'>
                <FormGroup>
                  <Label for='select'>{t('Select')}</Label>
                  <Input type='select' name='col_name'>
                    <option value='' selected disabled>Select...</option>
                    <option value='attacker_ip'>{t('Attacker IPs')}</option>
                    <option value='target_ip'>{t('Target IP')}</option>
                  </Input>
                </FormGroup>
              </Col>
              <Col md='4'>
                <div className='mt-2'>
                  <InputGroup className='input-group-merge' tag={FormGroup}>
                    <InputGroupAddon addonType='prepend'>
                      <InputGroupText>
                        <Icons.Search size={14} />
                      </InputGroupText>
                    </InputGroupAddon>
                    <Input
                      name="search_val"
                      placeholder='Search ...'
                    />
                  </InputGroup>
                </div>
              </Col>
              <Col md='2'>
                <div className='mb-1'>
                  {(loading === false) ? <Button.Ripple color='primary' type="submit">{t('Generate')}</Button.Ripple> : <Button.Ripple type="button" color='primary' disabled> <Spinner size="sm" />&nbsp;{t('Checking')}</Button.Ripple>}
                </div>
              </Col>
            </Row>
          </Form>
        </CardBody>
      </Card>
      <Card>
        {(tableLoading) ? <SearchTable tableData={tableData} searchVal={searchVal} /> : ""}
      </Card>
    </Fragment>
  )
}

export default ColumnForm