#!/usr/bin/env python3
# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py --test prod-like; sleep 1; done

import argparse
from collections import deque
from enum import Enum
import time
import socket
import json

# ~~~~~============== CONFIGURATION  ==============~~~~~
team_name = "CodeGPT"

# ~~~~~============== MAIN LOOP ==============~~~~~

# You should put your code here! We provide some starter code as an example,
# but feel free to change/remove/edit/update any of it as you'd like. If you
# have any questions about the starter code, or what to do next, please ask us!
#
# To help you get started, the sample code below tries to buy BOND for a low
# price, and it prints the current prices for VALE every second. The sample
# code is intended to be a working example, but it needs some improvement
# before it will start making good trades!


def main():
    args = parse_arguments()

    exchange = ExchangeConnection(args=args)

    # Store and print the "hello" message received from the exchange. This
    # contains useful information about your positions. Normally you start with
    # all positions at zero, but if you reconnect during a round, you might
    # have already bought/sold symbols and have non-zero positions.
    hello_message = exchange.read_message()
    # print("First message from exchange:", hello_message)

    # Send an order for BOND at a good price, but it is low enough that it is
    # unlikely it will be traded against. Maybe there is a better price to
    # pick? Also, you will need to send more orders over time.
    # for i in range(27):

    # exchange.send_add_message(
    #     order_id=230000030, symbol="BOND", dir=Dir.BUY, price=999, size=10)

    # exchange.send_add_message(
    #     order_id=40000031, symbol="BOND", dir=Dir.SELL, price=1001, size=10)

    # Set up some variables to track the bid and ask price of a symbol. Right
    # now this doesn't track much information, but it's enough to get a sense
    # of the VALE market.
    vale_bid_price, vale_ask_price = 0, 0
    vale_last_print_time = time.time()

    def Step3function(bond_ask_price, gs_ask_price,
                      ms_ask_price, wfc_ask_price,
                      bond_bid_price, gs_bid_price,
                      ms_bid_price, wfc_bid_price,
                      xlf_bid_price, xlf_ask_price):
        xlf_literal_price = (3*(bond_ask_price) +
                             2*(gs_ask_price) +
                             3*(ms_ask_price) +
                             2*(wfc_ask_price)) / 10

        bucket_selling_price = (3*(bond_bid_price) +
                                2*(gs_bid_price) +
                                3*(ms_bid_price) +
                                2*(wfc_bid_price)) / 10

        # buy from other stocks and conver to xlf for sell
        price_diff_sell_xlf = xlf_bid_price - xlf_literal_price
        price_diff_buy_xlf = bucket_selling_price - xlf_ask_price
        order_id = 6202
        # print("price_diff_sell_xlf:", price_diff_sell_xlf)
        # print("price_diff_buy_xlf:", price_diff_buy_xlf)
        if (price_diff_sell_xlf > 10):
            # print("78")
            # buy from other stocks 3 bonds, 2 gs, 3ms, 2wfc
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="BOND", dir=Dir.BUY, price=bond_ask_price, size=3)
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="GS", dir=Dir.BUY, price=gs_ask_price, size=2)
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="MS", dir=Dir.BUY, price=ms_ask_price, size=3)
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="WFC", dir=Dir.BUY, price=wfc_ask_price, size=2)

            # conver to xlf*10
            order_id += 1
            exchange.send_convert_message(
                order_id=order_id, symbol="XLF", dir=Dir.BUY, size=10)

            # sell xlf*10
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="XLF", dir=Dir.SELL, price=xlf_bid_price, size=10)

        elif (price_diff_buy_xlf > 10):
            # buy from xlf
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="XLF", dir=Dir.BUY, price=xlf_ask_price, size=10)
            # convert to other stock
            order_id += 1
            exchange.send_convert_message(
                order_id=order_id, symbol="XLF", dir=Dir.SELL, size=10)
            # sell other stock
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="BOND", dir=Dir.SELL, price=bond_bid_price, size=3)
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="GS", dir=Dir.SELL, price=gs_bid_price, size=2)
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="MS", dir=Dir.SELL, price=ms_bid_price, size=3)
            order_id += 1
            exchange.send_add_message(
                order_id=order_id, symbol="WFC", dir=Dir.SELL, price=wfc_bid_price, size=2)

    # Here is the main loop of the program. It will continue to read and
    # process messages in a loop until a "close" message is received. You
    # should write to code handle more types of messages (and not just print
    # the message). Feel free to modify any of the starter code below.
    #
    # Note: a common mistake people make is to call write_message() at least
    # once for every read_message() response.
    #
    # Every message sent to the exchange generates at least one response
    # message. Sending a message in response to every exchange message will
    # cause a feedback loop where your bot's messages will quickly be
    # rate-limited and ignored. Please, don't do that!
    id_test = 9320
    price_threshhold = 1000
    cur_bond = 100
    max_bond = 20
    min_bond = 5

    bond_ask_price = 0
    gs_ask_price = 0
    ms_ask_price = 0
    wfc_ask_price = 0
    bond_bid_price = 0
    gs_bid_price = 0
    ms_bid_price = 0
    wfc_bid_price = 0
    xlf_bid_price = 0
    xlf_ask_price = 0
    vale_ask_price = 0
    vale_bid_price = 0
    vallbz_ask_price = 0
    vallbz_bid_price = 0
    vale_bid_amount = 0
    while True:
        message = exchange.read_message()

        # Some of the message types below happen infrequently and contain
        # important information to help you understand what your bot is doing,
        # so they are printed in full. We recommend not always printing every
        # message because it can be a lot of information to read. Instead, let
        # your code handle the messages and just print the information
        # important for you!
        if message["type"] == "close":
            print("The round has ended")
            break
        elif message["type"] == "error":
            print(message)
        elif message["type"] == "reject":
            print(message)
        elif message["type"] == "fill":
            print(message)
        elif message["type"] == "book":
            if message["symbol"] == "BOND":

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]
                # print("book:,", message)

                bond_bid_price = best_price("buy")
                bond_ask_price = best_price("sell")

                # step 3
                condition = [bond_ask_price, gs_ask_price,
                             ms_ask_price, wfc_ask_price,
                             bond_bid_price, gs_bid_price,
                             ms_bid_price, wfc_bid_price,
                             xlf_bid_price, xlf_ask_price]
                if not 0 in condition and not None in condition:
                    Step3function(bond_ask_price, gs_ask_price,
                                  ms_ask_price, wfc_ask_price,
                                  bond_bid_price, gs_bid_price,
                                  ms_bid_price, wfc_bid_price,
                                  xlf_bid_price, xlf_ask_price)

                # print("bond_bid_price", bond_bid_price)
                # print("bond_ask_price", bond_ask_price)
                now = time.time()
                if(bond_ask_price != None and bond_bid_price != None):
                    if (bond_ask_price <= 1000):
                        exchange.send_add_message(
                            order_id=id_test, symbol="BOND", dir=Dir.BUY, price=bond_ask_price, size=10)
                        id_test += 1
                    if (bond_bid_price > 1000):
                        id_test += 1
                        exchange.send_add_message(
                            order_id=id_test, symbol="BOND", dir=Dir.SELL, price=bond_bid_price, size=10)
            # attract price for VALE
            if message["symbol"] == "VALE":

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                vale_bid_price = best_price("buy")
                vale_ask_price = best_price("sell")

            # attract price from VALBZ
            elif message["symbol"] == "VALBZ":

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                vallbz_bid_price = best_price("buy")
                vallbz_ask_price = best_price("sell")

            # Attract price from GS
            elif message["symbol"] == "GS":

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                gs_bid_price = best_price("buy")
                gs_ask_price = best_price("sell")

                # step 3
                condition = [bond_ask_price, gs_ask_price,
                             ms_ask_price, wfc_ask_price,
                             bond_bid_price, gs_bid_price,
                             ms_bid_price, wfc_bid_price,
                             xlf_bid_price, xlf_ask_price]
                if not 0 in condition and not None in condition:
                    Step3function(bond_ask_price, gs_ask_price,
                                  ms_ask_price, wfc_ask_price,
                                  bond_bid_price, gs_bid_price,
                                  ms_bid_price, wfc_bid_price,
                                  xlf_bid_price, xlf_ask_price)

            # attract price for MS
            elif message["symbol"] == "MS":

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                ms_bid_price = best_price("buy")
                ms_ask_price = best_price("sell")

                # step 3
                condition = [bond_ask_price, gs_ask_price,
                             ms_ask_price, wfc_ask_price,
                             bond_bid_price, gs_bid_price,
                             ms_bid_price, wfc_bid_price,
                             xlf_bid_price, xlf_ask_price]
                if not 0 in condition and not None in condition:
                    Step3function(bond_ask_price, gs_ask_price,
                                  ms_ask_price, wfc_ask_price,
                                  bond_bid_price, gs_bid_price,
                                  ms_bid_price, wfc_bid_price,
                                  xlf_bid_price, xlf_ask_price)

            # attract price for WFC
            elif message["symbol"] == "WFC":
                # print("wfc entered")

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                wfc_bid_price = best_price("buy")
                wfc_ask_price = best_price("sell")

                # step 3
                condition = [bond_ask_price, gs_ask_price,
                             ms_ask_price, wfc_ask_price,
                             bond_bid_price, gs_bid_price,
                             ms_bid_price, wfc_bid_price,
                             xlf_bid_price, xlf_ask_price]
                if not 0 in condition and not None in condition:
                    # print("line 294 entered")
                    Step3function(bond_ask_price, gs_ask_price,
                                  ms_ask_price, wfc_ask_price,
                                  bond_bid_price, gs_bid_price,
                                  ms_bid_price, wfc_bid_price,
                                  xlf_bid_price, xlf_ask_price)

            # attract price for XLF
            elif message["symbol"] == "XLF":
                # print("xlf entered")

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                xlf_bid_price = best_price("buy")
                xlf_ask_price = best_price("sell")

                # step 3
                condition = [bond_ask_price, gs_ask_price,
                             ms_ask_price, wfc_ask_price,
                             bond_bid_price, gs_bid_price,
                             ms_bid_price, wfc_bid_price,
                             xlf_bid_price, xlf_ask_price]
                if not 0 in condition and not None in condition:
                    Step3function(bond_ask_price, gs_ask_price,
                                  ms_ask_price, wfc_ask_price,
                                  bond_bid_price, gs_bid_price,
                                  ms_bid_price, wfc_bid_price,
                                  xlf_bid_price, xlf_ask_price)

        # print(pricedic)
        #         id_test += 1
        # if message["symbol"] == "GS":

        #     def best_price(side):
        #         if message[side]:
        #             return message[side][0][0]
        #     print("book:,", message)

        #     GS_bid_price = best_price("buy")
        #     GS_ask_price = best_price("sell")
        #     print("bond_bid_price", GS_bid_price)
        #     print("GS_ask_price", GS_ask_price)
        #     now = time.time()
        #     if(GS_ask_price <= 1000):
        #         exchange.send_add_message(
        #             order_id=id_test, symbol="GS", dir=Dir.BUY, price=GS_ask_price, size=10)
        #         id_test += 1
        #     if(GS_bid_price > 1000):
        #         exchange.send_add_message(
        #             order_id=id_test, symbol="GS", dir=Dir.SELL, price=GS_bid_price, size=10)
        #         id_test += 1

        # if(cur_bond < max_bond):
        #     id_test += 1
        #     exchange.send_add_message(
        #         order_id=id_test, symbol="BOND", dir=Dir.BUY, price=999, size=2)
        # if(cur_bond > min_bond):
        # if(cur_bond > 10):
        #     id_test += 1
        #     exchange.send_add_message(
        #         order_id=id_test, symbol="BOND", dir=Dir.SELL, price=1010, size=2)
        #     cur_bond -= 2
        # if(cur_bond < 10):
        #     id_test += 1
        #     exchange.send_add_message(
        #         order_id=id_test, symbol="BOND", dir=Dir.SELL, price=1010, size=2)
        #     cur_bond -= 2
        # if bond_ask_price < price_threshhold & cur_bond < max_bond:
        #     id_test += 1
        #     exchange.send_add_message(
        #         order_id=id_test, symbol="BOND", dir=Dir.BUY, price=bond_bid_price, size=1)

        #     cur_bond += 1
        # if bond_bid_price > price_threshhold & min_bond < cur_bond:
        #     id_test += 1
        #     exchange.send_add_message(
        #         order_id=id_test, symbol="BOND", dir=Dir.SELL, price=bond_ask_price, size=1)
        #     cur_bond -= 1

    # if now > vale_last_print_time + 1:
    #     vale_last_print_time = now

    #     print(
    #         {
    #             "vale_bid_price": vale_bid_price,
    #             "vale_ask_price": vale_ask_price,
    #         }
    #     )


