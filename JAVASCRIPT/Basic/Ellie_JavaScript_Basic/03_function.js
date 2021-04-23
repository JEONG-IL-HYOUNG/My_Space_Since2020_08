// Function
// - fundamental building block in the program
// - subprogram can be used multiple times
// - performs a task or calculates a value

// 1. Function declaration
// funvrion name(param1, param2) { body....return;}
// one function === one thing 하나의 함수는 한가지 일만 하도록 작성
// naming: doSomething, command, verb
//e.g. createCardAndPoint -> createCard, createPoint
// function is object in JS

function printHello(){
    console.log('Hello')
}
printHello()

function log(message) {
    console.log(message)
}
log('abcde')
log(1234)

// 2. Parameters
// primitive parameters: passed by value
// object parameters: passed by reference
function changeName(obj){
    obj.name = 'coder'
}
//오브젝트는 레퍼런스로 전달 되기 때문에 함수안에서
//오브젝트의 값을 변경하게 되면 변경된 사항이 그대로 메모리에 적용
const ellie = {name: 'ellie'}
changeName(ellie)
console.log(ellie)

// 3. Default Parameters(added in ES6)

function showMessage(message, from){
    console.log(`${message} by ${from}`)
}
showMessage('hi ')

//예전 방법
function showMessage(message, from){
    if (from === undefined){
        from = 'unknown'
    }
    console.log(`${message} by ${from}`)
}
showMessage('hi ')

// ES 6
function showMessage(message, from = 'hello'){
    console.log(`${message} by ${from}`)
}
showMessage('hi ')

// 4. Rest parameters (added in ES6)
function printAll(...args){ //배열형태로 전달하는 파라미터
    for ( let i = 0; i < args.length; i++ ){
        console.log(args[i])
    }
    //간단한 문법으로 출력도 가능함
    for (const arg of args){
        console.log(arg)
    }
    args.forEach((arg) => console.log(arg))

}
printAll('dream', 'coding', 'ellie')


// 5. Local scope
let globalMessage = 'global' // global variable
// 밖에서는 안이 보이지 않고 안에서만 밖을 볼 수 있다.
function printMessage(){
    let message = 'hello'
    console.log(message) // local variable
    console.log(globalMessage)
    function printAnother(){
        let childMessage = 'hello11'
    }
    //console.log(childMessage) // error
}
printMessage()


// 6. Return a value
function sum (a, b){
    return a+b
}
const result = sum(1,2) //3
console.log(`sum: ${sum(3,5)}`)


// 7. Early return, early exit
// bad
function upgradeUser(user){
    if(user.point >10){
        //long upgrade logic
    }
}
// good
function upgradeUser(user){
    if(user.point <= 10){
        return;        
    }
    //long upgrade logic
}
//======================================================
//======================================================
// First - class function
// functions are treatedd like any other variable 
// can be assigned as a value to variable           할당도 됨
// can be passed as an argument to other functions  파라미터로전달도됨
// can be returned by another function              리턴도 됨

// 1. Function Express
// a function declaration can be valled earlier than it is defiend.(hoisted)
// a function expression is created when the execution reaches it.
const print = function(){// anonymous function 함수에 이름이 없는거를 이렇게 부름
    console.log('print')
}
print()
const printAgain = print
printAgain()
const sumAgain = sum
console.log(sumAgain(1,3))


// 2. Callback function using function expression
// 함수를 전달해서 맞는거 찾아오는 걸 callback
function randomQuiz(answer, printYes, printNo){
    if(answer === 'kkkkk'){
        printYes()
    }
    else{
        printNo()
    }
}
//anonymous function
const printYes = function(){
    console.log('yesyes')
}
// named function
// better debugging in debugger's stack traces
// recurisons - 함수안에서 함수 자신을 부르는것
const printNo = function print(){
    console.log('nono')
    //print()  -- recursion 걸림 개발자도구 무한으로 돌아감
}
randomQuiz('wrong', printYes, printNo)
randomQuiz('kkkkk', printYes, printNo)

// Arrow fuction - 함수를 간결하게 만들어줌
// always anonymous
const simplePrint1 = function(){
    console.log('simplePrint1')
}
//위에껄 변형
const simplePrint2 = () => console.log('simplePrint2')

const add1 = function(a,b){
    return a + b
}
const add2 = ( a, b ) => a + b

const simpleMultiply = ( a, b ) => { //block을 사용하면 return을 써야함
    //do something more
    return a*b
}

// IIFE: Immediately Invoked Function Expression
// 함수를 선언함과 동시에 호출하는 것 최근에는 잘 안씀
(function hello() {
    console.log('IIFE')
})()

// Fun quiz time
// function calculate(command, a, b)
// command:(add, substract, divide, multiply, remainder)

function caluate(commandm a, b){
    switch(commandm){
        case 'add':
            return a+b
        case 'substact':
            return a-b
        case 'divide':
            return a/b
        case 'multiply':
            return a*b
        case 'remainder':
            return a%b
        default:
            throw Error('unknown command')
    }
}
console.log(caluate('add', 2, 3))
