import React, { Component } from "react";
import axios from "axios";
import { Table, Form, Input, Button, message } from 'antd';
import { format } from 'date-fns';

class PendingOrder extends Component {
    state = {
        pendingOrder: [],
        orderQuantity: 1,
        couponCode: null,
        couponData: {}
    }

    componentDidMount(){
        this.fetchPendingOrder();
    }

    handleChange = e => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }

    fetchPendingOrder = () => {
        axios.get('http://127.0.0.1:8000/api/pending_order/')
        .then(res => {
            this.setState({
                pendingOrder: res.data
            })
        }).catch(err => message.info(err, 1))
    }

    handleVoidPendingOrder = (pendingOrderID, e) => {
        e.preventDefault();
        axios.delete(`http://127.0.0.1:8000/api/void_pending_order/${pendingOrderID}`)
        .then(res => {
            if(res.status === 204){
                this.fetchPendingOrder();
            }
        }).catch(err => message.error(err, 1))
    }

    handleTransaction = (pendingOrderID, e) => {
        e.preventDefault()

        const { orderQuantity, couponData } = this.state;

        axios.post('http://127.0.0.1:8000/api/transaction/', { pendingOrderID, orderQuantity, couponData })
        .then(res => {
            if(res.status === 201){
                message.success('Thanks for shopping!', 1);
                this.fetchPendingOrder();
            }
        }).catch(err => {
            message.error('insufficient stocks', 1)
        })
    }

    handleCoupon = e => {
        const { couponCode } = this.state;
        axios.get(`http://127.0.0.1:8000/api/${couponCode}/coupon/`)
        .then(res => {
            this.setState({
                couponData: res.data
            })
        }).catch(err => alert('invalid code'))
    }

    render(){
        let arr = [];
        for (let x=1; x<101; x++){
            arr.push(x)
        }

        const { pendingOrder, orderQuantity, couponData } = this.state; 
        const { amount } = couponData;

        const columns = [
            { title: '', dataIndex: 'enterQuantity', key: 'enterQuantity' },
            { title: 'Item', dataIndex: 'item', key: 'item' },
            { title: 'Price', dataIndex: 'price', key: 'price' },
            { title: 'Date', dataIndex: 'timestamp', key: 'timestamp' },
            { title: '', dataIndex: 'void', key: 'void' },
            { title: '', dataIndex: 'confirm', key: 'confirm' },
        ];
        
        const data = pendingOrder.map(item => {
            return(
                    {
                        key: item.code,
                        enterQuantity: <form>
                                            <select name='orderQuantity' value={orderQuantity} onChange={this.handleChange}>
                                                {arr.map(num => <option >{num}</option>)}
                                            </select>
                                        </form>,
                        item: item.pending_order_item,
                        price: <p>PHP {item.pending_order_price}</p>,
                        timestamp: format(new Date(item.timestamp), 'MM-dd-yyyy'),
                        void: <Button
                                type="danger" 
                                onClick={(e) => this.handleVoidPendingOrder(item.id, e)}
                                >
                                Void
                            </Button>,
                        confirm: <Button 
                        onClick={(e) => this.handleTransaction(item.id, e)}
                                >
                                Confirm
                            </Button>
                    }
                )
            }
        )

        return(
            <div style={{ textAlign: 'center' }}>
            <Table
                columns={columns}
                dataSource={data}
                bordered
                footer={
                    () => 
                    pendingOrder.length === 0
                    ?
                    ''
                    :
                    <Form>
                        <Form.Item
                            onChange={this.handleChange}
                            value='couponCode'
                        >
                            <Input 
                                name='couponCode'
                                placeholder="enter coupon code..." 
                                style={{ width: '180px' }}
                            />
                            <Button onClick={this.handleCoupon}>Submit</Button>
                        </Form.Item>
                        {amount === undefined ? '' : <p><strong>PHP {amount}</strong></p>}
                    </Form>
                }
            />
                
            </div>
        )
    }
}

export default PendingOrder;
