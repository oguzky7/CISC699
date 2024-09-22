import logging, unittest
from unittest.mock import patch, AsyncMock
from test_init import BaseTestSetup, CustomTextTestRunner

"""
File: test_!stop_monitoring_price.py
Purpose: This file contains unit tests for the !stop_monitoring_price command in the Discord bot.
The tests validate both successful and error scenarios, ensuring that the bot stops monitoring prices or handles errors.
"""

class TestStopMonitoringPriceCommand(BaseTestSetup):
    @patch('control.PriceControl.PriceControl.receive_command', new_callable=AsyncMock)
    async def test_stop_monitoring_price_error(self, mock_receive_command):
        """Test the stop_monitoring_price command when it encounters an error."""
        logging.info("Starting test: test_stop_monitoring_price_error")

        # Simulate a failure during price monitoring stop
        mock_receive_command.return_value = "Failed to stop monitoring."

        # Retrieve the stop_monitoring_price command from the bot
        command = self.bot.get_command("stop_monitoring_price")
        self.assertIsNotNone(command)

        # Call the command
        await command(self.ctx)

        # Verify the correct error message is sent
        expected_message = "Failed to stop monitoring."
        self.ctx.send.assert_called_with(expected_message)
        logging.info("Verified error handling during price monitoring stop.")

if __name__ == "__main__":
    unittest.main(testRunner=CustomTextTestRunner(verbosity=2))
