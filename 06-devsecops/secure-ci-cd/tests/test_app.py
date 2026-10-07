import json
import unittest
from app.calculator import calculate
from app.server import application


class CalculatorTests(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(calculate("10 + 20"), 30)

    def test_zero(self):
        self.assertEqual(calculate("0+0"), 0)

    def test_limit(self):
        self.assertEqual(calculate("999999999+1"), 1000000000)

    def test_reject_invalid_inputs(self):
        for value in ["", "1", "1+2+3", "1.2+3", "-1+2", "1000000000+0", "١+٢", None,
                      "__import__('os').system('id')", "1" * 101]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                calculate(value)


class HttpTests(unittest.TestCase):
    def request(self, path, query="", method="GET"):
        response = {}
        def start(status, headers):
            response.update(status=status, headers=dict(headers))
        body = b"".join(application({"PATH_INFO": path, "QUERY_STRING": query,
                                      "REQUEST_METHOD": method}, start))
        return response, body

    def test_health(self):
        response, body = self.request("/health")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(json.loads(body)["status"], "ok")

    def test_page(self):
        response, body = self.request("/")
        self.assertIn(b"TechSecure", body)
        self.assertEqual(response["headers"]["X-Content-Type-Options"], "nosniff")

    def test_api_sum(self):
        response, body = self.request("/api/calculate", "expression=10%2B20")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(json.loads(body)["result"], 30)

    def test_api_reject(self):
        self.assertEqual(self.request("/api/calculate", "expression=eval")[0]["status"], "400 Bad Request")

    def test_missing(self):
        self.assertEqual(self.request("/missing")[0]["status"], "404 Not Found")

    def test_method(self):
        self.assertEqual(self.request("/", method="POST")[0]["status"], "405 Method Not Allowed")


if __name__ == "__main__":
    unittest.main()
