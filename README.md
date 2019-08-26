# TELLEE

## Introduction

“Telle” mission - our platform connects rotating equipment to Cloud services or customer’s on-premises servers; collects and stores industrial data; analyzes machine performance with the help of machine-learning algorithms.

Moreover, Tellee is capable of connecting various industrial equipment and performing analysis to improve operational efficiency.

Modern industrial production implies the presence of automated technology process and lean business processes, which are evaluated based on integrated plant performance factors, such as cost of a single production unit, faulty production expenses, downtime expenses, costs related to delivery and storage of end products; efficiency and productivity of deployed equipment. 

In the process of improving the productivity of the enterprise, machine learning and big data analysis are the key instruments that supplement classical methods of production optimization. 

The most common examples of machine learning use include:
increase in productivity of manufacturing activity as a result of equipment optimal operation mode selection; 
increase in end-product quality through diagnostics of critical factors that influence the end product;
optimization of maintenance  and repairs of expensive manufacturing equipment, predictive diagnostics and analysis of the reduction in efficiency of equipment;
dynamic management of supply chain – optimization and forecasting of the procurement process, delivery, storage, demand and supply;
comprehensive enhancement of production indexes by means of detecting implicit factors that affect the production process, deployment of new methods for equipment operation modelling with the use of digital technologies.

![tellee](/uploads/8a8baa9b3faf7d123aa92a02bac3236c/tellee.png)


Описание TELLY

## Mainflux

