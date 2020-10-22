createUser = """
var axios = require('axios');
var data = JSON.stringify({"name":"myName","username":"coolUsername","password":"S7r0ngPa55"});

var config = {
  method: 'post',
  url: 'localhost:5000/users',
  headers: { 
    'Content-Type': 'application/json'
  },
  data : data
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});"""

deleteUser = """
var axios = require('axios');

var config = {
  method: 'delete',
  url: 'localhost:5000/users/user1',
  headers: { 
    'Authorization': 'Basic Y0phzmFydy7lOmJoYXfUcnRoYQ=='
  }
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});
"""

getUserList = """
var axios = require('axios');
var data = '';

var config = {
  method: 'get',
  url: 'localhost:5000/users?query=a&count=10',
  headers: { },
  data : data
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});
"""

getUser = """
var axios = require('axios');
var data = '';

var config = {
  method: 'get',
  url: 'localhost:5000/users/uname',
  headers: { },
  data : data
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});
"""