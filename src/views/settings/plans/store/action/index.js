import axios from '@axios'
import { token } from '@utils'

// ** Get all Data
export const plan_details = () => {
  return async dispatch => {
    await axios.get('/planlist/', { headers: { Authorization: token()} }).then(response => {
      if (response.data.message_type === 'data_found') {
       dispatch({
        type: 'Plan_ALL_DATA',
        data: response.data.data
      })
    }
    })
  }
}