import unittest
import bot

from aiogram_unittest import Requester
from aiogram_unittest.handler import MessageHandler
from aiogram_unittest.types.dataset import MESSAGE


class TestBot(unittest.IsolatedAsyncioTestCase):
    async def test_start(self):
        requester = Requester(request_handler=MessageHandler(bot.start, commands=["start"]))

        message = MESSAGE.as_object(text="/start")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "Привет!Я помогу отличить кота от хлеба! Объект перед тобой квадратный?")

    async def test_square_start(self):
        requester = Requester(request_handler=MessageHandler(bot.first_question))

        message = MESSAGE.as_object(text="/start")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "Привет!Я помогу отличить кота от хлеба! Объект перед тобой квадратный?")

    async def test_square_yes(self):
        requester = Requester(request_handler=MessageHandler(bot.first_question))

        message = MESSAGE.as_object(text="Ага")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "У него есть уши?")

    async def test_square_no(self):
        requester = Requester(request_handler=MessageHandler(bot.first_question))

        message = MESSAGE.as_object(text="ноуп")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "Это кот, а не хлеб! Не ешь его!")

    async def test_square_error(self):
        requester = Requester(request_handler=MessageHandler(bot.first_question))

        message = MESSAGE.as_object(text="хорошая идея")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, 'Ничего не понял')

    async def test_ears_start(self):
        requester = Requester(request_handler=MessageHandler(bot.second_question))

        message = MESSAGE.as_object(text="/start")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "Привет!Я помогу отличить кота от хлеба! Объект перед тобой квадратный?")

    async def test_ears_yes(self):
        requester = Requester(request_handler=MessageHandler(bot.second_question))

        message = MESSAGE.as_object(text="да")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "Это кот, а не хлеб! Не ешь его!")

    async def test_ears_no(self):
        requester = Requester(request_handler=MessageHandler(bot.second_question))

        message = MESSAGE.as_object(text="Найн")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, "Это хлеб, а не кот! Ешь его!")

    async def test_ears_error(self):
        requester = Requester(request_handler=MessageHandler(bot.second_question))

        message = MESSAGE.as_object(text="пожалуй откажусь")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, 'Ничего не понял')