import React, { Component } from "react";
import axios from "axios";
import { message, Table } from "antd";
import { format } from 'date-fns';

class Inventory extends Component {
    state = {
        inventory: []
    }

    componentDidMount(){
        this.fetchInventory();
    }

    fetchInventory = () => {
        axios.get('http://127.0.0.1:8000/api/item/inventory/')
        .then(res => {
            this.setState({
                inventory: res.data
            })
        }).catch(err => message.error(err, 1))
    }

    render(){

        const { inventory } = this.state;
        const { active_items_total, expired_items_total, active_expired_items_total, item_qs = [] } = inventory;
        const columns = [
            { title: 'Item', dataIndex: 'item', key: 'item' },
            { title: 'Stocks', dataIndex: 'stocks', key: 'stocks' },
            { title: 'Price', dataIndex: 'price', key: 'price' },
            { title: 'Status', dataIndex: 'status', key: 'status' },
            { title: 'Category', dataIndex: 'category', key: 'category' },
            { title: 'Date Added', dataIndex: 'timestamp', key: 'timestamp' },
            { title: 'Total', dataIndex: 'total', key: 'total' },
        ];
        
        const data = item_qs.map(item => {
            return(
                {
                    key: item.id,
                    item: item.name,
                    stocks: item.stocks,
                    price: <p>PHP {item.price}</p>,
                    status: item.is_expired ? <p><strong>Expired</strong></p> : 'Active',
                    category: item.category,
                    timestamp: format(new Date(item.timestamp), 'MM-dd-yyyy'),
                    total: <p><strong>PHP {item.total}</strong></p>,
                }
            )
        })

        return(
            <div>
                <Table
                    columns={columns}
                    dataSource={data}
                    bordered
                    title={() =>
                        <p>
                            <strong>Active Items Total : PHP {active_items_total}</strong>
                            <br />
                            <strong>Expired Items Total : PHP {expired_items_total}</strong>
                            <br />
                            <strong>Active & Expired Items Total : PHP {active_expired_items_total}</strong>
                        </p>   
                    }
                />
            </div>
        )
    }
}

export default Inventory;

