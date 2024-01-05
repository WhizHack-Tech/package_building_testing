// ================================================================================================
//  File Name: MultipleTabs.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React, { useState, useEffect } from 'react'
import './multiple-tabs.css'
import { token, selectThemeColors } from '@utils'
import axios from '@axios'
import { Card, CardHeader, CardTitle, CardBody, Badge, Button, Input, Label, Spinner } from 'reactstrap'
import Select from 'react-select'
import Swal from 'sweetalert2'
import { X } from 'react-feather'
import withReactContent from 'sweetalert2-react-content'
import { useTranslation } from 'react-i18next'
const SwalAlert = withReactContent(Swal)

const classLists = [
    { value: "Network Trojan was detected", label: "Network Trojan was detected", color: '#00B8D9', isFixed: true },
    { value: "A suspicious filename was detected", label: "A suspicious filename was detected", color: '#00B8D9', isFixed: true },
    { value: "Suspicious string was detected", label: "Suspicious string was detected", color: '#00B8D9', isFixed: true },
    { value: "System call was detected", label: "System call was detected", color: '#00B8D9', isFixed: true },
    { value: "access to a potentially vulnerable web application", label: "access to a potentially vulnerable web application", color: '#00B8D9', isFixed: true },
    { value: "Attempt to login by a default username and password", label: "Attempt to login by a default username and password", color: '#00B8D9', isFixed: true },
    { value: "Attempted Administrator Privilege Gain", label: "Attempted Administrator Privilege Gain", color: '#00B8D9', isFixed: true },
    { value: "Attempted Denial of Service", label: "Attempted Denial of Service", color: '#00B8D9', isFixed: true },
    { value: "Attempted Information Leak", label: "Attempted Information Leak", color: '#00B8D9', isFixed: true },
    { value: "Attempted User Privilege Gain", label: "Attempted User Privilege Gain", color: '#00B8D9', isFixed: true },
    { value: "Decode of an RPC Query", label: "Decode of an RPC Query", color: '#00B8D9', isFixed: true },
    { value: "Detection of a Denial-of-Service Attack", label: "Detection of a Denial-of-Service Attack", color: '#00B8D9', isFixed: true },
    { value: "Detection of a Network Scan", label: "Detection of a Network Scan", color: '#00B8D9', isFixed: true },
    { value: "Detection of a non-standard protocol or event", label: "Detection of a non-standard protocol or event", color: '#00B8D9', isFixed: true },
    { value: "Device Retrieving External IP Address Detected", label: "Device Retrieving External IP Address Detected", color: '#00B8D9', isFixed: true },
    { value: "Executable code was detected", label: "Executable code was detected", color: '#00B8D9', isFixed: true },
    { value: "Generic Protocol Command Decode", label: "Generic Protocol Command Decode", color: '#00B8D9', isFixed: true },
    { value: "Information Leak", label: "Information Leak", color: '#00B8D9', isFixed: true },
    { value: "Malware Command and Control Activity Detected", label: "Malware Command and Control Activity Detected", color: '#00B8D9', isFixed: true },
    { value: "Misc activity", label: "Misc activity", color: '#00B8D9', isFixed: true },
    { value: "Misc Attack", label: "Misc Attack", color: '#00B8D9', isFixed: true },
    { value: "Not Alert", label: "Not Alert", color: '#00B8D9', isFixed: true },
    { value: "Possible Social Engineering Attempted", label: "Possible Social Engineering Attempted", color: '#00B8D9', isFixed: true },
    { value: "Possibly Unwanted Program Detected", label: "Possibly Unwanted Program Detected", color: '#00B8D9', isFixed: true },
    { value: "Potential Corporate Privacy Violation", label: "Potential Corporate Privacy Violation", color: '#00B8D9', isFixed: true },
    { value: "Potentially Bad Traffic", label: "Potentially Bad Traffic", color: '#00B8D9', isFixed: true },
    { value: "Web Application Attack", label: "Web Application Attack", color: '#00B8D9', isFixed: true },
    { value: "Normal Traffic", label: "Normal Traffic", color: '#00B8D9', isFixed: true }
]

