from grpc.beta import implementations
import tensorflow as tf
from data_processing import *
from tensorflow.core.framework import types_pb2
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2


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




