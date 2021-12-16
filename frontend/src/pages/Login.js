import React, { Component } from 'react';
import axios from 'axios';
import { Form, Input, Button, message, Row, Modal } from 'antd';
import { Redirect } from 'react-router-dom';

class Login extends Component {
    state = {
        visible: false
    }

    onFinish = (values) => {
        const { username , password } = values;
        axios.post('http://127.0.0.1:8000/api/auth/login/', { username, password })
        .then(res => {
            if(res.status === 200){
                localStorage.setItem('key', res.data.key);
                window.location.reload();
            }
        }).catch(err => {
            message.error('invalid username or password', 1)
        })
    };
    
    render(){

        const token = localStorage.getItem('key');
        
        return(
            <div>
                {
                    token === null 
                    ?
                    
                    <Modal 
                        visible={true} 
                        title={<p style={{ textAlign: 'center' }}><strong>D&D Mart</strong></p>}
                        footer=''
                        centered
                        closable={false}
                        //style={{ height: '25px' }}
                    >
                    <Row type="flex" justify="center" align="middle">
                    <Form
                        onFinish={this.onFinish}
                        style={{ width: '250px', float: '-moz-initial' }}
                    >
                    <Form.Item
                        label="Username"
                        name="username"
                        rules={[
                        {
                            required: true,
                            message: 'Please input your username!',
                        },
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        label="Password"
                        name="password"
                        rules={[
                        {
                            required: true,
                            message: 'Please input your password!',
                        },
                        ]}
                    >
                        <Input.Password />
                    </Form.Item>

                    <Form.Item
                        wrapperCol={{
                        offset: 8,
                        span: 16,
                        }}
                    >
                        <Button type="primary" htmlType="submit">
                        Login
                        </Button>
                    </Form.Item>
                    </Form>
                    </Row>
                    </Modal>
                    
                    :
                    <Redirect to='/' />
                }
            </div>
        )
    }
} 

export default Login;

