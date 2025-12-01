<h2>1. INTRODUCCION</h2>
Este proyecto corresponde al desarrollo de un Sistema Básico de Inventario implementado con Flask, SQLite y una estructura modular de plantillas HTML, hojas de estilo y rutas protegidas por autenticación. El sistema permite gestionar información de productos y almacenes mediante una interfaz sencilla, organizada y funcional, diseñada especialmente para fines académicos dentro del contexto de la Universidad de Sonora.

El proyecto integra conceptos clave del desarrollo web, tales como rutas dinámicas, manejo de sesiones, validación de usuarios, conexión con base de datos, renderizado de información con plantillas, y uso de Bootstrap para mejorar la presentación visual. Asimismo, se aplican principios de seguridad básicos, como el cifrado de contraseñas, el control de accesos y la protección de páginas mediante decoradores personalizados.

<h2>2. OBJETIVOS</h2>

El objetivo principal de este proyecto es desarrollar un sistema web que permita gestionar un inventario básico mediante:

✔ Un módulo de autenticación seguro que controle el acceso de los usuarios.

✔ La visualización estructurada de productos y almacenes obtenidos desde una base de datos SQLite.

✔ El uso de un diseño limpio y responsivo mediante componentes de Bootstrap.

✔ La integración de sesiones, rutas protegidas y plantillas HTML de forma adecuada y organizada.

✔ La aplicación práctica de conceptos fundamentales de desarrollo con Flask.

<h2>EXPLICACIÓN DE CÓDIGO</h2>

<h3>Estructura</h3>
Nuestro proyecto está estructurado de manera en que separamos por carpetas los diferentes elementos que utilizaremos durante nuestro proyecto. <br> 
Componentes, Paginas, Imagenes, Templates<br>
La estructura de nuestro proyecto se muestra de esta manera: <br>
<img width="264" height="668" alt="image" src="https://github.com/user-attachments/assets/13c12ae0-fe60-4306-a781-5cdfe6b6acff" /> <br>
<h3>Carpeta de instancia</h3>
En este apartado tenemos localizada nuestra base de datos con la que trabajaremos durante todo el proyecto <br>
<img width="203" height="56" alt="image" src="https://github.com/user-attachments/assets/b5e4b00d-2884-4131-a7d1-3e1af5d0ee5c" /> <br>
<h3>Componentes</h3>
Nuestros componentes están costituídos por dos elementos. <br>
Buttons y headers <br>
<img width="229" height="125" alt="image" src="https://github.com/user-attachments/assets/934e5a65-8d6a-4237-91b8-d9b746203d06" /> <br>
Estos dos componentes se utilizan prácticamente en toda la página. Por lo que reutilizamos sus atributos repetidas veces. <br>
<h4>buttons.css</h4><br>
<img width="383" height="69" alt="image" src="https://github.com/user-attachments/assets/c8a114f0-43a8-4752-87cb-0d20fbdb1b50" />
<img width="413" height="62" alt="image" src="https://github.com/user-attachments/assets/f0a605dc-2ef1-4cc8-b4ef-1c4a80194420" /><br>
<img width="134" height="232" alt="image" src="https://github.com/user-attachments/assets/56d1d360-0c37-406d-a085-a6823e6d4e2c" />
<img width="135" height="231" alt="image" src="https://github.com/user-attachments/assets/fb012e8c-fe3d-428c-9e07-8b8240118d0f" />
<img width="191" height="65" alt="image" src="https://github.com/user-attachments/assets/38862153-1ce9-4d8c-aa28-db3e50cbe7d8" /> <br>
Estos son sólo algunos de los elementos que podemos observar durante la exploración de la interfaz. <br>
Se realizo de esta manera para mantener un control y mayor manipulación sobre los diferentes componentes que utilizaremos.<br>
Aquí un fragmento de código que se utilizó para estos elementos en dónde podemos observar los diferentes atributos de los diferentes botones. <br>
archivo buttons.css ⬇
<img width="664" height="822" alt="image" src="https://github.com/user-attachments/assets/25752cc6-5d93-4153-92fa-5c1a747a6eee" /><br>
<h4>header.css</h4> <br>
<img width="382" height="109" alt="image" src="https://github.com/user-attachments/assets/3f8688e9-38be-4f16-b201-8e25b3852826" /><br>
<img width="449" height="99" alt="image" src="https://github.com/user-attachments/assets/7e177fe9-a4ec-4dd5-9241-b5cb7c30ecd2" /><br>
<br>
<h3>Pages</h3><br>
<img width="211" height="124" alt="image" src="https://github.com/user-attachments/assets/3b7829e5-6fa1-47e4-bd78-87fb06d8ee67" /><br>
En este apartado de pages se seccionó el apartado de diseño para los diferentes templates html que utilizamos para las diferentes vistas<br>
<h4>base.css</h4><br>
En este apartado de base.css adjuntamos reglas generales que utilizamos en el proyecto, como por ejemplo algunos colores, tipografía, la redondes de los botones, entre otras reglas.<br>
<img width="118" height="31" alt="image" src="https://github.com/user-attachments/assets/e31493f2-02d1-4f25-9a40-e2ee0fa65087" /><br>