# ~~~~~============== PROVIDED CODE ==============~~~~~

# You probably don't need to edit anything below this line, but feel free to
# ask if you have any questions about what it is doing or how it works. If you
# do need to change anything below this line, please feel free to


class Dir(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class ExchangeConnection:
    def __init__(self, args):
        self.message_timestamps = deque(maxlen=500)
        self.exchange_hostname = args.exchange_hostname
        self.port = args.port
        exchange_socket = self._connect(
            add_socket_timeout=args.add_socket_timeout)
        self.reader = exchange_socket.makefile("r", 1)
        self.writer = exchange_socket

        self._write_message({"type": "hello", "team": team_name.upper()})

    def read_message(self):
        """Read a single message from the exchange"""
        message = json.loads(self.reader.readline())
        if "dir" in message:
            message["dir"] = Dir(message["dir"])
        return message

    def send_add_message(
        self, order_id: int, symbol: str, dir: Dir, price: int, size: int
    ):
        """Add a new order"""
        self._write_message(
            {
                "type": "add",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "price": price,
                "size": size,
            }
        )

    def send_convert_message(self, order_id: int, symbol: str, dir: Dir, size: int):
        """Convert between related symbols"""
        self._write_message(
            {
                "type": "convert",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "size": size,
            }
        )

    def send_cancel_message(self, order_id: int):
        """Cancel an existing order"""
        self._write_message({"type": "cancel", "order_id": order_id})

    def _connect(self, add_socket_timeout):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if add_socket_timeout:
            # Automatically raise an exception if no data has been recieved for
            # multiple seconds. This should not be enabled on an "empty" test
            # exchange.
            s.settimeout(5)
        s.connect((self.exchange_hostname, self.port))
        return s

    def _write_message(self, message):
        what_to_write = json.dumps(message)
        if not what_to_write.endswith("\n"):
            what_to_write = what_to_write + "\n"

        length_to_send = len(what_to_write)
        total_sent = 0
        while total_sent < length_to_send:
            sent_this_time = self.writer.send(
                what_to_write[total_sent:].encode("utf-8")
            )
            if sent_this_time == 0:
                raise Exception("Unable to send data to exchange")
            total_sent += sent_this_time

        now = time.time()
        self.message_timestamps.append(now)
        if len(
            self.message_timestamps
        ) == self.message_timestamps.maxlen and self.message_timestamps[0] > (now - 1):
            print(
                "WARNING: You are sending messages too frequently. The exchange will start ignoring your messages. Make sure you are not sending a message in response to every exchange message."
            )


def parse_arguments():
    test_exchange_port_offsets = {"prod-like": 0, "slower": 1, "empty": 2}

    parser = argparse.ArgumentParser(description="Trade on an ETC exchange!")
    exchange_address_group = parser.add_mutually_exclusive_group(required=True)
    exchange_address_group.add_argument(
        "--production", action="store_true", help="Connect to the production exchange."
    )
    exchange_address_group.add_argument(
        "--test",
        type=str,
        choices=test_exchange_port_offsets.keys(),
        help="Connect to a test exchange.",
    )

    # Connect to a specific host. This is only intended to be used for debugging.
    exchange_address_group.add_argument(
        "--specific-address", type=str, metavar="HOST:PORT", help=argparse.SUPPRESS
    )

    args = parser.parse_args()
    args.add_socket_timeout = True

    if args.production:
        args.exchange_hostname = "production"
        args.port = 25000
    elif args.test:
        args.exchange_hostname = "test-exch-" + team_name
        args.port = 25000 + test_exchange_port_offsets[args.test]
        if args.test == "empty":
            args.add_socket_timeout = False
    elif args.specific_address:
        args.exchange_hostname, port = args.specific_address.split(":")
        args.port = int(port)

    return args


if __name__ == "__main__":
    # Check that [team_name] has been updated.
    assert (
        team_name != "REPLACEME"
    ), "Please put your team name in the variable [team_name]."

    main()
