// ================================================================================================
//  File Name: GeneralTabContent.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useState } from 'react'
import { AvForm, AvInput } from 'availity-reactstrap-validation-safe'
import { Button, Media, Label, Row, Col, Input, FormGroup, Alert, Spinner } from 'reactstrap'
import { toast } from 'react-toastify'
import axios, { staticPath } from '@axios'
import { token, updateUserInfo } from '@utils'
import Avatar from '@components/avatar'
import { useDispatch } from 'react-redux'
import { updateProfile } from '@store/actions/auth'
import { useTranslation } from 'react-i18next'

const GeneralTabs = ({ data }) => {
  const {t} = useTranslation()
  const dispatch = useDispatch()
  const avt = (data.profile_photo_path !== null && data.profile_photo_path !== undefined) ? <Media object className='rounded mr-50' src={`${data.profile_photo_path}`} alt='Profile Pic' height='80' width='80' /> : <Avatar color={'primary'} className='mr-1' imgHeight='40' imgWidth='40' status='online' content={(data.first_name) ? data.first_name : ""} initials />
  const [email, setEmail] = useState(data.email ? data.email : '')
  const [fname, setFName] = useState(data.first_name ? data.first_name : '')
  const [lname, setLname] = useState(data.last_name ? data.last_name : '')
  const [avatar, setAvatar] = useState(avt)
  const [username, setUsername] = useState(data.username ? data.username : '')
  const [loading, setLoading] = useState(false)
  const [checkFile, setCheckFile] = useState(false)
  const [photoName, setPhotoName] = useState("")

  const formSubmit = (event) => {
    event.preventDefault()
    setLoading(true)
    const formData = new FormData(event.target)

    if (checkFile === false) {
      formData.delete("profile_photo")
    }

    axios("/account-genral-update", {
      method: "post",
      data: formData,
      headers: { Authorization: token() }
    })
      .then(res => {
        setLoading(false)
        if (res.data.message_type === "updated") {

          if (checkFile) {
            setAvatar(<Media object className='rounded mr-50' src={`${res.data.data.profile_photo_path}`} alt='Profile Pic' height='80' width='80' />)
            setCheckFile(false)
          }

          updateUserInfo(res.data.data)
          dispatch(updateProfile(res.data.data))

          toast.success(`Information Updated`, {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined
          })
        }
      }).catch(err => {
        setLoading(false)
      })
  }

  const profile_file_handle = (files) => {
    setPhotoName(files.target.files[0].name)
    setCheckFile(true)
  }

  return (
    <Fragment>
      <h6 className='section-label mx-0 mb-1'>{t('General info')}</h6>
      <AvForm className='mt-2' onSubmit={formSubmit}>
        <div className='mb-0'>
          {/* <Media className="mb-2">
            <Media className='mr-25' left>
              {avatar}
            </Media>
            <Media className='mt-0 ml-1' body>
              <Button.Ripple tag={Label} for="profile_pic" className='mr-75' size='sm' color='primary'>
                {t('Upload')} {photoName}
                <Input type='file' id="profile_pic" onChange={profile_file_handle} name="profile_photo" hidden accept='image/*' />
              </Button.Ripple>
              <p>{t('Allowed JPG, PNG. Max size of 800kB')}</p>
            </Media>
          </Media> */}
          <Row>
            <Col sm='6'>
              <FormGroup>
                <Label for='email'>{t('E-mail')}</Label>
                <AvInput
                  type='email'
                  id='email'
                  disabled
                  name="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder='Email'
                />
              </FormGroup>
            </Col>
            <Col sm='6'>
              <FormGroup>
                <Label for='username'>{t('Username')}</Label>
                <AvInput
                  id='username'
                  name='username'
                  value={username}
                  disabled
                  onChange={e => setUsername(e.target.value)}
                  required
                />
              </FormGroup>
            </Col>
            <Col sm='6'>
              <FormGroup>
                <Label for='first_name'>{t('First Name')}</Label>
                <AvInput
                  id='first_name'
                  name='first_name'
                  value={fname}
                  onChange={e => setFName(e.target.value)}
                  required
                />
              </FormGroup>
            </Col>
            <Col sm='6'>
              <FormGroup>
                <Label for='last_name'>{t('Last Name')}</Label>
                <AvInput
                  id='last_name'
                  name='last_name'
                  value={lname}
                  onChange={e => setLname(e.target.value)}
                  required
                />
              </FormGroup>
            </Col>
            <Col className='mt-1' sm='12'>
              {(loading === false) ? <Button.Ripple color='primary' type="submit">{t('Save Changes')}</Button.Ripple> : <Button.Ripple type="button" color='primary' disabled> <Spinner size="sm" />&nbsp;{t('Saving')}...</Button.Ripple>}
            </Col>
          </Row>
        </div>
      </AvForm>
    </Fragment>
  )
}

export default GeneralTabs
