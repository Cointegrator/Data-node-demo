import openai
import re
import json
from flask_cors import CORS
from flask import Flask, request, jsonify


openai.api_key = "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"


def get_indicators(ticker):
    model_engine="gpt-3.5-turbo"
    max_tokens=1024
    temperature=0
    init_messages = [
        {"role": "system", "content": "You are a trading strategy generator assistant for Indicator lab. Your task is to help me find some good on chain, and off chain indicators for the Crypto coin {ticker} that can predict price change of the coin ."}]

    def generate_text(messages, model_engine="gpt-3.5-turbo", max_tokens=1024, temperature=0):
        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0,
        )

        message = completions.choices[0].message.content
        return message.strip()

