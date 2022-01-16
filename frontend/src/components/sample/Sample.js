import React, {useState, useEffect} from 'react';
import {connect} from "react-redux";
import PropTypes from 'prop-types'

import {getCountries} from "../../actions/airpollution";

// --------------------------------------- JSX ---------------------------------------
function JSXElement() {
    let some_id = 123;
    let some_array = ['book', 'title', 'idea', 'marek', 'and', 'two', 'cans', 'of', 'heinz', 'beans']
    let style_array = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'dark']

    return <React.Fragment>
        <p>I'm a paragraph. Plain ol paragraph. I'll be rendered into... well, an HTML paragraph!</p>
        <div>I'm a div. Good ol div. I will also be rendered into an HTML div.</div>
        <strong>I'm a strong. You know where I'm going with this?</strong>

        <p id={some_id}>I have an id! You are probably used to seeing quotation marks and some text in it. Using \{}
            allows us to place JS in it. Like this: {some_id === 123 ? "FOO" : "BAR"}</p>

        <p className="alert alert-primary">Argh!!! I knew it you son of a b***ch! I knew you will mess something up!
            Why className and not class?! Huh? Why?!</p>

        <div className="row">
            {some_array.map((word, index) => {
                let i = Math.floor(style_array.length * Math.random());
                let style_class = 'col-1 alert alert-' + style_array[i]
                return <div key={index} className={style_class}>{word}</div>
            })}
        </div>
        <hr/>

    </React.Fragment>
}

// ---------------------------- Function based component + state + props + handling events ----------------------------

function FunctionComponent(props) {
    const [dividend, setDividend] = useState(props.initial_dividend)
    const [divisor, setDivisor] = useState(props.initial_divisor)

    function handleChangeDividend(e) {
        setDividend(parseInt(e.target.value))
    }

    function handleChangeDivisor(e) {
        setDivisor(parseInt(e.target.value))
    }

    return <React.Fragment>
        <p>
            Dividend: <input type="number" onChange={handleChangeDividend} value={dividend}/>
        </p>
        <p>
            Divisor: <input type="number" onChange={handleChangeDivisor} value={divisor}/>
        </p>
        <p>
            Result: {divisor === 0 ? 'Divisor can\'t be 0.' : dividend / divisor}
        </p>

        <hr/>
    </React.Fragment>
}

// ----------------------------- Class based components + state + props + handling events-----------------------------

class ClassComponent extends React.Component {
    state = {
        new_item: '',
        item_list: this.props.initial_list ? this.props.initial_list : []
    }

    handleChange = (e) => {
        this.setState({...this.state, new_item: e.target.value})
    }

    handleSubmit = (e) => {
        e.preventDefault()
        this.state.item_list.push(this.state.new_item)
        this.state.new_item = ''
        this.setState(this.state)
    }

    handleDelete = (index) => {
        this.state.item_list.splice(index, 1)
        this.setState(this.state)
    }

    renderForm() {
        return <form onSubmit={this.handleSubmit}>
            New Item: <input type="text" onChange={this.handleChange} value={this.state.new_item}/>
        </form>
    }

    renderList() {
        return <ul>
            {this.state.item_list.map((item, index) => <li key={index}>{item}
                <button className="btn btn-danger" onClick={() => this.handleDelete(index)}>delete</button>
            </li>)}
        </ul>
    }

    render() {
        return <React.Fragment>
            {this.renderForm()}
            {this.renderList()}

            <hr/>
        </React.Fragment>
    }
}

// --------------------------------------- Handling unidirectional data flow ---------------------------------------

class AddItemForm extends React.Component {
    state = {
        new_item: ''
    }

    handleChange = (e) => {
        this.setState({...this.state, new_item: e.target.value})
    }

    handleSubmit = (e) => {
        e.preventDefault()
        this.props.handleSubmit(this.state.new_item)
        this.state.new_item = ''
    }

    render() {
        return <form onSubmit={this.handleSubmit}>
            New Item: <input type="text" onChange={this.handleChange} value={this.state.new_item}/>
        </form>
    }
}

class ListItems extends React.Component {
    handleDelete = (index) => {
        this.state.item_list.splice(index, 1)
        this.setState(this.state)
    }

