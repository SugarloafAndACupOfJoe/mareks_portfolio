import React, {Component} from 'react';
import ReactDOM from 'react-dom';

import CountryAdd from "./airpollution/CountryAdd";
import CountryList from './airpollution/CountryList';

import {Provider} from 'react-redux';
import store from '../store';

class App extends Component {
    render() {
        return (
            <Provider store={store}>
                <CountryAdd />
                <CountryList/>
            </Provider>
        );
    }
}

ReactDOM.render(<App/>, document.getElementById('app'));