[Mainflux](https://www.mainflux.com/) - is modern, scalable, secure open source and patent-free IoT cloud platform written in [Go](https://golang.org/doc/).

It accepts user and thing connections over various network protocols (i.e. [HTTP](https://ru.wikipedia.org/wiki/HTTP), [MQTT](https://ru.wikipedia.org/wiki/MQTT), [WebSocket](https://ru.wikipedia.org/wiki/WebSocket), [CoAP](http://lib.tssonline.ru/articles2/internet-of-things/protokol-interneta-veschey-coap)), thus making a seamless bridge between them. It is used as the IoT middleware for building complex IoT solutions.

<ul>
<li>Protocol bridging (i.e. [HTTP](https://ru.wikipedia.org/wiki/HTTP), [MQTT](https://ru.wikipedia.org/wiki/MQTT), [WebSocket](https://ru.wikipedia.org/wiki/WebSocket), [CoAP](http://lib.tssonline.ru/articles2/internet-of-things/protokol-interneta-veschey-coap))</li>
<li>[Device management and provisioning](https://mainflux.readthedocs.io/en/latest/messaging/)</li>
<li>[Fine-grained access control](https://mainflux.readthedocs.io/en/latest/provisioning/)</li>
<li>[Platform logging and instrumentation support](https://mainflux.readthedocs.io/en/latest/storage/)</li>
<li>Container-based deployment using Docker [Docker](https://docs.docker.com/)</li>
</ul>

### Components applied for the project.

<ul>
<li>users	Manages platform's users and auth concerns
<li>things	Manages platform's things, channels and access policies
<li>normalizer	Normalizes SenML messages and generates the "processed" messages stream
<li>http-adapter	Provides an HTTP interface for accessing communication channels
<li>mqtt-adapter	Provides an MQTT interface for accessing communication channels
<li>application 
</ul>

### HTTP adapter

Representational State Transfer (REST) is a software architectural style that defines a set of constraints to be used for creating Web services. Web services that conform to the REST architectural style, called RESTful Web services (RWS), provide interoperability between computer systems on the Internet. RESTful Web services allow the requesting systems to access and manipulate textual representations of Web resources by using a uniform and predefined set of stateless operations. Other kinds of Web services, such as SOAP Web services, expose their own arbitrary sets of operations.

"Web resources" were first defined on the World Wide Web as documents or files identified by their URLs. However, today they have a much more generic and abstract definition that encompasses every thing or entity that can be identified, named, addressed, or handled, in any way whatsoever, on the Web. In a RESTful Web service, requests made to a resource's URI will elicit a response with a payload formatted in HTML, XML, JSON, or some other format. The response can confirm that some alteration has been made to the stored resource, and the response can provide hypertext links to other related resources or collections of resources. When HTTP is used, as is most common, the operations (HTTP methods) available are GET, HEAD, POST, PUT, PATCH, DELETE, CONNECT, OPTIONS and TRACE.


### MQTT Broker

The counterpart of the MQTT client is the MQTT broker. The broker is at the heart of any publish/subscribe protocol. Depending on the implementation, a broker can handle up to thousands of concurrently connected MQTT clients. The broker is responsible for receiving all messages, filtering the messages, determining who is subscribed to each message, and sending the message to these subscribed clients. The broker also holds the sessions of all persisted clients, including subscriptions and missed messages (more details). Another responsibility of the broker is the authentication and authorization of clients. Usually, the broker is extensible, which facilitates custom authentication, authorization, and integration into backend systems. Integration is particularly important because the broker is frequently the component that is directly exposed on the internet, handles a lot of clients, and needs to pass messages to downstream analyzing and processing systems.


### MQTT adapter

To send and receive messages over MQTT you could use Mosquitto tools, or Paho if you want to use MQTT over WebSocket.


### Bootstrap

Bootstrapping refers to a self-starting process that is supposed to proceed without external input. Mainflux platform supports bootstrapping process, but some of the preconditions need to be fulfilled in advance. The device can trigger a bootstrap when: - device contains only bootstrap credentials and no Mainflux credentials - device, for any reason, fails to start a communication with the configured Mainflux services (server not responding, authentication failure, etc..). - device, for any reason, wants to update its configuration

Bootstrapping and provisioning are two different procedures. Provisioning refers to entities management while bootstrapping is related to entity configuration.

Bootstrapping procedure is the following:

Configure device 

1) Configure device with Bootstrap service URL, an external key and external ID

Provision Mainflux channels Optionally create Mainflux channels if they don't exist

Provision Mainflux things Optionally create Mainflux thing if it doesn't exist

Upload configuration 

2) Upload configuration for the Mainflux thing

Bootstrap 

3) Bootstrap - send a request for the configuration

Update, enable/disable, remove 

4) Connect/disconnect thing from channels, update or remove configuration


#### Configuration

The configuration of Mainflux thing consists of three major parts:

<ul>
<li>The list of Mainflux channels the thing is connected to</li>
<li>Custom configuration related to the specific thing</li>
<li>Thing key and certificate data related to that thing</li>
</ul>

There are two more fields: `external_id` and `external_key`. External ID represents an ID of the device that corresponds to the given thing. For example, this can be a MAC address or the serial number of the device. The external key represents the device key. This is the secret key that's safely stored on the device and it is used to authorize the thing during the bootstrapping process. Please note that external ID and external key and Mainflux ID and Mainflux key are completely different concepts. External id and key are only used to authenticate a device that corresponds to the specific Mainflux thing during the bootstrapping procedure.


### Provisioning

Provisioning is a process of configuration of an IoT platform in which system operator creates and sets-up different entities used in the platform - users, channels and things.


#### Account creation

Use the Mainflux API to create user account:

Необходимо рассписать создание профилей пользователей через использование KEYCLOAK + FLASH

#### Access control

#### Provisioning things

Создание/удаление/смена названия и тд

#### Provisioning applications

Создание/удаление/смена названия и тд


### NATS

NATS was built to meet the distributed computing needs of today and tomorrow. NATS is simple and secure messaging made for developers and operators who want to spend more time developing modern applications and services than worrying about a distributed communication system.

<ul>
<li>Easy to use for developers and operators</li>
<li>High-Performance</li>
<li>Always on and available</li>
<li>Extremely lightweight</li>
<li>At Most Once and At Least Once Delivery</li>
<li>Support for Observable and Scalable Services and Event/Data Streams</li>
<li>Client support for over 30 different programming languages</li>
<li>Cloud Native, a CNCF project with Kubernetes and Prometheus integrations</li>
</ul>


### Influxdb

InfluxDB is the open source time series database that is part of the TICK (Telegraf, InfluxDB, Chronograf, Kapacitor) stack.

InfluxDB is a high-performance data store written specifically for time series data. It allows for high throughput ingest, compression and real-time querying. InfluxDB is written entirely in Go and compiles into a single binary with no external dependencies. It provides write and query capabilities with a command-line interface, a built-in HTTP API, a set of client libraries (e.g., Go, Java, and JavaScript) and plugins for common data formats such as Telegraf, Graphite, Collectd and OpenTSDB.

InfluxDB works with InfluxQL, a SQL-like query language for interacting with data. It has been lovingly crafted to feel familiar to those coming from other SQL or SQL-like environments while also providing features specific to storing and analyzing time series data. InfluxQL supports regular expressions, arithmetic expressions, and time series-specific functions to speed up data processing.


## Faceplate

[Faceplate](http://www.faceplate.io/) служит для разработки человеко-машинного интерфейса, посредством которого оператор контролирует протекание технологических процессов на объекте управления. В качестве рабочего места оператора может выступать персональный компьютер, планшет или смартфон. Часто системы для разработки человеко-машинного интерфейса называют SCADA-системами.

В общих чертах процесс разработки скада системы с помощью Faceplate можно представить в виде следующих шагов:

<ul>
<li>Создание логической структуры проекта, определение контролируемых точек - тегов. (см. [Редактор тегов](http://docs.faceplate.io/docs/ru/work_with_tags#%D1%80%D0%B5%D0%B4%D0%B0%D0%BA%D1%82%D0%BE%D1%80-%D1%82%D0%B5%D0%B3%D0%BE%D0%B2)).</li>
<li>Создание мнемосхем (см. [Графический редактор](http://docs.faceplate.io/docs/ru/graph_redactor#%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D1%80%D0%B5%D0%B4%D0%B0%D0%BA%D1%82%D0%BE%D1%80))</li>
<li>Создание соединений с контроллерами и определение привязок (см. [Соединения](http://docs.faceplate.io/docs/ru/connection))</li>
<li>Конфигурирование системы сообщений (см. [Система сообщений](http://docs.faceplate.io/docs/ru/sms_system)).</li>
<li>Конфигурирование системы архивирования (см. [Система архивирования](http://docs.faceplate.io/docs/ru/archive_system)).</li>
<li>В системах, где объектом управляют более одного оператора, которые могут иметь разные уровни доступа к объекту настраиваются права доступа операторов (см. [Управление правами пользователей](http://docs.faceplate.io/docs/ru/user_rules_control)).</li>
</ul>

Для систем, где требуется горячее резервирование и/или участие нескольких серверов выполняется конфигурирование подключенных к системе серверов и распределение функций между ними (см. [Конфигурирование серверов](http://docs.faceplate.io/docs/ru/server_config)).

Настройка отчетных форм, позволяющих агрегировать различную архивируемую информацию в удобном для восприятия виде выполняется с помощью Редактора отчетов.

Разработка дополнительных программных модулей исполняемых сервером в режиме исполнения выполняется с помощью Редактора скриптов.

Faceplate может использоваться для обработки в режиме реального времени видеопотоков поступающих с видеокамер. Подсистема видео позволяет транслировать видеопоток на мнемосхемы, а также определять возникновение движения и реакцию на него (см.[ Работа с видео](http://docs.faceplate.io/docs/ru/work_with_video)).

Поддержка мультиязычных интерфейсов описана в разделе [Разработка мультиязычных проектов](http://docs.faceplate.io/docs/ru/multi_lang_projects).


## Tensorflow serving APP

### TensorFlow Serving

TensorFlow Serving is a flexible, high-performance serving system for machine learning models, designed for production environments. TensorFlow Serving makes it easy to deploy new algorithms and experiments, while keeping the same server architecture and APIs. TensorFlow Serving provides out-of-the-box integration with TensorFlow models, but can be easily extended to serve other types of models and data.

Detailed developer documentation on TensorFlow Serving is available:

<ul>
<li>[Architecture Overview](https://www.tensorflow.org/tfx/serving/architecture)</li>
<li>[Server API](https://www.tensorflow.org/tfx/serving/api_docs/cc/)</li>
<li>[REST Client API](https://www.tensorflow.org/tfx/serving/api_rest)</li>
</ul>

### Protobuf

Protocol Buffers (Protobuf) is a method of [serializing](https://en.wikipedia.org/wiki/Serialization) structured data. It is useful in developing programs to communicate with each other over a wire or for storing data. The method involves an [interface description language](https://en.wikipedia.org/wiki/Interface_description_language) that describes the structure of some data and a program that generates source code from that description for generating or parsing a stream of bytes that represents the structured data.

[Google](https://en.wikipedia.org/wiki/Google) developed Protocol Buffers for use internally and has provided a [code generator](https://en.wikipedia.org/wiki/Code_generation_(compiler)) for multiple languages under an [open source](https://en.wikipedia.org/wiki/Open_source_software) license.

### TFS MQTTT Agent

If I choose a second option, I need an additional component — Web server to host TensorFlow Serving client. I will use sample GAN model that hosted by a TensorFlow server in a Docker container as backend. I will create a simple Flask application with TensorFlow client and dockerize it. For convenience the application will provide Swagger documentation for our simple REST API.
Our REST API will have a single resource prediction with a single operation POST on it. It expects an image as an input parameter and returns JSON object with 3 most probable digits and their probabilities for Street View House Numbers. Here I extracted a couple of images for tests.

We have created a Web application that provides public REST API for Street View House Numbers prediction. This is a Flask web application that is, effectively, an adapter of TensorFlow Serving capabilities. It hosts TensorFlow Serving client, transforms HTTP(S) REST requests into protobufs and forwards them to a TensorFlow Serving server via gRPC. TensorFlow server, in its turn, host a GAN model, which do, actually, a prediction job.

Introduced architecture benefits from using of an effective communication (gRPC + protobufs) between internal services and exposes a public REST API for external use.



## Keycloak

Keycloak is an open source Identity and Access Management solution aimed at modern applications and services. It makes it easy to secure applications and services with little to no code.

This page gives a brief introduction to Keycloak and some of the features. For a full list of features refer to the documentation.

Trying Keycloak is quick and easy. Take a look at the Getting Started tutorial for details.

Users authenticate with Keycloak rather than individual applications. This means that your applications don't have to deal with login forms, authenticating users, and storing users. Once logged-in to Keycloak, users don't have to login again to access a different application.

Through the admin console administrators can centrally manage all aspects of the Keycloak server.



## Flash

`FLash` разработан на основе проекта с открытым исходным кодом `Chronograf`. `Flash`, является средой визуализации для данных поступающих с базы данных `InfluxDB` из стэка `Mainflux`. Для Single-Sign-On (SSO), аутентификации и авторизации пользователей во `Flash` интегрирована [OIDC Keycloak](https://www.keycloak.org/documentation.html). Графические компоненты `Flash` основаны на библиотеках:

* D3 | [Home Page](https://d3js.org/), [Docs](https://github.com/d3/d3/wiki)
* Predix UI | [Home Page](https://www.predix-ui.com/#/home), [Docs](https://docs.predix.io/en-US/content/platform/web_application_development/predix_ui/get-started-with-predix-ui-components)
* Dygraphs | [Home Page](http://dygraphs.com/), [Docs](http://dygraphs.com/tutorial.html)

### Chronograf

Chronograf is InfluxData’s open source web application. Use Chronograf with the other components of the TICK stack to visualize your monitoring data and easily create alerting and automation rules.

### Key features

#### Infrastructure monitoring

* View all hosts and their statuses in your infrastructure
* View the configured applications on each host
* Monitor your applications with Chronograf’s pre-created dashboards

#### Alert management

Chronograf offers a UI for Kapacitor, InfluxData’s data processing framework for creating alerts, running ETL jobs, and detecting anomalies in your data.

* Generate threshold, relative, and deadman alerts on your data
* Easily enable and disable existing alert rules
* View all active alerts on an alert dashboard
* Send alerts to the supported event handlers, including Slack, PagerDuty, HipChat, and more

#### Data visualization

* Monitor your application data with Chronograf’s pre-created dashboards
* Create your own customized dashboards complete with various graph types and template variables
* Investigate your data with Chronograf’s data explorer and query templates

#### Database management

* Create and delete databases and retention policies
* View currently-running queries and stop inefficient queries from overloading your system
* Create, delete, and assign permissions to users (Chronograf supports InfluxDB OSS and InfluxEnterprise user management)

#### Multi-organization and multi-user support

* Create organizations and assign users to those organizations
* Restrict access to administrative functions
* Allow users to set up and maintain unique dashboards for their organizations


## Mainflux Admin Panel

Административная панель(АП) разработана для удобного управления `Things`, `Channels` и `Users` `Mainflux`-а. АП представляет собой интерфейс и API( с помощью которого производится взаимодействие с `Mainflux` и `Bootstrap`). Основной задачей АП, является настройка конфигурации для определенных типов устройств, для их дальнейшей работы с `Bootstrap`.

Mainflux Admin Panel будет взаимодействовать с провайдером OIDC `Keycloak`, для распределения пользователей АП по организациям (только участники одной организации могут просматривать конфигурацию для устройств принадлежащих к это организации).


# Functional description

Tellen Edge can transmit and receive data from most of the industrial sources that include: sensors, Programmable Logic Controllers, SCADA/ICS systems, MES systems and corporate EAM (Enterprise Asset Management) systems. Depending on the configuration,  data can be transmitted directly to Tellee or via Telle Edge.

Telle’s architecture is based on the microservices ideology that enables a secure and easily scalable environment for data processing and comprehensive analysis. One of Telle’s strongest assets is the proactive approach to emergencies and process alarms that’s in the core of the platform.

Generally, this is the sequence of the platform’s operation:
<ul>
<li>Edge Connection- connect industrial equipment and other data sources</li>
<li>Data processing- monitor data, visualize efficiency, analyze anomalies, perform predictive diagnostics</li>
<li>Analysis and following action- manage and optimize the production process, increase KPI and OEE</li>
<ul>

![tellee1](/uploads/3e6adf4452e2023038d2eb3025783b68/tellee1.png)


## TELLEE EDGE

Telle Edge receives and transmits data to Tellee and allows integration of trained machine learning models into local systems for analysis of source information.
Telle Edge supports various platforms and operating systems. It can operate on both ARM and Intel processors. Security is ensured by data encryption and token-based system that issues unique tokens to each edge device. 
Support for industrial data protocols such as Modbus, Modbus TCP/IP, OPC DA, OPC UA.
Telle edge is capable of buffering data and in case of a connection interruption, it will synchronize all the buffered data as soon as the connection is up again. 
A variable schema for storage of structured or unstructured data. Tools for creation and configuration of connections to the equipment. Role-based authentication configuration at the Edge level. User authentication at the Edge level uses 128-bit password hashing algorithm.


![tellee2](/uploads/f5a6a9697d7d3f4ad095faa2e6ed8046/tellee2.png)



## TELLE λ (lambda) - Service

Tellee is capable of forecasting equipment operation, providing all the necessary information regarding the technology process that is compiled from the PLC data. 

Main stages of machine learning models integration

<ul>
<li>Assigning the objectives and conditions for models of successful operation</li>
<li>Definition of metrics and criteria for conformance of models to real-life equipment</li>
<li>Rating of data accessibility, processing of data</li>
<li>Selection of type of models and methods of machine learning. Training and testing of models</li>
<li>Deployment, support, update and if necessary retraining of models</li>
</ul>


![tellee3](/uploads/939a60ca63c0329aeafb9266b208d0f6/tellee3.png)


reprocessing and trimmings of the data are crucial for the correct utilization of data for machine learning. Unprocessed data are often distorted and unreliable. Employing this kind of data during the building of models might lead to incorrect results. These steps are a part of the processing stage and often implicate the initial examination of data.

Research of normal equipment operation patterns in comparison to abnormal operation and screening of features that define the model structure.

Development of equipment operation model, design of infrastructure, classification of common factors, the combinations of various types of models, equipment failure probability forecasting. Research of possible way to deliver alarms that contain forecasted equipment failure possibility.

Deployment of a trained model into production. Depending on a customer request, it can be deployed either in the cloud or at the edge device. Machine learning models are limited only to computational resources of a device they are deployed on and in some cases by the speed of data transfer.

## UI/UX

Telle Flash user interface provides industry-ready IoT visualization that allows event management without the need for any additional software.

Flash’s Integrated toolkit allows users to monitor equipment operation, analyze anomalies and events. Machine Learning analytics provide predictive alarms that can help operating staff take preventive action to minimize the effects of abnormality early on. Moreover, users can dissect the abnormality in order to get to the root of the problem.

Criticality analysis enables users to set their priorities in relation to the importance of enterprise assets

User interface elements are optimized for long hour shifts. Operators can switch between dark and light themes depending on their preferences. Color palette is adjusted in a way that minimizes eye strain but at the same time delivers information efficiently.


![tellee4](/uploads/e3e98ae8c0c1dbb0118595280355423b/tellee4.png)



## Installation

Deployment of Influx services based on docker containers.
Detailed procedure to be provided.

Tellee start procedure 

Detailed procedure to be provided.


## Bootstarping

Bootstrapping refers to a self-starting process that is supposed to proceed without external input. 
Currently, the bootstrapping procedure is executed over the HTTP protocol. Bootstrapping is nothing else but fetching and applying the configuration that corresponds to the given Tellee things. 

The platform supports bootstrapping process, but some of the preconditions need to be fulfilled in advance. The device can trigger a bootstrap when:
<ul>
<li>the device contains only bootstrap credentials and no Tellee credentials</li>
<li>the device, for any reason, fails to start a communication with the configured services (server not responding, authentication failure, etc..).</li>
<li>the device, for any reason, wants to update its configuration</li>
</ul>


![tellee5](/uploads/7be1c46c1f39609ef270084e14452f50/tellee5.png)


## Mainflux Admin Panel

The administrative panel (AP) is designed for convenient management of Things, Channels and Users Mainflux. The AP is an interface and API (through which it interacts with Mainflux and Bootstrap). The main task of the AP is to configure for certain types of devices, for their further work with Bootstrap.
The Mainflux Admin Panel will work with the OIDC Keycloak provider to distribute AP users by organization (only members of one organization can view the configuration for devices belonging to there organization).


## Data Flow

Описываются основные потоки распределения информации