    render() {
        return <ul>
            {this.props.item_list.map((item, index) => <li key={index}>{item}
                <button className="btn btn-danger" onClick={() => this.props.handleDelete(index)}>-</button>
            </li>)}
        </ul>
    }
}

class ListManager extends React.Component {
    state = {
        item_list: this.props.initial_list ? this.props.initial_list : []
    }

    handleSubmit = (item) => {
        this.state.item_list.push(item)
        this.setState(this.state)
    }

    handleDelete = (index) => {
        this.state.item_list.splice(index, 1)
        this.setState(this.state)
    }

    render() {
        return <React.Fragment>
            <AddItemForm handleSubmit={this.handleSubmit}/>
            <ListItems item_list={this.state.item_list} handleDelete={this.handleDelete}/>

            <hr/>
        </React.Fragment>
    }
}

// --------------------------------------------- Lifecycle methods ---------------------------------------------

function LifecycleMethodsFunction() {
    const [input_text, setInputText] = useState('')
    const [button_text, setButtonText] = useState('OFF')

    // Mount, Change
    useEffect(() => {
        console.log('always runs')
    })

    // Change input_text
    useEffect(() => {
        console.log('only when updated input text')
    }, [input_text])

    // Change button_text
    useEffect(() => {
        console.log('only when clicked button')
    }, [button_text])

    // Unmount
    useEffect(() => {
        return () => {
            console.log('do something when unmounting')
        }
    })

    function handleChange(e) {
        setInputText(e.target.value)
    }

    function handleClick() {
        setButtonText(button_text === 'ON' ? 'OFF' : 'ON')
    }

    return <React.Fragment>
        <input type="text" onChange={handleChange} value={input_text}/>
        <button onClick={handleClick}>{button_text}</button>
    </React.Fragment>
}

class LifecycleMethodsClass extends React.Component {
    state = {
        input_text: '',
        button_text: 'OFF'
    }

    componentDidMount() {
        console.log('do something once the component has been mounted')
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevState.input_text !== this.state.input_text) {
            console.log('text has been changed')
        }
        if (prevState.button_text !== this.state.button_text) {
            console.log('button has been clicked')
        }
    }

    componentWillUnmount() {
        console.log('do something before unmounting the component')
    }

    handleChange = (e) => {
        this.setState({...this.state, input_text: e.target.value})
    }

    handleClick = () => {
        this.setState({...this.state, button_text: this.state.button_text === 'ON' ? 'OFF' : 'ON'})
    }

    render() {
        return <React.Fragment>
            <input type="text" onChange={this.handleChange} value={this.state.input_text}/>
            <button onClick={this.handleClick}>{this.state.button_text}</button>
        </React.Fragment>
    }
}

class LifecycleManager extends React.Component {
    state = {
        function_component: false,
        class_component: false,
    }

    handleClickClass = () => {
        this.setState({...this.state, class_component: !this.state.class_component})
    }

    handleClickFunction = () => {
        this.setState({...this.state, function_component: !this.state.function_component})
    }

    render() {
        return <React.Fragment>

            <div>
                <button onClick={this.handleClickFunction}>Toggle Function Component</button>
                {this.state.function_component ? <LifecycleMethodsFunction/> : null}
            </div>

            <div>
                <button onClick={this.handleClickClass}>Toggle Class Component</button>
                {this.state.class_component ? <LifecycleMethodsClass/> : null}
            </div>

        </React.Fragment>
    }
}


// Put it all together
class Sample extends React.Component {
    static propTypes = {
        countries: PropTypes.array.isRequired
    };

    componentDidMount() {
        this.props.getCountries();
    }

    render() {
        return <React.Fragment>
            <JSXElement/>
            <FunctionComponent initial_dividend={0} initial_divisor={1}/>
            <ClassComponent initial_list={['foo', 'bar']}/>
            <ListManager initial_list={['hello', 'world']}/>
            <LifecycleManager/>
        </React.Fragment>
    }
}

const mapStateToProps = state => ({
    countries: state.airpollution.countries
});

export default connect(mapStateToProps, {getCountries})(Sample)
