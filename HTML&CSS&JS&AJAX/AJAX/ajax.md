## 1.AJAX

###   1.什么是AJAX

​	Asynchronous Javascript And Xml
​		异步的       JS        和   xml(*EX*tensible *M*arkup *L*anguage)可扩展标记语言（保存数据用）

​    通过 JS 异步的向服务器发送请求并接收响应数据

​	同步访问：
​		当客户端向服务器发送请求时，服务器在处理的过程中，浏览器只能等待，效率较低

​	异步访问：
​		当客户端向服务器发送请求时，服务器在处理的过程中，客户端可以做其他的操作，不需要一直等待

​	AJAX优点：

​		1.异步访问

​		2.局部刷新

​	使用场合：

​		1.搜索建议

​		2.表单验证

​		3.前后端分离



通过在后台与服务器进行少量数据交换，Ajax 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。

### 2.AJAX核心对象 - 异步对象(XMLHttpRequest)

#### 	1.什么是XMLHttpRequest [简称为 xhr]

​		称为 "异步对象"，代替浏览器向服务器发送异步的请求并接收响应

​		[xhr 是由JS来提供的]

#### 	2.创建 异步对象 (xhr)

​		1.IE7+,Chrome,Firefox,Safari,Opera)  -> 调用 XMLHttpRequest 生成 xhr对象

​		2.IE低版本浏览器中(IE6以及以下) -> 调用 ActiveXObject() 生成xhr

```javascript
//由于上述浏览器的不同，写如下判断来创建xhr
//通常写入一个.js文件中，放到static文件夹下。
<script>
	if(window.XMLHttpRequest){
		//支持 XMLHttpRequest
		var xhr = new XMLHttpRequest();
	}else{
		//不支持XMLHttpRequest,使用 ActiveXObject 创建异步对象
		var xhr = new ActiveXObject("Microsoft.XMLHTTP");
	}
</script>
```

#### 	3.xhr 的成员

​		1.方法 - open()

​			作用：创建请求

​			语法：open(method,url,asyn)

​			参数：

​				method:请求方式，取值'get' 或 'post'

​				url:请求地址，字符串

​				asyn:是否采用异步的方式  - true:异步 / false:同步

```html
<script>
        console.log(xhr);
        xhr.open('get','http://127.0.0.1:5000/getServer',true);
</script>
```

```python
@app.route("/getServer")
def getServer():
    return "接收AJSX get 请求成功"
```



​		2.方法 - send()

​			作用：通知xhr向服务器端发送请求

​			语法：send(body)

​			参数：

​				get请求：body的值为null  ->  send(null)

​				post请求：body的值为请求数据  ->  send("请求数据")	

​		3.属性 - readyState

​			作用：请求状态，通过不同的请求状态来表示xhr与服务器的交互情况

​			由0-4共5个值来表示5个不同的状态

|      状态       |                      说明                      |
| :-------------: | :--------------------------------------------: |
|        0        |      代理被创建，但尚未调用 open() 方法。      |
|        1        |           `open()` 方法已经被调用。            |
|        2        |  `send()` 方法已经被调用，响应头也已经被接收   |
|        3        | 下载中； `responseText` 属性已经包含部分数据。 |
| 4--**重点关注** |                 下载操作已完成                 |

​		4.属性 - responseText

​			作用：响应数据

​		5.属性 - status

​			作用：服务器端的响应状态码

| 状态码 |                   说明                   |
| :----: | :--------------------------------------: |
|  200   | 表示服务器正确处理所有的请求以及给出响应 |
|  403   | 禁止访问（权限不足） |
|  404   |              请求资源不存在              |
|  405   | 请求方式不允许（视图函数不接收get或者post请求） |
|  500   |              服务器内部错误              |

​		6.事件 - onreadystatechange

​			语法：xhr.onreadystatechange=function(){}

​			作用：每当xhr的readyState发生改变的时候都要触发的操作；

​			也称作回调函数；当readyState的值为4且status值为200的时候，才可以获取响应数据

