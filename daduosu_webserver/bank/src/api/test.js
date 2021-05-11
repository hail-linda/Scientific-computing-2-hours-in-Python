import request from '@/utils/request'
import axios from 'axios';
export function test(data){
  return request({
    url:'/login',
    method:'post',
    params:data
  })
}
export const requestLogin = params => {
  return axios.post('/login', params).then(res => res.data);
};
