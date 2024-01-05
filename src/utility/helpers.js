// =============================================================================================
//  File Name: helpers.js
//  Description: Details of the helpers Utility component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

function splitWord(input) {
    let formattedOutput = input

    if (input !== undefined || input !== null) {
        const parts = input.split("-")
        if (parts.length >= 3) {
            formattedOutput = `${parts[1].toUpperCase()} ${parts[2].charAt(0).toUpperCase()}${parts[2].slice(1)}`
        }
    }

    return formattedOutput
}

function selectOptionFormat(input) {
    const output = []

    for (const item of input) {
        const formattedItem = {
            label: item
                .split('-')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' '),
            value: item,
            color: "#00B8D9",
            isFixed: true
        }

        output.push(formattedItem)
    }

    return output
}

export { splitWord, selectOptionFormat }