```html
#xhr.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>xhr</title>
</head>
<body>
    <h1>xhr</h1>
    <div id='show'></div>
    <!-- 导入外部js文件  获取xhr -->
    <!-- /static flask指定的默认的查找静态文件的路径 -->
    <script src="/static/common.js"></script>
    <script>
        // var xhr = new XMLHttpRequest();
        console.log(xhr);
        //1.通过xhr对象创建请求
        // open(method,url,asyn)
        xhr.open('get','http://127.0.0.1:5000/getServer',true);
        //2.监听xhr.readyState 的值 
        //每次值发生改变 都会触发xhr.onreadystatechange事件
        xhr.onreadystatechange = function(){
            if(xhr.readyState == 4 && xhr.status == 200){
                //如果响应全部完成 同时 响应状态码为200
                var div = document.getElementById('show');
                div.innerHTML = xhr.responseText;
            }
            // if(xhr.readyState == 4){
            //     console.log('获取响应结果完成')
            //     //判断响应结果的状态 如果响应状态码 为200 表示一切正常
            //     //这时可以获取响应结果
            //     if(xhr.status == 200){
            //         console.log(xhr.responseText)
            //         document.getElementById('show').innerHTML = xhr.responseText
            //     }
            // }
        }
        //3.发送请求
        xhr.send(null);
    </script>
</body>
</html>
```



### 	3.AJAX的操作步骤

#### 		1.GET请求	

```javascript
//1.创建xhr请求
var xhr = createXhr();
//2.创建请求 - open()
xhr.open('get',url,asyn[true|false])
//3.设置回调函数 - onreadystatechange
xhr.onreadystatechange = function(){
    if(xhr.readyState == 4 && xhr.status == 200){
        //接收响应
        var res = xhr.responseText;
        
    }
}
//4.发送请求
xhr.send(null);

//注意：若含有请求参数 - URL后拼接 查询字符串 QueryString
//ex: xhr.open('get','/url?key=value&key=value',asyn)
```

#### 		2.POST请求

```javascript
//1.创建xhr请求
var xhr = createXhr();
//2.创建请求 - open()
xhr.open('post',url,asyn[true|false])
//3.设置回调函数 - onreadystatechange
xhr.onreadystatechange = function(){
    if(xhr.readyState == 4 && xhr.status == 200){
        //接收响应
        xhr.responseText;
    }
}
//4设置Content-Type;
//默认ajax post的Content-Type为 "text/plain;charset=utf-8"
xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
//5.发送请求
xhr.send('请求数据');
//请求数据同查询字符串 "uname=guoxiaonao&age=18"
```

```html
#ajax-get.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <input type="text" id="uname" > 
    <button id="btn">发送get请求</button>
    <div id="show"></div>
    <script src="/static/common.js"></script>
    <script>
        var uname = document.getElementById('uname')
        var btn = document.getElementById('btn')
        btn.onclick = function(){
            var url = '/getServer?uname='+uname.value
            xhr.open('get',url,true)
            xhr.onreadystatechange = function(){
                if(xhr.readyState == 4 && xhr.status == 200){
                    var div = document.getElementById('show');
                    div.innerHTML = xhr.responseText;
                }
            }
            xhr.send(null)
        }
       
    </script>
    <script>
        // 0.创建xhr对象 
        var xhr = new XMLHttpRequest()
        // 1.创建请求
        // 获取文本框
        var uname = document.getElementById('uname')
        //将get请求需要提交的数据拼接到地址栏
        var url = '/getServer?uname='+uname.value
        console.log(url);///getServer?uname=shibw
        xhr.open('get',url,true)
        //2.监听事件  处理响应结果
        xhr.onreadystatechange = function(){
            if(xhr.readyState == 4 && xhr.staus == 200){
                var div = document.getElementById('show');
                div.innerHTML = xhr.responseText;
            }
        }
        //3.发送请求
        xhr.send(null)
    </script>
</body>
</html>
```

```html
#ajax-post.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <div>
        姓名  <input type="text" id="uname">
    </div>
    <div>
        年龄  <input type="text" id="age">
    </div>
    <div>
        邮箱  <input type="text" id="email">
    </div>
    <button id="btn">提交</button>
    <div id="show"></div>
    <script src="/static/common.js"></script>
    <script>
        var btn = document.getElementById('btn');
        btn.onclick = function(){
            xhr.open('post','/postServer',true);
            xhr.onreadystatechange = function(){
                if(xhr.readyState == 4 && xhr.status == 200){
                    var div = document.getElementById('show');
                    div.innerHTML = xhr.responseText;
                }
            }
            //uname=guoxiaonao&age=18&email=guoxn@tedu.cn
            var uname = document.getElementById('uname').value
            var age = document.getElementById('age').value
            var email = document.getElementById('email').value
            var data = 'uname='+uname+'&age='+age+'&email='+email
            xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded')
            xhr.send(data);
        }
    </script>
</body>
</html>
```

