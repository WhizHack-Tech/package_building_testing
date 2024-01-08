// ================================================================================================
//  File Name: DefalutPage.js
//  Description: Details of the Setting ( Edit Plan ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import { useEffect, useState } from 'react'
import { useParams } from "react-router-dom"
import axios from '@axios'
import { token } from '@utils'
import { toast } from 'react-toastify'
import { Form, Label, Input, CustomInput, Col, Button, Spinner, Card } from 'reactstrap'
import "../Loader.css"
const SwitchField = () => {
  const [default_page, setDefault_page] = useState('')
  const [envTrace, setEnvTrace] = useState('')
  const [envWazuh, setEnvWazuh] = useState('')
  const [envnids, setEnvnids] = useState('')
  const [envhids, setEnvhids] = useState('')
  const [live_map, setLive_map] = useState('')

  const [envSoar, setEnvSoar] = useState(false)
  const [healthCheck, setHealthCheck] = useState(false)
  const [mediaManagement, setMediaManagement] = useState(false)
  const [tpThreadFeed, setTpThreadFeed] = useState(false)
  const [sandBox, setSandBox] = useState(false)
  const [ess, setEss] = useState(false)
  const [tpSource, setTpSource] = useState(false)

  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const { id } = useParams()

  const [loadingAPI, setLoadingAPI] = useState(true)
  const [dataNotFound, setDataNotFound] = useState(false)

  const setEnvValue = (event) => {
    let envParams = {}
    if (event.target.id === "env_wazuh") {
      setEnvWazuh(event.target.checked)
      envParams = {
        plan_id: id,
        env_wazuh: event.target.checked
      }
    } else if (event.target.id === "env_trace") {
      setEnvTrace(event.target.checked)
      envParams = {
        plan_id: id,
        env_trace: event.target.checked
      }
    } else if (event.target.id === "env_nids") {
      setEnvnids(event.target.checked)
      envParams = {
        plan_id: id,
        env_nids: event.target.checked
      }
    } else if (event.target.id === "env_hids") {
      setEnvhids(event.target.checked)
      envParams = {
        plan_id: id,
        env_hids: event.target.checked
      }
    } else if (event.target.id === "default_page") {
      setDefault_page(event.target.value)
      envParams = {
        plan_id: id,
        default_page: event.target.value
      }
    } else if (event.target.id === "xdr_live_map") {
      setLive_map(event.target.checked)
      envParams = {
        plan_id: id,
        xdr_live_map: event.target.checked
      }
    } else if (event.target.id === "env_soar") {
      setEnvSoar(event.target.checked)
      envParams = {
        plan_id: id,
        env_soar: event.target.checked
      }
    } else if (event.target.id === "env_hc") {
      setHealthCheck(event.target.checked)
      envParams = {
        plan_id: id,
        env_hc: event.target.checked
      }
    } else if (event.target.id === "env_mm") {
      setMediaManagement(event.target.checked)
      envParams = {
        plan_id: id,
        env_mm: event.target.checked
      }
    } else if (event.target.id === "env_tptf") {
      setTpThreadFeed(event.target.checked)
      envParams = {
        plan_id: id,
        env_tptf: event.target.checked
      }
    } else if (event.target.id === "env_sbs") {
      setSandBox(event.target.checked)
      envParams = {
        plan_id: id,
        env_sbs: event.target.checked
      }
    } else if (event.target.id === "env_ess") {
      setEss(event.target.checked)
      envParams = {
        plan_id: id,
        env_ess: event.target.checked
      }
    } else if (event.target.id === "env_tps") {
      setTpSource(event.target.checked)
      envParams = {
        plan_id: id,
        env_tps: event.target.checked
      }
    }

    setLoading(true)

    axios.post('/pruduct-update-details-plan2', envParams, { headers: { Authorization: token() } })
      .then(res => {
        if (res.data.message_type === "updated_successfully") {

          if (res.data.data.default_page !== undefined) {
            setData(pre => ({ ...pre, default_page: res.data.data.default_page }))
          }

          if (event.target.checked) {
            toast.success("Changed Successfully")
          } else {
            if (event.target.value) {
              toast.success("Changed Successfully")
            }
          }
        }
      })
      .catch(error => {
        // Handle error
      })
      .finally(() => {
        setLoading(false)
      })
  }

  useEffect(() => {
    axios.get(`/display-updated-plan/${id}/`, { headers: { Authorization: token() } })
      .then(res => {
        if (res.data.message_type === "success") {
          setEnvTrace(res.data.data.env_trace)
          setEnvWazuh(res.data.data.env_wazuh)
          setEnvnids(res.data.data.env_nids)
          setEnvhids(res.data.data.env_hids)
          setLive_map(res.data.data.xdr_live_map)
          setData(res.data.data)
          setEnvSoar(res.data.data.env_soar)
          setHealthCheck(res.data.data.env_hc)
          setMediaManagement(res.data.data.env_mm)
          setTpThreadFeed(res.data.data.env_tptf)
          setSandBox(res.data.data.env_sbs)
          setEss(res.data.data.env_ess)
          setTpSource(res.data.data.env_tps)

        } else {
          setDataNotFound(true)
        }
      })
      .catch(e => {
        // Handle error
      })
      .finally(() => {
        setLoadingAPI(false)
      })
  }, [])

  return (
    <Card>
      {loading ? (
        <div className='d-flex justify-content-center'>
          <div class="tri-color-ripple-spinner">
            <div class="ripple ripple1"></div>
            <div class="ripple ripple2"></div>
          </div>
        </div>
      ) : (
        <Form>
          {loadingAPI ? (
            <div className='d-flex justify-content-center'>
              <div class="tri-color-ripple-spinner">
                <div class="ripple ripple1"></div>
                <div class="ripple ripple2"></div>
              </div>
            </div>
          ) : dataNotFound ? (
            <div className='d-flex justify-content-center'>
              Data Not Found
            </div>
          ) : (
            <>
              <Col className='mb-1' md='6' sm='12'>
                <Label>Default Page</Label>
                <Input
                  type='select'
                  id='default_page'
                  // checked={default_page}
                  onChange={setEnvValue}
                >
                  <option value='' disabled selected>
                    ...Select...
                  </option>
                  <option value='/nids/alerts' selected={data.default_page === '/nids/alerts'}>NIDS</option>
                  <option value='/hids/alerts' selected={data.default_page === '/hids/alerts'}>HIDS</option>
                  <option value='/trace/alerts' selected={data.default_page === '/trace/alerts'}>Trace</option>
                  <option value='/health-check/sensor-health' selected={data.default_page === '/health-check/sensor-health'}>Health Check</option>
                  <option value='/soar' selected={data.default_page === '/soar'}>Soar</option>
                  <option value='/media-management' selected={data.default_page === '/media-management'}>Media Management</option>
                  <option value='/tp-thread-feed' selected={data.default_page === '/tp-thread-feed'}>TP Thread Feed</option>
                  <option value='/sand-box' selected={data.default_page === '/sand-box'}>Sand Box</option>
                  <option value='/ess' selected={data.default_page === '/ess'}>ESS</option>
                  <option value='/tp-source' selected={data.default_page === '/tp-source'}>TP Source</option>
                </Input>
              </Col>
              <div className='demo-inline-spacing ml-1'>
                <CustomInput
                  type='switch'
                  id='env_trace'
                  name='env_trace'
                  label='Trace'
                  inline
                  checked={envTrace}
                  onChange={setEnvValue}
                />

                <CustomInput
                  type='switch'
                  id='env_nids'
                  name='env_nids'
                  label='NIDS'
                  inline
                  checked={envnids}
                  onChange={setEnvValue}
                />

                <CustomInput
                  type='switch'
                  id='env_hids'
                  name='env_hids'
                  label='HIDS'
                  inline
                  checked={envhids}
                  onChange={setEnvValue}
                />

                <CustomInput
                  type='switch'
                  id='xdr_live_map'
                  name='xdr_live_map'
                  label='Live Map'
                  inline
                  checked={live_map}
                  onChange={setEnvValue}
                />

                <CustomInput
                  type='switch'
                  id='env_soar'
                  name='env_soar'
                  label='Soar'
                  inline
                  checked={envSoar}
                  onChange={setEnvValue}
                />
                <CustomInput
                  type='switch'
                  id='env_hc'
                  name='env_hc'
                  label='Health Check'
                  inline
                  checked={healthCheck}
                  onChange={setEnvValue}
                />

                <CustomInput
                  type='switch'
                  id='env_mm'
                  name='env_mm'
                  label='Media Management'
                  inline
                  checked={mediaManagement}
                  onChange={setEnvValue}
                />

                <CustomInput
                  type='switch'
                  id='env_tptf'
                  name='env_tptf'
                  label='TP Thread Feed'
                  inline
                  checked={tpThreadFeed}
                  onChange={setEnvValue}
                />

                <CustomInput
                  type='switch'
                  id='env_sbs'
                  name='env_sbs'
                  label='Sand Box'
                  inline
                  checked={sandBox}
                  onChange={setEnvValue}
                />

                <CustomInput
                  type='switch'
                  id='env_ess'
                  name='env_ess'
                  label='ESS'
                  inline
                  checked={ess}
                  onChange={setEnvValue}
                />

                <CustomInput
                  type='switch'
                  id='env_tps'
                  name='env_tps'
                  label='TP Source'
                  inline
                  checked={tpSource}
                  onChange={setEnvValue}
                />

              </div>
              <Col className='mt-2 d-flex justify-content-end' sm='12'>
                <Button color='primary' className='btn-submit'>
                  Save Changes
                </Button>
              </Col>
            </>
          )}
        </Form>
      )}
    </Card>

  )
}

export default SwitchField
