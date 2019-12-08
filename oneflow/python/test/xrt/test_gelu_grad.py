import unittest
import numpy as np

import oneflow as flow

def make_job(shape, dtype=flow.float32):
    @flow.function
    def gelu_grad_job(x = flow.input_blob_def(shape, dtype=dtype),
                      dy = flow.input_blob_def(shape, dtype=dtype)):
        flow.config.use_xla_jit(False)
        flow.config.use_tensorrt(False)
        return flow.keras.activations.gelu_grad(x, dy)
    return gelu_grad_job

def make_xla_job(shape, dtype=flow.float32):
    @flow.function
    def xla_gelu_grad_job(x = flow.input_blob_def(shape, dtype=dtype),
                          dy = flow.input_blob_def(shape, dtype=dtype)):
        flow.config.use_xla_jit(True)
        return flow.keras.activations.gelu_grad(x, dy)
    return xla_gelu_grad_job


class TestGeluGrad(unittest.TestCase):
    def _test_body(self, x, dy, dtype=np.float32):
        f1 = make_job(x.shape, dtype=flow.float32)
        f2 = make_xla_job(x.shape, dtype=flow.float32)
        a = f1(x, dy).get()
        b = f2(x, dy).get()
        print("without xla: ", a)
        print("with xla", b)
        self.assertTrue(np.allclose(a, b , rtol=1e-03, atol=1e-05))

        flow.clear_default_session()

    def _test_ones_body(self, shape, dtype=np.float32):
        x = np.ones(shape, dtype=dtype)
        dy = np.ones(shape, dtype=dtype)
        self._test_body(x, dy, dtype=dtype)

    def _test_random_body(self, shape, dtype=np.float32):
        x = np.random.random(shape).astype(dtype)
        dy = np.random.random(shape).astype(dtype)
        self._test_body(x, dy, dtype=dtype)

    def test_ones_input(self):
        self._test_ones_body((1))
        self._test_ones_body((1, 10))
        self._test_ones_body((2, 10, 2))
        self._test_ones_body((2, 5, 2, 2))

    def test_random_input(self):
        self._test_random_body((1))
        self._test_random_body((1, 10))
        self._test_random_body((2, 10, 2))
        self._test_random_body((2, 5, 2, 2))

if __name__ == '__main__':
    unittest.main()
