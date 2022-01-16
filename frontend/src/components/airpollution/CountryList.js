import React, { Component, Fragment } from 'react';
import {connect} from "react-redux";
import PropTypes from 'prop-types'

import {deleteCountry, getCountries} from "../../actions/airpollution";

class CountryList extends Component {
    static propTypes = {
        deleteCountry: PropTypes.func.isRequired,
        getCountries: PropTypes.func.isRequired,
        countries: PropTypes.array.isRequired
    };

    componentDidMount() {
        this.props.getCountries();
    }

    render() {
        return <Fragment>
            <h1>Country List</h1>
            <table>
                <thead>
                <tr>
                    <th>Iso Code</th>
                    <th>Name</th>
                    <th />
                </tr>
                </thead>
                <tbody>
                {this.props.countries.map(country => (
                    <tr key={country.iso_code}>
                        <td>{country.iso_code}</td>
                        <td>{country.name}</td>
                        <td onClick={this.props.deleteCountry.bind(this, country.iso_code)}>delete</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </Fragment>
    }
}

const mapStateToProps = state => ({
    countries: state.airpollution.countries
});

export default connect(mapStateToProps, {deleteCountry, getCountries})(CountryList)