```html
#calc.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>calc</title>
</head>
<body>
    <div>
        <input type="text" id="num1">
    </div>
    <div>
        <select name="" id="opt">
            <option value="0">加</option>
            <option value="1">减</option>
        </select>
    </div>
    <div>
        <input type="text" id="num2">
    </div>
    <button id="btn">计算</button>
    <div id="show"></div>

    <script src="/static/common.js"></script>
    <script>
        var xhr = new XMLHttpRequest();
        var btn = document.getElementById('btn');
        btn.onclick = function(){
            //获取用户输入的num1  num2  opt的值
            var num1 = document.getElementById('num1').value
            var opt = document.getElementById('opt').value
            var num2 = document.getElementById('num2').value
            //将值和地址拼接成字符串
            //    /calcServer?num1=10&opt=0&num2=20
            var url = '/calcServer?num1='+num1+'&opt='+opt+'&num2='+num2

            //创建请求    open('get',url,asyn)
            xhr.open('get',url,true);
            //监听事件  onreadystatechange
                        //如果 readyState==4  同时  status==200
                        //获取响应结果  responseText  放入div#show中
            xhr.onreadystatechange = function(){
                if(xhr.readyState==4 && xhr. status==200){
                    var div = document.getElementById('show');
                    div.innerHTML = xhr.responseText;
                }
            }
            //发送请求 send(null)
            xhr.send(null);
        }
    </script>
</body>
</html>
```

```python
#服务端程序

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__,)

#http://127.0.0.1:5000/
@app.route('/')
def index_view():
    # return '这是响应的字符串'
    return render_template('index.html')


#http://127.0.0.1:5000/user/login
#methods=['get','post']  
#表示当前的视图函数可以接收get请求和post请求
@app.route('/user/login',methods=['get','post'])
def login_view():
    #接收form表单get请求提交的数据
    # print(request.args)
    # #从前端获取 input name='uname'的值
    # uname = request.args.get('uname')
    # pwd = request.args.get('pwd')
    
    #接收表单post提交的数据
    print (request.headers) 
    uname = request.form.get('uname')
    print(uname+10)
    pwd = request.form.get('pwd')
    #登录验证 ...
    return '欢迎您%s' % uname

#http://127.0.0.1:5000/xhr
@app.route('/xhr')
def xhr_view():
    return render_template('xhr.html')

#http://127.0.0.1:5000/getServer
@app.route('/getServer')
def  get_server():
    uname = request.args.get('uname')
    if uname:
        return '欢迎%s' % uname
    else:
        return '接收AJAX get请求成功'

#http://127.0.0.1:5000/01get
@app.route('/01get')
def get_01():
    return render_template('ajax-get.html')


#请求和响应的数据类型都为str
#http://127.0.0.1:5000/calcServer
@app.route('/calcServer')
def server_calc():  
    print(request.method)
    #如果是get请求时
    if request.method == 'GET':
        #如果有数据   处理get请求提交的数据
        #如果没有数据  显示页面calc.html
        if request.args:
            #接收前端get请求提交的数据 num1,num2,opt
            #判断opt的值  如果opt == 0   返回 num1 + num2
            #如果opt == 1 返回 num1 - num2
            num1 = request.args.get('num1')#str
            num2 = request.args.get('num2')#str
            opt = request.args.get('opt')#str
            if int(opt) == 0:
                #加
                res =   int(num1)+int(num2)#int
                return '%s+%s=%s' %(num1,num2,res)#str
            else:
                #减
                res = int(num1)-int(num2)
                return '%s-%s=%s' %(num1,num2,res)
        else:
            return render_template('calc.html')      
    #如果是post请求时
    # ...

#http://127.0.0.1:5000/postServer
@app.route('/postServer',methods=['get','post'])
def server_post():
    #如果是get请求  显示页面ajax-post.html
    #如果是post请求  处理数据 
    if request.method == 'GET':
        return render_template('ajax-post.html')
    elif request.method == 'POST':
        uname = request.form.get('uname')
        age = request.form.get('age')
        email = request.form.get('email')
        print(request.form)
        print(uname,age,email)
        return '接收post数据成功'

if __name__ == '__main__':
    #http://127.0.0.1:5000/
    app.run(debug=True)
```