const MultipleTabs = () => {
    const { t } = useTranslation()
    const [threatClassValue, setThreateClassValue] = useState([])
    const [tagLists, setTagLists] = useState([])
    const [apiDataSelecte, setApiDataSelecte] = useState([])
    const [apiLoading, setApiLoading] = useState(false)
    const [apiDataLoading, setApiDataLoading] = useState(true)

    const defaultValuSelect = (defaultVal) => {
        let finalData = []

        if (defaultVal !== undefined) {
            for (let p = 0; p < Object.keys(classLists).length; p++) {
                for (let i = 0; i < defaultVal.length; i++) {
                    if (classLists[p].value === defaultVal[i]) {
                        finalData.push(classLists[p])
                    }
                }
            }
        }

        return finalData
    }

    const getDataFromApi = () => {
        setApiDataLoading(false)
        axios.get('get-blacklisted-details', { headers: { Authorization: token() } })
            .then(res => {
                setApiDataLoading(true)
                if (res.data.message_type = "data_found") {
                    setTagLists(res.data.data.blacklisted_ip)
                    setThreateClassValue(res.data.data.blacklisted_class)
                    setApiDataSelecte(defaultValuSelect(res.data.data.blacklisted_class))
                }
            })
            .catch(e => {
                setApiDataLoading(true)
                console.log(e.message)
            })
    }

    useEffect(() => {
        getDataFromApi()
    }, [])

    const submitHandle = () => {
        setApiLoading(true)
        axios.post('/add-blacklisted-details', {
            blacklisted_class: threatClassValue,
            blacklisted_ip: tagLists
        }, { headers: { Authorization: token() } })
            .then(res => {
                setApiLoading(false)

                if (res.data.message_type === "updated" || res.data.message_type === "added") {
                    SwalAlert.fire({
                        title: 'Good job!',
                        text: 'Sit Back and Relax',
                        icon: 'success',
                        customClass: {
                            confirmButton: 'btn btn-primary'
                        },
                        buttonsStyling: false
                    })
                }

            })
            .catch(e => {
                setApiLoading(false)
                console.log(e.message)
            })


    }

    const threatClassHanle = (event) => {
        let values = []
        if (event !== null) {
            event.forEach(item => {
                values.push(item.value)
            })
        }
        setApiDataSelecte(event)
        setThreateClassValue(values)
    }

    function handleKeyDown(e) {

        if (e.key !== ',' && e.key !== 'Enter' && e.key !== ' ') return
        const value = e.target.value
        const value_trim = value.trim()
        if (!value.trim()) return
        setTagLists([...tagLists, value_trim.split(",").join("")])
        e.target.value = null
    }

    function removeTag(index) {
        setTagLists(tagLists.filter((el, i) => i !== index))
    }

    return (
        <Card>
            <CardHeader className='pl-0 pt-0'>
                <CardTitle>
                    <h6 className='section-label mx-0 mb-1'>{t('IP & Threat Classes')}</h6>
                </CardTitle>
            </CardHeader>
            <CardBody className='p-0'>
                {apiDataLoading ? (<React.Fragment>
                    <Label className='form-label'>{t('Add IP')}</Label>
                    <div className="tags-input-container">
                        {tagLists.map((tag, index) => (
                            <Badge key={index} color='primary'>
                                <span className='align-middle pr-1'>{tag}</span>
                                <X size={12} className='align-middle cursor' onClick={() => removeTag(index)} />
                            </Badge>
                        ))}
                        <Input onKeyDown={handleKeyDown} type="text" className="tags-input" placeholder="Type IPs" />
                    </div>
                    <div className='mt-2'>
                        <Label className='form-label'>{t('Threat Class')}</Label>
                        <Select
                            isClearable={false}
                            theme={selectThemeColors}
                            isMulti
                            name='colors'
                            value={apiDataSelecte}
                            options={classLists}
                            className='react-select'
                            classNamePrefix='select'
                            onChange={threatClassHanle}
                        />
                    </div>
                    <div className='mt-2'>
                        {
                            (apiLoading) ? <Button.Ripple color='primary' type='button'><Spinner color='white' size='sm' /> Saving...</Button.Ripple> : <Button.Ripple color='primary' type='button' onClick={submitHandle}>Save Changes</Button.Ripple>
                        }
                    </div>
                </React.Fragment>) : (<div className='d-flex justify-content-center'><Spinner color='primary' type='grow' /></div>)}
            </CardBody>
        </Card>
    )
}

export default MultipleTabs