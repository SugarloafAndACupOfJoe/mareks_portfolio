import axios from 'axios';

import { ADD_COUNTRY, DELETE_COUNTRY, GET_COUNTRIES } from './types';

// ADD COUNTRY
export const addCountry = (country) => (dispatch, getState) => {
  axios
    .post(`/api/airpollution/country/`, country)
    .then((res) => {
      dispatch({
        type: ADD_COUNTRY,
        payload: res.data,
      });
    })
    .catch((err) => console.log(err));
};

// DELETE COUNTRY
export const deleteCountry = (iso_code) => (dispatch, getState) => {
  axios
    .delete(`/api/airpollution/country/${iso_code}/`)
    .then((res) => {
      dispatch({
        type: DELETE_COUNTRY,
        payload: iso_code,
      });
    })
    .catch((err) => console.log(err));
};

// GET COUNTRIES
export const getCountries = () => (dispatch, getState) => {
  axios
    .get('/api/airpollution/country/')
    .then((res) => {
      dispatch({
        type: GET_COUNTRIES,
        payload: res.data,
      });
    })
    .catch((err) => console.log(err));
};
