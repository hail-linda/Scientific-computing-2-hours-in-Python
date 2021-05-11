import Mock from 'mockjs';

const LoginUsers = [{
  id: 1,
  username: 'admin',
  password: '123456',
  name: '李某某'
}];

const Users = [];

for (let i = 0; i < 86; i++) {
  Users.push(Mock.mock({
    id: Mock.Random.guid(),
    name: Mock.Random.cname(),
    sex: Mock.Random.integer(0, 1),
    'age|18-60': 1,
    birth: Mock.Random.date(),
    addr: Mock.mock('@county(true)'),
  }));
}

export {
  LoginUsers,
  Users
};
