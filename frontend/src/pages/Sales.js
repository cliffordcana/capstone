import React, { Component } from "react";
import axios from "axios";
import { Table, message } from "antd";
import { format } from 'date-fns'

class Sales extends Component {
    state = {
        sales: [],
    }

    componentDidMount(){
        this.fetchSales();
    }

    fetchSales = () => {
        axios.get('http://127.0.0.1:8000/api/transaction/sales/')
        .then(res => {
            this.setState({
                sales: res.data
            })
        }).catch(err => message.info(err, 1))
    }

    render(){
        const { transaction_qs = [], sales_today, sales_weekly, sales_monthly } = this.state.sales;

        const columns = [
            { title: 'Item', dataIndex: 'item', key: 'item' },
            { title: 'Transaction Date', dataIndex: 'timestamp', key: 'timestamp' },
            { title: 'Quantity', dataIndex: 'quantity', key: 'quantity' },
            { title: 'Price', dataIndex: 'price', key: 'price' },
            { title: 'Coupon Discount', dataIndex: 'couponDiscount', key: 'couponDiscount' },
            { title: 'Total', dataIndex: 'total', key: 'total' },
        ];
        
        const data = transaction_qs.map(sale => {
            return(
                {
                    key: sale.id,
                    item: sale.transaction_item,
                    timestamp: format(new Date(sale.timestamp), 'MM-dd-yyyy'), 
                    quantity: sale.transaction_quantity,
                    price: sale.transaction_price,
                    couponDiscount: sale.coupon === null ? 'N/A' : sale.coupon_amount,
                    total: sale.transaction_total
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
                            <strong>Daily Sales : PHP {sales_today} </strong>
                            <br />
                            <strong>Weekly Sales : PHP {sales_weekly}</strong>
                            <br />
                            <strong>Monthly Sales  : PHP {sales_monthly}</strong>
                        </p>   
                    }
                    
                />
            </div>
        )
    }
}

export default Sales;
