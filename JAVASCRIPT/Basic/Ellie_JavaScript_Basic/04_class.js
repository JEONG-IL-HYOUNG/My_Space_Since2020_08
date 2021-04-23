'use strict'
//Object-oriented programming
// class : template
// object: instance of a class

// Javascript classes
// - introduced in ES6
// - syntactical sugar over prototype-based inheitance

// 1. Class declaration
class Person{
    //constructor
    constructor(name, age){ //생성자
        //fields
        this.name = name
        this.age = age
    }

    // methods
    speak(){
        console.log(`${this.name}: hello!`)
    }
}
// object 생성
const ellie = new Person('ellie' , 20)
console.log(ellie.name)
console.log(ellie.age)
ellie.speak()


// 2. Getter and setters
class User {
    constructor(firstName, lastName, age){
        this.firstName = firstName
        this.lastName = lastName
        this.age = age
    }
    get age(){
        return this._age

    }
    set age(value){
        /*방법1
        if(value < 0){
            throw Error('age can not be negative')
        }
        this._age = value
        */
       this._age = value < 0 ? 0 : value
    }
}

const user1 = new User('Steve', 'Job', -1)
console.log(user1.age)

// 3. Fields ( public, private)
// Too soon 지금은 쓰기엔 무리..21/02/04
class Experiment{
    publicField = 2
    #privateField =0
}
const experiment = new Experiment()
console.log(experiment.publicField)
console.log(experiment.privateField)

// 4. Static properties and methods
// Too soon!
// 클래스에 잇는 고유한 값 . 오브젝트에 상관없이 클래스에 연결
class Article{
    static publisher = 'Dream Coding'
    constructor(articleNumber){
        this.articleNumber = articleNumber
    }
    static printPublisher(){
        console.log(Article.publisher)
    }
}
const aricle1 = new Article(1)
const aricle2 = new Article(2)
// console.log(aricle1.publisher) - 스태틱을 만들지 않앗다면 출력가능
// 콘솔에 undefined로 나옴
console.log(Article.publisher) // 클래스에 연결하여 사용
Article.printPublisher()

// 상속과 다양성
// 5. Inheritance
// a way for one class to extend another class
class Shape{
    constructor(width, height, color){
        this.width = width
        this.height = height
        this.color = color
    }
    draw(){
        console.log(`drawing ${this.color} color of`)
    }
    getArea(){
        return this.width * this.height
    }
}

class Rectangle extends Shape{}
class Triangle extends Shape{
    //over riding
    //필요한 함수만 골라와서 바꿀수있음
    draw(){
        super.draw() //부모의 드로우함수를 먼저불러온 다음에 정의한 함수사용
        console.log('overide - draw')
    }
    getArea(){
        return (this.width * this.height) / 2
    }
    toString(){
        return `Triangle: color: ${this.color}`
    }
}

const rectangle = new Rectangle(20,20,'blue')
rectangle.draw()
console.log(rectangle.getArea())

const triangle = new Triangle(20,20,'red')
triangle.draw()
console.log(triangle.getArea())

// 6. Class checking: instanceOf
console.log(rectangle instanceof Rectangle)
// 왼쪽에 잇는 오브젝트가 오른쪽의 클래스안에 있는 인스턴스인지 아닌지 t or f
console.log(triangle instanceof Rectangle)
console.log(triangle instanceof Triangle)
console.log(triangle instanceof Shape)
console.log(triangle instanceof Object)
console.log(triangle.toString());


//MDN javascript reference 참고



