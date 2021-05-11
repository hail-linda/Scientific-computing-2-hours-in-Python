import axios from 'axios'

const service = axios.create({
  timeout:15000
})
export default service
