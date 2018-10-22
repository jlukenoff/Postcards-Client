import React, { Component } from 'react';
import UserData from '../UserData/UserData';

// import PropTypes from 'prop-types';

import styles from './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      users: [],
      ...props,
    };
  }

  componentDidMount() {
    fetch('/api/all_users')
      .then(chunk => chunk.json())
      .then((users) => {
        const date = +(new Date().getMonth().toString() + new Date().getDate().toString());
        this.setState({
          users: users.filter(user => user.anniversay === date),
        });
      })
      .catch(console.error);
  }

  render() {
    /**
     * TODO:
      * - add filtering and sort-by functionality
      * - parse users to a table and display relevent columns
     */
    return (
      <div className={styles.rootContainer}>
        <UserData {...this.state} />
      </div>
    );
  }
}

// App.propTypes = {
// };

export default App;