## 2.JSON

### 	1.JSON介绍

​		JSON:JavaScript Object Notation

​		在ajax中，允许将 复杂格式的响应数据 构建成 JSON的格式再进行响应

### 	2.JSON表现

#### 		1.JSON表示单个对象

​			1.使用 {} 表示单个对象

​			2.在 {} 中使用 key:value 的形式来表示属性(数据)

​			3.Key必须要用 " " 引起来

​			4.value如果是字符串的话，也需要用" "引起来

```javascript
    var obj = {
            "name":"王老师",
            "age" : 30,
            "gender" : "Unknown"
    }
```

#### 		2.JSON表示一个数组

​			1.使用 [] 表示一个数组

​			2.数组中允许包含若干JSON对象 或 字符串

​				1.使用JSON数组表示若干字符串

```javascript
	var arr = ["王伟超","王夫人","王小超"];
```

​				2.使用JSON数组表示若干对象

```javascript
    var arr = [
        {
            "name":"王老师",
            "age":30,
            "gender":"男"
                            },
        {
            "name":"王夫人",
            "age":28,
            "gender":"男"
                            }
        ];
```

#### 	3.后端处理JSON

​		在后台查询出数据再转换为JSON格式的字符串，再响应给前端

​		1.后台先获取数据

​			类型允许为：元组|列表|字典

​			元组和字典转换后传到前端变成数组，字典则是JSON对象。

​		2.在后台将数据转换为符合JSON格式的字符串

​		3.在后台将JSON格式的字符串进行响应



#### 	4.Python中的JSON处理

```python
import json
jsonStr = json.dumps(元组|列表|字典)
#json.dumps中separators参数默认值（", ",": ")带多余的空格
return json.dumps(data,separators=(",",":"),sort_keys=True)
json.dumps(cartdata,{"Content-Type","application/json"})
jsonObj=json.loads("JSON字符串")

return jsonStr
```

​	Django中的JSON处理

```python
#方法1 使用Django中提供的序列化类来完成QuerySet到JSON字符串的转换
from django.core import serializers
json_str = serializers.serialize('json',QuerySet)
return HttpResponse(json_str)

#方法2
d = {'a': 1}
return JsonResponse(d)

```
####    5.Flask中JSON处理

```python
jsonify()是flask中对json.dumps()的封装
```


```python
{"name":"shibw"}:
如果是表单形式的提交，会转成上面的内容。获取前端提交的JSON字符串，转换成JSON对象
需要设置Content-Type="application/json"
request.get_date()# 字节
request.get_json()#JSON对象
request.json#JSON对象
```


#### 	6.前端中的JSON处理

​	服务器端响应回来的数据是 String，需进行转换

```javascript
// 字符串转对象，用来转成可供前端使用的类型。
JSON对象=JSON.parse(JSON字符串)
//对象转字符串，用于前端传输到后端。
JSON字符串=JSON.stringify(JSON对象)
```


## jquery对 ajax 的支持

#### 1.$obj.load()

​		作用：载入远程的HTML文件到指定的元素中

```javascript
$obj.load(url,data,callback)
	$obj:显示响应内容的jq元素
	url:请求地址
	data:请求参数(可省略)
		方式1:字符串传参
		"key1=value1&key2=value2"  #查询字符串
		注：此种传参会使用 get 方式发送请求
		方式2:使用JS对象传参
		{
   		 key1:"value1",
         key2:"value2"
		}
		注：此种传参会使用 post 方式发送请求
	   callback:响应成功后的回调函数(可省略)

举栗子：
//load  加载指定页面的全部内容到#show
$('#show').load('/load_server');

//load 加载指定的元素
$('#show').load('/load_server  #btn2');

//使用查询字符串传参  发送GET请求
uname=shibw&age=18 Query String 查询字符串
$('#show').load('/load_server','uname=shibw&age=18')

//使用js对象传参  发送POST请求
//如果服务器路由地址不接受post请求，响应状态码为405.
//Content-Type: application/x-www-form-urlencoded; charset=UTF-8
$("#show").load("/load_server",{uname:"syuying"});


$('#show').load('/load_server',function(){alert('I am callback function!');})

//测试远程页面
$('#show').load('http://www.taobao.com')
```

