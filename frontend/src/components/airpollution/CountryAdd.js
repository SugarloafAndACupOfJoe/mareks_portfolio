import React, {Component, Fragment} from 'react';
import {connect} from "react-redux";
import PropTypes from 'prop-types'

import {addCountry} from "../../actions/airpollution";

class CountryAdd extends Component {
    state = {
        iso_code: '',
        name: '',
        color: '',
        longitude: 0.0,
        latitude: 0.0,
        altitude: 0.0,
    }

    static propTypes = {
        addCountry: PropTypes.func.isRequired,
    };

    onChange = (e) => this.setState({[e.target.name]: e.target.value});

    onSubmit = (e) => {
        e.preventDefault();
        const {iso_code, name, color, longitude, latitude, altitude} = this.state;
        const country = {iso_code, name, color, longitude, latitude, altitude};
        this.props.addCountry(country);
        this.setState({
            iso_code: '',
            name: '',
            color: '',
            longitude: 0.0,
            latitude: 0.0,
            altitude: 0.0,
        });
    };

    render() {
        const {iso_code, name, color, longitude, latitude, altitude} = this.state;
        return <Fragment>
            <h1>Country Add</h1>
            <form onSubmit={this.onSubmit}>
                <div className="form-group">
                    <label>Iso Code</label>
                    <input
                        className="form-control"
                        type="text"
                        name="iso_code"
                        onChange={this.onChange}
                        value={iso_code}
                    />
                </div>
                <div className="form-group">
                    <label>Name</label>
                    <input
                        className="form-control"
                        type="text"
                        name="name"
                        onChange={this.onChange}
                        value={name}
                    />
                </div>
                <div className="form-group">
                    <label>Color</label>
                    <input
                        className="form-control"
                        type="text"
                        name="color"
                        onChange={this.onChange}
                        value={color}
                    />
                </div>
                <div className="form-group">
                    <label>Longitude</label>
                    <input
                        className="form-control"
                        type="number"
                        name="longitude"
                        onChange={this.onChange}
                        value={longitude}
                    />
                </div>
                <div className="form-group">
                    <label>Latitude</label>
                    <input
                        className="form-control"
                        type="number"
                        name="latitude"
                        onChange={this.onChange}
                        value={latitude}
                    />
                </div>
                <div className="form-group">
                    <label>Altitude</label>
                    <input
                        className="form-control"
                        type="number"
                        name="altitude"
                        onChange={this.onChange}
                        value={altitude}
                    />
                </div>

                <div className="form-group">
                    <button type="submit" className="btn btn-primary">
                        Submit
                    </button>
                </div>
            </form>
        </Fragment>
    }
}

export default connect(null, {addCountry})(CountryAdd)
