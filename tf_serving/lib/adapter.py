import paho.mqtt.client as mqtt

from grpc.beta import implementations
import tensorflow as tf
from data_processing import *
from tensorflow.core.framework import types_pb2
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

cli = mqtt.Client()

def prediction(address, value):

    tf.app.flags.DEFINE_string('server', address, 'inception_inference service host:port')
    FLAGS = tf.app.flags.FLAGS

    # Prepare request
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'cnn'
    request.model_spec.signature_name = 'predict'
    request.inputs['input'].dtype = types_pb2.DT_INT32

    request.inputs['input'].CopyFrom(tf.contrib.util.make_tensor_proto(value.astype(dtype=numpy.float32)))
    request.inputs['prob'].CopyFrom(tf.contrib.util.make_tensor_proto(0.8))
    request.output_filter.append('output')

    # Send request
    host, port = FLAGS.server.split(':')
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    prediction = stub.Predict(request, 10.0)
    floats = prediction.outputs['output'].float_val
    output_value = numpy.array(floats)

    return {output_value}

class Nats_to_TF():

    def __init__(self, address, thing_id, thing_key, channel_id, thing_ext_id, dt):

        self.address = address
        self.thing_id = thing_id
        self.thing_key = thing_key
        self.channel_id =channel_id
        self.dt =dt

        cli.username_pw_set(self.thing_id, self.thing_key)
        cli.connect([self.address.split(":")])

        cli.loop_start()
        cli.on_message = self.on_message


    def on_message(self, message, dt):

        print("\n Received message =", str(message.payload.decode("utf-8")))


    def tf_worker(self, address):

        value_from_tf = None

        while True:

            channel_id = "channels/{channel_id}/messages"

            res = cli.subscribe(channel_id)

            if res is None or len(res) == 0:
                print("{timestamp: }No any data from NATS".format(timestamp=self.dt))
            else:
                value_from_nats = cli.subscribe(channel_id)
                value_from_tf = prediction(address.split(":"), value_from_nats)

            payload = "[{\"n\":\"prediction\",\"u\":\"m\",\"v\":" + str(value_from_tf) + "}]"
            cli.publish(channel_id, payload =payload)
