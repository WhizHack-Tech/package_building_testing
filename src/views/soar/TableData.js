// ================================================================================================
//  File Name: Table.js
//  Description: Details of the Soar.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { useState, useEffect, useRef, Fragment } from 'react'
// ** Third Party Components
import ReactPaginate from 'react-paginate'
import { Link } from 'react-router-dom'
import { ChevronDown, Link2, Copy } from 'react-feather'
import DataTable from 'react-data-table-component'
import axios from '@axios'
import { token } from '@utils'
import { useSelector } from 'react-redux'
import PreLoader from '../hids/preLoader'
// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, Badge, Nav, NavItem, NavLink, TabContent, TabPane, Row, Col, Button, Input, Label } from 'reactstrap'
import { jsPDF } from 'jspdf'
import 'jspdf-autotable'
import "./pdfStyles.css"
import { useTranslation } from 'react-i18next'
import CopyToClipboard from 'react-copy-to-clipboard'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

const DataTableWithButtons = () => {
    const { t } = useTranslation()
    const [currentPage, setCurrentPage] = useState(0)
    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])
    const filterState = useSelector((store) => store.dashboard_chart)
    const [checkApiData, setCheckApiData] = useState(true)
    const [searchQuery, setSearchQuery] = useState('')
    const [urlLink, setUrlLink] = useState([])

    useEffect(() => {
        axios.get(`user-soar-urls-details`, { headers: { Authorization: token() } }).then(res => {
            if (res.data.message_type === "success") {
                setUrlLink(res.data.data)
            }
        })
    }, [])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/soar-blocked-ips-table`, { headers: { Authorization: token() } })
            .then(res => {
                setApiLoader(false)

                if (res.data.message_type === "d_not_f") {
                    setCheckApiData(false)
                }

                if (res.data.message_type === "success") {
                    setCheckApiData(true)
                    setTableData(res.data.data)
                }
            })
            .catch(error => {
                setApiLoader(false)
                console.log(error.message)
            })
    }

    useEffect(() => {
        DetailsApiLogic()
    }, [filterState.values, filterState.refreshCount])
    const ExpandableTable = ({ data }) => {
        const [active, setActive] = useState('1')
        const ObjKeys = Object.keys(data)
        const ObjVal = Object.values(data)

        const ListTableData = () => {

            if (ObjKeys.length > 0) {
                return ObjKeys.map((values, i) => {
                    return (
                        <Row className="m-1" key={i}>
                            <p xs={2} md={2}>{values}: {JSON.stringify(ObjVal[i])}</ p>
                        </Row>
                    )
                })

            } else {
                return <p>{t('Data Not Found')}</p>
            }

        }

        const JsonRenderData = () => {

            if (ObjKeys.length > 0) {
                return <pre style={{ color: "#8177f2" }}> {JSON.stringify(data, null, '\t')} </pre>
            } else {
                return <p>{t('Data Not Found')}</p>
            }
        }


        const toggle = tab => {
            if (active !== tab) {
                setActive(tab)
            }
        }
        return (

            <Fragment>
                <div className='expandable-content'>
                    <Nav tabs>
                        <NavItem>
                            <NavLink
                                active={active === '1'}
                                onClick={() => {
                                    toggle('1')
                                }}
                            >
                                {t('Table')}
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink
                                active={active === '2'}
                                onClick={() => {
                                    toggle('2')
                                }}
                            >
                                {t('JSON')}
                            </NavLink>
                        </NavItem>

                    </Nav>
                    <TabContent className='py-50 ml-1' activeTab={active}>
                        <TabPane tabId='1'>
                            <ListTableData />
                        </TabPane>
                        <TabPane tabId='2'>
                            <JsonRenderData />
                        </TabPane>
                    </TabContent>
                </div>
            </Fragment>
        )
    }

    const filteredData = tableData.filter((row) => Object.values(row).some((value) => {
        return value !== null ? value.toString().toLowerCase().includes(searchQuery.toLowerCase()) : ''
    }))

    const handleSearch = (e) => {
        setSearchQuery(e.target.value.trim())
    }

    const Columns = [
        {
            name: t('Blocked IPS'),
            sortable: true,
            selector: row => row.blocked_ips,
            wrap: true,
            width: "180px"
        },
        {
            name: t('Target Endpoint'),
            sortable: true,
            selector: row => row.target_endpoint,
            wrap: true,
            width: "180px"
        },
        {
            name: t('Blocked IPS Count'),
            sortable: true,
            selector: row => row.blocked_ips_count,
            wrap: true,
            width: "180px"
        },
        {
            name: t('Source Feed'),
            sortable: true,
            selector: row => row.source_feed,
            wrap: true,
            width: "180px"
        },
        {
            name: t('Blocked IPS'),
            sortable: true,
            selector: row => row.blocked_ips_string,
            width: "780px"
        },
        {
            name: 'Copy',
            cell: (row) => (
                <CopyToClipboard text={JSON.stringify(row, null, '\t')}
                    onCopy={() => toast.success('Copied to clipboard')} // Use `toast.success` here
                >
                    <Copy size={14} />
                </CopyToClipboard>
            ),
            button: true,
            allowOverflow: true,
            wrap: true,
            width: '150px'
        }
    ]


    return (
        <Card>
            <CardHeader className='flex-md-row flex-column align-md-items-center align-items-start border-bottom'>
                <CardTitle className='fw-bolder mt-1' tag='h4'>{t('Soar')}</CardTitle>
                <div className='d-flex mt-md-0 mb-1'>
                    <div className='d-flex align-items-center mb-1 mr-1 mt-1'>
                        <a href={urlLink.soar_sensor_host_url} target="_blank" rel="noopener noreferrer">
                            <Button.Ripple
                                className='btn-icon'
                                color='primary'
                                size='sm'
                            >
                                Playbook <Link2 size={12} />
                            </Button.Ripple>
                        </a>

                    </div>
                </div>
            </CardHeader>
            <Row className='justify-content-end mx-0'>
                <Col className='d-flex align-items-center justify-content-end mt-1' md='6' sm='12'>
                    <Label className='me-1' for='search-input'>
                        {t('Search')}
                    </Label>
                    <Input
                        className='dataTable-filter mb-50'
                        type='text'
                        bsSize='sm'
                        id='search-input'
                        value={searchQuery}
                        onChange={handleSearch}
                        placeholder='Search...'
                    />
                </Col>
            </Row>
            <div className='react-dataTable'>
                {checkApiData ? (
                    <DataTable
                        noHeader
                        pagination
                        data={filteredData}
                        expandableRows
                        columns={Columns}
                        paginationPerPage={10}
                        expandOnRowClicked
                        className='react-dataTable'
                        sortIcon={<ChevronDown size={10} />}
                        paginationDefaultPage={currentPage + 1}
                        expandableRowsComponent={ExpandableTable}
                        paginationRowsPerPageOptions={[10, 25, 50, 100]}
                    />
                ) : (
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                        <p>{t('Data Not Found')}</p>
                    </div>
                )}
            </div>
            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default DataTableWithButtons
