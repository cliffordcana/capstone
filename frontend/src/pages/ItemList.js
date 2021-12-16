import React, { Component } from "react";
import { Input, Button, message, Table, Form } from 'antd';
import axios from 'axios';

class ItemList extends Component {
    state = {
        items: [],
        query: null,
        queryResponse: null
    }

    componentDidMount(){
        this.fetchItemList();
    }

    handleChange = e => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }

    fetchItemList = () => {
        const { queryResponse } = this.state;
        axios.get('http://127.0.0.1:8000/api/item')
        .then(res => {
            this.setState({
                items: queryResponse === null ? res.data : queryResponse
            })
        });
    };

    handleSearch = () => {
        const { query } = this.state;
        axios.get(`http://127.0.0.1:8000/api/item/?search=${query}`)
        .then(res => {
            res.data.length > 0
            ?
            this.setState({
                queryResponse: res.data
            })
            :
            message.info('no results found');
            this.fetchItemList();
        }).catch(err => {
            message.error(err, 1)
        })
    }

    handlePendingOrder = (id, e) => {
        e.preventDefault();
        axios.post('http://127.0.0.1:8000/api/pending_order/', { id })
        .then(res => {
            if(res.status === 201){
                message.success('added to cart', 1)
            }
        }).catch(err => {
            message.error(err, 1)
        })
    }

    render(){

        const { items, queryResponse } = this.state;

        const columns = [
            { title: '', dataIndex: 'addToCart', key: 'addToCart' },
            { title: 'Items', dataIndex: 'items', key: 'items' },
            { title: 'Price', dataIndex: 'price', key: 'price' },
            { title: 'Stocks', dataIndex: 'stocks', key: 'stocks' },
            { title: 'Code', dataIndex: 'code', key: 'code' },
          ];
          
          const data = items.map(item => {
              return(
                {
                    key: item.id,
                    addToCart: <Button 
                                    size='large' 
                                    type='primary'
                                    onClick={(e) => this.handlePendingOrder(item.id, e)}
                                >
                                    add to cart
                                </Button>,
                    items: item.name,
                    price: <p>PHP {item.price}</p>,
                    stocks: item.stocks,
                    code: item.code,
                  }
              )
          })

        return(
            <div>
            <Form>
                <Form.Item
                    onChange={this.handleChange}
                    value='query'
                >   
                    <Input name='query' placeholder="search..." style={{ width: '250px' }} />
                    <Button onClick={this.handleSearch}>Search</Button>
                </Form.Item>
            </Form>
            <Table
                columns={columns}
                dataSource={data}
            />,
            {
                    queryResponse === null 
                    ? 
                    '' 
                    : 
                    <div style={{ textAlign: 'center' }}>
                        <Button size='large' type='link' onClick={() => window.location.reload()}>Go back</Button>
                    </div>
            }
            </div>
            
        )
    }
}

export default ItemList;
