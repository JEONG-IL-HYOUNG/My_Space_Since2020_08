'use strict';

// Array
// 1. Declaration
const arr1 = new Array()
const arr2 = [1,2]

// Index position
const fruits = ['apple', 'banana']
console.log(fruits)
console.log(fruits.length)
console.log(fruits[1])
console.log(fruits.length - 1)
console.log(fruits[fruits.length - 1])

// 3. Looping over an array
// print all fruits
// a. for
for (let i = 0; i< fruits.length; i ++){
    console.log(fruits[i])
}

// b. for of
for(let fruit of fruits){
    console.log(fruit)
}

// c. forEach
//fruits.forEach() //forEach는 콜백함수를 받아옴. 컨트롤 눌러서 확인해봐
/*
    * Performs the specified action for each element in an array.
    * @param callbackfn  A function that accepts up to three arguments.
        forEach calls the callbackfn function one time for each element in the array.
    * @param thisArg  An object to which the this keyword can refer in the callbackfn function.
        If thisArg is omitted, undefined is used as the this value.
    forEach(callbackfn: (value: T, index: number, array: T[]) => void, thisArg?: any): void;
*/
fruits.forEach(function (fruit, index){  //unnomynous function은 애로우 함수 사용가으
    console.log(fruit, index)
}
)
fruits.forEach((fruit, index) => console.log(fruit, index))

// 4. Addition, deletion, copy
// push : add an item to the end
fruits.push('peach')
console.log(fruits)
// pop: remove an item from the end
fruits.pop()
console.log(fruits)

// unshift: add in item to the beggining
fruits.unshift('lemon')
console.log(fruits)
// shift: remove an item from the beggining
fruits.shift()
console.log(fruits)

// note!! shift, unshift are slower than pop, puth

// splice: remove an item by index position
fruits.push('strawberry', 'peach', 'lemon')
console.log(fruits)
fruits.splice(1,1)
console.log(fruits)
fruits.splice(1,1,'melon', 'watermelon')
console.log(fruits)

// combine two array
const fruits2 = ['abc', 'def']
const newFruits = fruits.concat(fruits2)
console.log(newFruits)

// 5. Searching
// indexOf: find the index
// includes : t, f 반환
console.log('555555')
console.log(fruits.indexOf('lemon')) // 배열안에 해당값 없으면 -1반환
console.log(fruits.includes('lemon')) // t, f 반환

// lastIndexOf
console.log(fruits)
fruits.push('apple')
console.log(fruits)
console.log(fruits.indexOf('apple'))
console.log(fruits.lastIndexOf('apple'))