Fragmento de código de base.css⬇ <br>
<img width="648" height="836" alt="image" src="https://github.com/user-attachments/assets/8a2345b1-7112-4335-833f-90db79d96899" /><br>

<h3>Images</h3><br>
En este proyecto se utilizó sólo una imagen, esta es su ruta dentro de la estructura y un fragmento de código donde se implementó <br>
<img width="169" height="42" alt="image" src="https://github.com/user-attachments/assets/7aa5c5c0-ca30-4446-9906-f9fd9dbf480d" /><br>
<img width="536" height="93" alt="image" src="https://github.com/user-attachments/assets/348d75ae-29ad-4157-9450-aa9ea10b89d7" /><br>

La imagen se utilizó en este apartado de inicio<br>
<img width="541" height="529" alt="image" src="https://github.com/user-attachments/assets/5831467e-cfc8-4792-aefd-b79d6003b41a"/><br>

<h3>Templates</h3><br>
Se utilizaron distintos templates de html para las distintas vistas de la interfaz. <br>
A continuación una demostración de las vistas con sus respectivos templates.<br>
<img width="209" height="193" alt="image" src="https://github.com/user-attachments/assets/f045adff-2187-42c4-9c55-86f7151bf43f" /><br>

<h3>Login</h3><br>
Vista para inicio de sesión del usuario.<br>
<a href = "https://github.com/zencifer/Sistema_Inventario/blob/master/templates/login.html">login.html</a>
<img width="956" height="467" alt="image" src="https://github.com/user-attachments/assets/46b52200-99c4-48dd-b256-c3499ca13982" />

<h3>Inicio</h3><br>
Vista de inicio una vez validado el usuario. Aquí el usuario puede interactuar entre las diferentes vistas disponibles.<br>
<a href="https://github.com/zencifer/Sistema_Inventario/blob/master/templates/inicio.html">inicio.html</a>
<img width="956" height="467" alt="image" src="https://github.com/user-attachments/assets/849be122-08b3-49ed-bff5-8c44c564c67f" />

<h3>Productos</h3><br>
Vista interactiva donde podemos utilizar filtros para interactuar con la base de datos agregando, modificando y eliminando productos.<br>
<a href = "https://github.com/zencifer/Sistema_Inventario/blob/master/templates/productos.html">productos.html</a>
<img width="956" height="467" alt="image" src="https://github.com/user-attachments/assets/11b56e91-d9e5-4bbe-ae33-f3d853740568" />

<h3>Agregar procutos</h3><br>
Vista interactiva donde agregamos productos a la base de datos atraves de un form<br>
<a href="https://github.com/zencifer/Sistema_Inventario/blob/master/templates/producto_form.html">producto_form.html</a>
<img width="1910" height="946" alt="image" src="https://github.com/user-attachments/assets/88fc3924-f211-4b51-bf1d-ba58a3f090fe" />

<h3>Almacenes</h3><br>
Vista interactiva para interactuar con la base de datos de almacenes.<br>
<a href ="https://github.com/zencifer/Sistema_Inventario/blob/master/templates/almacenes.html">almacenes.html</a><br>
<img width="1916" height="950" alt="image" src="https://github.com/user-attachments/assets/5df4b8f1-f15a-4528-b622-69408b6a9163" />

<h3>Agregar Almacen</h3><br>
Vista donde podemos agregar un nuevo registro de alamacen<br>
<a href ="https://github.com/zencifer/Sistema_Inventario/blob/master/templates/almacen_form.html">almacen_form.html</a><br>
<img width="1915" height="947" alt="image" src="https://github.com/user-attachments/assets/97968c0f-d84b-48b8-b1b9-8ea96d5ae093" />





