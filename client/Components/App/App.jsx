import React, { Component } from 'react';

// import PropTypes from 'prop-types';

import styles from './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      anniversaryUsers: [],
      allUsers: [],
      ...props,
    };
  }

  componentDidMount() {
    fetch('/api/all_users')
      .then(chunk => chunk.json())
      .then((users) => {
        const date = +(new Date().getMonth().toString() + new Date().getDate().toString());
        this.setState({
          anniversaryUsers: users.filter(user => user.anniversay === date),
          allUsers: users,
        });
      })
      .catch(console.error);
  }

  render() {
    const { anniversaryUsers, allUsers } = this.state;
    return (
      <div className={styles.rootContainer}>
        <div className={styles['user-container--all']}>
          <p>All Users:</p>
          {allUsers.map(user => (<li>{user.name}</li>))}
        </div>
        <div className={styles['user-container--anniversary']}>
          <p>These users will be sent a postcard today:</p>
          {anniversaryUsers.length > 0 && (
          <ul>
            {anniversaryUsers.map(user => (<li>{user.name}</li>))}
          </ul>)}
        </div>
      </div>
    );
  }
}

// App.propTypes = {
// };

export default App;
