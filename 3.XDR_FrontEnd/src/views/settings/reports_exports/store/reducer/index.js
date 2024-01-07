// ================================================================================================
//  File Name: index.js
//  Description: Details of the Dynamic Report ( Reducer ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
const initialState = {
  rowData: [],
  selectedList: [],
  availableList: [],
  availableListRows: [],
  indexNameList: [],
  defaultIndexName: "",
  searchQuery: {},
  loading: false,
  errStatus: false,
  errMsg: ""
}

const reports_exports = (state = initialState, action) => {
  switch (action.type) {
    case 'GET_DEFAULT_DATA':
      return {
        ...state,
        rowData: action.rowData,
        availableList: action.availableList,
        availableListRows: action.availableList,
        indexNameList: action.indexNameList,
        defaultIndexName: action.defaultIndexName,
        searchQuery: action.searchQuery
      }
      break

    case 'GET_DATA_BY_INDEX_NAME':
      return {
        ...state,
        rowData: action.rowData,
        availableList: action.availableList,
        availableListRows: action.availableList,
        searchQuery: action.searchQuery,
        selectedList: []
      }
      break

    case 'SET_INDEX_NAME':
      return {
        ...state,
        defaultIndexName: action.defaultIndexName
      }
      break

    case 'API_LOADER':
      return {
        ...state,
        loading: action.loading,
        errStatus: action.errStatus || state.errStatus,
        errMsg: action.errMsg || state.errMsg
      }
      break

    case 'ADD_SELECTED_LIST_ITEM':

      return {
        ...state,
        selectedList: [...state.selectedList, action.selectedList],
        availableList: state.availableList.filter(val => val !== action.selectedList)
      }
      break

    case 'REMOVE_SELECTED_LIST_ITEM':

      return {
        ...state,
        availableList: [action.availableList, ...state.availableList],
        selectedList: state.selectedList.filter(val => val !== action.availableList)
      }
      break

    case 'DYNAMIC_REPORT_BY_SCROLL':
      return {
        ...state,
        rowData: [...state.rowData, ...action.scrollData]
      }

      break

    case 'HEADER_FILTER_DATA':
      return {
        ...state,
        rowData: action.rowData,
        searchQuery: action.searchQuery
      }
      break

    default:
      return state
  }
}

export default reports_exports
