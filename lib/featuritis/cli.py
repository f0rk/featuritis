# Copyright 2020, Ryan P. Kelly.

import argparse
import csv
import os
import sys

import featuritis.exc
from featuritis.init import initialize
from featuritis.manager import Manager


class App(object):

    def run(self):

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--config",
            "-c",
            help="path to featuritis configuration file",
        )

        subparsers = parser.add_subparsers(dest="command")

        init_parser = subparsers.add_parser("init")
        init_parser.set_defaults(func=self.init)

        add_parser = subparsers.add_parser("add")
        add_parser.set_defaults(func=self.add)

        add_parser.add_argument(
            "id",
            help="identifier of the ticket, story, etc.",
        )

        add_parser.add_argument(
            "--description",
            "-d",
            help="description for this item",
        )

        add_parser.add_argument(
            "--author",
            "-a",
            help="author(s) for this item",
        )

        add_parser.add_argument(
            "--ticketing-system",
            "-t",
            help=(
                "which ticketing system this feature belongs to. should match "
                "a configuration key in the featuritis config file."
            ),
        )

        list_parser = subparsers.add_parser("list")
        list_parser.set_defaults(func=self.list)

        list_parser.add_argument(
            "--format",
            "-f",
            help="format to print",
            choices=["table", "csv"],
            default="table",
        )

        args = parser.parse_args()

        try:
            args.func(args)
            return 0
        except featuritis.exc.FeaturitisError as e:
            sys.stderr.write(e.message)
            sys.stderr.write("\n")
            sys.stderr.flush()

            return 1

    def init(self, args):
        initialize(os.getcwd())

    def add(self, args):
        manager = Manager(config_path=args.config)
        feature_path = manager.add(
            args.id,
            description=args.description,
            author=args.author,
        )

        feature_path = os.path.abspath(feature_path)

        print("feature added {}".format(feature_path))

    def list(self, args):

        manager = Manager(config_path=args.config)
        features = manager.get_all_features()

        as_list = list(features.values())
        as_list.sort(key=lambda v: v["timestamp"])
        as_list.reverse()

        if args.format == "table":
            print("id: timestamp author: description")

            for item in as_list:
                print(
                    "{}: {} {}: {}"
                    .format(
                        item["feature_id"],
                        item["timestamp"].strftime("%Y-%m-%d"),
                        item["author"],
                        item["description"],
                    )
                )
        elif args.format == "csv":
            fields = [
                "feature_id",
                "timestamp",
                "author",
                "description",
            ]

            writer = csv.DictWriter(
                sys.stdout,
                fieldnames=fields,
                extrasaction="ignore",
            )
            writer.writeheader()

            for item in as_list:
                row = {}
                for field in fields:
                    row[field] = item[field]

                row["timestamp"] = row["timestamp"].strftime("%Y-%m-%d")

                writer.writerow(row)
        else:
            raise Exception(
                "Implementation Error: 'table' or 'csv' were expected, got {!r}"
                .format(args.format)
            )
