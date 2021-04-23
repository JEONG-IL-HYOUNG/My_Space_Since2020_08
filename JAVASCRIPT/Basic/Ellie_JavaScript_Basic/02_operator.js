// 1. String concatenation(문자열 연결)
console.log('my' + 'cat');
console.log('1' + 2);
console.log(`string literals:
''''
1+2 = ${1 + 2}`);

console.log("jih's \n\t notebook")

// 2. Numeric operators
console.log(1 + 1);
console.log(1 - 1);
console.log(1 / 1);
console.log(1 * 1);
console.log(5 % 2);
console.log(2 ** 3);

// 3. Increment & decrement operators
let counter =2;
const preIncrement = ++ counter;
console.log(`preIncrement: ${preIncrement}, counter: ${counter}`);
const postIncrement = counter++;
console.log(`postIncrement: ${postIncrement}, counter: ${counter}`);

// 4. Assignment operators
let x = 3;
let y = 6;
x+=y; //x= x+y;
x-=y;

// 5. Comparison operators
console.log(10 < 6);
console.log(10 <= 6);
console.log(10 > 6);
console.log(10 >= 6);

// 6. logical operator: \\ (or) , && (and), ! (not)
const value1 = false;
const value2 = 4 < 2 ;

// \\ (or), finds the first turthy value
// or 연산자는 처음 value1에서 트루가 나오면 멈춘다.
// check() 함수까지 호출하지 않음
console.log(`or: ${value1 || value2 || check()}`);

// && (and), finds the first falsy value
//첫번째 value1이 false 면 바로 멈춤.
console.log(`or: ${value1 && value2 && check()}`);

// &&은 null값 체크할때도 자주쓰임
// often used to compress long if-statement
// nullable object && nullableObject.someting
/*ex)

if (nullableObject != null){
    nullableObject.something;
}
*/

function check() {
    for (let i =0; i<10; i++){
        //wasting time
        console.log('hoho')
    }
    return true;
}

// ! (not) 값을 반대로 바꿔줌
console.log(!value1);


// 7. Equlity
const stringFive = '5';
const numberFive = 5;

// == loose equality, with type conversion 타입 변경후 비교
console.log(stringFive == numberFive);
console.log(stringFive != numberFive);

// === strict equalitym no type conversion
console.log(stringFive === numberFive);
console.log(stringFive !== numberFive);

//object equality by reference
const jih1 = { name: 'jih'};
const jih2 = { name: 'jih'};
const jih3 = jih1;
console.log(jih1 == jih2);
console.log(jih1 === jih2);
console.log(jih1 === jih3);

// quiz time!!
console.log(0 == false);  //t
console.log(0 === false); //f
console.log('' == false); //t
console.log('' == false); //f
console.log(null == undefined); //t
console.log(null === undefined); // f

// 8. Conditional operators: if
// if, else if, else
const name1= 'jih'
if (name1 === 'jih'){
    console.log('wellcome jih');
}
else if (name1 === 'coder'){
    console.log('you are jih');
}
else{
    console.log('unknown');
}

// 9. Ternary operator: ? 
// if 문을 더 간결하게 쓰는..
// condition ? value1 : value2;
console.log(name1 === 'jih' ? 'yes' : 'no')

// 10. Switch statement
// use for multiple if checks
// use for enum-like value check
// use for multiple type checks in TS
const browser = 'IE'
switch (browser){
    case 'IE':
        console.log('go away!')
        break
    case 'Chrome':
        console.log('love you!')
        break
    case 'Firefox':
        console.log('love you!')
        break
    default:
        console.log('same all!')
        break
}

// 11. Loops
// while loop, while the condition is truthy,
// body code is executed.
// condition이 false가 나오기 전까지 계속 돔.
let i = 3
while (i > 0){
    console.log(`while: ${i}`)
    i--;
}

// do while 은 do의 블락안에 먼저 실행 후 while문 실행
do{
    console.log(`do while: ${i}`)
    i--
} while ( i> 0)


// for loop, for(begin; condition; step)
for( i = 3; i > 0; i--){    
    console.log(`for: ${i}`)
}
for(let i =3; i > 0; i -=2 ){
    //inline variable declaration
    console.log(`inline variable for: ${i}`)
}

//nest loops
for(let i =0; i<10; i++){
    for(let j =0; j<10; j++){
        console.log(`i:${i}, j:${j}`)
    }
}

//quiz
// break, continue
// break-루프끝내기, continue-지금것만 스킵하고 다음 스텝으로 
//Q1. iterate from 0 to 10 and print only even numbers
//(use continue)
for(let i=0; i<11; i++){
    if(i%2 !== 0){
        continue;
    }
    console.log(`q1. ${i}`)
}
// 실무에서는 이게 더 좋음
for(let i=0; i<11; i++){
    if(i%2 == 0){ 
        console.log(`q1. ${i}`)       
    }    
}

// Q2. iterate from 0 to 10 and print numbers until reaching 8
//(use break)
for (let i = 0; i <11; i ++){
    if(i>8){
        break
    }
    console.log(`q2. ${i}`)
}