#### 2.$.get() 和 $.post()

​		作用：通过get方式异步的向远程地址发送请求

```javascript
$.get(url,data,callback,type)
		url:请求地址
		data:传递到服务器端的参数
		可以是字符串 ："name=sf.zh&age=18"
		也可以是js对象:
			{
				name:"sf.zh",
				age:18
			}
		callback:响应成功后的回调函数
        ex: function(data){
           console.log(data)
        }
		type:响应回来的数据的格式
			取值如下:
			1.html : 响应回来 的文本是html文本
			2.text : 响应回来的文本是text文本
			3.script : 响应回来的文本是js执行脚本
			4.json : 响应回来的文本是json格式的文本
            
$.post  -> 请求头中的Content-Type:application/x-www-form-urlencoded; charset=UTF-8  
即为表单post提交。 后台django可通过request.POST获取数据 

考虑 csrf_token ->  请求参数里 拼上
csrfmiddlewaretoken


//举栗子
//前端请求：
$(function(){
            $("#btn").click(function(){
                var params={uname:"syuying",age:"20"};
                $.get("/get_server",params,function(response){
                    console.log(response)
                    $("#show").html(response.msg)
                },'json')
            })
        })

//服务端：
@app.route("/get_server")  
def get_server():
    uname=request.args.get("uname","没找到")
    age=request.args.get("age","没找到")
    s="name is %s,age is %s"%(uname,age)
    json_data=json.dumps({"code":200,"msg":s})
//设置响应头中的数据类型的格式是json格式
    return json_data,{"Content-Type":"application-json"}
```

#### 3. $.ajax()

```javascript
参数对象中的属性：
	1.url : 字符串，表示异步请求的地址
	2.type : 字符串，请求方式，get 或 post
	3.data : 传递到服务器端的参数
		可以是字符串 ："name=sf.zh&age=18"
		也可以是js对象:
			{
				name:"sf.zh",
				age:18
			}
	4.dataType : 字符串，响应回来的数据的格式
		1.'html'
		2.'xml'
		3.'text' 
		4.'script'
		5.'json'
		6.'jsonp' : 有关跨域的响应格式
	5.success:回调函数，请求和响应成功时回来执行的操作
	6.error : 回调函数，请求或响应失败时回来执行的操作
	7.beforeSend : 回调函数，发送ajax请求之前执行的操作，如果return false，则终止请求
    	使用场景：
        	1，发请求之前可将提交摁钮置成不可点击状态，防止用户重复提交
            2，摁钮点击后，loading画面
    		3，所有数据相关的校验
    
    8.async  是否启用异步请求，默认为true【异步】
    9.contentType:application/json    前端发送JSON数据给服务器端是指定
    
```

## 跨域

#### 1，什么是跨域

​	跨域：非同源的网页，相互发送请求的过程，就是跨域

```
浏览器的同源策略：
同源：多个地址中，相同协议，相同域名，相同端口被视为是"同源"
在HTTP中，必须是同源地址才能互相发送请求，非同源拒绝请求(<script>和<img>除外)。

http://www.tedu.cn/a.html
http://www.tedu.cn/b.html
以上地址是 "同源"

http://www.tedu.cn/a.html
https://www.tedu.cn/b.html
由于 协议不同 ，所以不是"同源"

http://localhost/a.html
http://127.0.0.1/a.html
由于 域名不同 ，所以不是"同源"

http://www.tedu.cn:80/a.html
http://www.tedu.cn:8080/b.html
由于端口不同 ， 所以不是"同源"
```

#### 2，解决方案

通过 script标签 src 向服务器资源发送请求
由服务器资源指定前端页面的哪个方法来执行响应的数据

```
我的网站：

function test(data){

​	气象局给我的data

}

<script src='http://www.qixiangju.com/cross'>

气象局返回： test('25C')
```


