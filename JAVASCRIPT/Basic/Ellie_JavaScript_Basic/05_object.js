// Objects
// one of the Javascipt`s data types/
// a collection of related data and/or functionality
// Nearly all objects in javaScript are instances of Object
// object = { key : value }


// 1. Literals and properties
const name = 'ellie'
const age = 444
function print(name, age){
    console.log(name)
    console.log(age)
}
print(name, age)

const ellie = { name:'ellie', age: 41}
function print(person){
    console.log(person.name)
    console.log(person.age)
}
print(ellie)

//object 생성방법
const obj1 = {}
const obj2 = new Object() //new를 사용하여 클래스 템플릿 이용

ellie.hasJob = true // 오브젝트를 ellie를 정의 했어도 뒤늦게 추가도 가능함.
console.log(ellie.hasJob)

delete ellie.hasJob
console.log(ellie.hasJob) //뒤늦게 삭제도 가능 .

// 2. Computed properties 계산된 property
console.log(ellie.name)
console.log(ellie['name']) // key should be always string
console.log(ellie[name]) // 값이 안나옴
ellie['hasJob'] = true
console.log(ellie.hasJob)

function printValue(obj, key){
    //console.log(obj.key)
    console.log(obj[key])
}
printValue(ellie, 'name')
printValue(ellie, 'age')

// 3. Property value shorthand
const person1 = { name: 'bob' , age : 2 }
const person2 = { name: 'steve' , age : 3 }
const person3 = { name: 'dave' , age : 4 }
// const person4 = makePerson('abc' , 30)
const person4 = new Person('abc', 33)
console.log(person4)
console.log(person3)

// 클래스가 생기기 이전에는 이런식으로 만들었엇다.
// function makePerson(name, age){
//     return{
//         // name: name, 키와 밸류가 동일하다면 밑에 처럼해도 됨.
//         // age: age
//         name,
//         age
//     }
// }

//오브젝트를 생성하는 함수는 보통 이런식으로 한다.
// 4. Constructor function
function Person(name, age){
    //this ={} 생략된부분임 자동으로 처리
   this.name = name
   this.age = age
   //return this  생략된부분임 자동으로 처리
}

// 5. in operator: property existence check (key in obj)
console.log('name' in ellie)
console.log('age' in ellie)
console.log('random' in ellie)
console.log(ellie.random)

// 6. for..in  vs for..of
// for (key in obj)
console.clear()
for(key in ellie){
    console.log(key)
}
//for(value of iterable)
const array = [1,2,4,5]
// for(let i =0; i<array.length; i++){
//     console.log(array[i])
// } 예전 방법
//
for(value of array){
    console.log(value)
}

// 7. Fun cloning
// Object.assign(dest, [obj1, obj2, obj3...])
const user = { name : 'ellie', age : 20 }
const user2 = user

user2.name = 'coder'
console.log(user)

// old way
const user3 = {}
for ( key in user){
    user3[key] = user[key]
}
console.log(user3)

// new way
// const user4 = {}
// Object.assign(user4, user)
const user4 = Object.assign({}, user)
console.log(user4)

// another exampl
const fruit1 = { color : 'red' }
const fruit2 = { color : 'blue', size : 'big' }
const mixed = Object.assign({}, fruit1, fruit2)
console.log(mixed)
console.log(mixed.color)// color는 블루로 나옴. 뒤에거가 덮어씌워지는 식
console.log(mixed.size)




















