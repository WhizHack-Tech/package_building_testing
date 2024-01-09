// ================================================================================================
//  File Name: multipleOption.js
//  Description: Details of the Administration ( Add Organization Location Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import Select from 'react-select'
import { selectThemeColors } from '@utils'

const MultipleOptions = ({ options, childId, stateParent, repeateOneId, filterTypes }) => {
    const data = []
    if (options.length > 0) {
        options.forEach((v) => {
            data.push({ value: v.id, label: v.key_name })
        })
    }

    return <Select
        theme={selectThemeColors}
        isClearable={false}
        isMulti
        onChange={(e) => {
            stateParent.data[repeateOneId].filters[filterTypes][`child_node_${childId}`].values = e
        }}
        options={data}
        className='react-select'
        classNamePrefix='select'
    />
}

export default MultipleOptions