// ================================================================================================
//  File Name: Sidebar.js
//  Description: Details of the Dynamic Report.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import PerfectScrollbar from 'react-perfect-scrollbar'
import { Plus, X } from "react-feather"
import { Card, CardBody, Label, Input, Button } from "reactstrap"
import { Fragment, useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Select from 'react-select'
import { selectThemeColors } from '@utils'
import { addSelectedListItem, removeSelectedListItem, setIndexData } from './store/actions'
import { splitWord } from '../../../utility/helpers'
import PreLoader from './preLoader'
import "./reports.css"
import { useTranslation } from 'react-i18next'

const SideBar = () => {
    const { t } = useTranslation()
    const { loading, availableList, selectedList, defaultIndexName, indexNameList } = useSelector(state => state.reports_exports)
    const filterState = useSelector((store => store.dashboard_chart))
    const [colFilteredData, setColFilteredData] = useState([])

    const dispatch = useDispatch()

    useEffect(() => {

        if (defaultIndexName) {
            dispatch(setIndexData(defaultIndexName, filterState.values ? filterState.values : 'last_1_hour'))
        }

    }, [filterState.values, filterState.refreshCount])

    const handleFilter = (e) => {
        const value = e.target.value.trim()

        let updatedData = []

        if (value.length) {
            updatedData = availableList.filter((item) => {

                const startsWith =
                    item.toLowerCase()
                        .startsWith(value.trim().toLowerCase())

                const includes =
                    item.toLowerCase()
                        .includes(value.trim().toLowerCase())

                return startsWith || includes
            })
        }

        setColFilteredData(updatedData)
    }

    const colFilterRender = colFilteredData.length ? colFilteredData : availableList

    return (
        <Card>
            <CardBody>
                <Fragment>
                    <h6 className='section-label text-secondary'>{t('Index Names')}</h6>
                    <Select
                        isClearable={false}
                        theme={selectThemeColors}
                        className='react-select'
                        classNamePrefix='select'

                        options={
                            indexNameList.map((list) => ({
                                value: list,
                                label: splitWord(list),
                                color: '#00B8D9',
                                isFixed: true
                            }))
                        }

                        value={
                            {
                                value: defaultIndexName,
                                label: splitWord(defaultIndexName),
                                color: '#00B8D9',
                                isFixed: true
                            }
                        }

                        onChange={(e) => {
                            dispatch(setIndexData(e.value, filterState.values ? filterState.values : 'last_1_hour'))
                        }}
                    />
                    <div className='d-flex align-items-center flex-wrap mt-1'>
                        <h6 className='section-label text-secondary'>
                            Search Field Names
                        </h6>
                        <Input
                            className='mb-50 col-search-input'
                            type='text'
                            bsSize='sm'
                            id='col-search-input'
                            onKeyUp={handleFilter}
                            placeholder="Search"
                        />
                    </div>
                </Fragment>

                <PerfectScrollbar className="scroll-box-list" options={{ wheelPropagation: true }}>

                    <div>
                        <h6 className='section-label text-secondary mt-1 mb-2'>{t('Selected fields')}</h6>
                        {
                            selectedList.map((row, index) => (
                                <div key={index + 2} className='d-flex justify-content-between my-1'>
                                    <span className='h5  text-primary word-break'>
                                        {row}
                                    </span>

                                    <Button.Ripple className='btn-icon' color='flat-danger' onClick={() => {
                                        dispatch(removeSelectedListItem(row))
                                    }}>
                                        <X size={16} />
                                    </Button.Ripple>
                                </div>
                            ))
                        }
                    </div>

                    <div className="mt-1">
                        <h6 className='section-label text-secondary mt-1 mb-2'>{t('Available fields')}</h6>
                        {
                            colFilterRender.map((row, index) => (
                                <div key={index + 5} className='d-flex justify-content-between my-1'>
                                    <span className='h5  text-primary word-break'>
                                        {row}
                                    </span>

                                    <Button.Ripple className='btn-icon' color='flat-primary' onClick={() => {
                                        dispatch(addSelectedListItem(row))
                                    }}>
                                        <Plus size={16} />
                                    </Button.Ripple>
                                </div>
                            ))
                        }

                    </div>

                </PerfectScrollbar>

            </CardBody>

            {loading ? <PreLoader /> : null}
        </Card>
    )
}

export default SideBar