#### 3,   jquery 的跨域

jsonp - json with padding
用户传递一个callback参数给服务端，然后服务端返回数据时会将这个callback参数作为函数名来包裹住JSON数据

只支持get请求

ex:
​	当前地址： http://127.0.0.1:8000/index
​    欲访问地址： http://localhost:8000/data?callback=xxx

```javascript
$.ajax({
	url:'xxx',
	type:'get',
	dataType:'jsonp',//指定为跨域访问
	jsonp:'callback',//定义了callback的参数名，以便获取callback传递过去的函数名   
	jsonpCallback:'xxx' //定义jsonp的回调函数名
});


//超简版本
$.ajax({
	url:'xxx',
	type:'get',
	dataType:'jsonp',//指定为跨域访问
	success: function(data){
        console.log(data);       
    }
});


```



```html
//网页购物车小demo
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1 id="title">xxx的购物车</h1>
    <table border="1" cellspacing="0">
        <tr>
            <th>id</th>
            <th>name</th>
            <th>price</th>
            <th>count</th>
            <th>sku_name</th>
            <th>selected</th>
        </tr>
        <tbody id="content">
            <tr>
                <td>1</td>
                <td>蓝色小尺寸</td>
                <td>100</td>
                <td>11</td>
                <td>安踏A/尺寸：15寸，安踏A/颜色：蓝色</td>
                <td>
                    <input type="checkbox" checked>
                </td>
            </tr>
        </tbody>
    </table>

    <script src="/static/js/jquery.min.js"></script>
    <script>
        $(function(){
            $.ajax({
                url:"/get_data_server",
                type:'get',
                dataType:'json',
                success:function(data){
                    console.log(data);
                    var html=data.username+"的购物车";
                    $("#title").html(html);
                    
                    var html="";
                    $.each(data.cart,function(i,obj){
                        html+="<tr>";
                        html+="<td>"+obj.id+"</td>";
                        html+="<td>"+obj.name+"</td>";
                        html+="<td>"+obj.price+"</td>";
                        html+="<td>"+obj.count+"</td>";
                        html+="<td>"+obj.sku_sale_attr_name[0]+obj.sku_sale_attr_val[0]+","+obj.sku_sale_attr_name[1]+obj.sku_sale_attr_val[1]+"</td>";
                        if(obj.selected=="true"){
                            html+="<td><input type='checkbox' checked></td>";}
                        else{
                            html+="<td><input type='checkbox'></td>";}
                        html+="</tr>";
                        $("#content").html(html);
                    })

                }
            })
        })
    </script>
</body>
</html>
```

```python
from flask import Flask,render_template,jsonify,json


app=Flask(__name__)

#127.0.0.1:5000/get_data
@app.route("/get_data")
def get_data():
    return render_template("get_data.html")

@app.route("/get_data_server")
def get_data_server():
    cartdata={
    "username":"qi941129",
    "password":"123",
    "cart":[
        {
            "id":"1",
            "count":"11",
            "name":"蓝色小尺寸",
            "default_image_url":"http://114.116.244.115:7001/media/2_5pdezhv.jpg",
            "price":100,
            "selected":"true",
            "sku_sale_attr_name":["安踏A/尺寸：","安踏A/颜色："],
            "sku_sale_attr_val":["15寸","蓝色"]
        },
        {
            "id":"2",
            "count":"9",
            "name":"红色大尺寸",
            "default_image_url":"http://114.116.244.115:7001/media/3_JGA6F97.jpg",
            "price":10000,
            "selected":"true",
            "sku_sale_attr_name":["安踏A/尺寸：","安踏A/颜色："],
            "sku_sale_attr_val":["18寸","绿色"]
        },
        {
            "id":"3",
            "count":"10",
            "name":"蓝色小尺寸",
            "default_image_url":"http://114.116.244.115:7001/media/4_z3FdRMq.jpg",
            "price":1000,
            "selected":"true",
            "sku_sale_attr_name":["安踏B/尺寸：","安踏B/颜色："],
            "sku_sale_attr_val":["18寸","蓝色"]
        }
        ]
        }

    return jsonify(cartdata)



if __name__ == "__main__":
    app.run(debug=True)
    
```



