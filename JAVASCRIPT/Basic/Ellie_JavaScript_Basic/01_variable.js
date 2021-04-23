//1. Use strict
// added in ES 5
// use this for Vanilla JS
'use strict';

// 2. Variable (read&write)
// let (added in ES6)

// ES 6 변수에 대한 규격이 신설됐다
// 1. var
// 2. let
// 3. const

// var의 특징
// 변수의 재 선언이 가능하다
// var str = 'aaa';
// var str = 'bbb';

// let의 특징 (read&write)
// 변수의 재 선언이 불가능, but 값의 재 할당은 가능
// let str = 'aaa';
// str = 'aaa'; // 가능
// let str = 'bbb'; // 불가능

// const의 특징 (read only)
// 변수의 재선언 불가능, 값의 재 할당도 불가능
// const str = 'aaaa';
// str = 'bbb'; 불가능
// const str = 'bbb'; 불가능
console.log(age);

let globaltest = 'globbbbb'
{
    let aaa = 'hihi';
    console.log(aaa);
    aaa = 'tetettt'
    console.log(aaa);
    console.log(globaltest);
}
//console.log(aaa); // 블록 밖에 있어서 보이지 않음
console.log(globaltest); //블록밖에서 글로벌 변수 사용은 자주 않하는게 좋다.

//var (don't ever use this!)
//var hoisting( move declaration from bottom to top)
//has no block scope
{
age = 4;
var age;
}
console.log(age);


// 3. Constant 변하지 않은 상수 (read only)
//선언함과 동시에 할당. 그리고 변경 못함
//favor immutable data type always for a few reasons:
//- security
//- thread safety
// - reduce human mistakes
const daysInWeek = 7;
const maxNunber = 5;

// Note!
// Immutable data types: primitive types, frozen onjects(i.e. object.freeze())
// Mutable data types: all objects by default are mutable in JS

// 4. Variable types
// primitive, single item 더 이상 작은 단위로 쪼개지지 않는
// - number, string, boolean, null, undefine, symbol
// object, box container 
// - 싱글 아이템들을 모아서 박스단위로 관리
// function, first-class function 함수도 변수에 할당 가능 

const count = 17;
const size = 17.1;
console.log(`value:${count}, type:${typeof count}`);
console.log(`value:${size}, type:${typeof size}`);

//number - special numeric values: infinity, -infinity, NaN
const infinity = 1 / 0;
const negativeInfinity = -1 / 0;
const nAn = 'not a number' /2;
console.log(infinity);
console.log(negativeInfinity)
console.log(nAn)

//string
const char ='c';
const abcd ='dfkajqd'
const greeting ='hello' + abcd;
console.log(`value:${greeting}, type:${typeof greeting}`);
const helloBob = `hi ${abcd}!`; //template literals(string)

console.log(`value:${helloBob}, type:${typeof helloBob}`);
console.log('value: '+helloBob+'type: '+ typeof helloBob);

// boolean
// false = 0, null, undefined, NaN, ''
// true = any other value
const canRead = true;
const test = 3<1 ;
console.log(`value:${canRead}, type:${typeof canRead}`);
console.log(`value:${test}, type:${typeof test}`);

// null
// null값으로 선언하고, 너는 아무것도 들어있지 않다, 텅텅비어있다 선언
let nothing = null;
console.log(`value:${nothing}, type:${typeof nothing}`);

// undefined
// 아무 값이 지정되어 있지 않을때.
let x;
console.log(`value:${x}, type:${typeof x}`);

// symbol , create unique identifiers for objects
// 맵이나 자료구조에서 고유한 식별자가 필요하거나
// 동시 다발적으로 작업을 할 경우우선순위를 주고싶을때 고유 식별자
const symbol1 = Symbol('id');
const symbol2 = Symbol('id');
//동일한 스트링으로 작성을했어도 다른 심볼로 만들어짐
console.log(symbol1 == symbol2);
//같게 만드는 방법
const gSymbol1 = Symbol.for('id');
const gSymbol2 = Symbol.for('id');

console.log(gSymbol1 == gSymbol2);


//심볼은 이렇게 출력하면 오류가남
//console.log(`value:${symbol1}, type:${typeof symbol1}`);
//스트링으로 변환해서 출력해야함
console.log(`value:${symbol1.description}, type:${typeof symbol1}`);



// 5. Dynamic typing : dynamically typed language
// 어떤 타입인지 선언을 하지 않고 런타임때 할당된 값에 따라 타입변경이 가능

let text = 'hello';
console.log(`value:${text}, type:${typeof text}`);
text = 1;
console.log(`value:${text}, type:${typeof text}`);
text = '7' + 5;
console.log(`value:${text}, type:${typeof text}`);


// 6. objectm real-life, data structure
const ellie = { name: 'ellie', age: 20};
ellie.age =21;
// 이런식으로 변경 가능















































