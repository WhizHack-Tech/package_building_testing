import React, { useEffect, useState, Fragment } from 'react'
import { Card, CardHeader, Spinner, CardTitle, CardBody, FormGroup, Form, Label, Input, CustomInput, Button, Row, Col } from 'reactstrap'
import "./edit-application.css"
import { XCircle, Plus } from 'react-feather'
import axios from '@axios'
import { token } from '@utils'
import { useParams } from "react-router-dom"
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
const MySwal = withReactContent(Swal)

let addCount = 0
const AppDetails = () => {
  const { id } = useParams()
  const [apiData, setApiData] = useState([{ application_descriptions: "", application_name: "" }])
  let [repeatChild, setRepeatChild] = useState([])
  const [imgPath, setImgPath] = useState("")
  const [btnLoader, setBtnLoader] = useState(false)


  useEffect(() => {
    setBtnLoader(true)
    axios.get(`/application-views/${id}/`, { headers: { Authorization: token() } }).then(res => {
      setBtnLoader(false)
      if (res.data.message_type === "success") {
        let resData = res.data.data
        setApiData(resData)
        setImgPath(resData.application_image)
        if (resData.application_steps !== undefined && resData.application_steps.length > 0) {

          let inputVal = []
          for (let x of resData.application_steps) {
            inputVal.push({ stepVal: x, inputCount: addCount })
            addCount += 1
          }

          setRepeatChild(inputVal)
        }
      }
    }).catch(e => {
      setBtnLoader(false)
    })
  }, [])

  const addChild = () => {
    if (repeatChild.length === 0) {
      addCount = 0
      setRepeatChild([{ stepVal: "", inputCount: addCount }])
    } else {
      setRepeatChild([...repeatChild, { stepVal: "", inputCount: addCount }])
    }
    addCount += 1
  }

  const repeatChildInput = (e, indexCount) => {
    const newRepeat = [...repeatChild]
    newRepeat[indexCount].stepVal = e.target.value
    setRepeatChild(newRepeat)
  }

  const onRemove = (indexCount) => {
    const arrRemove = repeatChild.filter(function (rowArr) {
      return rowArr.inputCount !== indexCount
    })
    setRepeatChild(arrRemove)
  }

  const formHandle = (event) => {
    event.preventDefault()
    const bodyFormData = new FormData(event.target)
    setBtnLoader(true)

    axios({
      method: "post",
      url: 'add-app-details',
      data: bodyFormData,
      headers: { Authorization: token() }

    }).then(res => {
      setBtnLoader(false)
      if (res.data.message_type === "success") {
        if (res.data.img_path !== "null" && res.data.img_path !== undefined) {
          setImgPath(res.data.img_path)
        }

        MySwal.fire({
          title: "update",
          text: 'Update success',
          icon: 'success',
          customClass: {
            confirmButton: 'btn btn-primary'
          },
          buttonsStyling: false
        })
      }
    }).catch((e) => {
      setBtnLoader(false)
    })
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle tag='h4'>Application Details</CardTitle>
      </CardHeader>
      <CardBody>
        <Form onSubmit={formHandle}>
          <Row>
            <Col className='mb-1' xl='12' md='12' sm='12'>
              <FormGroup>
                <Label for='application_name'>Application Name <i className='text-danger'>*</i></Label>
                <Input type='text' name="application_name" defaultValue={apiData.application_name} id='application_name' />
                <input type="hidden" name='id' value={id} />
              </FormGroup>
              <FormGroup>
                <Label for='application_desc'>Application Description <i className='text-danger'>*</i></Label>
                <Input type="textarea" name="application_descriptions" defaultValue={apiData.application_descriptions} id='application_desc' />
              </FormGroup>
              <Row className="align-items-center">
                <Col xl='3' md='3' sm='12'>
                  <p className='p-0'>Application Photo Preview</p>
                  <div className='app-avatar-box border rounded'>
                    <div className='app-avatar' style={{ backgroundImage: `url(${imgPath})` }}>
                    </div>
                  </div>
                </Col>
                <Col xl='9' md='9' sm='9'>
                  <FormGroup>
                    <Label for='appication_photo'>Application Photo</Label>
                    <CustomInput type='file' accept='image/*' name="application_image" id='appication_photo' />
                  </FormGroup>
                </Col>
              </Row>
              {repeatChild.map((componentObj, indexCount) => (<div key={`repeat-child-box-${componentObj.inputCount}`}>
                <Col xl='12' md='12' sm='12'>
                  <div className='text-right text-danger'><XCircle onClick={(e) => {
                    onRemove(componentObj.inputCount)
                  }} className='cursor-pointer' /> </div>
                  <FormGroup>
                    <Label for={`title_${indexCount}`}>Step(s) Title</Label>
                    <Input id={`title_${indexCount}`} defaultValue={componentObj.stepVal || ""} onInput={(e) => {
                      repeatChildInput(e, indexCount)
                    }} type="text" name="application_steps[]" />
                  </FormGroup>
                </Col>
              </div>))}

              <div className='row justify-content-between mt-1 mb-1'>
                {(btnLoader === false) ? <Button.Ripple color='primary'>Save</Button.Ripple> : <Button.Ripple color='primary'><Spinner size='sm' />&nbsp;Save... </Button.Ripple>}
                <Button.Ripple color='primary' type="button" onClick={addChild} outline><Plus /></Button.Ripple>
              </div>

            </Col>
          </Row>
        </Form>
      </CardBody>
    </Card>
  )
}

export default AppDetails