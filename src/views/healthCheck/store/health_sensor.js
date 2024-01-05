// ================================================================================================
//  File Name: index.js
//  Description: Details of the HIDS Incident Graph (Redux).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Redux Imports
// import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

export const filterValues = createAsyncThunk('Health/sensor', async ({ filters, filter_name, refreshCount }, { rejectWithValue }) => {
    return { filters, filter_name, refreshCount }
})

export const dataFiltersSlice = createSlice({
    name: 'filterReducer',
    initialState: {
        values: null,
        refreshCount: null,
        filter_name: null
    },
    reducers: {
    },
    extraReducers: builder => {
        builder
            .addCase(filterValues.fulfilled, (state, action) => {
                state.values = action.payload.filters
                state.refreshCount = action.payload.refreshCount
                state.filter_name = action.payload.filter_name
            })
    }
})

export default dataFiltersSlice.reducer
