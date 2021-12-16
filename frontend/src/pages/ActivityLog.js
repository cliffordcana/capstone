import React, { Component } from 'react';
import { List, message } from 'antd';
import axios from 'axios';
import { format } from 'date-fns';

class ActivityLog extends Component {
  state = {
    data: []
  }

  componentDidMount(){
    this.fetchActivityLog();
  }

  fetchActivityLog = () => {
    axios.get('http://127.0.0.1:8000/api/activity_log/')
    .then(res => {
      this.setState({
        data: res.data
      })
    }).catch(err => message.error(err, 1))
  }

  render(){
    const { data } = this.state;

    return(
      <div>
        <List
          dataSource={data}
          renderItem={log => (
            <List.Item key={log.id}>
              <List.Item.Meta
                title={log.item_log || log.transaction_log || log.coupon_log || log.pending_order_log}
              />
              <div>{format(new Date(log.timestamp), "MM-dd-yyyy 'at' h:mm a")}</div>
            </List.Item>
          )}
        />
      </div>
    )
  }
}

export default ActivityLog;

