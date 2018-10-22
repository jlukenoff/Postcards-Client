import React from 'react';
// import PropTypes from 'prop-types';

import styles from './UserData.css';

const UserData = ({ users, displayParams }) => (
  <div className={styles['user-container']}>
    <table>
      <tr>
        <th>
          Name
        </th>
        <th>
          Join Date
        </th>
        <th>
          Street Address
        </th>
        <th>
          City
        </th>
        <th>
          State
        </th>
      </tr>
      {users.filter(user => {
          if (!displayParams.filter) return true;
        })
        .sort(user => {
          if (!displayParams.sort) return 0;
        })
        .map(user => (
          <tr>
            <th>
              {user.name}
            </th>
            <th>
              {user.anniversary}
            </th>
            <th>
              {user.address_line1}
            </th>
            <th>
              {user.city}
            </th>
            <th>
              {user.state}
            </th>
          </tr>
        ))}
    </table>
  </div>
);

// UserData.propTypes = {
// };

export default UserData;
