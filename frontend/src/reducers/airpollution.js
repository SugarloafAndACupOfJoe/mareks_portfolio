import { ADD_COUNTRY, DELETE_COUNTRY, GET_COUNTRIES } from '../actions/types.js';

const initialState = {
  countries: [],
};

export default function (state = initialState, action) {
  switch (action.type) {
    case ADD_COUNTRY:
      return {
        ...state,
        countries: [...state.countries, action.payload]
      }
    case DELETE_COUNTRY:
      return {
        ...state,
        countries: state.countries.filter(country => country.iso_code !== action.payload)
      }
    case GET_COUNTRIES:
      return {
        ...state,
        countries: action.payload,
      };
    default:
      return state;
  }
}
