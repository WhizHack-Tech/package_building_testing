// ================================================================================================
//  File Name: index.js
//  Description: Details of the Dynamic Report ( Store, Action ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import axios from '@axios'
import { token } from '@utils'
import { toast } from "react-toastify"

const limit = 20

// ** GET Default Data
export const getDefaultData = filterCondition => {

  return dispatch => {
    dispatch({ type: 'API_LOADER', loading: true })
    
    axios.get(`/get-indices-name?condition_type=${filterCondition}&limit=${limit}`, { headers: { Authorization: token() } }, { filterCondition })
      .then(res => {
        dispatch({
          type: 'API_LOADER',
          loading: false,
          errStatus: false
        })

        if (res.data.message_type === 'success') {

          const searchQuery = {
            query: [],
            index_name: res.data.data.default_index,
            limit,
            time_filter: filterCondition
          }

          if (res.data.data.indices?.length > 0) {
            dispatch({
              type: 'GET_DEFAULT_DATA',
              rowData: res.data.data.default_data,
              indexNameList: res.data.data.indices,
              defaultIndexName: res.data.data.default_index,
              availableList: res.data.data.default_data?.length > 0 ? Object.keys(res.data.data.default_data[0]) : [],
              searchQuery
            })
          }
        }

        if (res.data.message_type === 'd_not_f') {
          dispatch({
            type: 'API_LOADER',
            loading: false,
            errStatus: true,
            errMsg: 'Data Not Found.'
          })
        }

      })
      .catch(err => {
        dispatch({
          type: 'API_LOADER',
          loading: false,
          errStatus: true,
          errMsg: err.message
        })
      })
  }
}

export const setIndexData = (index_type, condition_type) => {

  return dispatch => {
    dispatch({ type: 'API_LOADER', loading: true })

    axios.get(`/get-indice-details?condition_type=${condition_type}&limit=${limit}&offset=0&index_name=${index_type}`, { headers: { Authorization: token() } }, { index_type })
      .then(res => {

        dispatch({
          type: 'API_LOADER',
          loading: false,
          errStatus: false
        })

        dispatch({
          type: 'SET_INDEX_NAME',
          defaultIndexName: index_type
        })

        if (res.data.message_type === 'success') {

          const searchQuery = {
            query: [],
            index_name: index_type,
            limit,
            time_filter: condition_type
          }

          if (res.data.data?.length > 0) {
            dispatch({
              type: 'GET_DATA_BY_INDEX_NAME',
              rowData: res.data.data,
              availableList: Object.keys(res.data.data[0]),
              searchQuery
            })
          }

        }

        if (res.data.message_type === 'd_not_f') {
          dispatch({
            type: 'API_LOADER',
            loading: false,
            errStatus: true,
            errMsg: 'Data Not Found.'
          })

          dispatch({
            type: 'GET_DATA_BY_INDEX_NAME',
            rowData: [],
            availableList: []
          })
        }

      })
      .catch(err => {
        dispatch({
          type: 'API_LOADER',
          loading: false,
          errStatus: true,
          errMsg: err.message
        })
      })
  }

}

export const addSelectedListItem = val => {
  return dispatch => {
    dispatch({
      type: 'ADD_SELECTED_LIST_ITEM',
      selectedList: val
    })
  }
}

export const removeSelectedListItem = val => {
  return dispatch => {
    dispatch({
      type: 'REMOVE_SELECTED_LIST_ITEM',
      availableList: val
    })
  }
}

export const filterApi = searchQuery => {

  return dispatch => {
    dispatch({ type: 'API_LOADER', loading: true })

    axios.post(`/dynamic-report-filter`, { ...searchQuery }, { headers: { Authorization: token() } })
      .then(res => {

        dispatch({
          type: 'API_LOADER',
          loading: false,
          errStatus: false
        })

        if (res.data.message_type === 'success') {

          if (res.data.data?.length > 0) {
            dispatch({
              type: 'HEADER_FILTER_DATA',
              rowData: res.data.data,
              searchQuery
            })
          }

        }

        if (res.data.message_type === 'd_not_f') {
          toast.error('Data Not Found.')

          dispatch({
            type: 'API_LOADER',
            loading: false,
            errStatus: true,
            errMsg: 'Data Not Found.'
          })
        }

      })
      .catch(err => {
        toast.error(err.message)
        dispatch({
          type: 'API_LOADER',
          loading: false,
          errStatus: true,
          errMsg: err.message
        })
      })
  }
}