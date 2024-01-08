// ================================================================================================
//  File Name: dashboardConfig.js
//  Description: Details of the Administration ( Add Organization Location Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** React Imports
import { useState, useEffect, useReducer } from 'react'
import axios from '@axios'
// ** Icons Imports
import { X, Plus } from 'react-feather'

// ** Reactstrap Imports
import { Row, Col, FormGroup, Label, Button } from 'reactstrap'

// ** Custom Components
import Repeater from '@components/repeater'
import MultipleOptions from './multipleOption'

const initStates = {
  loading: true,
  data: null,
  selectedVals: []
}

const reducer = (state, action) => {
  switch (action.type) {
    case "FETCH_SUCCESS":
      return {
        ...state,
        loading: false,
        data: action.payload
      }
    case "SET_SELECTED_VALUES":

      return {
        ...state,
        selectedVals: { ...state.selectedVals, ...action.payload }
      }

    default:
      return state

  }
}

const DashboardConfig = ({ stateParent, dispatchParent, repeateOneId }) => {
  // ** State
  const [count, setCount] = useState(0)

  const [state, dispatch] = useReducer(reducer, initStates)

  useEffect(() => {

    axios.get(`/get-filter-details`)
      .then(res => {
        const DATA = res.data.data
        dispatch({
          type: "FETCH_SUCCESS",
          payload: DATA
        })
      })
      .catch(error => {
        console.log(error.message)
      })
  }, [])


  function handleParentChange(event, i) {
    let childData
    state.data.forEach(row => {
      if (row[event.target.value] !== undefined) {
        childData = row[event.target.value]
      }
    })

    dispatch({
      type: "SET_SELECTED_VALUES",
      payload: { [i]: childData }
    })
    stateParent.data[repeateOneId].filters.dashboard_filters[`child_node_${i}`].name = event.target.value
  }

  const increaseCount = () => {
    setCount(count + 1)

    dispatchParent({
      type: "DASH_ADD_CHILD",
      payload: { parentId: repeateOneId, childNode: { [`child_node_${count}`]: { name: null, values: [] } } }
    })

  }

  const deleteForm = e => {
    e.preventDefault()
    e.target.closest('div.children-box').remove()
    let dataID = e.target.closest('div.children-box').getAttribute("dataid")

    dispatchParent({
      type: "DASH_DELETE_CHILD",
      payload: { parentId: repeateOneId, childId: `child_node_${dataID}` }
    })
  }

  return (
    <div className='border border-success rounded p-2 mb-2 '>
      <div className='content-header'>
        <h5 className='mb-0'>Dashboard Config</h5>
      </div>
      <Repeater count={count}>
        {i => (
          <div key={i} dataid={i} className='border border-warning children-box rounded p-2 mb-2'>
            <Row className='justify-content-between align-items-end'>
              <Col md={6} className='mb-md-0 mb-1'>
                <FormGroup>
                  <Label>Select Filter Type</Label>
                  <select className="form-control" id={`name-${i}`} onChange={(e) => { handleParentChange(e, i) }}>
                    <option value="">-- Select Filter Type--</option>
                    {(!state.loading) ? state.data.map((opt, key) => (
                      <option key={key} valueid={key} value={opt.name_alias}>{opt.name}</option>
                    )) : null}
                  </select>
                </FormGroup>
              </Col>
              <Col md={6} className='mb-md-0 mb-1'>
                <FormGroup>
                  <Label>Add Filter Values</Label>
                  <MultipleOptions filterTypes='dashboard_filters' stateParent={stateParent} repeateOneId={repeateOneId} childId={i} options={(state.selectedVals[i] !== undefined) ? state.selectedVals[i] : []} />
                </FormGroup>
              </Col>
              <Col md={2}>
                <Button color='danger' className='text-nowrap px-1' onClick={deleteForm} outline>
                  <X size={14} className='me-50' />
                  <span>Delete</span>
                </Button>
              </Col>
            </Row>
          </div>
        )}
      </Repeater>
      <Button className='btn-icon mt-2 mb-2' color='primary' onClick={increaseCount}>
        <Plus size={14} />
        <span className='align-middle ms-25'>Add New</span>
      </Button>
    </div>
  )
}

export default DashboardConfig