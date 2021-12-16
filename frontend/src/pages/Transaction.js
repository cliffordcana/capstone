import React, { Component } from "react";
import axios from "axios";
import { PageHeader, Button, Descriptions, message, Input, Modal, Form } from 'antd';
import { format } from 'date-fns';

const extraContent = (
    <div
        style={{
        display: 'flex',
        width: 'max-content',
        justifyContent: 'flex-end',
        }}
    >
    </div>
);
  
const Content = ({ children, extra }) => (
    <div className="content">
        <div className="main">{children}</div>
        <div className="extra">{extra}</div>
    </div>
);
  
class Transaction extends Component {
    state = {
        transactions: [],
        payload: null,
        visible: false,
        transactionReceipt: []
    }

    componentDidMount(){
        this.fetchTransaction();
    }

    handleChange = e => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }

    fetchTransaction = () => {
        axios.get('http://127.0.0.1:8000/api/transaction/')
        .then(res => {
            this.setState({
                transactions: res.data
            })
        })
    }

    handleRefund = (transactionID, e) => {
        e.preventDefault();
        const action = 'REFUND';
        axios.put(`http://127.0.0.1:8000/api/transaction/${transactionID}/`, { action })
        .then(res => {
            if(res.status === 200){
                message.info('transaction refunded', 1);
                this.fetchTransaction();
            }
        })
    }

    handleReturn = (transactionID, e) => {
        e.preventDefault();
        const action = 'RETURN';
        axios.put(`http://127.0.0.1:8000/api/transaction/${transactionID}/`, { action })
        .then(res => {
            if(res.status === 200){
                message.info('transaction canceled', 1);
                this.fetchTransaction();
            }
        })
    }

    handleDelete = (transactionID, e) => {
        e.preventDefault();
        axios.delete(`http://127.0.0.1:8000/api/transaction/${transactionID}/`)
        .then(res => {
            if(res.status === 204){
                message.info('transaction deleted', 1);
                this.fetchTransaction();
            }
        })
    }

    handleTransactionReceipt = e => {
        e.preventDefault();
        const { payload } = this.state;
        axios.post('http://127.0.0.1:8000/api/transaction/receipt', { payload })
        .then(res => {
            this.setState({
                transactionReceipt: res.data,
                visible: true
            })
        })
    } 

    render(){
        const { transactions, visible, transactionReceipt } = this.state;
        const { transaction_receipt = [], transaction_total } = transactionReceipt;
        
        return(
            <div style={{ textAlign: 'center' }}>
                <Form>
                    <Form.Item
                        onChange={this.handleChange}
                        value='payload'
                    >
                        <Input 
                            name='payload'
                            placeholder="enter confirmation number or number of orders..." 
                            style={{ width: '350px' }}
                        />
                        <Button onClick={this.handleTransactionReceipt}>Get Receipt</Button>
                    </Form.Item>
                </Form>
                 {
                     transactions.map(transaction => 
                        <PageHeader
                                className="site-page-header-responsive"
                                title={transaction.transaction_item}
                                subTitle={transaction.transaction_category}
                            extra={[
                            <Button key="3" 
                                type="danger"
                                onClick={(e) => this.handleDelete(transaction.id, e)}
                            >
                                {transaction.transaction_status === 'COMPLETED' ? 'Cancel' : ''}
                            </Button>,
                            <Button key="2" 
                                type="danger"
                                onClick={(e) => this.handleRefund(transaction.id, e)}
                            >
                                {transaction.transaction_status === 'COMPLETED' ? 'Refund' : ''}
                            </Button>,
                            <Button key="1" 
                                type="danger"
                                onClick={(e) => this.handleReturn(transaction.id, e)}
                            >
                                {transaction.transaction_status === 'COMPLETED' ? 'Return' : ''}
                            </Button>,
                            ]}
                        >
                            <Content extra={extraContent}>
                                <Descriptions size="small" column={2}>
                                    <Descriptions.Item label="Date">{format(new Date(transaction.timestamp), 'MM-dd-yyyy')}</Descriptions.Item>
                                    <Descriptions.Item label="Confirmation Number">
                                    {transaction.confirmation_number}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="Coupon Discount">
                                        {
                                            transaction.coupon_amount === undefined ? 'N/A' : transaction.coupon_amount
                                        }
                                    </Descriptions.Item>
                                    <Descriptions.Item label="Status">{transaction.transaction_status}</Descriptions.Item>
                                    <Descriptions.Item label="Price">{transaction.transaction_price}</Descriptions.Item>
                                    <Descriptions.Item label="Quantity">{transaction.transaction_quantity}</Descriptions.Item>
                                    <Descriptions.Item label="Total">{transaction.transaction_total}</Descriptions.Item>
                                </Descriptions>
                            </Content>
                        </PageHeader>,
                        visible &&
                        Modal.success({
                            content:
                            
                            <div style={{ textAlign: 'center' }}>
                                <p><strong>D&D Mart</strong></p>
                                {
                                    transaction_receipt.map(transaction => 
                                        <ul key={transaction.id}>
                                            <li>
                                                <p>Item: {transaction.transaction_item}</p>
                                                <p>Confirmation Number: {transaction.confirmation_number}</p>
                                                <p>
                                                    Date: {format(new Date(transaction.timestamp), 'MM-dd-yyyy')}
                                                </p>
                                                <p>Price: {transaction.transaction_price}</p>
                                                <p>Quantity: {transaction.transaction_quantity}</p>
                                                
                                                {
                                                transaction.coupon === null 
                                                ? 
                                                '' 
                                                : 
                                                <p>Coupon Discount: {transaction.coupon_amount}</p>
                                                }
                                                
                                                <p><strong>Total: {transaction.transaction_total}</strong></p>
                                            </li>
                                        </ul>
                                            
                                    )
                                    
                                }
                                {
                                    transaction_total === undefined 
                                    ? 
                                    '' 
                                    : 
                                    <p><strong>Total Amount: {transaction_total}</strong></p>
                                }
                                <p><strong>This receipt is only valid for 3 days from date of purchased.</strong></p>
                            </div>
                            
                          })
                            
                        
                    )
                 }
            </div>  
        )
    }
}

export default Transaction;
