import axios from '@axios'
import { token } from '@utils'

// ** Get all Data
export const email_details = () => {
  return async dispatch => {
    await axios.get('/displayemailconfig', { headers: { Authorization: token()} }).then(response => {
      dispatch({
        type: 'Email_ALL_DATA',
        data: response.data
      })
    })
  }
}
