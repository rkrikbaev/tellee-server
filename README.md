# TELLY

Сюда добавить схему 
https://drive.google.com/file/d/1jvZtF90YoJIa2G289WVRiT4i6o60chOG/view?usp=sharing


Описание TELLY

## Mainflux

[Mainflux](https://www.mainflux.com/) - is modern, scalable, secure open source and patent-free IoT cloud platform written in [Go](https://golang.org/doc/).

Он принимает соединения пользователя и вещи через различные сетевые протоколы (т.е. [HTTP](https://ru.wikipedia.org/wiki/HTTP), [MQTT](https://ru.wikipedia.org/wiki/MQTT), [WebSocket](https://ru.wikipedia.org/wiki/WebSocket), [CoAP](http://lib.tssonline.ru/articles2/internet-of-things/protokol-interneta-veschey-coap)), тем самым создавая плавный мост между ними. Он используется в качестве промежуточного программного обеспечения IoT для построения сложных решений IoT.

<ul>
<li>Соединение протоколов (т.е. [HTTP](https://ru.wikipedia.org/wiki/HTTP), [MQTT](https://ru.wikipedia.org/wiki/MQTT), [WebSocket](https://ru.wikipedia.org/wiki/WebSocket), [CoAP](http://lib.tssonline.ru/articles2/internet-of-things/protokol-interneta-veschey-coap))</li>
<li>[Управление устройством и обеспечение](https://mainflux.readthedocs.io/en/latest/messaging/)</li>
<li>[Детальное управление доступом](https://mainflux.readthedocs.io/en/latest/provisioning/)</li>
<li>[Поддержка платформ и инструментария](https://mainflux.readthedocs.io/en/latest/storage/)</li>
<li>Развертывание на основе контейнеров с использованием [Docker](https://docs.docker.com/)</li>
</ul>

### HTTP

Representational State Transfer (REST) is a software architectural style that defines a set of constraints to be used for creating Web services. Web services that conform to the REST architectural style, called RESTful Web services (RWS), provide interoperability between computer systems on the Internet. RESTful Web services allow the requesting systems to access and manipulate textual representations of Web resources by using a uniform and predefined set of stateless operations. Other kinds of Web services, such as SOAP Web services, expose their own arbitrary sets of operations.

"Web resources" were first defined on the World Wide Web as documents or files identified by their URLs. However, today they have a much more generic and abstract definition that encompasses every thing or entity that can be identified, named, addressed, or handled, in any way whatsoever, on the Web. In a RESTful Web service, requests made to a resource's URI will elicit a response with a payload formatted in HTML, XML, JSON, or some other format. The response can confirm that some alteration has been made to the stored resource, and the response can provide hypertext links to other related resources or collections of resources. When HTTP is used, as is most common, the operations (HTTP methods) available are GET, HEAD, POST, PUT, PATCH, DELETE, CONNECT, OPTIONS and TRACE.

To publish message over channel, thing should send following request:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -X POST -H "Content-Type: application/senml+json" -H "Authorization: <thing_token>" https://localhost/http/channels/<channel_id>/messages -d '[{"bn":"some-base-name:","bt":1.276020076001e+09, "bu":"A","bver":5, "n":"voltage","u":"V","v":120.1}, {"n":"current","t":-5,"v":1.2}, {"n":"current","t":-4,"v":1.3}]'

Note that if you're going to use senml message format, you should always send messages as an array.

### MQTT Broker

The counterpart of the MQTT client is the MQTT broker. The broker is at the heart of any publish/subscribe protocol. Depending on the implementation, a broker can handle up to thousands of concurrently connected MQTT clients. The broker is responsible for receiving all messages, filtering the messages, determining who is subscribed to each message, and sending the message to these subscribed clients. The broker also holds the sessions of all persisted clients, including subscriptions and missed messages (more details). Another responsibility of the broker is the authentication and authorization of clients. Usually, the broker is extensible, which facilitates custom authentication, authorization, and integration into backend systems. Integration is particularly important because the broker is frequently the component that is directly exposed on the internet, handles a lot of clients, and needs to pass messages to downstream analyzing and processing systems.


### MQTT

To send and receive messages over MQTT you could use Mosquitto tools, or Paho if you want to use MQTT over WebSocket.

To publish message over channel, thing should call following command:

    mosquitto_pub -u <thing_id> -P <thing_key> -t channels/<channel_id>/messages -h localhost -m '[{"bn":"some-base-name:","bt":1.276020076001e+09, "bu":"A","bver":5, "n":"voltage","u":"V","v":120.1}, {"n":"current","t":-5,"v":1.2}, {"n":"current","t":-4,"v":1.3}]'

To subscribe to channel, thing should call following command:

    mosquitto_sub -u <thing_id> -P <thing_key> -t channels/<channel_id>/messages -h localhost

In order to pass content type as part of topic, one should append it to the end of an existing topic. Content type value should always be prefixed with `/ct/`. If you want to use standard topic such as `channels/<channel_id>/messages` with SenML content type, you should use following topic `channels/<channel_id>/messages/ct/application_senml-json`. If there is no `/ct/` prefix in the subtopic, then content type will have the default value which is `application/senml+json`. Content type will be removed from the topic under the hood. You should pass content type only when you're publishing a message. Characters like `_` and `-` in the content type will be replaced with `/` and `+` respectively.

If you are using TLS to secure MQTT connection, `add --cafile docker/ssl/certs/ca.crt` to every command.

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

Also, the configuration contains an external ID and external key, which will be explained later. In order to enable the thing to start bootstrapping process, the user needs to upload a valid configuration for that specific thing. This can be done using the following HTTP request:

    curl -s -S -i -X POST -H "Authorization: <user_token>" -H "Content-Type: application/json" http://localhost:8200/things/configs -d '{
            "external_id":"09:6:0:sb:sa",
            "thing_id": "1b9b8fae-9035-4969-a240-7fe5bdc0ed28",
            "external_key":"key",
            "name":"some",
            "channels":[
                    "c3642289-501d-4974-82f2-ecccc71b2d83",
                    "cd4ce940-9173-43e3-86f7-f788e055eb14",
                    "ff13ca9c-7322-4c28-a25c-4fe5c7b753fc",
                    "c3642289-501d-4974-82f2-ecccc71b2d82"
    ],
            "content": "config...",
            "client_cert": "PEM cert",
            "client_key": "PEM client cert key",
            "ca_cert": "PEM CA cert"
    }'
    
In this example, channels field represents the list of Mainflux `channel` IDs the thing is connected to. These channels need to be provisioned before the configuration is uploaded. Field content represents custom configuration. This custom configuration contains parameters that can be used to set up the thing. It can also be empty if no additional set up is needed. Field name is human readable `name` and `thing_id` is an ID of the Mainflux thing. This field is not required. If `thing_id` is empty, corresponding Mainflux thing will be created implicitly and its ID will be sent as a part of `Location` header of the response. Fields `client_cert`, `client_key`, and `ca_cert` represent PEM or base64-encoded DER client certificate, client certificate key, and trusted CA, respectively.

There are two more fields: `external_id` and `external_key`. External ID represents an ID of the device that corresponds to the given thing. For example, this can be a MAC address or the serial number of the device. The external key represents the device key. This is the secret key that's safely stored on the device and it is used to authorize the thing during the bootstrapping process. Please note that external ID and external key and Mainflux ID and Mainflux key are completely different concepts. External id and key are only used to authenticate a device that corresponds to the specific Mainflux thing during the bootstrapping procedure.

#### Bootstrapping

Currently, the bootstrapping procedure is executed over the HTTP protocol. Bootstrapping is nothing else but fetching and applying the configuration that corresponds to the given Mainflux thing. In order to fetch the configuration, the thing needs to send a bootstrapping request:

    curl -s -S -i -H "Authorization: <external_key>" http://localhost:8200/things/bootstrap/<external_id>
    
The response body should look something like:

    {
       "mainflux_id":"7c9df5eb-d06b-4402-8c1a-df476e4394c8",
       "mainflux_key":"86a4f870-eba4-46a0-bef9-d94db2b64392",
       "mainflux_channels":[
          {
             "id":"ff13ca9c-7322-4c28-a25c-4fe5c7b753fc",
             "name":"some channel",
             "metadata":{
                "operation":"someop",
                "type":"metadata"
             }
          },
          {
             "id":"925461e6-edfb-4755-9242-8a57199b90a5",
             "name":"channel1",
             "metadata":{
                "type":"control"
             }
          }
       ],
       "content":"config..."
    }
The response consists of an ID and key of the Mainflux thing, the list of channels and custom configuration (`content` field). The list of channels contains not just channel IDs, but the additional Mainflux channel data (`name` and `metadata` fields), as well.

Enabling and disabling things
Uploading configuration does not automatically connect thing to the given list of channels. In order to connect the thing to the channels, user needs to send the following HTTP request:

    curl -s -S -i -X PUT -H "Authorization: <user_token>" -H "Content-Type: application/json" http://localhost:8200/things/state/<thing_id> -d '{"state": 1}'

In order to disconnect, the same request should be sent with the value of state set to 0.

For more information about Bootstrap API, please check out the [API documentation](https://github.com/mainflux/mainflux/blob/master/bootstrap/swagger.yml).

### Provisioning

Provisioning is a process of configuration of an IoT platform in which system operator creates and sets-up different entities used in the platform - users, channels and things.

#### Account creation

Use the Mainflux API to create user account:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -X POST -H "Content-Type: application/json" https://localhost/users -d '{"email":"john.doe@email.com", "password":"123"}'

Note that when using official `docker-compose`, all services are behind `nginx` proxy and all traffic is `TLS` encrypted.

#### Obtaining an authorization key

In order for this user to be able to authenticate to the system, you will have to create an authorization token for him:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -X POST -H "Content-Type: application/json" https://localhost/tokens -d '{"email":"john.doe@email.com", "password":"123"}'
Response should look like this:
    
    {
          "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MjMzODg0NzcsImlhdCI6MTUyMzM1MjQ3NywiaXNzIjoibWFpbmZsdXgiLCJzdWIiOiJqb2huLmRvZUBlbWFpbC5jb20ifQ.cygz9zoqD7Rd8f88hpQNilTCAS1DrLLgLg4PRcH-iAI"
    }
    
#### System provisioning

Before proceeding, make sure that you have created a new account, and obtained an authorization key.

#### Provisioning things
Things are provisioned by executing request `POST /things` with a JSON payload. Note that you will also need `user_auth_token` in order to provision things that belong to this particular user.

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -X POST -H "Content-Type: application/json" -H "Authorization: <user_auth_token>" https://localhost/things -d '{"name":"weio"}'

Response will contain Location header whose value represents path to newly created thing:

    HTTP/1.1 201 Created
    Content-Type: application/json
    Location: /things/81380742-7116-4f6f-9800-14fe464f6773
    Date: Tue, 10 Apr 2018 10:02:59 GMT
    Content-Length: 0

#### Retrieving provisioned things

In order to retrieve data of provisioned things that is written in database, you can send following request:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -H "Authorization: <user_auth_token>" https://localhost/things

Notice that you will receive only those things that were provisioned by `user_auth_token` owner.

    HTTP/1.1 200 OK
    Content-Type: application/json
    Date: Tue, 10 Apr 2018 10:50:12 GMT
    Content-Length: 1105
    
    {
      "total": 2,
      "offset": 0,
      "limit": 10,
      "things": [
        {
          "id": "81380742-7116-4f6f-9800-14fe464f6773",
          "name": "weio",
          "key": "7aa91f7a-cbea-4fed-b427-07e029577590"
        },
        {
          "id": "cb63f852-2d48-44f0-a0cf-e450496c6c92",
          "name": "myapp",
          "key": "cbf02d60-72f2-4180-9f82-2c957db929d1"
        }
      ]
    }

You can specify `offset` and `limit` parameters in order to fetch specific group of things. In that case, your request should look like:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -H "Authorization: <user_auth_token>" https://localhost/things?offset=0&limit=5

If you don't provide them, default values will be used instead: 0 for `offset`, and 10 for `limit`. Note that `limit` cannot be set to values greater than 100. Providing invalid values will be considered malformed request.

#### Removing things

In order to remove you own thing you can send following request:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -X DELETE -H "Authorization: <user_auth_token>" https://localhost/things/<thing_id>

#### Provisioning channels

Channels are provisioned by executing request `POST /channels`:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -X POST -H "Content-Type: application/json" -H "Authorization: <user_auth_token>" https://localhost/channels -d '{"name":"mychan"}'

After sending request you should receive response with `Location` header that contains path to newly created channel:

    HTTP/1.1 201 Created
    Content-Type: application/json
    Location: /channels/19daa7a8-a489-4571-8714-ef1a214ed914
    Date: Tue, 10 Apr 2018 11:30:07 GMT
    Content-Length: 0

#### Retrieving provisioned channels

To retreve provisioned channels you should send request to `/channels` with authorization token in `Authorization` header:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -H "Authorization: <user_auth_token>" https://localhost/channels

Note that you will receive only those channels that were created by authorization token's owner.

    HTTP/1.1 200 OK
    Content-Type: application/json
    Date: Tue, 10 Apr 2018 11:38:06 GMT
    Content-Length: 139
    
    {
      "total": 1,
      "offset": 0,
      "limit": 10,
      "channels": [
        {
          "id": "19daa7a8-a489-4571-8714-ef1a214ed914",
          "name": "mychan"
        }
      ]
    }

You can specify  offset and  limit parameters in order to fetch specific group of channels. In that case, your request should look like:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -H "Authorization: <user_auth_token>" https://localhost/channels?offset=0&limit=5

If you don't provide them, default values will be used instead: 0 for `offset`, and 10 for `limit`. Note that `limit` cannot be set to values greater than 100. Providing invalid values will be considered malformed request.

#### Removing channels

In order to remove specific channel you should send following request:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -X DELETE -H "Authorization: <user_auth_token>" https://localhost/channels/<channel_id>

#### Access control

Channel can be observed as a communication group of things. Only things that are connected to the channel can send and receive messages from other things in this channel. things that are not connected to this channel are not allowed to communicate over it.

Only user, who is the owner of a channel and of the things, can connect the things to the channel (which is equivalent of giving permissions to these things to communicate over given communication group).

To connect thing to the channel you should send following request:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -X PUT -H "Authorization: <user_auth_token>" https://localhost/channels/<channel_id>/things/<thing_id>

You can observe which things are connected to specific channel:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -H "Authorization: <user_auth_token>" https://localhost/channels/<channel_id>/things

Response that you'll get should look like this:

    {
      "total": 2,
      "offset": 0,
      "limit": 10,
      "things": [
        {
          "id": "3ffb3880-d1e6-4edd-acd9-4294d013f35b",
          "name": "d0",
          "key": "b1996995-237a-4552-94b2-83ec2e92a040",
          "metadata": "{}"
        },
        {
          "id": "94d166d6-6477-43dc-93b7-5c3707dbef1e",
          "name": "d1",
          "key": "e4588a68-6028-4740-9f12-c356796aebe8",
          "metadata": "{}"
        }
      ]
    }

You can also observe to which channels is specified thing connected:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -H "Authorization: <user_auth_token>" https://localhost/things/<thing_id>/channels

Response that you'll get should look like this:

    {
      "total": 2,
      "offset": 0,
      "limit": 10,
      "channels": [
        {
          "id": "5e62eb13-2695-4860-8d87-85b8a2f80fd4",
          "name": "c1",
          "metadata": "{}"
        },
        {
          "id": "c4b5e19a-7ffe-4172-b2c5-c8b9d570a165",
          "name": "c0",
          "metadata":"{}"
        }
      ]
    }

If you want to disconnect your thing from the channel, send following request:

    curl -s -S -i --cacert docker/ssl/certs/mainflux-server.crt --insecure -X DELETE -H "Authorization: <user_auth_token>" https://localhost/channels/<channel_id>/things/<thing_id>

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

#### Use Cases

NATS can run anywhere, from large servers and cloud instances, through edge gateways and even IoT devices. Use cases for NATS include:
<ul>
<li>Cloud Messaging
<ul>
<li>Services (microservices, service mesh)</li>
<li>Event/Data Streaming (observability, analytics, ML/AI)</li>
</ul>
</li>

<li>Command and Control
<ul>
<li>IoT and Edge</li>
<li>Telemetry / Sensor Data / Command and Control</li>
</ul>
</li>

<li>Augmenting or Replacing Legacy Messaging Systems</li>
<ul>

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

## Flash



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



