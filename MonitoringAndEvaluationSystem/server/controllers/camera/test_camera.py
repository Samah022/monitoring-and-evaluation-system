import asyncio
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
from server.controllers.camera.camera import Camera
import numpy as np

class TestCameraMethods(unittest.TestCase):
    def setUp(self):
        self.camera = Camera()
        self.camera2 = Camera(ID=1, camera_name="Test Camera", camera_URL="rtsp://127.0.0.1:8554/test",evaluation_criteria=["uniform"])
    
    def test_get_camera_ID(self):
        self.assertEqual(self.camera2.get_camera_ID(), 1)

    def test_get_camera_name(self):
        self.assertEqual(self.camera2.get_camera_name(), "Test Camera")

    def test_get_camera_URL(self):
        self.assertEqual(self.camera2.get_camera_URL(), "rtsp://127.0.0.1:8554/test")

    def test_get_evaluation_criteria(self):
        self.assertEqual(self.camera2.get_evaluation_criteria(), ["uniform"])

    def test_set_camera_ID(self):
        self.assertTrue(self.camera.set_camera_ID(5))
        self.assertEqual(self.camera.get_camera_ID(), 5)

    def test_set_camera_ID_invalid_type(self):
        invalid_id = "123"
        result = self.camera.set_camera_ID(invalid_id)
        self.assertFalse(result) 
        self.assertIsNone(self.camera.get_camera_ID())

    def test_set_camera_name_valid(self):
        valid_name = "Test Camera"
        self.assertTrue(self.camera.set_camera_name(valid_name))
        self.assertEqual(self.camera.get_camera_name(), valid_name)

    def test_set_camera_name_invalid_type(self):
        invalid_name = 123
        result = self.camera.set_camera_name(invalid_name)
        self.assertFalse(result) 
        self.assertIsNone(self.camera.get_camera_name())

    def test_set_camera_name_invalid_length(self):
        long_name = "a" * 256
        self.assertFalse(self.camera.set_camera_name(long_name))

    def test_set_camera_URL_valid(self):
        valid_url = "rtsp://192.168.255.210:8080/h264_ulaw.sdp"
        self.assertTrue(self.camera.set_camera_URL(valid_url))
        self.assertEqual(self.camera.get_camera_URL(), valid_url)

    def test_set_camera_URL_invalid_type(self):
        invalid_url = 123
        self.assertFalse(self.camera.set_camera_URL(invalid_url))
        self.assertIsNone(self.camera.get_camera_URL())

    def test_set_camera_URL_invalid_format(self):
        invalid_url = "invalid_url"
        self.assertFalse(self.camera.set_camera_URL(invalid_url))
        self.assertIsNone(self.camera.get_camera_URL())

    def test_set_evaluation_criteria_valid(self):
        valid_criteria = ["emotion"]
        self.assertTrue(self.camera.set_evaluation_criteria(valid_criteria))
        self.assertEqual(self.camera.get_evaluation_criteria(), valid_criteria)

    def test_set_evaluation_criteria_none(self):
        camera = Camera()
        result = camera.set_evaluation_criteria(None)
        self.assertIsNone(result)
        self.assertIsNone(camera.get_evaluation_criteria())

    def test_set_evaluation_criteria_invalid_type(self):
        camera = Camera()
        invalid_criteria = "invalid_criteria"
        result = camera.set_evaluation_criteria(invalid_criteria)
        self.assertFalse(result)
        self.assertIsNone(camera.get_evaluation_criteria())

    def test_stream_frame(self):
            sample_frame = np.zeros((100, 100, 3), dtype=np.uint8)
            encoded_frame = self.camera2._Camera__stream_frame(sample_frame)
            self.assertIsInstance(encoded_frame, str)

    def test_stream_frame_invalid_type(self):
        invalid_frame = "not_a_frame"
        encoded_frame = self.camera2._Camera__stream_frame(invalid_frame)
        self.assertIsNone(encoded_frame)

    def test_stream_frame_encoding_error(self):
        with patch("cv2.imencode", return_value=(False, None)):
            sample_frame = np.zeros((100, 100, 3), dtype=np.uint8)
            with self.assertRaises(Exception):
                self.camera2._Camera__stream_frame(sample_frame)
                self.assertIsNone(sample_frame)

    async def test_generate_frame_vaild(self):
        camera = Camera()
        generator = camera.generate_frame(0)
        generated_frames = []
        async for data in generator:
            generated_frames.append(data)
            break
        self.assertIsNotNone(generated_frames)

    async def test_generate_frame_invaild(self):
        camera = Camera()
        rtsp_url = "http://192.168.111.210:8080/h264_ulaw.sdp"
        generator = camera.generate_frame(rtsp_url)
        generated_frames = []
        async for data in generator:
            generated_frames.append(data)
            break
        self.assertIsNotNone(generated_frames)

    async def test_analysis_frame_valid(self):
        mock_criteria = MagicMock()
        mock_criteria.detect = MagicMock()

        mock_criteria_factory_instance = MagicMock()
        mock_criteria_factory_instance.create_criteria.return_value = mock_criteria

        mock_criteria_factory = MagicMock()
        mock_criteria_factory.return_value = mock_criteria_factory_instance

        with patch("server.controllers.camera.camera.CriteriaFactory", mock_criteria_factory):
            camera = Camera()
            camera.set_camera_ID(8)
            camera.set_camera_URL("rtsp://127.0.0.1:8554/test")
            camera.set_evaluation_criteria(["uniform"])

            await camera.analysis_frame()

            mock_criteria_factory_instance.create_criteria.assert_called_once_with('uniform')

            mock_criteria.detect.assert_called_with(8, "rtsp://127.0.0.1:8554/test")

    async def test_analysis_frame_invalid(self):
        with patch("server.controllers.camera.camera.CriteriaFactory") as mock_criteria_factory:
            camera3 = Camera()

            mock_criteria_factory_instance = MagicMock()
            mock_criteria_factory_instance.create_criteria.side_effect = Exception("Test Exception")
            mock_criteria_factory.return_value = mock_criteria_factory_instance

            await camera3.analysis_frame()

            self.assertIsNone(camera3.get_camera_ID())
            self.assertIsNone(camera3.get_camera_URL())

    async def run_async_test(self, coro):
        loop = asyncio.get_event_loop()
        await coro()
        loop.stop()
    
test_case = TestCameraMethods()
loop = asyncio.get_event_loop()
loop.run_until_complete(test_case.run_async_test(test_case.test_generate_frame_vaild))
loop.run_until_complete(test_case.run_async_test(test_case.test_generate_frame_invaild))
loop.run_until_complete(test_case.run_async_test(test_case.test_analysis_frame_valid))
loop.run_until_complete(test_case.run_async_test(test_case.test_analysis_frame_invalid))
loop.close()
