import unittest

from cdp_use.cdp.registry import EventRegistry


class TestEventRegistry(unittest.IsolatedAsyncioTestCase):
    async def test_registering_two_handlers_for_same_event_calls_both(self) -> None:
        registry = EventRegistry()
        calls: list[str] = []

        registry.register(
            "Network.responseReceived",
            lambda params, session_id=None: calls.append("first"),
        )
        registry.register(
            "Network.responseReceived",
            lambda params, session_id=None: calls.append("second"),
        )

        handled = await registry.handle_event(
            "Network.responseReceived",
            {"requestId": "1"},
            None,
        )

        self.assertTrue(handled)
        self.assertEqual(calls, ["first", "second"])

    async def test_unregister_removes_all_handlers_for_method(self) -> None:
        registry = EventRegistry()
        calls: list[str] = []

        registry.register(
            "Network.responseReceived",
            lambda params, session_id=None: calls.append("first"),
        )
        registry.register(
            "Network.responseReceived",
            lambda params, session_id=None: calls.append("second"),
        )

        registry.unregister("Network.responseReceived")

        handled = await registry.handle_event(
            "Network.responseReceived",
            {"requestId": "1"},
            None,
        )

        self.assertFalse(handled)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
