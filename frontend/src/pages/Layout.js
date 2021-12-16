import React, { Component } from "react";
import { Layout, Menu, Tooltip } from 'antd';
import { Link } from 'react-router-dom';
import { LogoutOutlined } from '@ant-design/icons';
import axios from "axios";
import Login from "./Login";

const { Header, Content } = Layout;

class CustomLayout extends Component {

    handleLogOut = () => {
        axios.post('http://127.0.0.1:8000/api/auth/logout/')
        .then(res => {
            if(res.status === 200){
                localStorage.removeItem('key');
                window.location.reload();
            }
        })
    } 

    render(){
        const token = localStorage.getItem('key');
        
        return(
            <div>
            {
                //token === null
                //?
                //<Login />
                //:
                <Layout>
                <Header className="header">
                    <div className="logo" />
                    <Menu theme="dark" mode="horizontal">
                        <Menu.Item key="1"><Link to='/' />D&D Mart</Menu.Item>
                        <Menu.Item key="2"><Link to='/pending-order' />Pending Order</Menu.Item>
                        <Menu.Item key="3"><Link to='/activity-log' />Log</Menu.Item>
                        <Menu.Item key="4"><Link to='/transaction/sales' />Sales</Menu.Item>
                        <Menu.Item key="5"><Link to='/item/inventory' />Inventory</Menu.Item>
                        <Menu.Item key="6"><Link to='/transaction' />Transaction</Menu.Item>
                        <Menu.Item key="7" style={{ marginLeft: 'auto' }} >
                            <Tooltip title='Logout'>
                                <LogoutOutlined onClick={this.handleLogOut}/>
                            </Tooltip>
                        </Menu.Item>
                    </Menu>
                    </Header>
                    <Content style={{ padding: '0 50px' }}>
                    <div style={{ padding: 24 }}>
                        {
                            token === null 
                            ?
                            <Login />
                            :
                            this.props.children
                        }
                    </div>
                    </Content>
                </Layout>
            }
            </div>
        )
    }
}

export default CustomLayout;
